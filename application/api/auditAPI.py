from flask import Blueprint, request

from application.module.Audits import AuditModel
from application.utils.output import return_json, OutputObj
from . import *

audit_blueprint = Blueprint('audit', __name__)


@audit_blueprint.route('/list-audits', methods=['GET'])
@authenticate(PermissionEnum.VIEW_AUDIT)
def list_all_audits():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="Audits results", data=AuditModel.list_audits(page, per_page)))


@audit_blueprint.route('/get-audit/<int:audit_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_AUDIT)
def get_audit_information(audit_id):
    return return_json(OutputObj(code=200, message="Audits results", data=AuditModel.get_audit_detail(audit_id)))
