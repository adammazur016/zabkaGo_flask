from flask import request, Blueprint, jsonify
from app.src import app_config
import mysql.connector
from app.src.query_methods import hash_password, requires

register_endpoint = Blueprint('register', __name__)


def check_username_validity(username):
    # Minimum Length
    if len(username) < 4:
        return False, 'login_too_short', 400

    # Check if username is taken
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE login = '{username}')"
            cursor.execute(query)
            user_exists = cursor.fetchone()[0]

    if user_exists:
        return False, 'username_taken', 409

    return True, 'valid', 200


# For future use e.g. password length check
def check_password_validity(password):
    return True, 'valid', 200


def add_user(username, password):
    password = hash_password(password)
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"INSERT INTO `users` (`login`, `password`, `api_key`) VALUES \
                        ('{username}', '{password}', '')"
            cursor.execute(query)
        cnx.commit()


@register_endpoint.route('/register', methods=['POST'])
@requires('username', 'password')
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    is_valid_username, message, status_code = check_username_validity(username)
    if not is_valid_username:
        return jsonify({'status': 'fail', 'message': message}), status_code

    is_valid_password, message, status_code = check_password_validity(password)
    if not is_valid_password:
        return jsonify({'status': 'fail', 'message': message}), status_code

    add_user(username, password)

    return jsonify({'status': 'success'}), 200
