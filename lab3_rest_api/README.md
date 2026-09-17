# Лабораторная работа 3 — REST API

API хранит данные в памяти и реализует требуемые методы:

- `POST /items` — создание объекта со статусом `201`;
- `GET /items` — получение списка;
- `GET /items/{item_id}` — получение объекта или ответ `404`.

## Запуск

Из корня репозитория:

```powershell
python -m pip install -r lab3_rest_api/requirements.txt
python -m uvicorn lab3_rest_api.main:app --reload
```

Swagger будет доступен по адресу <http://127.0.0.1:8000/docs>.

Пример тела запроса для `POST /items`:

```json
{
  "name": "Ноутбук",
  "description": "Игровой ноутбук"
}
```

