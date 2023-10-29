from flask import Blueprint, request

from application.module.SchoolAdmin import SchoolAdminModel
from application.module.SchoolLearningGroup import SchoolLearningGroupsModel
from application.module.SchoolProject import SchoolProjectModel
from application.module.Schools import SchoolModel
from application.module.SchoolsRole import SchoolRoleModel
from application.utils.output import return_json, OutputObj
from . import *

school_blueprint = Blueprint('school', __name__)


@school_blueprint.route('/add-school', methods=['POST'])
@authenticate(PermissionEnum.ADD_SCHOOL)
def add_school():
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.add_school(req)))


@school_blueprint.route('/<int:school_id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def update_school_info(school_id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolModel.update_school(school_id, req)))


@school_blueprint.route('/<int:school_id>/toggle-status', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_SCHOOL)
@has_school_privilege
def toggle_status(school_id):
    return return_json(OutputObj(code=200, message=SchoolModel.toggle_status(school_id)))


@school_blueprint.route('/list', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
def list_school():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="school information", data=SchoolModel.list_all_schools(page, per_page)))


@school_blueprint.route('/<int:school_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL)
@has_school_privilege
def view_school_info(school_id):
    return return_json(OutputObj(code=200, message="school results", data=SchoolModel.view_school_info(school_id)))


@school_blueprint.route('/<int:school_id>/school-admins', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL_MANAGERS)
@has_school_privilege
def school_managers_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="school Admins results",
                  data=SchoolModel.get_account_admins(school_id, page, per_page)))


@school_blueprint.route('/<int:school_id>/parents', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PARENTS)
@has_school_privilege
def school_parents_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="school parents results", data=SchoolModel.get_parents(school_id, page, per_page)))


@school_blueprint.route('/<int:school_id>/students', methods=['GET'])
@authenticate(PermissionEnum.VIEW_STUDENTS)
@has_school_privilege
def school_students_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school students results",
                                 data=SchoolModel.get_students(school_id, page, per_page)))


@school_blueprint.route('/<int:school_id>/teachers', methods=['GET'])
@authenticate(PermissionEnum.VIEW_TEACHERS)
@has_school_privilege
def school_teachers_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school teachers results",
                                 data=SchoolModel.get_teachers(school_id, page, per_page)))


# ===================================== SCHOOL PROJECT =====================================

@school_blueprint.route('/<int:school_id>/projects', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PROJECTS)
@has_school_privilege
def school_projects_list(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school projects results",
                                 data=SchoolProjectModel.get_projects(school_id, page, per_page)))


@school_blueprint.route('/<int:school_id>/projects/search', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PROJECTS)
@has_school_privilege
def school_projects_search(school_id):
    query = request.args.get('query')
    return return_json(
        OutputObj(code=200, message="projects results", data=SchoolProjectModel.search_projects(query, school_id)))


@school_blueprint.route('/<int:school_id>/projects', methods=['POST'])
@authenticate(PermissionEnum.ADD_PROJECTS)
@has_school_privilege
def add_school_project(school_id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolProjectModel.add_project(school_id, req)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_PROJECTS)
@has_school_privilege
def update_school_project(school_id, project_id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolProjectModel.update_project(school_id, project_id, req)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_PROJECTS)
@has_school_privilege
def delete_school_project(school_id, project_id):
    return return_json(OutputObj(code=200, message=SchoolProjectModel.delete_project(school_id, project_id)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PROJECTS)
@has_school_privilege
def get_project_details(school_id, project_id):
    return return_json(OutputObj(code=200, message=SchoolProjectModel.view_project_detail(school_id, project_id)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>/deactivate', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_PROJECTS)
@has_school_privilege
def deactivate_school_project(school_id, project_id):
    req = request.json
    reason = req['reason']
    return return_json(
        OutputObj(code=200, message=SchoolProjectModel.deactivate_project(school_id, project_id, reason)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>/assign', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_PROJECTS)
@has_school_privilege
def assign_user_to_school_project(school_id, project_id):
    query = request.args.get('action', None)
    req = request.json

    if not query or query.lower() not in ('teacher', 'student'):
        raise CustomException(message="You need to specify if teacher or student you need to assign to project", status_code=400)

    return return_json(
        OutputObj(code=200, message=SchoolProjectModel.assign_user_to_project(school_id, project_id, req, query)))


@school_blueprint.route('/<int:school_id>/projects/<int:project_id>/remove', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_PROJECTS)
@has_school_privilege
def remove_user_from_school_project(school_id, project_id):
    query = request.args.get('action', None)
    req = request.json

    if not query or query.lower() not in ('teacher', 'student'):
        raise CustomException(message="You need to specify if teacher or student you need to assign to project", status_code=400)

    return return_json(
        OutputObj(code=200, message=SchoolProjectModel.remove_user_from_project(school_id, project_id, req, query)))


# ===================================== SCHOOL ADMIN =====================================

@school_blueprint.route('/<int:school_id>/add-school-admin', methods=['POST'])
@authenticate(PermissionEnum.ADD_SCHOOL_MANAGERS)
@has_school_privilege
def add_school_admin(school_id):
    req = request.json
    return return_json(OutputObj(code=200, message=SchoolAdminModel.add_school_admin(school_id, req)))


@school_blueprint.route('/<int:school_id>/get-admin/<int:user_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL_MANAGERS)
@has_school_privilege
def get_school_admin(school_id, user_id):
    return return_json(OutputObj(code=200, message="School Admin results", data=SchoolAdminModel.get_user(user_id, school_id)))


@school_blueprint.route('/<int:school_id>/update-school-admin', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_SCHOOL_MANAGERS)
@has_school_privilege
def update_school_admin(school_id):
    user_id = request.args.get('user_id', None)
    if not user_id or not user_id.isdigit():
        raise CustomException(message="You need to pass user id as query parameter", status_code=400)
    args = request.json
    return return_json(OutputObj(code=200, message="User information has been updated successfully", data=SchoolAdminModel.update_school_admin(user_id, school_id, args)))


@school_blueprint.route('/<int:school_id>/search-school-admin', methods=['GET'])
@authenticate(PermissionEnum.VIEW_SCHOOL_MANAGERS)
def search_school_admin(school_id):
    query = request.args.get('query')
    return return_json(OutputObj(code=200, message="Admin results", data=SchoolAdminModel.search_school_admin(query, school_id)))


@school_blueprint.route('/<int:school_id>/toggle-school-admin-status', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_SCHOOL_MANAGERS)
def delete_school_admin(school_id):
    args = request.json
    admin_id = args.get('admin_id')
    reason = args.get('reason')

    if not admin_id or not reason:
        raise CustomException(message="admin_id and reason must be provided")

    return return_json(
        OutputObj(code=200, message="Admin information", data=SchoolAdminModel.deactivate_school_user(admin_id, school_id, reason)))


@school_blueprint.route('/<int:school_id>/reset-school-admin-password', methods=['POST'])
@authenticate(PermissionEnum.RESET_SCHOOL_MANAGERS_PASSWORD)
def reset_school_admin_password(school_id):
    req = request.json
    user_id = req.get('user_id')
    if not user_id:
        raise CustomException(message="user_id is required")
    return return_json(OutputObj(code=200, message=SchoolAdminModel.reset_school_password(user_id, school_id)))


# ===================================== SCHOOL ROLE =====================================

@school_blueprint.route('/<int:school_id>/roles', methods=['GET'])
@authenticate(PermissionEnum.VIEW_ROLES)
@has_school_privilege
def list_school_roles(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school roles results",
                                 data=SchoolRoleModel.get_school_roles(school_id, page, per_page)))


@school_blueprint.route('/permissions', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PERMISSIONS)
def list_school_permissions():
    return return_json(OutputObj(code=200, message="school permissions results", data=SchoolRoleModel.GetAllPermissions()))


@school_blueprint.route('/<int:school_id>/roles/<int:role_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_ROLES)
@has_school_privilege
def get_school_role_detail(school_id, role_id):
    return return_json(OutputObj(code=200, message=SchoolRoleModel.get_role_details(school_id, role_id)))


@school_blueprint.route('/<int:school_id>/roles', methods=['POST'])
@authenticate(PermissionEnum.ADD_ROLES)
@has_school_privilege
def add_school_role(school_id):
    args = request.json
    name = args.get('name')
    description = args.get('description')
    return return_json(OutputObj(code=200, message="A new school role has been successfully added",
                                 data=SchoolRoleModel.create_school_role(name, description, school_id)))


@school_blueprint.route('/<int:school_id>/roles/<int:role_id>', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_ROLE)
@has_school_privilege
def delete_role_from_school(school_id, role_id):
    return return_json(OutputObj(code=200, message=SchoolRoleModel.delete_school_role(role_id, school_id)))


@school_blueprint.route('/<int:school_id>/roles/<int:role_id>/toggle-status', methods=['PUT'])
@authenticate(PermissionEnum.DEACTIVATE_ROLE)
@has_school_privilege
def toggle_school_role(school_id, role_id):
    return return_json(
        OutputObj(code=200, message=SchoolRoleModel.toggle_school_role_status(role_id, school_id)))


@school_blueprint.route('/<int:school_id>/roles/<int:role_id>', methods=['PATCH'])
@authenticate(PermissionEnum.MODIFY_ROLE)
@has_school_privilege
def update_role_school(role_id, school_id):
    args = request.json
    name = args.get('name', None)
    description = args.get('description', None)
    return return_json(
        OutputObj(code=200, message="School Role has been successfully updated", data=SchoolRoleModel.update_school_role(school_id, role_id, name, description)))


@school_blueprint.route('/<int:school_id>/permission', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_ROLE)
@has_school_privilege
def assign_permission_school_role(school_id):
    role_id = request.args.get('role_id')
    permission_id = request.args.get('permission_id')
    if not role_id or not permission_id or not role_id.isdigit() or not permission_id.isdigit():
        raise CustomException(message="Please pass a correct role id or permission id")
    return return_json(OutputObj(code=200, message="Permission has been successfully assigned to school role",
                                 data=SchoolRoleModel.assign_permission_to_school_role(school_id, role_id, permission_id)))


@school_blueprint.route('/<int:school_id>/permission', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_ROLE)
@has_school_privilege
def remove_school_permission_from_role(school_id):
    role_id = request.args.get('role_id', None)
    permission_id = request.args.get('permission_id', None)
    if not role_id or not permission_id or not role_id.isdigit() or not permission_id.isdigit():
        raise CustomException(message="Please pass a correct role id or permission id")
    return return_json(OutputObj(code=200, message="Permission has been successfully removed from school role",
                                 data=SchoolRoleModel.remove_permission_from_school_role(school_id, role_id,
                                                                                         permission_id)))


# ===================================== SCHOOL LEARNING GROUP =====================================

@school_blueprint.route('/<int:school_id>/learning-groups', methods=['GET'])
@authenticate(PermissionEnum.VIEW_LEARNING_GROUPS)
@has_school_privilege
def fetch_all_school_groups(school_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(OutputObj(code=200, message="school learning groups results", data=SchoolLearningGroupsModel.list_all_groups(school_id, page, per_page)))


@school_blueprint.route('/<int:school_id>/learning-groups/<int:group_id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_LEARNING_GROUPS)
@has_school_privilege
def get_school_group_detail(school_id, group_id):
    return return_json(OutputObj(code=200, message=SchoolLearningGroupsModel.get_group_detail(school_id, group_id)))


@school_blueprint.route('/<int:school_id>/learning-groups', methods=['POST'])
@authenticate(PermissionEnum.ADD_LEARNING_GROUPS)
@has_school_privilege
def add_school_learning_group(school_id):
    args = request.json
    return return_json(
        OutputObj(code=200, message="A new school learning group has been successfully added", data=SchoolLearningGroupsModel.create_learning_group(args, school_id)))


@school_blueprint.route('/<int:school_id>/learning-groups/<int:group_id>/toggle-status', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_LEARNING_GROUPS)
@has_school_privilege
def toggle_school_learning_group(school_id, group_id):
    return return_json(
        OutputObj(code=200, message=SchoolLearningGroupsModel.toggle_school_learning_group_status(school_id, group_id)))


@school_blueprint.route('/<int:school_id>/learning-groups/<int:group_id>', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_LEARNING_GROUPS)
@has_school_privilege
def delete_school_group(school_id, group_id):
    return return_json(OutputObj(code=200, message=SchoolLearningGroupsModel.delete_group(school_id, group_id)))


@school_blueprint.route('/<int:school_id>/learning-groups/<int:group_id>', methods=['PATCH'])
@authenticate(PermissionEnum.MODIFY_LEARNING_GROUPS)
@has_school_privilege
def update_school_group(group_id, school_id):
    args = request.json
    name = args.get('name', None)
    description = args.get('description', None)
    return return_json(OutputObj(code=200, message="School learning group has been successfully updated",
                                 data=SchoolLearningGroupsModel.update_group(school_id, group_id, name, description)))
