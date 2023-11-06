import hashlib
import os

from flask import Blueprint, request

from application import return_json, OutputObj
from application.Enums.Permission import PermissionEnum
from application.module.Subscriptions import SubscriptionModel
from application.module.Transactions import TransactionModel
from application.utils.authenticator import authenticate

transaction_blueprint = Blueprint('transaction', __name__)

paystack_key = os.environ.get('PAYSTACK_TEST')


def compute_hmac_sha512(key, json_input):
    result = ""
    secret_key_bytes = key.encode("utf-8")
    input_bytes = json_input.encode("utf-8")

    hmac_sha512 = hashlib.new("sha512", secret_key_bytes)
    hmac_sha512.update(input_bytes)
    hash_value = hmac_sha512.digest()

    result = hash_value.hex()
    return result


@transaction_blueprint.route('/paystack-webhook', methods=['POST'])
def paystack_webhook():
    print("webhook has been called")
    request_data = request.get_data()
    print(request_data)
    result = compute_hmac_sha512(paystack_key, request_data)
    print(result)
    print(request.headers.get('x-paystack-signature'))
    # combined_data = paystack_key + request_data.decode('utf-8')
    # _hash = hashlib.sha512(combined_data.encode()).hexdigest()
    if result.lower() == request.headers.get('x-paystack-signature'):
        # Retrieve the request's body
        event = request.get_json()
        if event:
            print(event)
            SubscriptionModel.process_subscription(event)
        # Do something with the event
        return '', 200  # Respond with a 200 status for successful validation

    return '', 403  # Respond with a 403 status for unauthorized requests


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
