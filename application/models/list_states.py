import time

from dynamorm import DynaModel, GlobalIndex, ProjectAll
from marshmallow import fields

now_timestamp = int(time.time())
# Our objects are defined as DynaModel classes


class State(DynaModel):
    # Define our DynamoDB properties
    class Table:
        name = 'tbl_nigeria_states'
        hash_key = 'id'
        read = 1
        write = 1

    # Define our data schema, each property here will become a property on instances of the Book class
    class Schema:
        id = fields.String(required=True)
        name = fields.String()
        date_saved = fields.Decimal(dump_default=now_timestamp)
        last_updation_timestamp = fields.Decimal(dump_default=now_timestamp)



class Lga(DynaModel):
    # Define our DynamoDB properties
    class Table:
        name = 'tbl_lga_nigeria'
        hash_key = 'id'
        range_key = 'state_id'
        read = 1
        write = 1

    class ByStateId(GlobalIndex):
        name = 'state_id-index'
        hash_key = 'state_id'
        read = 1
        write = 1
        projection = ProjectAll()

    # Define our data schema, each property here will become a property on instances of the Book class
    class Schema:
        id = fields.String(required=True)
        state_id = fields.String()
        name = fields.String()
        date_saved = fields.Decimal(dump_default=now_timestamp)
        last_updation_timestamp = fields.Decimal(dump_default=now_timestamp)
