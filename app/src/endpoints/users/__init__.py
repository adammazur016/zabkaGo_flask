from flask import request, Blueprint, jsonify, Response
from src import app_config
import mysql.connector

DEFAULT_USER_COUNT = 50
MAX_USERS_PER_REQUEST = 999
users_endpoint = Blueprint('users', __name__)


def get_users(count: int) -> list[dict]:
    """
    Looks up top 'count' users in database, sorted by ranking points.
    If 'count' parameter exceeds the limit, it is reduced to allowed maximum.
    :returns: List of users data represented as dictionary.
    """
    users_data = []
    # Limit number of users in single lookup
    if count > MAX_USERS_PER_REQUEST:
        count = MAX_USERS_PER_REQUEST
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT id, displayed_name, rank_points FROM users ORDER BY rank_points DESC LIMIT {count}"
            cursor.execute(query)
            data = cursor.fetchall()
            for user in data:
                users_data.append({"id": user[0], "name": user[1], "points": user[2]})
    return users_data


def get_user(user_id: int) -> dict:
    """
    Looks up user with provided id.
    :returns: user data as dictionary or empty dict if user does not exist.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"SELECT id, displayed_name, rank_points FROM users where id = {user_id}"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                user_data = {"id": data[0][0], "name": data[0][1], "points": data[0][2]}
                return user_data
            else:
                return {}


@users_endpoint.route('/users', methods=['GET'])
def return_users() -> (Response, int):
    """ /v1/users endpoint

    Returns data of 'count' number of users
    Maximum of 'MAX_USERS_PER_REQUEST' at once
    If 'count' is not found, it is replaced by 'DEFAULT_USER_COUNT'
    :returns: json serialized response, http status code
    """
    count = DEFAULT_USER_COUNT
    if request.args.get('count'):
        count = request.args.get('count')
    return jsonify(get_users(count)), 200


@users_endpoint.route('/user/<user_id>', methods=['GET'])
def return_user(user_id) -> (Response, int):
    """ /v1/user/<user_id> endpoint

    Returns data of user with provided user id.
    :returns: json serialized response, http status code
    """
    user_data = get_user(user_id)

    # Empty user_data -> user was not found
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"status": "fail", "message": "user_not_found"}), 404


def add_rank_point(session_token, amount=1):
    """
    Adds ranking point to user who owns provided session token
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"UPDATE users SET rank_points = rank_points + {amount} WHERE session_token = '{session_token}'"
            cursor.execute(query)
        cnx.commit()
