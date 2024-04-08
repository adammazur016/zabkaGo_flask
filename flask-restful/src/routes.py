from flask import Blueprint
from .endpoints import login, register, makevisit, getpoints, checkvisit, addrankpoint

# main blueprint to be registered with application
api_bp = Blueprint('api', __name__)


# Register endpoint blueprints
api_bp.register_blueprint(login.login_endpoint)
api_bp.register_blueprint(register.register_endpoint)
api_bp.register_blueprint(addrankpoint.addrankpoint_endpoint)
api_bp.register_blueprint(checkvisit.check_visit_endpoint)
api_bp.register_blueprint(getpoints.get_points_endpoint)
api_bp.register_blueprint(makevisit.makevisit_endpoint)