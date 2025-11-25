from src.twitter_clone_app import db
from datetime import datetime

class Retweet(db.Model):
    __tablename__ = "retweets"

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference_id = db.Column(db.Integer, nullable=False)
    retweeter_id  = db.Column(db.Integer, nullable=False)
    type  = db.Column(db.String(100), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.now, nullable=False)


    def __repr__(self):
        return f"<id={self.id}, reference id={self.reference_id}, retweeter id={self.retweeter_id}, created_at={self.created_at}>"

    def to_dict(self):
        pass
    