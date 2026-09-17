# Лабораторные работы по ТРПО

В репозитории выполнены три лабораторные работы:

1. **Git и GitHub.** В истории репозитория есть отдельная ветка
   `feature-branch`, конфликт при слиянии, merge-коммит, намеренно плохой коммит
   и его безопасная отмена через `git revert`. Итоговый файл — `hello.py`.
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

Для завершения части GitHub необходимо создать пустой удалённый репозиторий,
добавить его как `origin`, отправить ветки `main` и `feature-branch`, затем
оформить Pull Request. Эти действия требуют адреса репозитория и авторизации
в аккаунте GitHub.
