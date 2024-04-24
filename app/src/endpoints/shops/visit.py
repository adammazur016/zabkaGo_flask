from flask import request, Blueprint, jsonify, Response
import mysql.connector
from datetime import date
from app.src.query_methods import auth, requires
from app.src import app_config
from app.src.endpoints.users import add_rank_point

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
            query = f"INSERT INTO visits VALUES((SELECT id FROM users WHERE api_key = {session_token}), {shop_id}, {today_date}"
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
            query = f"SELECT date FROM visits WHERE user_id = (SELECT id FROM users WHERE api_key = '{session_token}') AND place_id = '{shop_id}' ORDER BY date DESC LIMIT 1;"
            cursor.execute(query)
            query_result = cursor.fetchall()
            # There is no information that the user ever visited the shop, it will be his first visit
            if len(query_result) == 0:
                return {"status": "success", "message": "visit_possible"}
        cnx.commit()

    if date.today() == query_result[0][0]:
        return {"status": "fail", "message": "visit_impossible"}

    return {"status": "success", "message": "visit_possible"}


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
    if check_query_result["status"] == "failed":
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
    api_key = request.args.get("session_token")
    query_result = check_visit_query(api_key, shop_id)

    # Status code 200 if visit is allowed, 403 if forbidden
    if query_result["status"] == "success":
        return jsonify(query_result), 200
    else:
        return jsonify(query_result), 403
