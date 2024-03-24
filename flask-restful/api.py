from flask import Flask
from flask_restful import Resource, Api, reqparse
from auth_methods import admin_auth, auth

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    method_decorators = [auth]

    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
