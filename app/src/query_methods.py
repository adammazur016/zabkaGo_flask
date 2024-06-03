from functools import wraps
from flask import request, jsonify, Response
import mysql.connector
from src import app_config
from src.achievements import check_triggers, Achievement
from src.helper_methods import get_user_id


def access_denied() -> (Response, int):
    """
    Default response when attempting to access an authentication-protected endpoint without a valid session token.

    :return: A prepared response along with the HTTP status code.
    """
    return {'status': 'fail', 'message': 'no_session_token'}, 401


def verify(session_token: str) -> bool:
    """
    (Part of the @auth decorator) Checks if the given session token is valid.

    :param session_token: The session token to be verified.
    :return: The verification result.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT * FROM users WHERE session_token = '{session_token}')"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    return exists


def requires(*args, **kwargs):
    """
    Decorator that checks if specified parameters were passed in the request.
    If any of them are missing, it automatically returns a 400 error with a message indicating the missing parameters and prevents the execution of the wrapped function.
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


def triggers(*args: list[Achievement]):
    """
    Decorator that, after the execution of the wrapped function, checks if the user may acquire new achievements.
    Requirement checks are only performed for achievements specified in the decorator arguments.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*wrapped_args, **wrapped_kwargs):
            ret_val = func(*wrapped_args, **wrapped_kwargs)
            if request.args['session_token']:
                user_id = get_user_id(request.args['session_token'])
                achievements = [achievement for achievement_list in args for achievement in achievement_list]
                check_triggers(user_id, achievements)
            elif request.args['user_id']:
                user_id = int(request.args['user_id'])
                achievements = [achievement for achievement_list in args for achievement in achievement_list]
                check_triggers(user_id, achievements)
            return ret_val
        return wrapper
    return decorator


def auth(func):
    """
    Decorator used in endpoints requiring standard authorization.
    Checks for the existence of the session_token parameter in the request, then verifies if it's valid.
    """
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('session_token') and verify(request.args.get('session_token')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key
