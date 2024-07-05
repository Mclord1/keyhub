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
        'database': 'keyhub'
    },
    "development": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'keyhubdev'
    },
    "stage": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'keyhubstage'
    },
    "production": {
        "username": DBUSERNAME,
        "password": DBPASSWORD,
        "host": DBHOST,
        "port": DBPORT,
        'database': 'keyhubprod'
    },
}
