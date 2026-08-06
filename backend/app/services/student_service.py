from fastapi import HTTPException
from sqlalchemy.orm import Session
import random

from app.models.student import Student
from app.security.hashing import hash_password, verify_password
from app.security.jwt_handler import create_access_token


# ==========================
# Student Registration
# ==========================
def register_student(db: Session, student_data):

    if student_data.password != student_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Password and Confirm Password do not match."
        )

    existing_email = db.query(Student).filter(
        Student.college_email == student_data.college_email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="College Email already registered."
        )

    existing_enrollment = db.query(Student).filter(
        Student.enrollment_no == student_data.enrollment_no
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Enrollment Number already registered."
        )

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
# Student Login (OAuth2)
# ==========================
def login_student(db: Session, login_data):

    student = db.query(Student).filter(
        Student.college_email == login_data.username
    ).first()

    if student is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    print("=" * 50)
    print("Email :", login_data.username)
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
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================
# Update Profile
# ==========================
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


# ==========================
# Change Password
# ==========================
def change_password(
    db: Session,
    current_student: Student,
    password_data
):

    if not verify_password(
        password_data.old_password,
        current_student.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Old Password is Incorrect"
        )

    if (
        password_data.new_password
        != password_data.confirm_new_password
    ):
        raise HTTPException(
            status_code=400,
            detail="New Password and Confirm Password do not match"
        )

    current_student.password_hash = hash_password(
        password_data.new_password
    )

    db.commit()
    db.refresh(current_student)

    return {
        "message": "Password Changed Successfully"
    }


# ==========================
# Forgot Password
# ==========================
def forgot_password(db: Session, data):

    student = db.query(Student).filter(
        Student.college_email == data.college_email
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    otp = str(random.randint(100000, 999999))

    student.reset_otp = otp

    db.commit()

    print("=" * 50)
    print("RESET OTP :", otp)
    print("=" * 50)

    return {
        "message": "OTP generated successfully. Check server console."
    }


# ==========================
# Reset Password
# ==========================
def reset_password(db: Session, data):

    student = db.query(Student).filter(
        Student.college_email == data.college_email
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if student.reset_otp != data.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    if data.new_password != data.confirm_new_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    student.password_hash = hash_password(
        data.new_password
    )

    student.reset_otp = None
    student.otp_created_at = None

    db.commit()

    return {
        "message": "Password reset successful"
    }