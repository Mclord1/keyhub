import os

DBHOST = os.getenv('DBHOST')
DBPORT = os.getenv('DBPORT')
DBUSERNAME = os.getenv('DBUSERNAME')
DBPASSWORD = os.getenv('DBPASSWORD')

DB_SETUP = {
    "local": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'defaultdb'
    },
    "development": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'defaultdb'
    },
    "stage": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'defaultdb'
    },
    "production": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'keyhubprod'
    },
}
