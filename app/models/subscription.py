import datetime
import uuid

from dynamorm import DynaModel, GlobalIndex, ProjectAll
from marshmallow import fields, validate

now_timestamp = datetime.datetime.now()

status_enums = ("cancelled", "processing", "failed", "declined", "active", "expired")
plan_enum = ("starter", "gold", "silver")


class SubscriptionTable(DynaModel):
    class Table:
        name = "tbl_subscription"
        hash_key = 'id'
        range_key = "user_id"
        read = 1
        write = 1

    class ByUserId(GlobalIndex):
        name = 'user_id-index'
        hash_key = 'user_id'
        read = 1
        write = 1
        projection = ProjectAll()

    class ByBillingDate(GlobalIndex):
        name = 'next_billing_date-index'
        hash_key = 'next_billing_date'
        read = 1
        write = 1
        projection = ProjectAll()

    class ByStatus(GlobalIndex):
        name = 'status-user_id-index'
        hash_key = 'status'
        range_key = "user_id"
        read = 1
        write = 1
        projection = ProjectAll()

    class BySubscriptionStatus(GlobalIndex):
        name = 'status-index'
        hash_key = 'status'
        read = 1
        write = 1
        projection = ProjectAll()

    class Schema:
        user_id = fields.String(required=True)
        id = fields.String(dump_default=uuid.uuid4())
        plan = fields.String(dump_default=plan_enum[0], validate=validate.OneOf(plan_enum))
        amount = fields.Decimal(dump_default=0.0)
        recurring = fields.Bool(dump_default=False)
        next_billing_date = fields.DateTime(allow_none=True, dump_default=None)
        start_date = fields.Date(allow_none=True, dump_default=None)
        end_date = fields.DateTime(allow_none=True, dump_default=None)
        payment_type = fields.String()
        mandate_code = fields.String()
        action = fields.Dict()
        status = fields.String(validate=validate.OneOf(status_enums))
        created_at = fields.DateTime(dump_default=now_timestamp)
        updated_at = fields.DateTime(dump_default=now_timestamp)
