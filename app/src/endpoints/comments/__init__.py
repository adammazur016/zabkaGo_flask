from flask import request, Blueprint, jsonify, Response
import mysql.connector
from app.src.query_methods import auth, requires, get_user_id
from app.src import app_config

comment_endpoint = Blueprint('comments', __name__)


def insert_comment(session_token: str, shop_id: int, main_id: str | None, content: str):
    """
    Inserts comment into database
    If it is original comment pass main_id as None, otherwise use parent comment id
    :params main_id: id of parent comment if it's a reply, points to itself if it's original comment
    TODO: Verify if user visited shop before inserting comment
    TODO: Verify if comment with main_id
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            user_id = get_user_id(session_token)
            query = "INSERT INTO comments (user_id, place_id, text_content, main_id) " \
                    "VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (user_id, shop_id, content, main_id))

            # If main_id is not specified it should be equal to comment id
            if not main_id:
                query = f"UPDATE comments SET main_id = LAST_INSERT_ID() WHERE id = LAST_INSERT_ID()"
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
            query = f"SELECT user_id, main_id, place_id, text_content FROM comments WHERE place_id = %s"
            cursor.execute(query, [shop_id])
            data = cursor.fetchall()

            for comment in data:
                comments.append({"user_id": comment[0],
                                 "main_id": comment[1],
                                 "place_id": comment[2],
                                 "content": comment[3]})

    return comments


def get_comment(shop_id: int, comment_id: int) -> dict:
    """
    Return content of all comments in shop discussion
    :returns: Comment data represented as dictionary
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT id, user_id, main_id, place_id, text_content FROM comments WHERE place_id = %s AND id = %s"
            cursor.execute(query, (shop_id, comment_id))
            data = cursor.fetchall()
            if data:
                comment_data = {"id": data[0][0],
                                "user_id": data[0][1],
                                "main_id": data[0][2],
                                "shop_id": data[0][3],
                                "content": data[0][4]}
                return comment_data
            else:
                return {}


@comment_endpoint.route('/shop/<shop_id>/comment', methods=['POST'])
@requires('session_token', 'content')
@auth
def write_comment(shop_id: int) -> (Response, int):
    """
    Checks if user can write comment in shop's thread then saves new comment in database
    main_id is optional and missing value returns null
    :returns: json serialized response, http status code
    """
    session_token = request.args.get("session_token")
    content = request.args.get("content")
    main_id = request.args.get("main_id")
    insert_comment(session_token, shop_id, main_id, content)
    return jsonify({"result": "success"}), 200


@comment_endpoint.route('/shop/<shop_id>/comment/<comment_id>', methods=['GET'])
def read_comment(shop_id: int, comment_id: int) -> (Response, int):
    """
    Return content of comment with provided id
    :returns: json serialized response, http status code
    """
    comment = get_comment(shop_id, comment_id)
    return jsonify(comment), 200


@comment_endpoint.route('/shop/<shop_id>/comments', methods=['GET'])
def read_comments(shop_id: int) -> (Response, int):
    """
    Returns all comments in shop's thread
    :returns: json serialized response, http status code
    TODO: Implement limit to number of comments per request and filters (date, most upvoted etc)
    """
    comments = get_comments(shop_id)
    return jsonify(comments), 200

# TODO: Add creation date to comment database
