from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from lab2_orm.crud import (
    add_product_to_order,
    create_category,
    create_order,
    create_product,
    delete_order,
    delete_product,
    get_order,
    get_product,
    get_products,
    update_category,
    update_order_status,
    update_product_stock,
)
from lab2_orm.database import Base


def make_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


def test_crud_filters_and_relationships():
    db = make_session()
    try:
        category = create_category(db, "Электроника", "Гаджеты")
        cheap = create_product(db, "Мышь", 1_500, category.id, stock=10)
        expensive = create_product(db, "Ноутбук", 120_000, category.id, stock=3)

        assert [item.name for item in get_products(db, min_price=1_000, max_price=2_000)] == ["Мышь"]
        assert update_category(db, category.id, name="Техника").name == "Техника"
        assert update_product_stock(db, cheap.id, 25).stock == 25

        order = create_order(db, "Иван Иванов", "ivan@example.com")
        first_item = add_product_to_order(db, order.id, cheap.id, quantity=2)
        second_item = add_product_to_order(db, order.id, cheap.id, quantity=1)
        add_product_to_order(db, order.id, expensive.id)
        assert first_item.id == second_item.id
        assert second_item.quantity == 3

        db.expire_all()
        saved_order = get_order(db, order.id)
        assert {product.name for product in saved_order.products} == {"Мышь", "Ноутбук"}
        assert update_order_status(db, order.id, "completed").status == "completed"

        assert delete_product(db, expensive.id) is True
        assert get_product(db, expensive.id) is None
        assert delete_order(db, order.id) is True
        assert get_order(db, order.id) is None
    finally:
        db.close()

