from typing import Optional, List, Union

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
    linkedin: str
    years_of_experience: Optional[str] = None
    has_bachelors_degree: Optional[bool] = None
    early_years_education: Optional[bool] = None
    how_you_heard_about_us: Optional[str] = None
    purpose_using_the_app: Optional[str] = None


class StudentSchema(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    gender: str
    dob: str
    age: Union[str, int]
    msisdn: Optional[str] = None
    email: Optional[str] = None
    country: str
    state: str
    address: str
    profile_image: str
    parent: Optional[int] = None
    middle_name: str
    nick_name: Optional[str] = None
    current_school: Optional[str] = None
    parent_name: Optional[str] = None
    parent_email: Optional[str] = None
    how_you_knew_about_us: Optional[str] = None
    why_use_us: str
    interest: str
    parent_msisdn: Optional[str] = None
    father_name: Optional[str] = None
    father_msisdn: Optional[str] = None
    father_address: Optional[str] = None
    father_email: Optional[str] = None
    mother_name: Optional[str] = None
    mother_msisdn: Optional[str] = None
    mother_address: Optional[str] = None
    mother_email: Optional[str] = None
    any_medical_condition: Optional[bool] = None
    medical_condition: Optional[str] = None
    any_educational_needs: Optional[bool] = None
    educational_needs: Optional[str] = None
    any_learning_delay: Optional[bool] = None
    learning_delay: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None


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
    relationship_to_student: str
    school_id: int
    student: Optional[list] = None


class SubscriptionSchema(BaseModel):
    name: str
    description: str
    billing_cycle: int
    amount: str
    features: List[str]
