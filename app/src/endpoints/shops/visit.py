from flask import request, Blueprint, jsonify
import mysql.connector
from datetime import date
from app.src.query_methods import auth, requires
from app.src import app_config

make_visit_endpoint = Blueprint('make_visit', __name__)
check_visit_endpoint = Blueprint('check_visit', __name__)


def mark_visit_query(api_key, shop_id):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            today_date = date.today()
            query = "INSERT INTO visits VALUES((SELECT id FROM `users` WHERE api_key = '" + api_key + "'), '" + shop_id + "', '" + today_date.strftime(
                "%Y-%m-%d") + "')"

            cursor.execute(query)
        cnx.commit()

    return {'status': 'success'}


def check_visit_query(api_key, shop_id):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = "SELECT visits.date FROM visits WHERE visits.user_id = (SELECT id FROM `users` WHERE api_key = '" + api_key + "') AND visits.place_id = '" + shop_id + "' ORDER BY visits.date DESC LIMIT 1;"
            cursor.execute(query)
            query_result = cursor.fetchall()
            # if there is no info about that the user ever visited the shop
            if len(query_result) == 0:
                return {'status': 'visit_possible'}

        cnx.commit()

    if date.today() == query_result[0][0]:
        return {'status': 'visit_impossible'}

    return {'status': 'visit_possible'}


@make_visit_endpoint.route('/<shop_id>/visit', methods=['POST'])
@auth
@requires("session_token")
def make_visit(shop_id):
    api_key = request.args.get("session_token")
    query_result = mark_visit_query(api_key, shop_id)

    return jsonify(query_result)


@check_visit_endpoint.route('/<shop_id>/visit', methods=['GET'])
@auth
@requires("session_token")
def check_visit(shop_id):
    api_key = request.args.get("session_token")
    query_result = check_visit_query(api_key, shop_id)

    return jsonify(query_result)

