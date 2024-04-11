from flask import request, Blueprint, jsonify
from app.src import app_config
import mysql.connector
from app.src.query_methods import auth
from app.src.endpoints.shops import visit

shops_endpoint = Blueprint('shops', __name__)


def get_shops_query():
    places = []

    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = "SELECT places.ID, places.lat, places.long FROM places"

            print(f'The query is: {query}')

            cursor.execute(query)

            data = cursor.fetchall()

            for place in data:
                place_id = place[0]
                place_lat = place[1]
                place_long = place[2]
                places.append({'place_id': place_id, 'latitude': place_lat, 'longitude': place_long})

    return places


@shops_endpoint.route('', methods=['GET'])
@auth
def get_shops():
    places = get_shops_query()
    return jsonify(places)


shops_endpoint.url_prefix = '/shops'
shops_endpoint.register_blueprint(visit.make_visit_endpoint)
shops_endpoint.register_blueprint(visit.check_visit_endpoint)

