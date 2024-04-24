from flask import request, Blueprint, jsonify, Response
import mysql.connector
from app.src.query_methods import auth, requires
from app.src import app_config

comment_endpoint = Blueprint('comments', __name__)


def insert_comment(user_id: int, content: str, shop_id: int):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"INSERT INTO `comments` (`user_id`, `place_id`, `text_content`) VALUES \
                        ('{user_id}', '{shop_id}', '{content}')"
            cursor.execute(query)
        cnx.commit()


@comment_endpoint.route('/shop/<shop_id>/comment', methods=['POST'])
@requires('session_token')
@auth
def write_comment(shop_id):
    pass


@comment_endpoint.route('/shop/<shop_id>/comment', methods=['POST'])
@requires('session_token')
@auth
def write_comment(shop_id):
    pass


@comment_endpoint.route('/shop/<shop_id>/comment/<comment_id>', methods=['GET'])
def read_comment():
    pass


@comment_endpoint.route('/shop/<shop_id>/comments', methods=['GET'])
def read_comment(count: int):
    pass
