from datetime import datetime
from src.extensions import db

class FeedEntry(db.Model):
    __tablename__ = "feed_entry"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id : int = db.Column(db.Integer, nullable=False)
    post_id : int = db.Column(db.Integer, nullable=False)
    score : float = db.Column(db.Float)
    position : int = db.Column(db.Integer)

    def __repr__(self):
        return f"<FeedEntry id={self.id}, user_id={self.user_id}, post_id={self.post_id}, score={self.score}, position={self.position}>"

    def to_dict(self):
        pass
    