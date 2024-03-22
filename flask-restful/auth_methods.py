from functools import wraps
from flask import request
import mysql.connector

def connectDb():
    mydb = mysql.connector.connect(
        host="172.18.0.2",
        user="db_user",
        password="db_user_pass"
    )
    print(mydb)



def access_denied():
    return {'error_message': 'Not correct credentials'}, 401


def admin_verify(admin_api_key: str):
    # To-Do: Implement verification via db
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(api_key: str):
    connectDb()
    # To-Do: Implement verification via db
    if api_key == 'test':
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
        if request.args.get('api_key') and verify(request.args.get('api_key')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key
