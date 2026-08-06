from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_student
from app.models.student import Student

from app.schemas.order import OrderCreate

from app.services.order_service import (
    place_order,
    get_my_orders,
    get_single_order
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/place")
def create_order(
    data: OrderCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    return place_order(
        db=db,
        student_id=current_student.id,
        data=data
    )


@router.get("/my-orders")
def my_orders(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    return get_my_orders(
        db=db,
        student_id=current_student.id
    )

@router.get("/{order_id}")
def single_order(
    order_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    return get_single_order(
        db=db,
        student_id=current_student.id,
        order_id=order_id
    )