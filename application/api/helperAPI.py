from flask import Blueprint
from flask_jwt_extended import jwt_required

from application.helpers.country import CountryModel
from application.utils.output import return_json, OutputObj

helper_blueprint = Blueprint('helper', __name__)


@helper_blueprint.route('/countries', methods=['GET'])
@jwt_required()
def list_countries():
    return return_json(OutputObj(code=200, message="Countries results", data=CountryModel.CountryList()))


@helper_blueprint.route('/countries/<int:id>', methods=['GET'])
@jwt_required()
def list_country_states(id):
    return return_json(OutputObj(code=200, message="States results", data=CountryModel.get_states_by_country(id)))
