from flask import Flask
from app.src.config.config import Config

# Generating app's configuration
app_config = Config().config

# Declaring flask application
app = Flask(app_config.APP_NAME)

# Swagger configuration
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': app_config.APP_NAME})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register main blueprint
from app.src.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/v1')
