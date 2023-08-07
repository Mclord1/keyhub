from typing import Optional, Union

from pydantic import BaseModel, EmailStr, constr, field_validator
from submodule_util_3kle.util.custom_exception.custom_exception import CustomException


class UserExistSchema(BaseModel):
    email: EmailStr
    phone_number: str


class AdminSignupSchema(UserExistSchema):
    password: str
    user_type: Optional[str] = 'admin'


class LoginSchema(BaseModel):
    phone_number: str
    password: str


class PhysicalAddressSchema(BaseModel):
    lga: str
    city: str
    state: str
    address: str


class DocumentSchema(BaseModel):
    document_uri: str


class IdentityProofSchema(DocumentSchema):
    document_type: str


class CompleteOnboardingSchema(BaseModel):
    gender: constr(strip_whitespace=True, min_length=1)
    last_name: str
    first_name: str
    date_of_birth: str
    profile_type: str
    country: str
    country_code: str
    is_active: bool
    pin: str
    image_uri: Optional[str] = None

    @field_validator('gender')
    def validate_gender(cls, v):
        # Ensure the gender is capitalized
        if v[0].isupper():
            return v
        raise CustomException(message='Gender must be capitalized.')


class SignupCallSchema(BaseModel):
    email: EmailStr
    phone_number: str
    password: Union[str, int]
    user_type: Optional[str] = '3kle-app-user'
    referral_code: Optional[str] = None


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
