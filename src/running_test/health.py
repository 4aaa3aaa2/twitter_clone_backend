
from flask import request, jsonify, Blueprint

health_bp = Blueprint("health_bp", __name__, url_prefix="/api")

@health_bp.route("/health")
def health():
    return "ok"