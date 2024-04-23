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
            query = f"SELECT login, rank_points FROM users ORDER BY rank_points DESC LIMIT {count}"
            cursor.execute(query)
            data = cursor.fetchall()
            for user in data:
                users_data.append({"name": user[0], "points": user[1]})
    return users_data


@users_endpoint.route('/users', methods=['GET'])
def return_users():
    # TO-DO: Argument validation
    count = DEFAULT_USER_COUNT
    if request.args.get('count'):
        count = request.args.get('count')
    return jsonify(get_users(count))


def add_rank_point(api_key):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = "UPDATE users SET rank_points = rank_points + 1 WHERE api_key = '" + api_key + "'"
            cursor.execute(query)
        cnx.commit()
