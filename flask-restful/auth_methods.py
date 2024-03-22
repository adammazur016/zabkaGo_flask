from functools import wraps
from flask import request
import mysql.connector

def access_denied():
    return {'error_message': 'Not correct credentials'}, 401


def admin_verify(admin_api_key: str):
    # To-Do: Implement verification via db
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(api_key: str):
    mydb = mysql.connector.connect(
        host="172.18.0.2",
        user="db_user",
        password="db_user_pass",
        database="app_db"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT count(api_key) AS number FROM users WHERE api_key = '"+api_key + "'")

    myresult = mycursor.fetchall()

    if myresult[0][0] == 1:
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
