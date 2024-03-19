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

def testDatabase():
    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Executing SQL Statements
    cursor.execute(''' INSERT INTO users VALUES(null, 'test', 'test', 'test') ''')

    # Saving the Actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()


class login(Resource):
    method_decorators = [auth]
    def get(self):
        # code 1 - login successfully
        # code 2 - login failed
        #testDatabase()
        return {'hello': 'yellow man'}


api.add_resource(login, '/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
