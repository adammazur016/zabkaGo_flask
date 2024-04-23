from flask import request, Blueprint, jsonify
from app.src import app_config
import mysql.connector
from app.src.query_methods import auth
from app.src.endpoints.shops import visit

shops_endpoint = Blueprint('shops', __name__)


def get_shops():
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


def get_shop(shop_id: int):
    shop_data = {}
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
            else:
                return {}
    return shop_data


# This probably needs optimization to not return ALL shops
@shops_endpoint.route('/shops', methods=['GET'])
def return_shops():
    places = get_shops()
    return jsonify(places)


@shops_endpoint.route('/shop/<shop_id>', methods=['GET'])
def return_shop(shop_id):
    places = get_shop(shop_id)
    return jsonify(places)


shops_endpoint.register_blueprint(visit.visit_endpoint)

