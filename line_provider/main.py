"""
Основной модуль FastAPI приложения line_provider,
которое отвечает за хранение и обновление событий (Event),
а также рассылку сообщений о завершении (FINISHED) в RabbitMQ.
"""
import time
import decimal
import asyncio
import logging

from fastapi import FastAPI, Path, HTTPException
from typing import Dict, Any
from aio_pika import connect_robust, Message, ExchangeType

from schemas import Event, EventState

# Локальное in-memory хранилище событий:
events: Dict[str, Event] = {}

app = FastAPI()

# Логгер
logger = logging.getLogger("line_provider")
logging.basicConfig(level=logging.INFO)

# Настройки для RabbitMQ
RABBITMQ_HOST: str = "rabbitmq"
RABBITMQ_PORT: int = 5672
EXCHANGE_NAME: str = "events_exchange"
ROUTING_KEY: str = "event.finished"


@app.on_event("startup")
async def startup_event() -> None:
    """
    При запуске приложения соединяемся с RabbitMQ и создаём обменник.
    Также создаём несколько тестовых событий в памяти.
    """
    app.state.rabbit_connection = await connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT
    )
    channel = await app.state.rabbit_connection.channel()
    app.state.exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.TOPIC)
    logger.info("Connected to RabbitMQ and declared exchange.")

    # Инициируем несколько тестовых событий в память
    events["1"] = Event(
        event_id="1",
        coefficient=decimal.Decimal("1.20"),
        deadline=int(time.time()) + 600,
        state=EventState.NEW
    )
    events["2"] = Event(
        event_id="2",
        coefficient=decimal.Decimal("1.15"),
        deadline=int(time.time()) + 60,
        state=EventState.NEW
    )
    events["3"] = Event(
        event_id="3",
        coefficient=decimal.Decimal("1.67"),
        deadline=int(time.time()) + 90,
        state=EventState.NEW
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    При остановке приложения корректно закрываем соединение с RabbitMQ.
    """
    await app.state.rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ.")


@app.get("/events")
async def get_events() -> Any:
    """
    Возвращает список не истёкших событий (deadline ещё не наступил).

    :return: Список событий (Event), у которых deadline > текущее время.
    """
    now = int(time.time())
    active_events = [
        e for e in events.values() if e.deadline and e.deadline > now
    ]
    return active_events


@app.get("/event/{event_id}")
async def get_event(event_id: str = Path(...)) -> Event:
    """
    Получить информацию об одном событии по его event_id.

    :param event_id: Идентификатор события (строка).
    :return: Объект события (Event).
    :raises HTTPException 404: если событие не найдено.
    """
    if event_id in events:
        return events[event_id]
    raise HTTPException(status_code=404, detail="Event not found")


@app.put("/event")
async def create_or_update_event(event: Event) -> Dict[str, str]:
    """
    Создать новое событие или обновить существующее.

    - Если событие не существует, оно будет создано.
    - Если обновляется состояние на FINISHED_WIN или FINISHED_LOSE,
      происходит отправка уведомления в RabbitMQ.

    :param event: Объект события (Event).
    :return: Словарь с полем "detail" о результате операции.
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


async def send_event_finished_notification(event: Event) -> None:
    """
    Отправить уведомление о завершённом событии в RabbitMQ.

    Формат сообщения: "event_id:FINISHED_WIN" или "event_id:FINISHED_LOSE".

    :param event: Объект события (Event), у которого статус FINISHED.
    """
    exchange = app.state.exchange
    message_body = f"{event.event_id}:{event.state}"
    message = Message(message_body.encode())
    # Публикуем сообщение в топик-экчендж с routing_key
    await exchange.publish(message, routing_key=ROUTING_KEY)
    logger.info(
        f"Sent finish notification for event {event.event_id} with state {event.state}"
    )
