
from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService
from src.util.get_auth_user_id import GetAuthUserId

from typing import List
from .notification_service import NotificationService

notification_bp = Blueprint("notification_bp",__name__, url_prefix="/api/notificaitons")

notification_service = NotificationService()

class NotificationController:
    
    @notification_bp.route("/get-unseen",methods=["GET"])
    def get_user_unseen_notifications(self):
        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        result = notification_service.get_user_unseen_ids_and_mark_all_as_seen(auth_user_id)
        return jsonify(result)
    
    @notification_bp.route("/get-notifications",methods=["POST"])
    def get_notificaitons(self):
        ids: List[int] = request.get_json()   
        print("Received request to retrieve notifications")
        result = notification_service.find_all_notification_dtos_by_id(ids)
        return jsonify(result)
    
