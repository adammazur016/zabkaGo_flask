from flask import Blueprint, jsonify, Response
import mysql.connector
from src import app_config

achievements_endpoint = Blueprint('achievements', __name__)


def get_achievements() -> list[dict]:
    """
    Retrieves data of all achievements from the database.

    :return: A list of achievements data represented as dictionaries.
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


def get_achievement(achievement_id: int) -> dict:
    """
    Retrieves data of the achievement with the provided ID from the database.

    :param achievement_id: The ID of the achievement to retrieve.
    :return: Achievement data represented as a dictionary.
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
    """
    /v1/achievement/<achievement_id> endpoint

    Retrieves data of the achievement with the provided ID.

    :param achievement_id: The ID of the achievement.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    achievement_data = get_achievement(achievement_id)
    if achievement_data:
        return jsonify(achievement_data), 200
    else:
        return jsonify({"status": "fail", "message": "achievement_not_found"}), 404


@achievements_endpoint.route('/achievements', methods=['GET'])
def return_achievements_data() -> (Response, int):
    """
    /v1/achievements endpoint

    Retrieves data of all achievements.
    TODO: Probably needs optimization in case the achievements database becomes too big.

    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    return jsonify(get_achievements()), 200
