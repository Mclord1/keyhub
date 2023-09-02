from flask_jwt_extended import verify_jwt_in_request, get_current_user, current_user

from application.models import *
import bcrypt
from exceptions.custom_exception import CustomException, ExceptionCode
from application.utils.output import OutputObj, return_json
import datetime
from application.Schema.users import *
from application.Schema import validator
from application import db, app
import random
import string
from sqlalchemy.exc import IntegrityError
from application.Schema.pagination import PaginationSchema
import json
current_user = current_user


def enum_serializer(value):
    if isinstance(value, datetime.datetime):
        return value.timestamp()
    else:
        return value.value
