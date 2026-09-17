import asyncio

import httpx

from lab3_rest_api.main import app, database


def setup_function():
    database.clear()


def test_create_list_get_and_not_found():
    async def scenario():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            first = await client.post(
                "/items",
                json={"name": "Ноутбук", "description": "Игровой ноутбук"},
            )
            second = await client.post("/items", json={"name": "Мышь"})

            assert first.status_code == 201
            assert second.status_code == 201
            first_item = first.json()
            assert first_item["id"]

            items = await client.get("/items")
            assert items.status_code == 200
            assert len(items.json()) == 2

            found = await client.get(f"/items/{first_item['id']}")
            assert found.status_code == 200
            assert found.json() == first_item

            missing = await client.get("/items/несуществующий_id")
            assert missing.status_code == 404
            assert missing.json() == {"detail": "Item not found"}

    asyncio.run(scenario())


def test_validation_rejects_empty_name_and_extra_fields():
    async def scenario():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            empty_name = await client.post("/items", json={"name": "   "})
            extra_field = await client.post("/items", json={"name": "Книга", "price": 1000})

            assert empty_name.status_code == 422
            assert extra_field.status_code == 422

    asyncio.run(scenario())
