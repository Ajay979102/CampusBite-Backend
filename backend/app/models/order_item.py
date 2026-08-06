from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    # Relationship with Order
    order = relationship(
        "Order",
        back_populates="order_items"
    )

    # Relationship with Menu
    menu_item = relationship(
        "MenuItem",
        back_populates="order_items"
    )