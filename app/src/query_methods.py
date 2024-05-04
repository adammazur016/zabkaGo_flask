from functools import wraps
from flask import request, jsonify, Response
from src import app_config
import mysql.connector
import hashlib


def get_user_id(session_token: str):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE session_token = '{session_token}'")
            result = cursor.fetchall()
            if not result:
                return ''
            else:
                return result[0][0]


def hash_password(password: str) -> str:
    """
    Hashes password using sha256 algorithm
    :returns: hashed password
    """
    # Convert password to bytes encoded in utf-8
    password_bytes = password.encode('utf-8')

    # Hash password with sha256
    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return hashed_password


def access_denied() -> (Response, int):
    """
    Default response when trying to access authentication protected endpoint with no valid session token
    :returns: prepared response, http status code
    """
    return {'status': 'fail', 'message': 'no_session_token'}, 401


def admin_verify(admin_api_key: str) -> bool:
    """
    At this moment it's unused method of authorization in endpoints reserved for admins.
    :returns: verification result
    TODO: Implement verification via db // Currently unnecessary
    """
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(session_token: str) -> bool:
    """
    (Part of @auth decorator) Checks if given session token is valid
    :returns: verification result
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE session_token = '{session_token}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    if exists:
        return True
    else:
        return False


def requires(*args, **kwargs):
    """
    Decorator which checks if specified parameters were passed in request.
    If they are missing, it automatically returns error 400 with missing parameters and prevents execution of wrapped function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*wrapped_args, **wrapped_kwargs):
            query_params = request.args
            missing_params = [param for param in args if param not in query_params]
            if missing_params:
                return jsonify({"status": "fail", "message": "missing_required_parameters", "missing": missing_params}), 400
            return func(*wrapped_args, **wrapped_kwargs)
        return wrapper
    return decorator


def admin_auth(func):
    """
    Decorator used in endpoints requiring admin authorization.
    Currently unused.
    """
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('session_token') and admin_verify(request.args.get('session_token')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key


def auth(func):
    """
    Decorator used in endpoints requiring normal authorization.
    Checks existence of session_token parameter in request, then verifies if it's valid.
    """
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('session_token') and verify(request.args.get('session_token')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key

# TODO: Add input sanitization decorator
# TODO: Add achievement trigger decorator
