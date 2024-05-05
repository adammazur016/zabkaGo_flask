from flask import request, Blueprint, jsonify, Response
import mysql.connector
from src.query_methods import auth, requires, get_user_id
from src import app_config

comment_endpoint = Blueprint('comments', __name__)


def verify_visit(session_token: str, shop_id: int):
    """
    Verifies if user visited provided shop
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            user_id = get_user_id(session_token)
            query = f"SELECT EXISTS(SELECT * FROM visits WHERE place_id = '{shop_id}' AND user_id = '{user_id}')"
            cursor.execute(query)
            visited = cursor.fetchone()[0]
    if visited:
        return True
    else:
        return False


def verify_comment_chain(shop_id: int, parent_id: str):
    """
    Verifies if shop_id matches between comment and parent comment to avoid mismatch
    """
    if not parent_id:
        return True

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM comments WHERE place_id = '{shop_id}' AND id = '{parent_id}')"
            cursor.execute(query)
            is_correct = cursor.fetchone()[0]
    if is_correct:
        return True
    else:
        return False


def insert_comment(session_token: str, shop_id: int, parent_id: str | None, content: str):
    """
    Inserts comment into database. If it is original comment pass parent_id as None, otherwise use parent comment id
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            user_id = get_user_id(session_token)
            query = "INSERT INTO comments (user_id, place_id, text_content, parent_id) " \
                    "VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (user_id, shop_id, content, parent_id))

            # If main_id is not specified it should be equal to comment id
            if not parent_id:
                query = f"UPDATE comments SET parent_id = LAST_INSERT_ID() WHERE id = LAST_INSERT_ID()"
                cursor.execute(query)
        cnx.commit()


def get_comments(shop_id: int) -> list[dict]:
    """
    Return data of all comments in shop discussion
    :returns: List of comments data represented as dictionary.
    """
    comments = []
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT user_id, parent_id, parent_id, text_content, creation_time FROM comments WHERE place_id = %s"
            cursor.execute(query, [shop_id])
            data = cursor.fetchall()

            for comment in data:
                comments.append({"user_id": comment[0],
                                 "parent_id": comment[1],
                                 "place_id": comment[2],
                                 "content": comment[3],
                                 "creation_time": comment[4]})

    return comments


def get_comment(shop_id: int, comment_id: int) -> dict:
    """
    Return content of all comments in shop discussion
    :returns: Comment data represented as dictionary
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT id, user_id, parent_id, place_id, text_content, creation_time FROM comments WHERE place_id = %s AND id = %s"
            cursor.execute(query, (shop_id, comment_id))
            data = cursor.fetchall()
            if data:
                comment_data = {"id": data[0][0],
                                "user_id": data[0][1],
                                "main_id": data[0][2],
                                "shop_id": data[0][3],
                                "content": data[0][4],
                                "creation_time": data[0][5]}
                return comment_data
            else:
                return {}


@comment_endpoint.route('/shop/<shop_id>/comment', methods=['POST'])
@auth
@requires('session_token', 'content')
def write_comment(shop_id: int) -> (Response, int):
    """ /v1/shop/<shop_id>/comment endpoint

    Checks if user can write comment in shop's thread then saves new comment in database
    parent_id is optional and missing value returns null
    :returns: json serialized response, http status code
    """
    session_token = request.args.get("session_token")
    content = request.args.get("content")
    parent_id = request.args.get("parent_id")
    # Check if user visited shop
    if not verify_visit(session_token, shop_id):
        return jsonify({"status": "fail", "message": "shop_not_visited"}), 403
    # Check if shop_id and parent_id combination is valid
    elif not verify_comment_chain(shop_id, parent_id):
        return jsonify({"status": "fail", "message": "shop_id_and_parent_id_mismatch"}), 400
    # Insert comment
    else:
        insert_comment(session_token, shop_id, parent_id, content)
        return jsonify({"status": "success"}), 200


@comment_endpoint.route('/shop/<shop_id>/comment/<comment_id>', methods=['GET'])
def read_comment(shop_id: int, comment_id: int) -> (Response, int):
    """ /v1/shop/<shop_id>/comment/<comment_id> endpoint

    Return content of comment with provided id
    :returns: json serialized response, http status code
    """
    comment = get_comment(shop_id, comment_id)
    return jsonify(comment), 200


@comment_endpoint.route('/shop/<shop_id>/comments', methods=['GET'])
def read_comments(shop_id: int) -> (Response, int):
    """ /v1/shop/<shop_id>/comments endpoint

    Returns all comments in shop's thread
    :returns: json serialized response, http status code
    TODO: Implement limit to number of comments per request and filters (date, most upvoted etc)
    """
    comments = get_comments(shop_id)
    return jsonify(comments), 200
