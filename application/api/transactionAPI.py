import base64
import hashlib
import hmac
import json
import os

from dotenv import load_dotenv

load_dotenv()
from flask import Blueprint, request, Response

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Subscriptions import SubscriptionModel
from application.module.Transactions import TransactionModel
from application.utils.authenticator import authenticate

transaction_blueprint = Blueprint('transaction', __name__)

paystack_key = os.environ.get('PAYSTACK_TEST')


@transaction_blueprint.route('/paystack-webhook', methods=['POST'])
def paystack_webhook():
    print(request.headers)
    print(request.method)
    print(paystack_key)

    if request.method != 'POST' or 'X-Paystack-Signature' not in request.headers:
        return "Method Not Allowed", 405

    ip = request.headers.get('X-Forwarded-For')

    print("webhook has been called")
    request_data = request.get_data()

    print("request-form")
    print(request.form)

    print("request-body")
    print(request.data)

    print("request-data")
    print(request_data)

    calculated_signature = hmac.new(paystack_key.encode(), request.data, hashlib.sha512).hexdigest()

    print("calculated-data")
    print(calculated_signature)

    client_ip = request.remote_addr

    print("IP ADDEREES:: ", client_ip)

    signature = request.headers['X-Paystack-Signature']

    print("body****")
    print(request.environ)

    print("JSON****")
    print(request.json)

    # if signature != calculated_signature:
    #     return "Forbidden", 403

    # if i

    response = Response(status=200)

    # Retrieve the request's body
    event = json.loads(request_data)

    print(event)
    SubscriptionModel.process_subscription(event)
    # Do something with the event
    return response


@transaction_blueprint.route('/all', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_all_transactions():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Transaction results", data=TransactionModel.get_transactions(page, per_page)))


@transaction_blueprint.route('/<int:transaction_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_single_transactions(transaction_id):
    return return_json(OutputObj(code=200, message="Transaction results", data=TransactionModel.get_single_transaction(transaction_id)))


@transaction_blueprint.route('/search-transaction', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def search_student():
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Transaction results", data=TransactionModel.search_school_transaction(query)))


@transaction_blueprint.route('/<int:transaction_id>/completed', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_TRANSACTION)
def mark_completed(transaction_id):
    return return_json(OutputObj(code=200, message="Transaction has been marked completed", data=TransactionModel.mark_as_completed(transaction_id)))


@transaction_blueprint.route('/<int:transaction_id>/cancelled', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_TRANSACTION)
def mark_cancelled(transaction_id):
    return return_json(OutputObj(code=200, message="Transaction has been marked cancelled", data=TransactionModel.mark_as_cancelled(transaction_id)))


import hashlib

SECRET_KEY = 'pk_test_0f44563f9339ea378c37ec1d8ce0c6ef85fb9467'  # Replace with your actual secret key



