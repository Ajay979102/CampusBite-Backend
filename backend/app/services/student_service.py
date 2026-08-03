from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.security.hashing import hash_password


def register_student(db: Session, student_data):

    # Password Match Check
    if student_data.password != student_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match."
        )

    # Duplicate Email Check
    existing_email = db.query(Student).filter(
        Student.college_email == student_data.college_email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="College Email already registered."
        )

    # Duplicate Enrollment Check
    existing_enrollment = db.query(Student).filter(
        Student.enrollment_no == student_data.enrollment_no
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Enrollment Number already registered."
        )

    # Create Student Object
    new_student = Student(
        full_name=student_data.full_name,
        college_email=student_data.college_email,
        enrollment_no=student_data.enrollment_no,
        mobile=student_data.mobile,
        department=student_data.department,
        year=student_data.year,
        section=student_data.section,
        password_hash=hash_password(student_data.password)
    )

    # Save to Database
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student Registered Successfully",
        "student_id": new_student.id,
        "full_name": new_student.full_name,
        "college_email": new_student.college_email
    }