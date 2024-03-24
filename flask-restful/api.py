from flask import Flask
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

    query = "SELECT password FROM users WHERE login = " + myLogin

    print(f'The query is: {query}')

    cursor.execute(query)

    data = cursor.fetchall()

    correctPassword = data[0][0]

    print(f'The password for user {myLogin} is {correctPassword}')

    # Saving the Actions performed on the DB
   # mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return correctPassword


class login(Resource):
    #method_decorators = [auth]
    def get(self, login3, password):
        correctPwd = testDatabase(login3, password)
        # code 1 - login2 successfully
        # code 2 - login2 failed
        if correctPwd == password:
            return {'auth': '1'}
        else:
            return {'auth': '-1'}


api.add_resource(login, '/login/<string:login3>/<string:password>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
