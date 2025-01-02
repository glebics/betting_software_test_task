# line_provider/tests/test_line_provider_integration.py
import pytest
import time
from decimal import Decimal
from httpx import AsyncClient
from uuid import uuid4
from decimal import Decimal

"""
Интеграционные тесты для line_provider, запущенного на http://localhost:8001
"""

LINE_PROVIDER_BASE_URL = "http://localhost:8001"


@pytest.mark.asyncio
async def test_create_and_update_event_integration():
    unique_event_id = f"test_event_{uuid4().hex}"
    test_event = {
        "event_id": unique_event_id,
        "coefficient": "1.30",
        "deadline": int(time.time()) + 300,
        "state": "NEW"
    }

    async with AsyncClient(base_url=LINE_PROVIDER_BASE_URL) as ac:
        # 1) Создаём событие
        resp = await ac.put("/event", json=test_event)
        assert resp.status_code == 200, f"Create Event Response: {resp.status_code}, {resp.text}"

        # 2) Проверяем, что оно создалось
        resp = await ac.get(f"/event/{unique_event_id}")
        assert resp.status_code == 200, f"Get Event Response: {resp.status_code}, {resp.text}"
        data = resp.json()
        assert float(Decimal(data["coefficient"])) == float(Decimal(test_event["coefficient"]))
        assert data["state"] == "NEW"

        # 3) Обновляем состояние события до FINISHED_WIN
        resp = await ac.put("/event", json={
            "event_id": unique_event_id,
            "state": "FINISHED_WIN"
        })
        assert resp.status_code == 200, f"Update Event Response: {resp.status_code}, {resp.text}"

        # 4) Проверяем финальное состояние
        resp = await ac.get(f"/event/{unique_event_id}")
        assert resp.status_code == 200, f"Get Updated Event Response: {resp.status_code}, {resp.text}"
        assert resp.json()["state"] == "FINISHED_WIN"
