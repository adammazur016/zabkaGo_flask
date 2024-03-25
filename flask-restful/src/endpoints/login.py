from flask import request, Blueprint
from .. import config
import mysql.connector

login_endpoint = Blueprint('login', __name__)


def simple_test(user: str, password: str):
    print(f"{user} {password}")
    if user == 'test' and password == 'test123':
        return True
    else:
        return False


# TO-DO: Split comparing password and receiving user api_key to separate queries
def get_password(user):
    # TO-DO: Secure it from SQL injection
    myLogin = "'" + user + "'"
    result = []
    with mysql.connector.connect(**config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements

            query = "SELECT password, id, api_key FROM users WHERE login = " + myLogin

            cursor.execute(query)
            data = cursor.fetchall()

            correct_password = data[0][0]
            user_id = data[0][1]
            user_api_key = data[0][2]

            result = [correct_password, user_id, user_api_key]
    return result


@login_endpoint.route('/login', methods=['POST'])
def login():
    login = request.args.get('user')
    password = request.args.get('password')

    query_result = get_password(login)

    correct_password = query_result[0]
    user_id = query_result[1]
    user_api_key = query_result[2]

    if password == correct_password:
        return {'auth': '1', 'id': user_id, 'api_key': user_api_key}
    else:
        return {'auth': '-1'}
