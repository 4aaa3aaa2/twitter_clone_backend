from src.extensions import db

class Follow(db.Model):
    __tablename__ = "follow"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    followed_id : int = db.Column(db.Integer, nullable=False)
    follower_id : int = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<id={self.id}, followed_id={self.followed_id}, follower_id={self.follower_id}>"
    
    def to_dict(self):
        pass
    