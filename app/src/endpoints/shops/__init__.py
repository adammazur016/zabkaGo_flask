from flask import Blueprint, jsonify, Response
from src import app_config
import mysql.connector
from src.endpoints.shops import visit, likes
from src.sanitize import sanitize

shops_endpoint = Blueprint('shops', __name__)


def get_shops() -> list[dict]:
    """
    Retrieves data of all shops from the database.

    :return: A list of shop data represented as dictionaries.
    """
    places = []
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT places.ID, places.lat, places.long, places.name, places.description FROM places"
            cursor.execute(query)
            data = cursor.fetchall()

            for place in data:
                places.append({"id": place[0],
                               "lat": place[1],
                               "long": place[2],
                               "name": place[3],
                               "description": place[4]})

    return places


def get_shop(shop_id: int) -> dict:
    """
    Retrieves data of the shop with the provided ID from the database.

    :param shop_id: The ID of the shop to retrieve.
    :return: Shop data represented as a dictionary, or an empty dictionary if the shop does not exist.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT places.id, places.lat, places.long, places.name, places.description FROM places where id = {shop_id}"
            cursor.execute(query)
            data = cursor.fetchall()
            if data:
                shop_data = {"id": data[0][0],
                             "lat": data[0][1],
                             "long": data[0][2],
                             "name": data[0][3],
                             "description": data[0][4]}
                return shop_data
            else:
                return {}


@shops_endpoint.route('/shops', methods=['GET'])
def return_shops() -> (Response, int):
    """
    /v1/shops endpoint

    Retrieves data of all shops.
    TODO: Probably needs optimization in case the shop database becomes too big.

    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    shops = get_shops()
    return jsonify(shops), 200


@shops_endpoint.route('/shop/<shop_id>', methods=['GET'])
def return_shop(shop_id) -> (Response, int):
    """
    /v1/shop/<shop_id> endpoint

    Retrieves data of the shop with the provided ID.

    :param shop_id: The ID of the shop.
    :return: JSON-serialized response, along with the corresponding HTTP status code.
    """
    # Check if passed parameters use allowed characters
    valid, response, code = sanitize([(shop_id, int)])
    if not valid:
        return response, code

    shop = get_shop(shop_id)
    if shop:
        return jsonify(shop), 200
    else:
        return jsonify({"status": "fail", "message": "shop_not_found"}), 404


shops_endpoint.register_blueprint(visit.visit_endpoint)
shops_endpoint.register_blueprint(likes.likes_endpoint)
