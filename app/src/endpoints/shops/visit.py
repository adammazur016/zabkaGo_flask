from flask import request, Blueprint, jsonify, Response
import mysql.connector
from datetime import date
from src.query_methods import auth, requires, get_user_id
from src import app_config
from src.endpoints.users import add_rank_point

visit_endpoint = Blueprint('visit', __name__)


def mark_visit_query(session_token, shop_id) -> dict:
    """
    Updates date of last visit in shop with provided id
    Identifies user based on session token
    :returns: response ready for json serialization
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            today_date = date.today().strftime('%Y-%m-%d')
            user_id = get_user_id(session_token)
            query = f"INSERT INTO visits VALUES ({user_id}, {shop_id}, '{today_date}')"
            cursor.execute(query)
        cnx.commit()
    return {"status": "success", "message": "visit_marked"}


def check_visit_query(session_token, shop_id) -> dict:
    """
    Checks if user is allowed to visit the shop with provided id
    Identifies user based on session token
    :returns: response ready for json serialization
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
    Receives list of all visits made by user with provided id from database.
    :returns: List of all visits made by user
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
def make_visit(shop_id) -> (Response, int):
    """
    Checks if user is allowed to visit the shop with provided id
    If it is allowed, marks his visit in database
    Requires authentication and identifies user based on session token
    :returns: json serialized response, http status code
    """
    session_token = request.args.get("session_token")
    # Check if visit is allowed
    check_query_result = check_visit_query(session_token, shop_id)
    if check_query_result["status"] == "fail":
        return jsonify(check_query_result), 403

    mark_query_result = mark_visit_query(session_token, shop_id)
    add_rank_point(session_token)
    return jsonify(mark_query_result), 200


@visit_endpoint.route('/shop/<shop_id>/visit', methods=['GET'])
@auth
@requires("session_token")
def check_visit(shop_id) -> (Response, int):
    """ /v1/shop/<shop_id>/visit endpoint

    Checks if user is allowed to visit the shop with provided id
    Requires authentication and identifies user based on session token
    :returns: json serialized response, http status code
    """
    session_token = request.args.get("session_token")
    query_result = check_visit_query(session_token, shop_id)

    # Status code 200 if visit is allowed, 403 if forbidden
    if query_result["status"] == "success":
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 403


@visit_endpoint.route('/user/<user_id>/visits', methods=['GET'])
def check_user_visits(user_id) -> (Response, int):
    """ /v1/user/<user_id>/visits endpoint

    Returns list of all shops visited by user, including visit date
    :returns: json serialized response, http status code
    """
    user_data = get_user_visits(user_id)

    # Empty user_data -> user was not found or haven't made any visits
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"status": "fail", "message": "no_visits_found"}), 404
