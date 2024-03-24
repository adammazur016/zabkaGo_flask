from flask import Blueprint
from .auth_methods import auth, admin_auth
from . import mysql
from .endpoints import login

# main blueprint to be registered with application
api_bp = Blueprint('api', __name__)

def getPointsFromDb():

    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    query = "SELECT places.ID, places.lat, places.long FROM places"

    print(f'The query is: {query}')

    cursor.execute(query)

    data = cursor.fetchall()

    places = []

    for place in data:
        placeID = place[0]
        placeLat = place[1]
        placeLong = place[2]
        places.append({'place_id': placeID, 'latitude': placeLat, 'longitude': placeLong})


    # Saving the Actions performed on the DB
    #mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return places


@api_bp.route('/test', methods=['POST'])
@auth
def test():
    places = getPointsFromDb()
    return places


# Register endpoint blueprints
api_bp.register_blueprint(login.login_endpoint)
