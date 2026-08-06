from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.security.hashing import hash_password, verify_password
from app.security.jwt_handler import create_access_token


# ==========================
# Student Registration
# ==========================
def register_student(db: Session, student_data):

    # Password Match
    if student_data.password != student_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match."
        )

    # Duplicate Email
    existing_email = db.query(Student).filter(
        Student.college_email == student_data.college_email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="College Email already registered."
        )

    # Duplicate Enrollment
    existing_enrollment = db.query(Student).filter(
        Student.enrollment_no == student_data.enrollment_no
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Enrollment Number already registered."
        )

    # Create Student
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

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student Registered Successfully",
        "student_id": new_student.id,
        "full_name": new_student.full_name,
        "college_email": new_student.college_email
    }


# ==========================
# Student Login
# ==========================
def login_student(db: Session, login_data):

    # Find Student
    student = db.query(Student).filter(
        Student.college_email == login_data.college_email
    ).first()

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    print("=" * 50)
    print("Email :", login_data.college_email)
    print("Entered Password :", login_data.password)
    print("Stored Hash :", student.password_hash)

    password_match = verify_password(
        login_data.password,
        student.password_hash
    )

    print("Password Match :", password_match)
    print("=" * 50)

    if not password_match:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    access_token = create_access_token(
        {
            "student_id": student.id,
            "email": student.college_email
        }
    )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
def update_student_profile(
    db: Session,
    current_student: Student,
    student_data
):
    current_student.mobile = student_data.mobile
    current_student.department = student_data.department
    current_student.year = student_data.year
    current_student.section = student_data.section

    db.commit()
    db.refresh(current_student)

    return {
        "message": "Profile Updated Successfully",
        "student": {
            "id": current_student.id,
            "full_name": current_student.full_name,
            "college_email": current_student.college_email,
            "mobile": current_student.mobile,
            "department": current_student.department,
            "year": current_student.year,
            "section": current_student.section
        }
    }