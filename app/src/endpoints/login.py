from flask import request, Blueprint, jsonify
from app.src import app_config
from app.src.query_methods import hash_password, requires
import mysql.connector
import base64
import os

login_endpoint = Blueprint('login', __name__)


def generate_session_token(length=128):
    random_bytes = os.urandom(length)
    base64_encoded = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    return base64_encoded


def user_exists(username):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE login = '{username}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    return exists


def create_session_token(user):
    new_token = generate_session_token()

    # Save new token in database
    # TO-DO: Handle query error in very (very) rare case of generating duplicate session token
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"UPDATE users SET api_key = '{new_token}' WHERE login = '{user}'"
            cursor.execute(query)
        cnx.commit()

    return new_token


def get_password(username):
    # TO-DO: Secure it from SQL injection
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT password FROM users WHERE login = '{username}'"

            print(query, flush=True)

            cursor.execute(query)
            data = cursor.fetchall()

            print(data, flush=True)

            correct_password = data[0][0]

    return correct_password


@login_endpoint.route('/login', methods=['POST'])
@requires('username', 'password')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # User does not exist, return 'wrong_password' to secure database from leaking valid users
    if not user_exists(username):
        return jsonify({'status': 'fail', 'message': 'user_does_not_exist'}), 401
    # User exists and password is correct, return newly generated session token
    elif hash_password(password) == get_password(username):
        session_token = create_session_token(username)
        return jsonify({'status': 'success', 'session_token': session_token})
    # Incorrect password
    else:
        return jsonify({'status': 'fail', 'message': 'wrong_password'}), 401
