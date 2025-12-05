from src.extensions import db
from datetime import datetime

class Poll(db.Model):
    __tablename__ = "polls"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id : int = db.Column(db.Integer)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    expired_at : datetime = db.Column(db.DateTime)

    def __repr__(self):
            return f"<id={self.id}, post={self.post_id}, created_at={self.created_at}, expired at={self.expired_at}>"

    def to_dict(self):
        pass