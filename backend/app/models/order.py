from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    TIMESTAMP,
    text
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    total_amount = Column(Float, nullable=False)

    status = Column(
        String,
        default="Pending"
    )

    token_number = Column(Integer, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    student = relationship("Student")
    order_items = relationship(
    "OrderItem",
    back_populates="order",
    cascade="all, delete"
    )