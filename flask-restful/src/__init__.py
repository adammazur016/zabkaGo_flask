from flask import Flask
from .config.config import Config

# choose config
config = Config().config

# declaring flask application
app = Flask(config.APP_NAME)


# Register api blueprint
from .routes import api_bp
app.register_blueprint(api_bp)

