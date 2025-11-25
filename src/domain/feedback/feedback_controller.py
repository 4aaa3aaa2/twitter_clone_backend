from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService

from .feedback_repository import FeedbackRepository
from .feedback import Feedback

feedback_bp = Blueprint("feedback_bp", __name__, url_prefix="/api/feedback")

feedback_repository = FeedbackRepository()

class FeedbackController:

    @feedback_bp.route("/add-feedback", methods=["POST"])
    def add_feedback():
        new_feedback = request.get_json()
        feedback = Feedback()
        feedback.user_id = new_feedback.get("user_id")
        feedback.type = new_feedback.get("type")
        feedback.text = new_feedback.get("text")
        feedback_repository.save(feedback)

        return jsonify(message = "feedback received")