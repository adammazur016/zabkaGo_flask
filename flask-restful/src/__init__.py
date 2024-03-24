from flask import Flask
from flask_restful import Api
from flask_mysqldb import MySQL
from .config.config import Config

# choose config
config = Config().config

# declaring flask application
app = Flask(config.APP_NAME)

# declare api
api = Api(app)

# configure database
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

# MySQL db instance
mysql = MySQL(app)

# Register api blueprint
from .routes import api_bp
app.register_blueprint(api_bp)

