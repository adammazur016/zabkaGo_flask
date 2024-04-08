from flask import request, Blueprint
from .. import config
import mysql.connector
from datetime import date
from ..auth_methods import auth

makevisit_endpoint = Blueprint('makevisit', __name__)

def make_visit_db(api_key, place_id):

    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            
            today_date = date.today()
            query = "INSERT INTO visits VALUES((SELECT id FROM `users` WHERE api_key = '" + api_key +"'), '" + place_id + "', '" + today_date.strftime("%Y-%m-%d") + "')"

            cursor.execute(query)
        cnx.commit()

    return {'Status': 'Made visit'}


@makevisit_endpoint.route('/makevisit', methods=['POST'])
@auth
def makevisit():
    place_id = request.args.get("place_id")
    api_key = request.args.get("api_key")
    query_result = make_visit_db(api_key, place_id)

    return query_result
