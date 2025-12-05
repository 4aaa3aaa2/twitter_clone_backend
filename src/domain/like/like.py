from src.extensions import db
from datetime import datetime

class Like(db.Model):
    __tablename__ = "like"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    liker_id : int = db.Column(db.Integer, nullable=False)
    post_id : int = db.Column(db.Integer, nullable=False)
    created_at : datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<post_id={self.post_id}, liker_id={self.liker_id}, created at={self.created_at}>"
    
    def to_dict(self):
        pass
    