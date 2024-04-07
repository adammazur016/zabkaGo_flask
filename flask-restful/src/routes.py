from flask import Blueprint
from .auth_methods import auth, admin_auth
import mysql.connector
from . import config
from .endpoints import login, register

# main blueprint to be registered with application
api_bp = Blueprint('api', __name__)


# TO-DO: Move to new endpoint
def get_points_from_db():
    places = []
    # Creating a connection cursor
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
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


@api_bp.route('/test', methods=['POST'])
@auth
def test():
    places = get_points_from_db()
    return places


# Register endpoint blueprints
api_bp.register_blueprint(login.login_endpoint)
api_bp.register_blueprint(register.register_endpoint)
