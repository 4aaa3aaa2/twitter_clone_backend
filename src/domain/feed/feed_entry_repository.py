from sqlalchemy import and_, text
from src.extensions import db
from .feed_entry import FeedEntry
import datetime
from typing import List

class FeedEntryRepository:

    @staticmethod
    def find_by_user_id_order_by_position_asc(user_id: int)-> List[FeedEntry]:
        return db.session.query(FeedEntry).filter_by(user_id=user_id).order_by(FeedEntry.position.asc()).all()


    @staticmethod
    def get_feed_post_ids_custom(user_id: int, cursor: int)->List[int]:
        sql = text("""
            SELECT f.post_id
            FROM feed_entry f
            WHERE f.user_id = :user_id AND f.position >= :cursor
            ORDER BY f.position ASC
            """)
        result = db.session.execute(sql,{"user_id": user_id, "cursor":cursor})

        return [row[0] for row in result.fetchall()]


    @staticmethod
    def delete_by_user_id(user_id: int):
        db.session.query(FeedEntry).filter_by(user_id=user_id).delete()
        db.session.commit()


    @staticmethod
    def find_by_post_id(post_id: int):
        return db.session.query(FeedEntry).filter_by(post_id=post_id).first()


    @staticmethod
    def find_by_post_id_and_user_id(post_id: int, user_id: int):
        return (
            db.session.query(FeedEntry)
            .filter_by(post_id=post_id, user_id=user_id)
            .first()
        )