from datetime import datetime
from src.extensions import db

class TrendEntity(db.Model):
    __tablenam__ = "trends"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(512))
    tweet_volume = db.Column(db.Integer)
    recorded_at = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self):
        pass

