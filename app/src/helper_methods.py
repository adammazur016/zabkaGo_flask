import mysql.connector
from src import app_config


def does_shop_exist(shop_id: int) -> bool:
    """
    Checks if a shop with the given id exists.

    :param shop_id: The id of the shop
    :return: True if the shop exists, False otherwise
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            # Replace login with display name later
            query = f"SELECT EXISTS(SELECT * FROM places where id = {shop_id})"
            cursor.execute(query)
            exists = cursor.fetchone()[0]
    return bool(exists)


def get_user_id(session_token: str):
    """
    Retrieves the user ID associated with the given session token from the database.

    :param session_token: The session token used to identify the user.
    :return: The user ID if the session token is valid, otherwise an empty string.
    """
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            cursor.execute(f"SELECT id FROM users WHERE session_token = '{session_token}'")
            result = cursor.fetchall()
            if not result:
                return ''
            else:
                return result[0][0]
