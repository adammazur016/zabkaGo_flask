from flask import Flask
from flask_restful import Resource, Api, reqparse
from auth_methods import admin_auth, auth
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)


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
