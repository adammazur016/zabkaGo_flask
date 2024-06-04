from flask import request, Blueprint, jsonify, Response
import mysql.connector
from src.query_methods import auth
from src.helper_methods import does_shop_exist, get_user_id
from src.endpoints.shops.visit import check_last_visit_date
from src import app_config
from src.sanitize import sanitize

likes_endpoint = Blueprint('comments', __name__)


def is_liked(user_id: int, shop_id: int) -> bool:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT EXISTS(SELECT * FROM likes WHERE place_id = {shop_id} AND user_id = {user_id})"
            cursor.execute(query)
            liked = cursor.fetchone()[0]
    return liked


def add_like(user_id: int, shop_id: int):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"INSERT INTO likes(user_id, place_id) VALUES ({user_id}, {shop_id})"
            cursor.execute(query)
        cnx.commit()


def remove_like(user_id: int, shop_id: int):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"DELETE FROM likes WHERE user_id = {user_id} AND place_id= {shop_id}"
            cursor.execute(query)
        cnx.commit()


def get_shop_likes(shop_id: int) -> int:
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT COUNT(*) FROM likes WHERE place_id = {shop_id}"
            cursor.execute(query)
            count = cursor.fetchone()[0]
    return count


@likes_endpoint.route('/shop/<shop_id>/like', methods=['GET'])
@auth
def return_is_liked(shop_id) -> (Response, int):
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int)])
    if not valid:
        return response, code

    user_id = get_user_id(request.args['session_token'])
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    elif check_last_visit_date(user_id, shop_id) == "never":
        return jsonify({"status": "fail", "message": "shop_not_visited"}), 403
    elif is_liked(user_id, shop_id):
        return jsonify({"status": "success", "message": "liked"}), 200
    else:
        return jsonify({"status": "success", "message": "not_liked"}), 200


@likes_endpoint.route('/shop/<shop_id>/like', methods=['POST'])
@auth
def like_shop(shop_id) -> (Response, int):
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int)])
    if not valid:
        return response, code

    user_id = get_user_id(request.args['session_token'])
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    elif check_last_visit_date(user_id, shop_id) == "never":
        return jsonify({"status": "fail", "message": "shop_not_visited"}), 403
    elif is_liked(user_id, shop_id):
        remove_like(user_id, shop_id)
        return jsonify({"status": "success", "message": "like_removed"}), 200
    else:
        add_like(user_id, shop_id)
        return jsonify({"status": "success", "message": "like_added"}), 200


@likes_endpoint.route('/shop/<shop_id>/likes', methods=['GET'])
def return_shop_likes(shop_id) -> (Response, int):
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int)])
    if not valid:
        return response, code

    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    else:
        likes_number = get_shop_likes(shop_id)
        return jsonify({"shop_id": int(shop_id), "likes": likes_number}), 200
