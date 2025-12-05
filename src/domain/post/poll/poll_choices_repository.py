from src.extensions import db
from typing import List
from .poll_choice import PollChoice


class PollChoiceRepository:
    @staticmethod
    def find_all_by_poll_id(poll_id: int)->List[PollChoice]:
        return db.session.query(PollChoice).filter(PollChoice.poll_id==poll_id).all()