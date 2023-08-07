import time

from dynamorm import DynaModel, GlobalIndex, ProjectAll
from marshmallow import fields

now_timestamp = int(time.time())


class Products(DynaModel):
    class Table:
        name = "products"
        hash_key = 'id'
        range_key = "name"
        read = 1
        write = 1

    class ByPlan(GlobalIndex):
        name = 'plan-index'
        hash_key = 'plan'
        read = 1
        write = 1
        projection = ProjectAll()

    class Schema:
        id = fields.String()
        owner = fields.String()
        country = fields.String()
        name = fields.String()
        type = fields.String()
        description = fields.String()
        plan = fields.String()
        section = fields.String()
        available = fields.String()
        created_at = fields.Decimal(dump_default=now_timestamp)
        updated_at = fields.Decimal(dump_default=now_timestamp)
