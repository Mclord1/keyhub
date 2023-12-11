from operator import and_
from typing import List

from sqlalchemy import func, or_, and_

from application import db
from application.models import *
from application.module import current_user
from exceptions.custom_exception import CustomException


class Communication:

    @classmethod
    def handle_user_2_user(cls, sender: User, receiver: User, content: str, content_type: str):
        last_message = Message.query.filter(
            or_(
                and_(Message.sender_id == sender.id, Message.receiver_id == receiver.id),
                and_(Message.sender_id == receiver.id, Message.receiver_id == sender.id)
            )
        ).order_by(Message.created_at.desc()).first()

        school_matches = not sender.admins and User.GetSchool(sender.id).id == User.GetSchool(receiver.id).id

        if sender.admins or (school_matches or (last_message and last_message.request_accepted)):
            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=content,
                content_type=content_type
            )
            message.save(refresh=True)

        elif not last_message and not school_matches:
            message = Message(
                sender_id=sender.id,
                receiver_id=receiver.id,
                content=content,
                request_accepted=False,
                content_type=content_type
            )
            message.save(refresh=True)

        elif last_message and not last_message.request_accepted and not school_matches:
            raise CustomException(message="Wait for receiver's acceptance to start the conversation")

    @classmethod
    def user_send_message(cls, receiver, content, content_type):

        sender: User = User.GetUser(current_user.id)
        receiver: User = User.GetUser(receiver)

        if content_type.lower() not in ('text', 'file'):
            raise CustomException(message="The file type is not supported", status_code=400)

        if receiver.id == sender.id:
            raise CustomException(message="You can't send yourself message", status_code=400)

        if not content:
            raise CustomException(message="Message cannot be empty", status_code=400)

        cls.handle_user_2_user(sender, receiver, content, content_type)

    @classmethod
    def take_decision_on_message_request(cls, sender_id, decision: bool):
        message: Message = Message.query.filter_by(sender_id=sender_id, receiver_id=current_user.id, request_accepted=False).first()

        if not message:
            raise CustomException(message="No message request was found", status_code=404)

        message.request_accepted = decision
        db.session.commit()
        return "You accepted the message" if decision else "You have declined the message"

    @classmethod
    def get_requests_messages(cls):
        messages_request: List[Message] = Message.query.filter_by(receiver_id=current_user.id, request_accepted=False).all()
        return [x.to_dict(add_filter=False) for x in messages_request]

    @classmethod
    def get_user_messages(cls):
        subquery = db.session.query(
            func.max(Message.id).label('max_id')
        ).filter(
            (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
        ).group_by(
            (func.LEAST(Message.sender_id, Message.receiver_id)),
            (func.GREATEST(Message.sender_id, Message.receiver_id))
        ).subquery()

        last_messages = db.session.query(Message, func.max(Message.created_at).label('last_message_time')).join(
            subquery, Message.id == subquery.c.max_id
        ).filter(
            (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
        ).group_by(
            Message.id,
            (func.LEAST(Message.sender_id, Message.receiver_id)),
            (func.GREATEST(Message.sender_id, Message.receiver_id))
        ).all()

        return [{
            'sender': User.GetUserFullName(message.sender_id) if message.sender_id != current_user.id else 'me',
            'receiver': User.GetUserFullName(message.receiver_id) if message.receiver_id != current_user.id else 'me',
            'content': message.content,
            'time': last_message_time,
            'is_read': message.is_read,
            'user_id': message.sender_id if current_user.id == message.receiver_id else message.receiver_id,
            'content_type': message.content_type,
            'request_accepted': message.request_accepted
        } for message, last_message_time in last_messages]

    @classmethod
    def get_chat_messages(cls, receiver_id):
        chats: List[Message] = db.session.query(Message).filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.created_at).all()

        return [
            {
                'sender': User.GetUserFullName(chat.sender_id) if chat.sender_id != current_user.id else 'me',
                'receiver': User.GetUserFullName(chat.receiver_id) if chat.receiver_id != current_user.id else 'me',
                'content': chat.content,
                'time': chat.created_at,
                'user_id': chat.sender_id if current_user.id == chat.receiver_id else chat.receiver_id,
                'content_type': chat.content_type,
                'is_read': chat.is_read,
                'request_accepted': chat.request_accepted
            }
            for chat in chats]



