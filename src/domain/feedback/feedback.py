from src.twitter_clone_app import db

class Feedback(db.Model):
    __tablename__ = "feedback"

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id : int = db.Column(db.Integer, nullable=False)
    text : str = db.Column(db.String(500), nullable=False)
    type : str = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<id={self.id}, user_id={self.user_id},text={self.text[50]}, type={self.type}>"

    def to_dict(self):
        pass
    