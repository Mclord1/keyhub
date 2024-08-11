from flask import Blueprint

from application.module.Notification import NotificationModel
from application.utils.output import return_json, OutputObj
from . import *

notification_blueprint = Blueprint('notification', __name__)


@notification_blueprint.route('/', methods=['GET'])
@authenticate()
def get_notifications():
    return return_json(OutputObj(code=200, message="notifications fetched", data=NotificationModel.get_notifications()))


@notification_blueprint.route('/<int:notification_id>', methods=['PUT'])
@authenticate()
def mark_notification_read(notification_id):
    return return_json(OutputObj(code=200, message="notifications read", data=NotificationModel.mark_read(notification_id)))


@notification_blueprint.route('/<int:notification_id>', methods=['DELETE'])
@authenticate()
def delete_notification(notification_id):
    return return_json(OutputObj(code=200, message="notifications deleted", data=NotificationModel.delete_notification(notification_id)))
