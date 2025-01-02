"""
Главный модуль FastAPI приложения bet_maker, отвечающего за работу со ставками (bets).
- Инициализирует подключение к БД (через init_db).
- Запускает прослушивание сообщений от RabbitMQ.
- Предоставляет эндпоинты для CRUD-операций со ставками.
"""
import os
import asyncio
import logging
from typing import List, Set, Dict, Any

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, update
from aio_pika import connect_robust, IncomingMessage, ExchangeType

from db import init_db, SessionLocal
from models import Bet
from schemas import BetCreate, BetDB

# Логгер
logger = logging.getLogger("bet_maker")
logging.basicConfig(level=logging.INFO)

RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", "5672"))
EXCHANGE_NAME: str = "events_exchange"
QUEUE_NAME: str = "events.finished"
ROUTING_KEY: str = "event.finished"

app = FastAPI()


@app.on_event("startup")
async def on_startup() -> None:
    """
    Хук, вызывающийся при старте приложения. 
    - Инициализирует базу данных.
    - Запускает задачу прослушивания очереди RabbitMQ.
    """
    # Инициализация БД
    await init_db()

    # Подключение к RabbitMQ + запуск фонового consume
    asyncio.create_task(consume_events())


@app.get("/events")
async def get_active_events() -> Dict[str, List[str]]:
    """
    Возвращает список событий, у которых есть хотя бы одна ставка 
    в статусе "NEW". (Упрощённая логика определения активных событий.)

    :return: Словарь с ключом "active_events" и списком ID событий.
    """
    async with SessionLocal() as session:
        # Выбираем события, у которых есть ставки в статусе NEW
        result = await session.execute(
            select(Bet.event_id).where(Bet.status == "NEW")
        )
        active_event_ids: Set[str] = set(row[0] for row in result.all())

    return {"active_events": list(active_event_ids)}


@app.post("/bet", response_model=BetDB)
async def create_bet(bet_data: BetCreate) -> BetDB:
    """
    Создаёт новую ставку (Bet) в базе данных.

    :param bet_data: Данные для создания ставки (event_id, amount).
    :return: Созданная ставка (BetDB).
    """
    # Здесь можно добавить дополнительные проверки:
    # 1) Существует ли такое событие (либо кэш, либо запрос к line_provider).
    # 2) Не истёк ли дедлайн.
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
async def get_bets() -> List[BetDB]:
    """
    Возвращает полную историю всех ставок (Bet) из базы данных.

    :return: Список всех ставок в формате BetDB.
    """
    async with SessionLocal() as session:
        result = await session.execute(select(Bet))
        bets = result.scalars().all()
    return [BetDB.from_orm(b) for b in bets]


async def consume_events() -> None:
    """
    Фоновая задача, подключающаяся к RabbitMQ, создаёт очередь 
    и подписывается на сообщения о завершении событий (event.finished).

    При получении каждого сообщения вызывается колбэк on_event_finished.
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


async def on_event_finished(message: IncomingMessage) -> None:
    """
    Колбэк, вызываемый при получении сообщения о завершённом событии.
    Формат тела сообщения: "event_id:FINISHED_WIN" или "event_id:FINISHED_LOSE".

    - Извлекает event_id и состояние (WIN/LOSE).
    - Обновляет все ставки с event_id, у которых статус "NEW", на соответствующий ("WIN" или "LOSE").

    :param message: Объект сообщения из RabbitMQ.
    """
    try:
        body: str = message.body.decode()
        event_id, state_str = body.split(":")
        logger.info(f"Received event finish: {event_id} - {state_str}")

        # Определяем новый статус ставок
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
