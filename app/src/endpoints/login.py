from flask import request, Blueprint, jsonify, Response
from src import app_config
from src.query_methods import hash_password, requires, get_user_id
import mysql.connector
import base64
import os

login_endpoint = Blueprint('login', __name__)


def generate_session_token(length: int = 128) -> str:
    """
    Generates a session token using URL-safe base64 encoding.

    :param length: (Default value = 128) The number of characters in the session token.
    :return: The newly generated session token.
    """
    random_bytes = os.urandom(length)
    base64_encoded = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

    return base64_encoded


def does_user_exists(username: str) -> bool:
    """
    Checks if the username exists in the database.

    :return: True if the username exists, False otherwise.
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
    Generates a new session token upon login.

    :return: The newly generated session token.
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
    Retrieves the hashed password associated with the given username from the database.

    :return: The hashed password of the user.
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
    """
    /v1/login endpoint.

    Verifies if the provided username and password match records in the database.
    Upon successful verification, generates a new session token and returns it to the user.

    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    username = request.args.get("username")
    password = request.args.get("password")

    # User does not exist, return 'wrong_password' to secure database from leaking valid users
    if not does_user_exists(username):
        return jsonify({"status": "fail", "message": "wrong_password"}), 401
    # User exists and password is correct, return newly generated session token
    elif hash_password(password) == get_password(username):
        session_token = create_session_token(username)
        user_id = get_user_id(session_token)
        return jsonify({"status": "success", "session_token": session_token, "user_id": user_id}), 200
    # Incorrect password
    else:
        return jsonify({"status": "fail", "message": "wrong_password"}), 401
