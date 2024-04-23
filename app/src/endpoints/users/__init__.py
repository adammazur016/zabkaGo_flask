from flask import request, Blueprint, jsonify
from app.src import app_config
import mysql.connector
from datetime import date
from app.src.query_methods import auth

DEFAULT_USER_COUNT = 50
users_endpoint = Blueprint('users', __name__)


def get_users(count: int):
    users_data = []
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT id, login, rank_points FROM users ORDER BY rank_points DESC LIMIT {count}"
            cursor.execute(query)
            data = cursor.fetchall()
            for user in data:
                users_data.append({"id": user[0], "name": user[1], "points": user[2]})
    return users_data


def get_user(user_id: int):
    user_data = {}
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT id, login, rank_points FROM users where id = {user_id}"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                user_data = {"id": data[0][0], "name": data[0][1], "points": data[0][2]}
            else:
                return {}
    return user_data


@users_endpoint.route('/users', methods=['GET'])
def return_users():
    # TO-DO: Argument validation
    count = DEFAULT_USER_COUNT
    if request.args.get('count'):
        count = request.args.get('count')
    return jsonify(get_users(count))


@users_endpoint.route('/user/<user_id>', methods=['GET'])
def return_user(user_id):
    user_data = get_user(user_id)
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({'status': 'fail', 'message': 'user_not_found'}), 404


def add_rank_point(api_key):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = "UPDATE users SET rank_points = rank_points + 1 WHERE api_key = '" + api_key + "'"
            cursor.execute(query)
        cnx.commit()
