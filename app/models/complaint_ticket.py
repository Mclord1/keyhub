import enum

import jsonschema
from jsonschema.exceptions import ValidationError
from sqlalchemy import JSON
from sqlalchemy.orm import validates

from app import db
from app.Mixins.GenericMixins import GenericMixin


class TicketStatusEnum(enum.Enum):
    OPEN = "open"
    PROCESSING = "processing"
    RESOLVED = "resolved"


class Ticket(db.Model, GenericMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=True)
    full_name = db.Column(db.String(250), nullable=True)
    complaint = db.Column(JSON, nullable=True)
    status = db.Column(db.Enum(TicketStatusEnum, nullable=True, values_callable=lambda x: [str(member.value) for member in TicketStatusEnum]))
    manager_id = db.Column(db.String(250), nullable=True)

    @validates("complaint")
    def validate_complaint(self, value):
        schema = {
            "type": "object",
            "properties": {
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["subject", "body"],
            "additionalProperties": False
        }
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(e)
        except Exception:
            raise ValidationError("Unknown error")
