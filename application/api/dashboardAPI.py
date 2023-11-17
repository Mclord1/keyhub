from flask import Blueprint, request

from application.module.dashboard import DashboardModel
from application.utils.authenticator import authenticate
from application.utils.output import return_json, OutputObj

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/school-statistics', methods=['GET'])
@authenticate()
def school_statistics():
    return return_json(OutputObj(code=200, message="", data=DashboardModel.school_stat()))


@dashboard_blueprint.route('/get-monthly-statistics', methods=['GET'])
@authenticate()
def get_monthly_statistics_():
    query = request.args.get('year', '2023')
    return return_json(OutputObj(code=200, message="", data=DashboardModel.get_monthly_statistics(query)))


@dashboard_blueprint.route('/activity-feed', methods=['GET'])
@authenticate()
def get_activity_feed():
    return return_json(OutputObj(code=200, message="", data=DashboardModel.activity_feed()))


@dashboard_blueprint.route('/monthly-revenue', methods=['GET'])
@authenticate()
def get_filter_revenue_by_month():
    year = int(request.args.get('year', 2023))
    month = int(request.args.get('month', 11))
    return return_json(OutputObj(code=200, message="", data=DashboardModel.filter_revenue_by_month(month, year)))


@dashboard_blueprint.route('/recent-school', methods=['GET'])
@authenticate()
def get_recently_added_school():
    return return_json(OutputObj(code=200, message="", data=DashboardModel.recently_added_school()))
