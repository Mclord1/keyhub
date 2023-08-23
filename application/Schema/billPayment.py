from pydantic import BaseModel


class CustomerValidationSchema(BaseModel):
    customer_id: str
    payment_code: int


class SendBillSchema(CustomerValidationSchema):
    msisdn: str
    amount: int
    transaction_pin: int
    categoryId: str


class CreateVoucherSchema(BaseModel):
    voucher_type: str
    expiration_date: str
    amount: int
    transaction_pin: int


class RedeemVoucherSchema(CustomerValidationSchema):
    voucher_code: int
    msisdn: str
