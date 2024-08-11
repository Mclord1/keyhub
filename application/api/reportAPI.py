from flask import Blueprint, request

from application.Enums.Permission import PermissionEnum
from application.module.reports import ReportModel
from application.utils.authenticator import authenticate
from application.utils.output import return_json, OutputObj

report_blueprint = Blueprint('reports', __name__)


@report_blueprint.route('/revenues', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_revenues():
    return return_json(OutputObj(code=200, message="", data=ReportModel.revenues()))


@report_blueprint.route('/subscription-transactions', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_subscription_transaction():
    return return_json(OutputObj(code=200, message="", data=ReportModel.subscription_transaction()))


@report_blueprint.route('/revenue-breakdown', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_revenue_breakdown():
    return return_json(OutputObj(code=200, message="", data=ReportModel.revenue_breakdown()))


@report_blueprint.route('/revenue-analytics', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TRANSACTIONS)
def get_revenue_analytics():
    year = int(request.args.get('year', 2023))
    return return_json(OutputObj(code=200, message="", data=ReportModel.revenue_analytics(year)))
