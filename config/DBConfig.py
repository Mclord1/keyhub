DB_SETUP = {
    "local": {
        "username": 'keyhub',
        "password": 'keyhub',
        "host": '3.145.101.11',
        "port": 5431,
        'database': 'keyhub'
    },
    "development": {
        "username": 'keyhub',
        "password": 'keyhub',
        "host": 'localhost',
        "port": 5431,
        'database': 'keyhub'
    },
    "stage": {
        "username": 'keyhub123',
        "password": 'keyhub123',
        "host": 'localhost',
        "port": 5431,
        'database': 'keyhub'
    },
    "production": {
        "username": 'keyhub123',
        "password": 'keyhub123',
        "host": 'localhost',
        "port": 5431,
        'database': 'keyhub'
    },
}

# 3.145.101.11


# {'event': 'charge.success', 'data': {'id': 3255509570, 'domain': 'test', 'status': 'success', 'reference': '1699108606589-4797', 'amount': 300000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2023-11-04T14:36:52.000Z', 'created_at': '2023-11-04T14:36:49.000Z', 'channel': 'card', 'currency': 'NGN', 'ip_address': '102.215.57.12', 'metadata': {'schoolId': 7, 'planId': 3, 'planName': 'Premium', 'planDuration': '30', 'referrer': 'http://localhost:8080/school/select-plans'}, 'fees_breakdown': None, 'log': None, 'fees': 14500, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_0u5fvmmiom', 'bin': '408408', 'last4': '4081', 'exp_month': '12', 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK', 'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_bGmTjswH4ERJ9OdTFIAH', 'account_name': None, 'receiver_bank_account_number': None, 'receiver_bank': None}, 'customer': {'id': 146500804, 'first_name': None, 'last_name': None, 'email': 'testadmin333@gmail.com', 'customer_code': 'CUS_lfg28644jlg2xhr', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': {}, 'subaccount': {}, 'split': {}, 'order_id': None, 'paidAt': '2023-11-04T14:36:52.000Z', 'requested_amount': 300000, 'pos_transaction_data': None, 'source': {'type': 'web', 'source': 'checkout', 'entry_point': 'request_inline', 'identifier': None}}}
