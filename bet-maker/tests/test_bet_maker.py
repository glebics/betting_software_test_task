import pytest
import time
import decimal

from httpx import AsyncClient
from bet_maker.main import app
from bet_maker.db import init_db, SessionLocal
from bet_maker.models import Bet


@pytest.mark.asyncio
async def test_create_bet():
    # Инициализируем БД (в тестовой среде обычно мокаем/запускаем тестовый контейнер)
    await init_db()

    bet_data = {
        "event_id": "test_event",
        "amount": "100.50"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/bet", json=bet_data)
        assert resp.status_code == 200
        created_bet = resp.json()
        assert created_bet["event_id"] == "test_event"
        assert created_bet["amount"] == "100.50"
        assert created_bet["status"] == "NEW"


@pytest.mark.asyncio
async def test_list_bets():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/bets")
        assert resp.status_code == 200
        bets = resp.json()
        assert isinstance(bets, list)
