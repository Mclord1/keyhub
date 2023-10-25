from typing import Optional, List

from pydantic import BaseModel, field_validator

from exceptions.custom_exception import CustomException


class PrimaryContact(BaseModel):
    email: str
    name: str
    gender: str
    msisdn: str
    address: str

    @field_validator('gender')
    def validate_gender(cls, v):
        # Ensure the gender is capitalized
        if v[0].isupper():
            return v
        raise CustomException(message='Gender must be capitalized.')


class SchoolSchema(BaseModel):
    name: str
    msisdn: str
    reg_number: str
    email: str
    country: str
    state: str
    address: str
    primary_contact: PrimaryContact


class UpdateSchoolSchema(BaseModel):
    name: Optional[str] = None
    msisdn: Optional[str] = None
    reg_number: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None


class ProjectSchema(BaseModel):
    name: str
    description: str
    teacher_id: Optional[int] = None
    student_id: Optional[List[int]] = None
    group_id: int


class LearningGroupSchema(BaseModel):
    name: str
    description: str
