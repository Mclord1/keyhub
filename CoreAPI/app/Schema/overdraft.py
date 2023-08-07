from typing import Union

from pydantic import BaseModel


class CreateOverdraftSchema(BaseModel):
    bank_name: str
    account_number: int
    account_name: str
    amount: Union[int, float]
