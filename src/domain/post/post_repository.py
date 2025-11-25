from sqlalchemy import and_, text
from src.twitter_clone_app import db
from .post import Post
import datetime
from typing import List, Optional

class PostRepository:
    
    @staticmethod
    def find_by_id(id: int)-> Optional[Post]:
        return db.session.query(Post).get(id)
    
    @staticmethod
    def find_all_by_id(ids: List[int])-> List[Post]:
        return db.session.query(Post).filter(Post.id.in_(ids)).all()
    
    @staticmethod
    def find_by_user_id(id: int)->Optional[Post]:
        pass
    
    @staticmethod
    def find_all_by_user_id(id: int)-> Optional[List[Post]]:
        return db.session.query(Post).filter(Post.user_id == id).all()
    
    @staticmethod
    def find_all_by_parent_id(id: int)-> List[Post]:
        return db.session.query(Post).filter(Post.parent_id == id).all()
    
    @staticmethod
    def find_paginated_tweet_and_retweet_ids_by_user_id(user_id: int, cursor: datetime):
        pass
    
    @staticmethod
    def find_post_ids_by_user_and_reposts(user_id: int, cursor: datetime, limit: int)-> List[int]:
        sql = text("""" 
            SELECT post_id FROM (
            SELECT p.id AS post_id, p.created_at AS activity_time
            FROM posts p
            WHERE p.user_id = :user_id
            AND p.parent_id IS NULL
            AND p.created_at <= :cursor

            UNION ALL

            SELECT r.reference_id AS post_id, r.created_at
            FROM retweets r
            JOIN posts p ON p.id = r.reference_id
            WHERE r.retweeter_id = :user_id
            AND p.user_id != :user_id
            AND r.created_at <= :cursor
            ) AS combined
            ORDER BY activity_time DESC
            LIMIT :limit
            """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit})
        return [row[0] for row in result.fetchall()].scalars().all()
    
    @staticmethod
    def find_next_paginated_post_ids_by_time(cursor, limit: int):
        sql = text("""
            SELECT p.id
            FROM posts p
            WHERE p.parent_id IS NULL AND p.created_at < :cursor
            ORDER BY p.created_at DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"cursor": cursor, "limit": limit}).scalars().all()
        return result
    
    @staticmethod
    def find_paginated_tweet_ids_by_user_id(user_id: int, cursor: int, limit: int):
        sql = text("""
            SELECT p.id FROM posts p
            WHERE p.user_id = :user_id AND p.parent_id IS NULL AND p.id < :cursor
            ORDER BY p.id DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit}).scalars().all()
        return result
    
    @staticmethod
    def find_paginated_tweets_by_user_id(user_id: int, cursor: int, limit: int):
        sql = text("""
            SELECT * FROM posts p
            WHERE p.user_id = :user_id AND p.parent_id IS NULL AND p.id < :cursor
            ORDER BY p.id DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit}).mappings().all()
        return result
    
    @staticmethod
    def find_paginated_reply_ids_by_user_id_by_time( user_id: int, cursor, limit: int):
        sql = text("""
            SELECT p.id
            FROM posts p
            WHERE p.user_id = :user_id
                AND p.parent_id IS NOT NULL
                AND p.created_at < :cursor
            ORDER BY p.created_at DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit}).scalars().all()
        return result
    
    @staticmethod
    def find_paginated_post_ids_from_followed_users_by_time(followed_user_ids, cursor, limit: int):
        sql = text("""
            SELECT p.id
            FROM posts p
            WHERE p.user_id = ANY(:followed_user_ids)
                AND p.parent_id IS NULL
                AND p.created_at < :cursor
            ORDER BY p.created_at DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {
            "followed_user_ids": followed_user_ids,
            "cursor": cursor,
            "limit": limit
        }).scalars().all()
        return result
    
    @staticmethod
    def find_all_post_ids(limit: int, offset: int = 0):
        sql = text("""
            SELECT p.id FROM posts p
            ORDER BY p.id
            LIMIT :limit OFFSET :offset
        """)
        result = db.session.execute(sql, {"limit": limit, "offset": offset}).scalars().all()
        return result
    
    @staticmethod
    def find_post_ids_by_author(author_id: int):
        sql = text("""
            SELECT p.id FROM posts p
            WHERE p.user_id = :author_id AND p.parent_id IS NULL
        """)
        result = db.session.execute(sql, {"author_id": author_id}).scalars().all()
        return result
    
    @staticmethod
    def find_all_top_level_posts(self):
        sql = text("SELECT * FROM posts WHERE parent_id IS NULL")
        result = db.session.execute(sql).mappings().all()
        return result
    
    @staticmethod
    def find_paginated_post_ids_with_media_by_user_id_by_time(user_id: int, cursor, limit: int):
        sql = text("""
            SELECT p.id
            FROM posts p
            WHERE p.user_id = :user_id
                AND p.created_at < :cursor
                AND EXISTS (
                SELECT 1 FROM post_media pm WHERE pm.post_id = p.id
                )
            ORDER BY p.created_at DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit": limit}).scalars().all()
        return result