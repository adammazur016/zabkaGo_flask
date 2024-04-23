from flask import Blueprint
from app.src.endpoints import login, register, shops, users, achievements

# main blueprint to be registered with application
api_bp = Blueprint('api', __name__)


# Register endpoint blueprints
api_bp.register_blueprint(login.login_endpoint)
api_bp.register_blueprint(register.register_endpoint)
api_bp.register_blueprint(users.users_endpoint)
api_bp.register_blueprint(shops.shops_endpoint)
api_bp.register_blueprint(achievements.achievements_endpoint)