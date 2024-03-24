from flask import request, Blueprint
from .. import mysql

login_endpoint = Blueprint('login', __name__)


def simple_test(user: str, password: str):
    print(f"{user} {password}")
    if user == 'test' and password == 'test123':
        return True
    else:
        return False


def testDatabase(user, password):

    # TO-DO: Secure it from SQL injection
    myLogin = "'" + user + "'"
    myPass = "'" + password + "'"
    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements

    query = "SELECT password, id, api_key FROM users WHERE login = " + myLogin

    print(f'The query is: {query}')

    cursor.execute(query)

    data = cursor.fetchall()

    correctPassword = data[0][0]
    userId = data[0][1]
    userApiKey = data[0][2]

    print(f'The password for user {myLogin} is {correctPassword}')

    # Saving the Actions performed on the DB
   # mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    result = [correctPassword, userId, userApiKey]

    return result


@login_endpoint.route('/login', methods=['POST'])
def login():
    login = request.args.get('user')
    password = request.args.get('password')

    apiResultDb = testDatabase(login, password)

    correctPassword = apiResultDb[0]
    userId = apiResultDb[1]
    userApiKey = apiResultDb[2]

    if password == correctPassword:
        return {'auth': '1', 'id': userId, 'api_key': userApiKey}
    else:
        return {'auth': '-1'}


@login_endpoint.route('/test_login', methods=['POST'])
def test_login():
    user = request.args.get('user')
    password = request.args.get('password')

    if simple_test(user, password):
        return {'auth': '1', 'id': 0, 'api_key': 12345}
    else:
        return {'auth': '-1'}
