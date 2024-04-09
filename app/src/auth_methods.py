from functools import wraps
from flask import request
from app.src import app_config
import mysql.connector


def access_denied():
    return {'error_message': 'incorrect_credentials'}, 401


def admin_verify(admin_api_key: str):
    # To-Do: Implement verification via db
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(api_key: str):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            cursor.execute("SELECT count(api_key) AS number FROM users WHERE api_key = '"+api_key + "'")
            result = cursor.fetchall()

            if result[0][0] == 1:
                return True

            return False


def admin_auth(func):
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('api_key') and admin_verify(request.args.get('api_key')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key


def auth(func):
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('api_key') and verify(request.args.get('api_key')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key
