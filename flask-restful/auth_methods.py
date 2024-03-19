from flask import Flask
from functools import wraps
from flask import request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '172.18.0.2'
app.config['MYSQL_USER'] = 'db_user'
app.config['MYSQL_PASSWORD'] = 'db_user_pass'
app.config['MYSQL_DB'] = 'app_db'

mysql = MySQL(app)


def testDatabase():
    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(''' INSERT INTO users VALUES(null, 'test', 'test', 'test') ''')

    # Saving the Actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()


def access_denied():
    return {'error_message': 'Not correct credentials'}, 401


def access_granted():
    return {'response_code': '1'}


def admin_verify(admin_api_key: str):
    # To-Do: Implement verification via db
    if admin_api_key == 'test':
        return True
    else:
        return False


def verify(login: str):
    # To-Do: Implement verification via db

    if login == 'test':
        testDatabase()
        return True
    else:
        return False


def admin_auth(func):
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('api_key') and admin_verify(request.args.get('api_key')):
            return func(*args, **kwargs)
        else:
            return access_denied()
    return verify_key


def auth(func):
    @wraps(func)
    def verify_key(*args, **kwargs):
        if request.args.get('login') and verify(request.args.get('login')):
            return access_granted()
        else:
            return access_denied()
    return verify_key
