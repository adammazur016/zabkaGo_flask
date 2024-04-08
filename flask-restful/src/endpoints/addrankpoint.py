from flask import request, Blueprint
from .. import config
import mysql.connector
from datetime import date
from ..auth_methods import auth

addrankpoint_endpoint = Blueprint('addrankpoint_endpoint', __name__)

def add_rank_point_db(api_key):
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            today_date = date.today()
            query = "UPDATE users SET rank_points = rank_points + 1 WHERE api_key = '" + api_key + "'"

            cursor.execute(query)
        cnx.commit()

    return {'Status': 'Rank point added'}


@addrankpoint_endpoint.route('/addrankpoint', methods=['POST'])
@auth
def addrankpoint():
    api_key = request.args.get("api_key")
    query_result = add_rank_point_db(api_key)

    return query_result
