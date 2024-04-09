from flask import request, Blueprint
from app.src import app_config
import mysql.connector
from app.src.auth_methods import hash_password

register_endpoint = Blueprint('register', __name__)


def check_username_validity(username):
    # Minimum Length
    if len(username) < 4:
        return False, 'too_short'

    # Check if username is taken
    username = "'" + username + "'"
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE login = {username})"
            cursor.execute(query)
            user_exists = cursor.fetchone()[0]

    if user_exists:
        return False, 'username_taken'

    return True, 'valid'


# For future use e.g. password length check
def check_password_validity(password):
    return True, 'valid'


# TO-DO: Password hashing
def add_user(username, password):
    password = hash_password(password)
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"INSERT INTO `users` (`login`, `password`, `api_key`) VALUES \
                        ('{username}', '{password}', '')"
            cursor.execute(query)
        cnx.commit()


@register_endpoint.route('/register', methods=['POST'])
def register():
    user = request.args.get('user')
    password = request.args.get('password')

    is_valid_username, message = check_username_validity(user)
    if not is_valid_username:
        return {'status': 'fail', 'message': message}

    is_valid_password, message = check_password_validity(password)
    if not is_valid_password:
        return {'status': 'fail', 'message': message}

    add_user(user, password)

    return {'status': 'success'}
