from src.twitter_clone_app import db
from .poll import Poll
from typing import Optional

class PollsRepository:
    @staticmethod
    def exits_by_post_id(post_id: int)->bool:
        return db.session.query(db.session.query(Poll).filter(Poll.post_id == post_id).exists()).scalar()
    
    @staticmethod
    def find_by_post_id(post_id: int)-> Optional[Poll]:
        return db.session.query(Poll).get( post_id)
    
    @staticmethod 
    def find_by_id(poll_id: int):
        return db.session.query(Poll).filter(Poll.id == poll_id).first()
