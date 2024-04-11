from flask import Flask
from app.src.config.config import Config

# choose config
app_config = Config().config

# declaring flask application
app = Flask(app_config.APP_NAME)

# Swagger configuration

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Zabka Go'})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register api blueprint
from app.src.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/v1')

