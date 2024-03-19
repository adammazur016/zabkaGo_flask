from flask import Flask
from functools import wraps
from flask import request
from flask_mysqldb import MySQL
from api import testDatabase


def access_denied():
    return {'error_message': 'Not correct credentials'}, 401


def access_granted():
    testDatabase()
    return {'response_code': '1'}


def admin_verify(admin_api_key: str):
    # To-Do: Implement verification via db
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(login: str):
    # To-Do: Implement verification via db
    if login == 'test':

        return True
    else:
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
        if request.args.get('login') and verify(request.args.get('login')):
            return access_granted()
        else:
            return access_denied()
    return verify_key
