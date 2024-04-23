from flask import request, Blueprint, jsonify
import mysql.connector
from datetime import date
from app.src.query_methods import auth, requires
from app.src import app_config

comment_endpoint = Blueprint('comments', __name__)


@comment_endpoint.route('/comment', methods=['POST'])
def write_comment():
    pass


@comment_endpoint.route('/comment', methods=['GET'])
def read_comment():
    pass


@comment_endpoint.route('/comments', methods=['GET'])
def read_comment(count: int):
    pass
