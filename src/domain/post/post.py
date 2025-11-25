from src.twitter_clone_app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "posts"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id : int = db.Column(db.Integer, nullable=False)
    parent_id : int = db.Column(db.Integer, nullable=False)
    text : str = db.Column(db.String(500), nullable=False)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
            return f"<user={self.user_id}, parent={self.parent_id}, text={self.text[50]}, created_at={self.created_at}>"

    def to_dict(self):
        pass
    