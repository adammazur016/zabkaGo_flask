from flask import Blueprint, jsonify, Response
from src import app_config
import mysql.connector
from src.endpoints.shops import visit

shops_endpoint = Blueprint('shops', __name__)


def get_shops() -> list[dict]:
    """
    Looks up all shops in database.
    :returns: List of shops data represented as dictionary.
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
    Looks up shop with provided id in database
    :returns: shop data represented as dictionary or empty dict if shop does not exist
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
    """ /v1/shops endpoint

    Returns data of all shops
    TODO: Probably needs optimization in case shop database becomes too big
    :returns: json serialized response, http status code
    """
    places = get_shops()
    return jsonify(places), 200


@shops_endpoint.route('/shop/<shop_id>', methods=['GET'])
def return_shop(shop_id) -> (Response, int):
    """ /v1/shop/<shop_id> endpoint

    Returns data of shop with provided id
    :returns: json serialized response, http status code
    """
    shop = get_shop(shop_id)
    return jsonify(shop), 200


shops_endpoint.register_blueprint(visit.visit_endpoint)
