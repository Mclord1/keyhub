from typing import Optional

from pydantic import BaseModel


class UserExistSchema(BaseModel):
    email: str
    phone_number: str


class SystemAdminSchema(BaseModel):
    email: str
    msisdn: str
    first_name: str
    last_name: str
    gender: str
    country: str
    state: str
    address: str
    role: int
    img: Optional[str] = None


class TeacherSchema(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    gender: str
    msisdn: str
    email: str
    country: str
    state: str
    address: str


class StudentSchema(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    gender: str
    date_of_birth: str
    age: str
    msisdn: str
    email: str
    country: str
    state: str
    address: str
    parent: Optional[int] = None
    img: Optional[str] = None


class ParentSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    age: str
    msisdn: str
    email: str
    country: str
    state: str
    address: str
    work_email: str
    work_msisdn: str
    work_country: str
    work_state: str
    work_address: str
    student: Optional[int] = None


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class PhysicalAddressSchema(BaseModel):
    lga: str
    city: str
    state: str
    address: str


class UserResponse(BaseModel):
    id: int
    email: str
    phone_number: str
    panic_balance: dict
    currency: str
    country: Optional[str] = None
    base_currency: str
    status: str
    user_subscription_plan: str
    notification_settings: dict
    created_at: int
    last_updated: int
    is_phone_verified: bool
    is_email_verified: bool
    phone_verification_failed_attempts: int
    email_verification_failed_attempts: int
