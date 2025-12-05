from src.extensions import db
from .feedback import Feedback

class FeedbackRepository:
    @staticmethod 
    def save(feedback: Feedback):
        db.session.add(feedback)
        db.session.commit()