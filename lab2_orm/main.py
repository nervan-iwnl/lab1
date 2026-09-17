"""Демонстрация CRUD-операций и связей между моделями."""

import logging

try:
    from .crud import (
        add_product_to_order,
        create_category,
        create_order,
        create_product,
        delete_product,
        get_categories,
        get_category,
        get_order,
        get_product,
        get_products,
        update_category,
        update_order_status,
        update_product_stock,
    )
    from .database import SessionLocal, reset_db
    from .models import Product
except ImportError:
    from crud import (
        add_product_to_order,
        create_category,
        create_order,
        create_product,
        delete_product,
        get_categories,
        get_category,
        get_order,
        get_product,
        get_products,
        update_category,
        update_order_status,
        update_product_stock,
    )
    from database import SessionLocal, reset_db
    from models import Product


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def demo() -> None:
    reset_db()
    logger.info("База данных инициализирована")

    db = SessionLocal()
    try:
        logger.info("=== 1. СОЗДАНИЕ ДАННЫХ ===")
        electronics = create_category(db, "Электроника", "Смартфоны, ноутбуки, планшеты")
        books = create_category(db, "Книги", "Художественная и техническая литература")

        iphone = create_product(db, "iPhone 14", 79_999.99, electronics.id, "Смартфон Apple", 10)
        laptop = create_product(db, "MacBook Pro", 199_999.99, electronics.id, "Ноутбук Apple", 5)
        book = create_product(db, "Python для начинающих", 1_500.00, books.id, "Учебник", 20)

        order = create_order(db, "Иван Иванов", "ivan@example.com")
        add_product_to_order(db, order.id, iphone.id, 1)
        add_product_to_order(db, order.id, book.id, 2)
        logger.info("Создан заказ #%s с двумя позициями", order.id)

        logger.info("=== 2. ЧТЕНИЕ И ФИЛЬТРАЦИЯ ===")
        for category in get_categories(db):
            logger.info("Категория: %s — %s", category.name, category.description)
        for product in get_products(db, min_price=1_000, max_price=100_000):
            logger.info("Товар в диапазоне: %s — %.2f руб.", product.name, product.price)

        order_with_items = get_order(db, order.id)
        assert order_with_items is not None
        for item in order_with_items.order_items:
            logger.info(
                "Позиция заказа: %s, количество: %s, цена: %.2f руб.",
                item.product.name,
                item.quantity,
                item.price_at_time,
            )

        logger.info("=== 3. ОБНОВЛЕНИЕ ДАННЫХ ===")
        update_category(db, electronics.id, name="Электроника и гаджеты")
        update_product_stock(db, iphone.id, 25)
        update_order_status(db, order.id, "completed")
        logger.info("Категория, остаток и статус заказа обновлены")

        logger.info("=== 4. УДАЛЕНИЕ ДАННЫХ ===")
        temp_product = create_product(db, "Временный товар", 999.99, books.id, "Будет удалён", 1)
        delete_product(db, temp_product.id)
        logger.info("Временный товар удалён: %s", get_product(db, temp_product.id) is None)

        logger.info("=== 5. РАБОТА СО СВЯЗЯМИ ===")
        category = get_category(db, electronics.id)
        assert category is not None
        new_product = Product(name="iPad Air", price=69_999.99, category=category, stock=15)
        db.add(new_product)
        db.commit()
        db.refresh(category)
        logger.info("В категории '%s' товаров: %s", category.name, len(category.products))
        logger.info("Ноутбук из демонстрации: %s", laptop.name)

        logger.info("=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")
    except Exception:
        db.rollback()
        logger.exception("Ошибка при выполнении демонстрации")
        raise
    finally:
        db.close()
        logger.info("Сессия закрыта")


if __name__ == "__main__":
    demo()

