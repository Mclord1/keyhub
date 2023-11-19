from typing import Optional, List

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
    msisdn: Optional[str] = None
    email: Optional[str] = None
    country: str
    state: str
    address: str
    profile_image: str
    parent: Optional[int] = None
    img: Optional[str] = None


class ParentSchema(BaseModel):
    first_name: str
    last_name: str
    gender: str
    age: int
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
    school_id: int
    student: Optional[list] = None


class SubscriptionSchema(BaseModel):
    name: str
    description: str
    billing_cycle: int
    amount: str
    features: List[str]
