from dynamorm import DynaModel
from marshmallow import fields
import time

now_timestamp = int(time.time())


class PinVerification(DynaModel):
    # Define our DynamoDB properties
    class Table:
        name = 'tbl_pin_verification'
        hash_key = 'email'
        read = 1
        write = 1

    # Define our data schema, each property here will become a property on instances of the Book class
    class Schema:
        email = fields.String(required=True)
        verified_on = fields.Decimal()
