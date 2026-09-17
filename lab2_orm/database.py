"""Подключение к SQLite и создание сессий SQLAlchemy."""

from collections.abc import Generator
import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DEFAULT_DB_PATH = Path(__file__).with_name("app.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Базовый класс всех ORM-моделей."""


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    """Включает каскадные внешние ключи в SQLite."""

    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db() -> Generator[Session, None, None]:
    """Возвращает сессию и гарантированно закрывает её после использования."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Создаёт все таблицы лабораторной работы."""

    try:
        from . import models  # noqa: F401
    except ImportError:
        import models  # type: ignore  # noqa: F401

    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    """Пересоздаёт учебную базу, чтобы демонстрация была повторяемой."""

    try:
        from . import models  # noqa: F401
    except ImportError:
        import models  # type: ignore  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

