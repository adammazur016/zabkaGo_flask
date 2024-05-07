from flask import request, Blueprint, jsonify, Response
import mysql.connector
from datetime import date
from src.query_methods import auth, requires, get_user_id, triggers, does_shop_exist
from src import app_config
from src.endpoints.users import add_rank_point
from src import achievements

visit_endpoint = Blueprint('visit', __name__)


def mark_visit_query(session_token, shop_id) -> dict:
    """
    Updates the date of the last visit in the shop with the provided ID.
    Identifies the user based on the session token.

    :param session_token: The session token of the user.
    :param shop_id: The ID of the shop.
    :return: The response ready for JSON serialization.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            today_date = date.today().strftime('%Y-%m-%d')
            user_id = get_user_id(session_token)
            query = f"INSERT INTO visits VALUES ({user_id}, {shop_id}, '{today_date}')"
            cursor.execute(query)
        cnx.commit()
    return {"status": "success", "message": "visit_done"}


def check_visit_query(session_token, shop_id) -> dict:
    """
    Checks if the user is allowed to visit the shop with the provided ID.
    Identifies the user based on the session token.

    :param session_token: The session token of the user.
    :param shop_id: The ID of the shop to be visited.
    :return: The response ready for JSON serialization.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            user_id = get_user_id(session_token)
            query = f"SELECT date FROM visits WHERE user_id = {user_id} AND place_id = {shop_id} ORDER BY date DESC LIMIT 1;"
            cursor.execute(query)
            query_result = cursor.fetchall()
            # There is no information that the user ever visited the shop, it will be his first visit
            if len(query_result) == 0:
                return {"status": "success", "message": "visit_possible"}

    if date.today() == query_result[0][0]:
        return {"status": "fail", "message": "visit_impossible"}

    return {"status": "success", "message": "visit_possible"}


def get_user_visits(user_id) -> list[dict]:
    """
    Retrieves a list of all visits made by the user with the provided ID from the database.

    :param user_id: The ID of the user.
    :return: A list of all visits made by the user.
    """
    visits = []

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT place_id, date FROM visits WHERE user_id = {user_id}"
            cursor.execute(query)
            data = cursor.fetchall()
            # There is no information that the user ever visited the shop, it will be his first visit
            for visit in data:
                visits.append({"shop_id": visit[0], "date": visit[1]})
    return visits


@visit_endpoint.route('/shop/<shop_id>/visit', methods=['POST'])
@auth
@requires("session_token")
@triggers(achievements.VisitCountAchievements, achievements.PointCountAchievements)
def make_visit(shop_id) -> (Response, int):
    """
    Checks if the user is allowed to visit the shop with the provided ID.
    If allowed, marks their visit in the database.
    Authentication is required, and the user is identified based on the session token.

    :param shop_id: The ID of the shop to be visited.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    session_token = request.args.get("session_token")
    # Check if shop exists
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    # Check if visit is allowed
    check_query_result = check_visit_query(session_token, shop_id)
    if check_query_result["status"] == "fail":
        return jsonify(check_query_result), 403
    # Mark visit
    mark_query_result = mark_visit_query(session_token, shop_id)
    # Add ranked points
    add_rank_point(session_token)
    # Send reply
    return jsonify(mark_query_result), 200


@visit_endpoint.route('/shop/<shop_id>/visit', methods=['GET'])
@auth
@requires("session_token")
def check_visit(shop_id) -> (Response, int):
    """
    /v1/shop/<shop_id>/visit endpoint

    Verifies if the user is allowed to visit the shop with the provided ID.
    Authentication is required, and the user is identified based on the session token.

    :param shop_id: The ID of the shop to be visited.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    # Check if shop exists
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404

    session_token = request.args.get("session_token")
    query_result = check_visit_query(session_token, shop_id)

    # Status code 200 if visit is allowed, 403 if forbidden
    if query_result["status"] == "success":
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 403


@visit_endpoint.route('/user/<user_id>/visits', methods=['GET'])
def check_user_visits(user_id) -> (Response, int):
    """
    /v1/user/<user_id>/visits endpoint

    Retrieves a list of all shops visited by the user, including visit dates.

    :param user_id: The ID of the user.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """

    user_data = get_user_visits(user_id)

    # Empty user_data -> user was not found or haven't made any visits
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"status": "fail", "message": "visits_not_found"}), 404
