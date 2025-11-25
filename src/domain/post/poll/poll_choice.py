from src.twitter_clone_app import db

class PollChoice(db.Model):
    __tablename__ = "poll_choices"

    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    choice = db.Column(db.String(100))
    vote_count = db.Column(db.Integer)
    poll_id = db.Column(db.Integer)