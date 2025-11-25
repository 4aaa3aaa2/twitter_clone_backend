from src.twitter_clone_app import db
from datetime import datetime
from sqlalchemy import and_, text
from typing import List, Optional
from .retweet import Retweet

class RetweetRepository:
    
    @staticmethod
    def find_all_by_retweeter_id(retweeter_id: int)-> List[Retweet]:
        return db.session.query(Retweet).filter(Retweet.retweeter_id == retweeter_id).all()
    
    @staticmethod
    def exists_by_retweeter_id_and_reference_id(retweeter_id: int, reference_id: int)->bool:
        return db.session.query(
            db.session.query(Retweet).filter(
                and_(Retweet.retweeter_id == retweeter_id,
                        reference_id == reference_id)
            ).exists()
        ).scalar()
    
    @staticmethod
    def find_by_retweeter_id_and_reference_id(retweeter_id: int, reference_id: int)->Retweet:
        return db.session.query(Retweet).filter_by(Retweet.retweeter_id == retweeter_id, Retweet.reference_id == reference_id).first()
    
    @staticmethod
    def find_all_by_reference_id(reference_id: int)-> List[Retweet]:
        return db.session.query(Retweet).filter(Retweet.reference_id == reference_id).all()

