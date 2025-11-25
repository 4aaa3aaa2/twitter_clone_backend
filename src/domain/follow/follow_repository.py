from sqlalchemy import and_, text
from src.twitter_clone_app import db

from .follow import Follow

from datetime import datetime
from typing import List, Optional

class FollowRepository:

    @staticmethod
    def find_all_by_follower_id(follower_id: int)->List[Follow]:
        return db.session.query(Follow).filter(Follow.follower_id == follower_id).all()


    @staticmethod
    def exists_by_followed_id_and_follower_id(followed_id: int, folower_id: int)->bool:
        return db.session.query(
            db.session.query(Follow).filter(
                and_(
                    Follow.followed_id == followed_id,
                    Follow.follower_id == folower_id
                )
            ).exists()
        ).scalar()


    @staticmethod
    def find_by_followed_id_and_follower_id(followed_id: int, follower_id: int)-> Optional[int]:
        return db.session.query(Follow).filter(
            Follow.followed_id == followed_id,
            Follow.follower_id == follower_id
        ).first()


    @staticmethod
    def find_all_by_followed_id(followed_id: int)->List[Follow]:
        return db.session.query(Follow).filter(Follow.followed_id == followed_id).all()
