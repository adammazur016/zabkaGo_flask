from flask import request, Blueprint
from .. import config
import mysql.connector
from datetime import date
from ..auth_methods import auth

check_visit_endpoint = Blueprint('checkvisit', __name__)


def check_visit_db(api_key, place_id):
    query_result = ""
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = "SELECT visits.date FROM visits WHERE visits.user_id = (SELECT id FROM `users` WHERE api_key = '" + api_key + "') AND visits.place_id = '"+place_id+"' ORDER BY visits.date DESC LIMIT 1;"
            print(query)
            cursor.execute(query)
            query_result = cursor.fetchall()
            # if there is no info about that the user ever visited the shop
            if len(query_result) == 0:
                return {'Status': 'Visit possible'}

        cnx.commit()

        
    if date.today() == query_result[0][0]:
        return {'Status': 'Visit imposible'}

    return {'Status': 'Visit possible'}


@check_visit_endpoint.route('/checkvisit', methods=['GET'])
@auth
def checkvisit():
    place_id = request.args.get("place_id")
    api_key = request.args.get("api_key")
    query_result = check_visit_db(api_key, place_id)

    return query_result
