from flask import request, Blueprint
from app.src import app_config
import mysql.connector
from datetime import date
from app.src.auth_methods import auth

users_endpoint = Blueprint('users', __name__)


def add_rank_point(api_key):
    with mysql.connector.connect(**app_config.MYSQL_CONFIG) as cnx:
        with cnx.cursor() as cursor:
            # Executing SQL Statements
            query = "UPDATE users SET rank_points = rank_points + 1 WHERE api_key = '" + api_key + "'"

            cursor.execute(query)
        cnx.commit()
