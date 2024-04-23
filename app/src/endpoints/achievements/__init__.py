from flask import request, Blueprint, jsonify
import mysql.connector
from datetime import date
from app.src.query_methods import auth, requires
from app.src import app_config

achievements_endpoint = Blueprint('achievements', __name__)


def get_achievements():
    achievements_data = []
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT id, name, description FROM achievements"
            cursor.execute(query)
            data = cursor.fetchall()
            for achievement in data:
                achievements_data.append({"id": achievement[0], "name": achievement[1], "description": achievement[2]})
    return achievements_data


def get_achievement(achievement_id: int):
    achievement_data = {}
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT id, name, description FROM achievements where id = {achievement_id}"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                achievement_data = {"id": data[0][0], "name": data[0][1], "description": data[0][2]}
            else:
                return {}
    return achievement_data


@achievements_endpoint.route('/achievement/<id>', methods=['GET'])
def return_achievement_data(id: int):
    achievement_data = get_achievement(id)
    if achievement_data:
        return jsonify(achievement_data), 200
    else:
        return jsonify({'status': 'fail', 'message': 'achievement_not_found'}), 404


@achievements_endpoint.route('/achievements', methods=['GET'])
def return_achievements_data():
    return jsonify(get_achievements())


# Needs testing
def mark_achievement(user_id: int, achievement_id: int):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"INSERT INTO achievements VALUES {user_id}, achievement_id"
            cursor.execute(query)
        cnx.commit()
