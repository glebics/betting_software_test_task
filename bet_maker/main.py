import os
import asyncio
import logging
from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, update
from aio_pika import connect_robust, IncomingMessage, ExchangeType

from db import init_db, SessionLocal
from models import Bet
from schemas import BetCreate, BetDB


# Логгер
logger = logging.getLogger("bet_maker")
logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
EXCHANGE_NAME = "events_exchange"
QUEUE_NAME = "events.finished"
ROUTING_KEY = "event.finished"

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    # Инициализация БД
    await init_db()

    # Подключение к RabbitMQ + запуск фонового consume
    asyncio.create_task(consume_events())


@app.get("/events")
async def get_active_events():
    """
    Возвращает список событий, у которых есть хотя бы одна ставка
    в статусе NEW. (Для упрощения.)
    """
    async with SessionLocal() as session:
        # Выбираем события, у которых есть ставки в статусе NEW
        result = await session.execute(
            select(Bet.event_id).where(Bet.status == "NEW")
        )
        active_event_ids = set(row[0] for row in result.all())

    return {"active_events": list(active_event_ids)}


@app.post("/bet", response_model=BetDB)
async def create_bet(bet_data: BetCreate):
    """
    Создание новой ставки
    """
    # Здесь можно добавить проверки:
    # 1) Существует ли такое событие (либо кэш, либо запрос к line_provider)
    # 2) Не истёк ли дедлайн
    # и т.д.
    new_bet = Bet(
        event_id=bet_data.event_id,
        amount=bet_data.amount,
        status="NEW"
    )

    async with SessionLocal() as session:
        session.add(new_bet)
        await session.commit()
        await session.refresh(new_bet)

    return BetDB.from_orm(new_bet)


@app.get("/bets", response_model=List[BetDB])
async def get_bets():
    """
    История всех ставок
    """
    async with SessionLocal() as session:
        result = await session.execute(select(Bet))
        bets = result.scalars().all()
    return [BetDB.from_orm(b) for b in bets]


async def consume_events():
    """
    Подключаемся к RabbitMQ, создаём очередь и подписываемся на сообщения
    о завершении событий.
    """
    try:
        connection = await connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT
        )
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        # Обменник и очередь
        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.TOPIC)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        # Связываем очередь с обменником
        await queue.bind(exchange, ROUTING_KEY)

        # Начинаем потреблять
        await queue.consume(on_event_finished, no_ack=False)
        logger.info("Started consuming events from RabbitMQ.")
    except Exception as e:
        logger.exception("Failed to connect or consume from RabbitMQ.")
        # Рестартим задачу через какое-то время (простейший механизм повторных попыток)
        await asyncio.sleep(5)
        asyncio.create_task(consume_events())


async def on_event_finished(message: IncomingMessage):
    """
    Callback, который вызывается при получении сообщения
    о завершённом событии. Формат: "event_id:FINISHED_WIN" или "event_id:FINISHED_LOSE".
    """
    try:
        body = message.body.decode()
        event_id, state_str = body.split(":")
        logger.info(f"Received event finish: {event_id} - {state_str}")

        # Обновляем все ставки по event_id
        new_status = "WIN" if state_str == "FINISHED_WIN" else "LOSE"
        async with SessionLocal() as session:
            await session.execute(
                update(Bet).
                where(Bet.event_id == event_id, Bet.status == "NEW").
                values(status=new_status)
            )
            await session.commit()

        await message.ack()  # Сообщение обработано успешно
    except Exception as e:
        logger.exception("Error processing message. Will requeue.")
        await message.nack(requeue=True)  # Чтобы сообщение было переотправлено
