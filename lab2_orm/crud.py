"""CRUD-операции для сущностей лабораторной работы 2."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    from .models import Category, Order, OrderItem, Product
except ImportError:
    from models import Category, Order, OrderItem, Product


def _commit_and_refresh(db: Session, entity: Any):
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def create_category(db: Session, name: str, description: str | None = None) -> Category:
    return _commit_and_refresh(db, Category(name=name, description=description))


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    statement = select(Category).order_by(Category.id).offset(skip).limit(limit)
    return list(db.scalars(statement))


def update_category(
    db: Session,
    category_id: int,
    name: str | None = None,
    description: str | None = None,
) -> Category | None:
    category = get_category(db, category_id)
    if category is None:
        return None
    if name is not None:
        category.name = name
    if description is not None:
        category.description = description
    return _commit_and_refresh(db, category)


def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if category is None:
        return False
    db.delete(category)
    db.commit()
    return True


def create_product(
    db: Session,
    name: str,
    price: float,
    category_id: int,
    description: str | None = None,
    stock: int = 0,
) -> Product:
    if get_category(db, category_id) is None:
        raise ValueError(f"Категория с id={category_id} не найдена")
    product = Product(
        name=name,
        price=price,
        category_id=category_id,
        description=description,
        stock=stock,
    )
    return _commit_and_refresh(db, product)


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Product]:
    statement = select(Product).order_by(Product.id)
    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)
    if min_price is not None:
        statement = statement.where(Product.price >= min_price)
    if max_price is not None:
        statement = statement.where(Product.price <= max_price)
    return list(db.scalars(statement.offset(skip).limit(limit)))


def update_product(
    db: Session,
    product_id: int,
    *,
    name: str | None = None,
    description: str | None = None,
    price: float | None = None,
    stock: int | None = None,
    category_id: int | None = None,
) -> Product | None:
    product = get_product(db, product_id)
    if product is None:
        return None
    if category_id is not None:
        if get_category(db, category_id) is None:
            raise ValueError(f"Категория с id={category_id} не найдена")
        product.category_id = category_id
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    return _commit_and_refresh(db, product)


def update_product_stock(db: Session, product_id: int, new_stock: int) -> Product | None:
    return update_product(db, product_id, stock=new_stock)


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True


def create_order(
    db: Session,
    customer_name: str,
    customer_email: str | None = None,
) -> Order:
    return _commit_and_refresh(
        db,
        Order(customer_name=customer_name, customer_email=customer_email),
    )


def add_product_to_order(
    db: Session,
    order_id: int,
    product_id: int,
    quantity: int = 1,
) -> OrderItem:
    if quantity <= 0:
        raise ValueError("Количество товара должно быть положительным")

    order = get_order(db, order_id)
    product = get_product(db, product_id)
    if order is None:
        raise ValueError(f"Заказ с id={order_id} не найден")
    if product is None:
        raise ValueError(f"Товар с id={product_id} не найден")

    statement = select(OrderItem).where(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id,
    )
    order_item = db.scalar(statement)
    if order_item is None:
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_time=product.price,
        )
    else:
        order_item.quantity += quantity
    return _commit_and_refresh(db, order_item)


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    statement = select(Order).order_by(Order.id).offset(skip).limit(limit)
    return list(db.scalars(statement))


def update_order_status(db: Session, order_id: int, status: str) -> Order | None:
    order = get_order(db, order_id)
    if order is None:
        return None
    order.status = status
    return _commit_and_refresh(db, order)


def delete_order(db: Session, order_id: int) -> bool:
    order = get_order(db, order_id)
    if order is None:
        return False
    db.delete(order)
    db.commit()
    return True

