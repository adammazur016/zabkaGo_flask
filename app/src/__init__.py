from flask import Flask
from app.src.config.config import Config

# choose config
app_config = Config().config

# declaring flask application
app = Flask(app_config.APP_NAME)


# Register api blueprint
from app.src.routes import api_bp
app.register_blueprint(api_bp)

