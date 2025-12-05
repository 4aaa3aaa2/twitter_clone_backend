from sqlalchemy import and_, text
from src.extensions import db
from .bookmark import Bookmark
import datetime
from typing import List

class BookmarkRepository:
        
    @staticmethod
    def find_by_id(id:int):
        return db.session.query(Bookmark).get(id)
        

    @staticmethod
    def find_all_by_bookmarked_by(user_id: int)-> List[Bookmark]:
        return db.session.query(Bookmark).filter(Bookmark.bookmarked_by == user_id).all()


    @staticmethod
    def find_all_by_bookmarked_post(bookmarked_post: int)-> List[Bookmark]:
        return db.session.query(Bookmark).filter(Bookmark.bookmarked_post == bookmarked_post).all()

    @staticmethod
    def exists_by_bookmarked_by_and_bookmarked_post(bookmarked_by: int, bookmarked_post: int)->bool:
        return db.session.query(
            db.session.query(Bookmark).filter(
                and_(Bookmark.bookmarked_by == bookmarked_by,
                        Bookmark.bookmarked_post == bookmarked_post)
            ).exists()
        ).scalar()

    @staticmethod
    def find_by_bookmarked_by_and_bookmarked_post(bookmarked_by: int, bookmarked_post: int):
        return db.session.query(Bookmark).filter(
            Bookmark.bookmarked_by == bookmarked_by,
            Bookmark.bookmarked_post == bookmarked_post
        ).first()

    @staticmethod
    def find_paginated_bookmarked_post_ids_by_time(user_id: int, cursor: datetime, limit: int=20)->List[int]:
        sql = text("""
            SELECT b.bookmarkedPost
            FROM bookmark b
            JOIN Post p ON b.bookmarkedPost = p.id
            WHERE b.bookmarkedBy = :user_id
            AND b.createdAt < :cursor
            ORDER BY b.createdAt DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit})
        return [row[0] for row in result.fetchall()]