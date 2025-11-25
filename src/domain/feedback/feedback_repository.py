from src.twitter_clone_app import db
from .feedback import Feedback

class FeedbackRepository:
    @staticmethod 
    def save(feedback: Feedback):
        db.session.add(feedback)
        db.session.commit()