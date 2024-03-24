from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from auth_methods import admin_auth, auth
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = '172.18.0.2'
app.config['MYSQL_USER'] = 'db_user'
app.config['MYSQL_PASSWORD'] = 'db_user_pass'
app.config['MYSQL_DB'] = 'app_db'

mysql = MySQL(app)


def testDatabase(loginGiven, passwordGiven):

    myLogin = "'" + loginGiven + "'"
    myPass = "'" + passwordGiven + "'"
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

def getPointsFromDb():

    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements

    query = "SELECT places.ID, places.lat, places.long FROM places"

    print(f'The query is: {query}')

    cursor.execute(query)

    data = cursor.fetchall()

    places = []

    for place in data:
        placeID = place[0]
        placeLat = place[1]
        placeLong = place[2]
        places.append({'place_id': placeID, 'latitude': placeLat, 'longitude': placeLong})


    # Saving the Actions performed on the DB
    #mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return places


@app.route('/login', methods=['POST'])
def login():
    #method_decorators = [auth]

    login = request.args.get('login')
    password = request.args.get('password')

    apiResultDb = testDatabase(login, password)

    correctPassword = apiResultDb[0]
    userId = apiResultDb[1]
    userApiKey = apiResultDb[2]

    if password == correctPassword:
        return {'auth': '1', 'id': userId, 'api_key': userApiKey}
    else:
        return {'auth': '-1'}

@app.route('/test', methods=['POST'])
@auth
def test():
    places = getPointsFromDb()
    return places


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
