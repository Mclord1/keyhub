from flask import Blueprint, request

from application.module.Messages import Communication
from application.utils.output import return_json, OutputObj
from . import *

message_blueprint = Blueprint('message', __name__)


@message_blueprint.route('/send-message', methods=['POST'])
@authenticate()
def send_message():
    req = request.json
    receiver = req.get('receiver')
    content = req.get('content')
    content_type = req.get('content_type')
    return return_json(OutputObj(code=200, message="message sent", data=Communication.user_send_message(receiver, content, content_type)))


@message_blueprint.route('/accept-request/<int:sender>', methods=['PUT'])
@authenticate()
def accept_request(sender):
    return return_json(OutputObj(code=200, message="Request Accepted", data=Communication.take_decision_on_message_request(sender, True)))


@message_blueprint.route('/decline-request/<int:sender>', methods=['PUT'])
@authenticate()
def decline_request(sender):
    return return_json(OutputObj(code=200, message="Request Declined", data=Communication.take_decision_on_message_request(sender, False)))


@message_blueprint.route('/get-request', methods=['GET'])
@authenticate()
def get_request():
    return return_json(OutputObj(code=200, message="Request fetched", data=Communication.get_requests_messages()))


@message_blueprint.route('/get-chats', methods=['GET'])
@authenticate()
def get_chats():
    return return_json(OutputObj(code=200, message="Chats fetched", data=Communication.get_user_messages()))


@message_blueprint.route('/get-chats/<int:sender>', methods=['GET'])
@authenticate()
def get_chats_message(sender):
    return return_json(OutputObj(code=200, message="Chats fetched", data=Communication.get_chat_messages(sender)))
