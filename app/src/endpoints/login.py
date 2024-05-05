from flask import request, Blueprint, jsonify, Response
from src import app_config
from src.query_methods import hash_password, requires, get_user_id
import mysql.connector
import base64
import os

login_endpoint = Blueprint('login', __name__)


def generate_session_token(length: int = 128) -> str:
    """
    Generates session token using url-safe base64
    :param length: (Default value = 128) number of characters in session token
    :returns: Returns new session token
    """
    random_bytes = os.urandom(length)
    base64_encoded = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    return base64_encoded


def user_exists(username: str) -> bool:
    """
    Checks if username exists in database
    :param username: str: Checked user
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE login = '{username}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    if exists:
        return True
    else:
        return False


def create_session_token(username: str) -> str:
    """
    Creates new session token upon login
    :returns: Returns newly generated session token
    """
    new_token = generate_session_token()

    # Save new token in database
    # TODO: Handle query error in very (very) rare case of generating duplicate session token
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"UPDATE users SET session_token = '{new_token}' WHERE login = '{username}'"
            cursor.execute(query)
        cnx.commit()

    return new_token


def get_password(username: str) -> str:
    """
    :param username: User whose password will be returned
    :returns: Returns user's hashed password
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT password FROM users WHERE login = '{username}'"

            cursor.execute(query)
            data = cursor.fetchall()

            correct_password = data[0][0]

    return correct_password


@login_endpoint.route('/login', methods=['POST'])
@requires('username', 'password')
def login() -> (Response, int):
    """ /v1/login endpoint

    Checks if given username and password match with database
    Successful verification generates new session token and returns it to user
    :returns: json serialized response, http status code
    """
    username = request.args.get("username")
    password = request.args.get("password")

    # User does not exist, return 'wrong_password' to secure database from leaking valid users
    if not user_exists(username):
        return jsonify({"status": "fail", "message": "wrong_password"}), 401
    # User exists and password is correct, return newly generated session token
    elif hash_password(password) == get_password(username):
        session_token = create_session_token(username)
        user_id = get_user_id(session_token)
        return jsonify({"status": "success", "session_token": session_token, "user_id": user_id}), 200
    # Incorrect password
    else:
        return jsonify({"status": "fail", "message": "wrong_password"}), 401
