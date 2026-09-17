"""REST API для создания и получения объектов в памяти процесса."""

from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(title="Мой первый REST API")


class Item(BaseModel):
    """Данные, принимаемые при создании объекта."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=200)]
    description: Annotated[str | None, Field(max_length=500)] = None


class ItemInDB(Item):
    """Объект, сохранённый сервером и дополненный уникальным ID."""

    id: str


database: dict[str, ItemInDB] = {}


@app.get("/items", response_model=list[ItemInDB])
async def get_all_items() -> list[ItemInDB]:
    """Возвращает все созданные объекты."""

    return list(database.values())


@app.post("/items", response_model=ItemInDB, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> ItemInDB:
    """Создаёт объект, генерирует UUID и сохраняет его в памяти."""

    item_to_save = ItemInDB(id=str(uuid4()), **item.model_dump())
    database[item_to_save.id] = item_to_save
    return item_to_save


@app.get("/items/{item_id}", response_model=ItemInDB)
async def get_item_by_id(item_id: str) -> ItemInDB:
    """Возвращает объект по ID или ошибку 404."""

    item = database.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("lab3_rest_api.main:app", host="127.0.0.1", port=8000, reload=True)

