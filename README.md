# Лабораторные работы по ТРПО

В репозитории выполнены три лабораторные работы:

1. **Git и GitHub.** В истории репозитория есть отдельная ветка
   `feature-branch`, новый конфликт между `main` и `feature-conflict`, его ручное
   разрешение, merge-коммиты, намеренно плохой коммит и его безопасная отмена
   через `git revert`. Итоговый файл — `hello.py`. Репозиторий опубликован:
   <https://github.com/nervan-iwnl/lab1>.
2. **SQLAlchemy ORM.** Проект `lab2_orm` содержит модели магазина, SQLite,
   CRUD-операции, фильтрацию и демонстрацию связей один-ко-многим и
   многие-ко-многим.
3. **FastAPI REST API.** Проект `lab3_rest_api` реализует создание объекта,
   получение списка, получение по ID, валидацию и ответ `404`.

## Подготовка окружения

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Запуск лабораторной работы 1

```powershell
python hello.py
git log --oneline --graph --decorate --all
```

## Запуск лабораторной работы 2

```powershell
python -m lab2_orm.main
```

Файл базы данных будет создан по пути `lab2_orm/app.db`.

## Запуск лабораторной работы 3

```powershell
python -m uvicorn lab3_rest_api.main:app --reload
```

Swagger: <http://127.0.0.1:8000/docs>

## Тесты

```powershell
python -m pytest -q
```

Ветки `main`, `feature-branch` и `feature-conflict` опубликованы в GitHub.
Снимки обнаруженного конфликта, результата его разрешения и истории GitHub
находятся в каталоге `screenshots/lab1`.
