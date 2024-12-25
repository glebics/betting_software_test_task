import pytest
import time
from httpx import AsyncClient

from line_provider.main import app


@pytest.mark.asyncio
async def test_create_and_update_event():
    test_event = {
        "event_id": "test_id",
        "coefficient": "1.30",
        "deadline": int(time.time()) + 300,
        "state": "NEW"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.put("/event", json=test_event)
        assert resp.status_code == 200
        assert resp.json().get("detail") == "Event created"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/event/test_id")
        assert resp.status_code == 200
        data = resp.json()
        assert data["coefficient"] == "1.30"

    # Обновляем состояние события
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.put("/event", json={"event_id": "test_id", "state": "FINISHED_WIN"})
        assert resp.status_code == 200
        assert resp.json().get("detail") == "Event updated"

    # Проверяем финальное состояние
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/event/test_id")
        assert resp.status_code == 200
        assert resp.json()["state"] == "FINISHED_WIN"
