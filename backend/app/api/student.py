from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_student
from app.models.student import Student

from app.schemas.student import (
    StudentRegister,
    StudentLogin,
    StudentUpdate,
    ChangePassword,
    ForgotPassword,
    ResetPassword
)

from app.services.student_service import (
    register_student,
    login_student,
    update_student_profile,
    change_password,
    forgot_password,
    reset_password
)
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# -----------------------------
# Register Student
# -----------------------------
@router.post("/register")
def register(
    student: StudentRegister,
    db: Session = Depends(get_db)
):
    return register_student(db, student)


# -----------------------------
# Login Student
# -----------------------------
@router.post("/login")
def login(
    student: StudentLogin,
    db: Session = Depends(get_db)
):
    return login_student(db, student)


# -----------------------------
# Get Logged-in Student Profile
# -----------------------------
@router.get("/me")
def get_my_profile(
    current_student: Student = Depends(get_current_student)
):
    return {
        "id": current_student.id,
        "full_name": current_student.full_name,
        "college_email": current_student.college_email,
        "enrollment_no": current_student.enrollment_no,
        "mobile": current_student.mobile,
        "department": current_student.department,
        "year": current_student.year,
        "section": current_student.section,
        "trust_score": current_student.trust_score,
        "created_at": current_student.created_at
    }


# -----------------------------
# Update Student Profile
# -----------------------------
@router.put("/update-profile")
def update_profile(
    student: StudentUpdate,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    return update_student_profile(
        db=db,
        current_student=current_student,
        student_data=student
    )
@router.put("/change-password")
def change_student_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    return change_password(
        db=db,
        current_student=current_student,
        password_data=password_data
    )
@router.post("/logout")
def logout_student(
    current_student: Student = Depends(get_current_student)
):
    return {
        "message": "Logout Successful. Please remove the token from the client."
    }

@router.post("/forgot-password")
def forgot_student_password(
    data: ForgotPassword,
    db: Session = Depends(get_db)
):
    return forgot_password(
        db=db,
        data=data
    )

@router.post("/reset-password")
def reset_student_password(
    data: ResetPassword,
    db: Session = Depends(get_db)
):
    return reset_password(
        db=db,
        data=data
    )