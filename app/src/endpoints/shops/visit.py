from flask import request, Blueprint, jsonify
import mysql.connector
from datetime import date
from app.src.query_methods import auth, requires
from app.src import app_config

visit_endpoint = Blueprint('visit', __name__)


def mark_visit_query(api_key, shop_id):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            today_date = date.today().strftime('%Y-%m-%d')
            query = f"INSERT INTO visits VALUES((SELECT id FROM users WHERE api_key = {api_key}), {shop_id}, {today_date}"
            cursor.execute(query)
        cnx.commit()

    return {'status': 'success'}


def check_visit_query(api_key, shop_id):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT date FROM visits WHERE user_id = (SELECT id FROM users WHERE api_key = '{api_key}') AND place_id = '{shop_id}' ORDER BY date DESC LIMIT 1;"
            cursor.execute(query)
            query_result = cursor.fetchall()
            # if there is no info about that the user ever visited the shop
            if len(query_result) == 0:
                return {'status': 'visit_possible'}

        cnx.commit()

    if date.today() == query_result[0][0]:
        return {'status': 'visit_impossible'}

    return {'status': 'visit_possible'}


@visit_endpoint.route('/shop/<shop_id>/visit', methods=['POST'])
@auth
@requires("session_token")
def make_visit(shop_id):
    api_key = request.args.get("session_token")
    query_result = mark_visit_query(api_key, shop_id)

    return jsonify(query_result)


@visit_endpoint.route('/shop/<shop_id>/visit', methods=['GET'])
@auth
@requires("session_token")
def check_visit(shop_id):
    api_key = request.args.get("session_token")
    query_result = check_visit_query(api_key, shop_id)

    return jsonify(query_result)

