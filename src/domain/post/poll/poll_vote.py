from src.extensions import db
from datetime import datetime

class PollVote:
    __tablename__ = "poll_votes"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    poll_id = db.Column(db.Integer)
    poll_choice_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    