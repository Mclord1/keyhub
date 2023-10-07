from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from application.module.authentication import Authentication
from application.utils.output import return_json, OutputObj

auth_blueprint = Blueprint('auth', __name__)
authenticationModel = Authentication()


@auth_blueprint.route('/refresh-token', methods=['GET'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return return_json(OutputObj(message="Token has been refreshed", data={"access_token": access_token}, code=200))


@auth_blueprint.route('/login', methods=['POST'])
def login():
    req = request.json
    email = req.get('email')
    password = req.get('password')
    return authenticationModel.Login(email, password)


@auth_blueprint.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    req = request.json
    code = req.get('otp')
    password = req.get('password')
    return authenticationModel.update_password(code, password)


@auth_blueprint.route('/ping')
def ping():
    return return_json(OutputObj(message="pong!!"))
