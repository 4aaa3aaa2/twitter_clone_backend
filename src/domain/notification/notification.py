from src.twitter_clone_app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    receiver_id : int = db.Column(db.Integer, nullable=False)
    sender_id : int = db.Column(db.Integer, nullable=False)
    type : str = db.Column(db.String(100), nullable=False)
    reference_id : int = db.Column(db.Integer, nullable=False)
    text : str = db.Column(db.String(500), nullable=False)
    seen : bool = db.Column(db.Boolean, default=False)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<sender={self.sender_id}, receiver={self.receiver_id}, text={self.text[50]}, created_at={self.created_at}>"

    def to_dict(self):
        pass
    