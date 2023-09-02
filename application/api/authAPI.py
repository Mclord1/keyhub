from flask import Blueprint, request
from flask_jwt_extended import create_access_token, current_user, jwt_required
from application.module.authentication import Authentication

from application.utils.output import return_json, OutputObj

auth_blueprint = Blueprint('auth', __name__)
authenticate = Authentication()


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    access_token = create_access_token(identity=current_user)
    return return_json(OutputObj(message="Token has been refreshed", data={"access_token": access_token}, code=200))


@auth_blueprint.route('/login', methods=['POST'])
def login():
    req = request.json
    email = req.get('email')
    password = req.get('password')
    return authenticate.Login(email, password)

