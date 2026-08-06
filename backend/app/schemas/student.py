from pydantic import BaseModel, EmailStr


class StudentRegister(BaseModel):
    full_name: str
    college_email: EmailStr
    enrollment_no: str
    mobile: str
    department: str
    year: int
    section: str
    password: str
    confirm_password: str


class StudentLogin(BaseModel):
    college_email: EmailStr
    password: str

class StudentUpdate(BaseModel):
    mobile: str
    department: str
    year: int
    section: str

class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

class ForgotPassword(BaseModel):
    college_email: EmailStr


class ResetPassword(BaseModel):
    college_email: EmailStr
    otp: str
    new_password: str
    confirm_new_password: str