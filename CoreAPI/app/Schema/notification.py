from pydantic import BaseModel


class NotificationIdSchema(BaseModel):
    notification_id: int

