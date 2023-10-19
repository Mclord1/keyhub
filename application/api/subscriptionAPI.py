from flask import Blueprint, request

from application.module.Subscriptions import SubscriptionModel
from application.utils.output import return_json, OutputObj
from . import *

subcription_blueprint = Blueprint('subscription', __name__)


@subcription_blueprint.route('/list-subscriptions', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SUBSCRIPTION)
def list_subscriptions():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="Subscriptions results", data=SubscriptionModel.get_subscriptions(page, per_page)))


@subcription_blueprint.route('/subscription-page-info', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SUBSCRIPTION)
def subscriptions_page_info():
    return return_json(OutputObj(code=200, message="Subscription page information",
                                 data=SubscriptionModel.get_subscription_page_info()))


@subcription_blueprint.route('/list-plans', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SUBSCRIPTION)
def list_subcription_plans():
    return return_json(OutputObj(code=200, message="subcription plans",
                                 data=SubscriptionModel.list_plans()))


@subcription_blueprint.route('/toggle-plan-status/<int:id>', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_SUBSCRIPTION)
def toggle_plan_status(id):
    return return_json(OutputObj(code=200, message="Subscription plan status has been changed",
                                 data=SubscriptionModel.disable_plan(id)))


@subcription_blueprint.route('/delete-plan/<int:id>', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_SUBSCRIPTION)
def delete_plan(id):
    return return_json(
        OutputObj(code=200, message="Subscription plan has been deleted", data=SubscriptionModel.delete_plan(id)))


@subcription_blueprint.route('/update-plan/<int:id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SUBSCRIPTION)
def update_plan(id):
    args = request.json
    return return_json(OutputObj(code=200, message="Subscription plan information has been modified",
                                 data=SubscriptionModel.update_plan(id, args)))


@subcription_blueprint.route('/add-plan', methods=['POST'])
@authenticate(PermissionEnum.ADD_SUBSCRIPTION)
def add_plan():
    args = request.json
    return return_json(
        OutputObj(code=200, message="New subcription plan has been added", data=SubscriptionModel.create_plan(args)))
