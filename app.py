import os
from application import app, jwt
from application.api import *
from application.models import User

EXEC_ENV = os.environ.get('EXEC_ENV')

# BLUEPRINT REGISTRATION
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(roles_permission_blueprint, url_prefix='/role-permission')


# @jwt.user_identity_loader
# def _user_identity_lookup(user):
#     return user.id


@jwt.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    # Retrieve the user object based on the identity (user ID)
    user = User.query.filter_by(id=identity).first()
    return user


if __name__ == '__main__':
    app.run(port=3000, debug=True)
