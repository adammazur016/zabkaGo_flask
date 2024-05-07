from flask import request, Blueprint, jsonify, Response
from src import app_config
import mysql.connector

DEFAULT_USER_COUNT = 50
MAX_USERS_PER_REQUEST = 999
users_endpoint = Blueprint('users', __name__)


def get_users(count: int) -> list[dict]:
    """
    Retrieves the top 'count' users from the database, sorted by ranking points.
    If the 'count' parameter exceeds the limit, it is reduced to the maximum allowed.

    :param count: The number of users to retrieve.
    :return: A list of user data represented as dictionaries.
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
    Retrieves the user with the provided ID.

    :param user_id: The ID of the user to retrieve.
    :return: User data as a dictionary, or an empty dictionary if the user does not exist.
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
    """
    /v1/users endpoint

    Retrieves data of 'count' number of users.
    Maximum of 'MAX_USERS_PER_REQUEST' at once.
    If 'count' is not specified, it defaults to 'DEFAULT_USER_COUNT'.

    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    count = DEFAULT_USER_COUNT
    if request.args.get('count'):
        count = request.args.get('count')
    return jsonify(get_users(count)), 200


@users_endpoint.route('/user/<user_id>', methods=['GET'])
def return_user(user_id) -> (Response, int):
    """
    /v1/user/<user_id> endpoint

    Retrieves data of the user with the provided user ID.

    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    user_data = get_user(user_id)

    # Empty user_data -> user was not found
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"status": "fail", "message": "user_not_found"}), 404


def add_rank_point(session_token, amount=1):
    """
    Adds a ranking point to the user who owns the provided session token.

    :param session_token: The session token of the user.
    :param amount: (Default value = 1) The number of ranking points to add.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"UPDATE users SET rank_points = rank_points + {amount} WHERE session_token = '{session_token}'"
            cursor.execute(query)
        cnx.commit()
