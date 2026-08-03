from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.student import StudentRegister
from app.services.student_service import register_student
from app.database.connection import get_db


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/register")
def register(
    student: StudentRegister,
    db: Session = Depends(get_db)
):
    return register_student(db, student)