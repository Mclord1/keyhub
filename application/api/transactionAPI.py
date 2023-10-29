import hashlib
import os

from flask import Blueprint, request

transaction_blueprint = Blueprint('transaction', __name__)

paystack_key = os.environ.get('PAYSTACK_TEST')


@transaction_blueprint.route('/paystack-webhook', methods=['POST'])
def paystack_webhook():
    request_data = request.get_data()
    _hash = hashlib.sha512(paystack_key.encode()).update(request_data).hexdigest()

    if _hash == request.headers.get('x-paystack-signature'):
        # Retrieve the request's body
        event = request.get_json()

        # Do something with the event
        return '', 200  # Respond with a 200 status for successful validation

    return '', 403  # Respond with a 403 status for unauthorized requests
