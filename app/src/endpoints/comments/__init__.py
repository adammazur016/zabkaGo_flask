from flask import request, Blueprint, jsonify, Response
import mysql.connector
from src.query_methods import auth, requires, get_user_id, does_shop_exist
from src import app_config
from src.sanitize import sanitize

comment_endpoint = Blueprint('comments', __name__)


def verify_visit(session_token: str, shop_id: int):
    """
    Verifies if the user visited the provided shop.

    :param session_token: The session token of the user.
    :param shop_id: The ID of the shop.
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
    Verifies if the shop_id matches between the comment and the parent comment to avoid mismatch.

    :param shop_id: The ID of the shop.
    :param parent_id: The ID of the parent comment.
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
    Inserts a comment into the database. If it is an original comment, pass None as the parent_id; otherwise, use the parent comment ID.

    :param session_token: The session token of the user.
    :param shop_id: The ID of the shop.
    :param parent_id: The ID of the parent comment, or None if it's an original comment.
    :param content: The content of the comment.
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
    Retrieves data of all comments in the shop discussion.

    :param shop_id: The ID of the shop.
    :return: A list of comments data represented as dictionaries.
    """
    comments = []
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT id, user_id, parent_id, place_id, text_content, creation_time FROM comments WHERE place_id = %s"
            cursor.execute(query, [shop_id])
            data = cursor.fetchall()

            for comment in data:
                comments.append({"id": comment[0],
                                 "user_id": comment[1],
                                 "parent_id": comment[2],
                                 "place_id": comment[3],
                                 "content": comment[4],
                                 "creation_time": comment[5]})

    return comments


def get_comment(shop_id: int, comment_id: int) -> dict:
    """
    Retrieves the content of the comment with the provided ID from the shop discussion.

    :param shop_id: The ID of the shop.
    :param comment_id: The ID of the comment.
    :return: Comment data represented as a dictionary.
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
@requires('content')
def write_comment(shop_id: int) -> (Response, int):
    """
    /v1/shop/<shop_id>/comment endpoint

    Checks if the user can write a comment in the shop's thread, then saves the new comment in the database.
    The parent_id is optional, and a missing value returns null.

    :param shop_id: The ID of the shop.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    session_token = request.args.get("session_token")
    content = request.args.get("content")
    parent_id = request.args.get("parent_id")
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int), (parent_id, int)])
    if not valid:
        return response, code
    # Check if shop exists
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
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
def read_comment(shop_id, comment_id) -> (Response, int):
    """
    /v1/shop/<shop_id>/comment/<comment_id> endpoint

    Retrieves the content of the comment with the provided ID.

    :param shop_id: The ID of the shop.
    :param comment_id: The ID of the comment.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int), (comment_id, int)])
    if not valid:
        return response, code
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    comment = get_comment(shop_id, comment_id)
    if comment:
        return jsonify(comment), 200
    else:
        return jsonify({"status": "fail", "message": "comment_not_found"}), 404


@comment_endpoint.route('/shop/<shop_id>/comments', methods=['GET'])
def read_comments(shop_id) -> (Response, int):
    """
    /v1/shop/<shop_id>/comments endpoint

    Retrieves all comments in the shop's thread.
    TODO: Implement a limit to the number of comments per request and filters (date, most upvoted, etc).

    :param shop_id: The ID of the shop.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int)])
    if not valid:
        return response, code
    if not does_shop_exist(shop_id):
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404
    comments = get_comments(shop_id)
    return jsonify(comments), 200
