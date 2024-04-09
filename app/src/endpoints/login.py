from flask import request, Blueprint
from app.src import app_config
from app.src.auth_methods import hash_password
import mysql.connector
import base64
import os

login_endpoint = Blueprint('login', __name__)


def generate_session_token(length=32):
    random_bytes = os.urandom(length)
    base64_encoded = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    return base64_encoded


def create_session_token(user):
    new_token = generate_session_token()

    # Save new token in database
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"UPDATE users SET api_key = '{new_token}' WHERE login = '{user}'"
            cursor.execute(query)
        cnx.commit()

    return new_token


def get_password(user):
    # TO-DO: Secure it from SQL injection
    user = "'" + user + "'"
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
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

    if hash_password(password) == get_password(user):
        session_token = create_session_token(user)

    if session_token:
        return {'status': 'success', 'session_token': session_token}
    else:
        return {'status': 'fail'}
