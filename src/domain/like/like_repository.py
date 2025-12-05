from sqlalchemy import and_, text
from src.extensions import db
from .like import Like
import datetime
from typing import Optional,List

class LikeRepository:
    @staticmethod
    def find_by_id(id:int)->Optional[Like]:
        return db.session.query(Like).get(id)
        

    @staticmethod
    def find_all_by_liker_id(id: int)->List[Like]:
        return db.session.query(Like).filter(Like.liker_id == id).all()

    @staticmethod
    def find_all_by_liked_post_id(id: int)->List[Like]:
        return db.session.query(Like).filter(Like.post_id == id).all()

    @staticmethod
    def exists_by_liker_id_and_liked_post_id(liker_id: int, liked_post_id: int)-> bool:
        return db.session.query(
            db.session.query(Like).filter(
                and_(Like.liker_id == liker_id,
                    Like.post_id == liked_post_id)
            ).exists()
        ).scalar()

    @staticmethod
    def find_by_liker_id_and_liked_post_id(liker_id: int, liked_post_id: int)->Optional[Like]:
        return db.session.query(Like).filter(
            Like.liker_id == liker_id,
            Like.post_id == liked_post_id
        ).first()

    @staticmethod
    def find_paginated_liked_post_ids_by_time(user_id: int, cursor: datetime, limit: int, offset: int)->List[int]:
        sql = text("""
            SELECT l.liked_post_id
            FROM likes l
            JOIN posts p ON l.liked_post_id = p.id
            WHERE l.liker_id = :user_id
                AND l.created_at < :cursor
            ORDER BY l.created_at DESC
            LIMIT :limit OFFSET :offset
        """)

        result = db.session.execute(sql, {
                "user_id": user_id,
                "cursor": cursor,
                "limit": limit,
                "offset": offset
            }).scalars().all()
        return result