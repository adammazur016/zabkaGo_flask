from flask import request, Blueprint
from .. import config
import mysql.connector
from datetime import date
from ..auth_methods import auth

get_points_endpoint = Blueprint('getpoints', __name__)

def get_points_from_db():
    places = []

    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
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


@get_points_endpoint.route('/getpoints', methods=['GET'])
@auth
def get_points():
    places = get_points_from_db()
    return places








