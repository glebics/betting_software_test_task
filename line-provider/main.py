import time
import decimal
import asyncio
import logging

from fastapi import FastAPI, Path, HTTPException
from typing import Dict
from aio_pika import connect_robust, Message, ExchangeType

from schemas import Event, EventState

# Локальное in-memory хранилище событий:
events: Dict[str, Event] = {}

app = FastAPI()

# Логгер
logger = logging.getLogger("line-provider")
logging.basicConfig(level=logging.INFO)

# Настройки для RabbitMQ
RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
EXCHANGE_NAME = "events_exchange"
ROUTING_KEY = "event.finished"


@app.on_event("startup")
async def startup_event():
    """
    При запуске приложения соединяемся с RabbitMQ и создаём обменник
    """
    app.state.rabbit_connection = await connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT
    )
    channel = await app.state.rabbit_connection.channel()
    app.state.exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.TOPIC)
    logger.info("Connected to RabbitMQ and declared exchange.")

    # Инициируем несколько тестовых событий в память
    events["1"] = Event(event_id="1", coefficient=decimal.Decimal("1.20"),
                        deadline=int(time.time()) + 600, state=EventState.NEW)
    events["2"] = Event(event_id="2", coefficient=decimal.Decimal("1.15"),
                        deadline=int(time.time()) + 60, state=EventState.NEW)
    events["3"] = Event(event_id="3", coefficient=decimal.Decimal("1.67"),
                        deadline=int(time.time()) + 90, state=EventState.NEW)


@app.on_event("shutdown")
async def shutdown_event():
    """
    При остановке приложения корректно закрываем соединение с RabbitMQ
    """
    await app.state.rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ.")


@app.get("/events")
async def get_events():
    """
    Возвращает список не истёкших событий (deadline ещё не наступил)
    """
    now = int(time.time())
    active_events = [
        e for e in events.values() if e.deadline and e.deadline > now
    ]
    return active_events


@app.get("/event/{event_id}")
async def get_event(event_id: str = Path(default=None)):
    """
    Получить информацию об одном событии
    """
    if event_id in events:
        return events[event_id]
    raise HTTPException(status_code=404, detail="Event not found")


@app.put("/event")
async def create_or_update_event(event: Event):
    """
    Создать или обновить событие.
    Если событие обновляется и оно завершено (FINISHED_WIN/LOSE),
    шлём уведомление через RabbitMQ.
    """
    existed_event = events.get(event.event_id)

    if not existed_event:
        # Создаём новое событие
        events[event.event_id] = event
        logger.info(f"Created new event: {event}")
        return {"detail": "Event created"}
    else:
        # Обновляем существующее
        for field, value in event.dict(exclude_unset=True).items():
            setattr(existed_event, field, value)

        # Если обновили статус и он FINISHED, отправляем уведомление
        if existed_event.state in (EventState.FINISHED_WIN, EventState.FINISHED_LOSE):
            await send_event_finished_notification(existed_event)

        logger.info(f"Updated event: {existed_event}")
        return {"detail": "Event updated"}


async def send_event_finished_notification(event: Event):
    """
    Отправить уведомление о завершённом событии в RabbitMQ
    """
    exchange = app.state.exchange
    message_body = f"{event.event_id}:{event.state}"
    message = Message(message_body.encode())
    # Публикуем сообщение в топик-экчендж с routing_key
    await exchange.publish(message, routing_key=ROUTING_KEY)
    logger.info(
        f"Sent finish notification for event {event.event_id} with state {event.state}")
