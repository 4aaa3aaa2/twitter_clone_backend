from .trend_entity import TrendEntity
from .trend_repository import TrendRepository

from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService
from typing import List

trend_bp = Blueprint("trend_bp", __name__,url_prefix="/api/trends")

trend_repository = TrendRepository()

class TrendController:
    
    @trend_bp.route("/get",methods=["GET"])
    def get_trends():
        trend_entity_list: List[TrendEntity] = trend_repository.find_all()
        return jsonify(trend_entity_list)
    
    @trend_bp.route("/get-top-five", methods=["GET"])
    def get_top_5_trends():
        result = trend_repository.find_top_5_by_tweet_volume()
        return jsonify(result)