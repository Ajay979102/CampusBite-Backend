from fastapi import APIRouter
from app.schemas.student import StudentRegister
from app.services.student_service import register_student


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/register")
def register(student: StudentRegister):
    return register_student(student)