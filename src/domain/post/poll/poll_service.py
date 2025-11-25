from src.twitter_clone_app import db
from src.util.poll_utils import POllUtils
from .poll import Poll
from .poll_vote_repository import PollVotesRepository
from .poll_choices_repository import PollChoiceRepository
from .poll_vote import PollVote
from .poll_choice import PollChoice
from .polls_repository import PollsRepository

from typing import List, Optional
from datetime import datetime

polls_repository = PollsRepository()
poll_choice_repository = PollChoiceRepository()
poll_vote_repository = PollVotesRepository()
class PollService:
    
    @staticmethod
    def create_new_poll_for_post(post_id: int, poll_choices: List[str], poll_expiry: List[str]):
        poll = Poll()
        poll.post_id = post_id
        poll.expired_at = datetime.strptime(poll_expiry, "%Y-%m-%d %H:%M:%S")
        db.session.add(poll)
        db.session.commit()

        if poll is None:
            raise ValueError("poll cannot be saved")
        for poll_choice in poll_choices:
            poll_choice_entiry = PollChoice()
            poll_choice_entiry.poll_id = poll.id
            poll_choice_entiry.vote_count = 0
            poll_choice_entiry.choice = poll_choice
            db.session.add(poll_choice_entiry)
        db.session.commit()     


    @staticmethod
    def submit_poll_vote( voter_id: int, choice_id: int, poll_id: int)-> List[PollChoice]:
        poll_to_check: Optional[Poll] = polls_repository.find_by_id(poll_id)
        if poll_to_check:
            poll: Poll = poll_to_check
            if POllUtils.check_poll_expiry():
                raise ValueError("poll expired")
        
        has_voted: bool = poll_vote_repository.exists_by_user_id_and_poll_id(voter_id, poll_id)
        if has_voted:
            raise ValueError("user has voted")
        vote = PollVote()
        vote.user_id = voter_id
        vote.poll_choice_id = choice_id
        vote.poll_id = poll_id
        db.session.add(vote)
        db.session.commit()
        return poll_choice_repository.find_all_by_poll_id(poll_id)
    
    @staticmethod
    def get_voted_choice_id(poll_id: int, user_id: int)-> int:
        poll_vote: Optional[PollVote] = poll_vote_repository.find_by_poll_id_and_user_id(poll_id, user_id)
        if poll_vote:
            return poll_vote.poll_id
        else:
            return -1
    
    @staticmethod
    def get_poll_choices(poll_id: int)-> List[PollChoice]:
        return poll_choice_repository.find_all_by_poll_id(poll_id)