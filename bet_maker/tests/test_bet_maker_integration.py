"""
Интеграционные тесты для bet_maker

Перед запуском:
    docker-compose up --build
Затем, в другом терминале:
    pytest bet_maker/tests/test_bet_maker_integration.py
"""
import pytest
import time
from decimal import Decimal
from httpx import AsyncClient


BET_MAKER_BASE_URL = "http://localhost:8002"


@pytest.mark.asyncio
async def test_create_bet_integration() -> None:
    """
    Тестирует создание новой ставки через эндпоинт /bet.
    Проверяет корректность кода ответа и наличие созданной ставки.
    """
    bet_data = {
        "event_id": "test_event_integration",
        "amount": "100.50"
    }
    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        resp = await ac.post("/bet", json=bet_data)
        assert resp.status_code == 200, f"Response: {resp.status_code}, {resp.text}"


@pytest.mark.asyncio
async def test_list_bets_integration() -> None:
    """
    Тестирует получение списка всех ставок через эндпоинт /bets.
    Проверяет, что ответ содержит ранее созданную тестовую ставку.
    """
    async with AsyncClient(base_url=BET_MAKER_BASE_URL) as ac:
        resp = await ac.get("/bets")
        assert resp.status_code == 200, f"Response: {resp.status_code}, {resp.text}"
        bets = resp.json()
        assert isinstance(bets, list)

        found = any(b["event_id"] == "test_event_integration" for b in bets)
        assert found, "Нашу тестовую ставку не нашли в списке!"
