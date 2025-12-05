from src.extensions import db
from .poll_vote import PollVote
from typing import Optional

class PollVotesRepository:
    @staticmethod 
    def exists_by_user_id_and_poll_id(user_id: int, poll_id: int)-> bool:
        return db.session.query(
            db.session.query(PollVote).filter(
            PollVote.user_id==user_id,
            PollVote.poll_id==poll_id
            ).exists()
        ).scalar()
    
    @staticmethod
    def find_by_poll_id_and_user_id(poll_id: int, user_id: int)-> Optional[PollVote]:
        return db.session.query(PollVote).filter(PollVote.poll_id==poll_id, PollVote.user_id==user_id).first()
