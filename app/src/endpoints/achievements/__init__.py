from flask import Blueprint, jsonify, Response
import mysql.connector
from app.src import app_config

achievements_endpoint = Blueprint('achievements', __name__)


def get_achievements():
    """
    Looks up all achievements in database.
    :returns: List of achievements data represented as dictionary.
    """

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
    """
    Looks up achievement in database.
    :returns: Achievement data represented as dictionary.
    """
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


@achievements_endpoint.route('/achievement/<achievement_id>', methods=['GET'])
def return_achievement_data(achievement_id: int) -> (Response, int):
    """ /v1/achievement/<achievement_id> endpoint

    Returns data of achievement with provided id
    :returns: json serialized response, http status code
    """
    achievement_data = get_achievement(achievement_id)
    if achievement_data:
        return jsonify(achievement_data), 200
    else:
        return jsonify({"status": "fail", "message": "achievement_not_found"}), 404


@achievements_endpoint.route('/achievements', methods=['GET'])
def return_achievements_data() -> (Response, int):
    """ /v1/achievements endpoint

    Returns data of all achievements
    TODO: Probably needs optimization in case shop database becomes too big
    :returns: json serialized response, http status code
    """
    return jsonify(get_achievements())


def add_achievement(user_id: int, achievement_id: int) -> None:
    """
    Mark achievement as acquired by user
    TODO: Check if achievement was already acquired to avoid duplicates
    TODO: Testing
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = f"INSERT INTO achievements VALUES {user_id}, {achievement_id}"
            cursor.execute(query)
        cnx.commit()
