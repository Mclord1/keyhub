import time

from dynamorm import DynaModel
from marshmallow import fields

now_timestamp = int(time.time())
# Our objects are defined as DynaModel classes


class State(DynaModel):
    # Define our DynamoDB properties
    class Table:
        name = 'tbl_state'
        hash_key = 'state_id'
        range_key = 'country_id'
        read = 1
        write = 1

    # Define our data schema, each property here will become a property on instances of the Book class
    class Schema:
        state_id = fields.String(required=True)
        country_id = fields.String()
        state_name = fields.String()
        country_name = fields.String()
        country_currency = fields.String()
        country_capital = fields.String()
        date_saved = fields.Decimal(dump_default=now_timestamp)
        last_updation_timestamp = fields.Decimal(dump_default=now_timestamp)
