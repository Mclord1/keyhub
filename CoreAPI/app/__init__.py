import os
from flask_sqlalchemy import SQLAlchemy
from config.DBConfig import DB_SETUP
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)
app.app_context().push()
app.config["ENVIRONMENT"] = os.environ.get("environment", "development")
environment = str(app.config["ENVIRONMENT"]).lower()

database = DB_SETUP[environment]

if not database:
    raise EnvironmentError

username = database['username']
password = database['password']
host = database['host']
port = database['port']
database_name = database['database']

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)
metadata = db.metadata
