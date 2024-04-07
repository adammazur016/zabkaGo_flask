from flask import request, Blueprint
from .. import config
import mysql.connector

login_endpoint = Blueprint('login', __name__)


def get_session_token(user):
    user = "'" + user + "'"
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = "SELECT api_key FROM users WHERE login = " + user

            cursor.execute(query)
            data = cursor.fetchall()
            session_token = data[0][0]

    return session_token


def get_password(user):
    # TO-DO: Secure it from SQL injection
    user = "'" + user + "'"
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = "SELECT password FROM users WHERE login = " + user

            cursor.execute(query)
            data = cursor.fetchall()

            correct_password = data[0][0]

    return correct_password


@login_endpoint.route('/login', methods=['POST'])
def login():
    user = request.args.get('user')
    password = request.args.get('password')
    session_token = None

    if password == get_password(user):
        session_token = get_session_token(user)

    if session_token:
        return {'status': 'success', 'session_token': session_token}
    else:
        return {'status': 'fail'}
