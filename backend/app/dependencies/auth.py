from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.student import Student
from app.security.jwt_handler import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/students/login")


def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    student = db.query(Student).filter(
        Student.id == payload["student_id"]
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student Not Found"
        )

    return student