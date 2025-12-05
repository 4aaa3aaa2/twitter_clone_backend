from sqlalchemy import func, text
from src.extensions import db
from .user import User
import datetime

class UserRepository:
    @staticmethod
    def find_by_username(username:str):
        return db.session.query(User).filter(func.lower(User.username) == username.lower()).first()

    @staticmethod
    def find_by_id(user_id: int):
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def exists_user_by_email(email: str) -> bool:
        return db.session.query(db.session.query(User).filter(User.email == email).exists()).scalar() 
    
    @staticmethod
    def find_by_email(email: str):
        return db.session.query(User).filter(User.email == email ).first()

    @staticmethod
    def exists_user_by_username( username:str) -> bool:
        return db.session.query(db.session.query(User).filter(User.username==username).exists()).scalar()

    @staticmethod
    def search_by_username_or_display_name(query: str):
        sql = text("""
            SELECT u FROM User u
            WHERE LOWER(u.username) LIKE LOWER(CONCAT('%', :query, '%'))
            OR LOWER(u.displayName) LIKE LOWER(CONCAT('%', :query, '%'))
        """)
        result = db.session.execute(sql,{"query" : query})
        return [row[0] for row in result.fetchall()].scalars().all()

    @staticmethod
    def find_user_ids_by_follower_count(cursor: int, limit: int):
        # Raw SQL query since it's complex aggregation
        sql = text("""
            SELECT u.id
            FROM users u
            LEFT JOIN follow f ON f.followed_id = u.id
            GROUP BY u.id
            HAVING COUNT(f.follower_id) <= :cursor
            ORDER BY COUNT(f.follower_id) DESC
            LIMIT :limit
        """)
        result = db.session.execute(sql, {'cursor': cursor, 'limit': limit})
        return [row[0] for row in result.fetchall()]

    @staticmethod
    def find_user_ids_by_created_at_custom(cursor: datetime, limit: int, offset: int = 0):
        # Emulating Pageable with limit + offset
        sql = text("""
            SELECT u.id
            FROM users u
            WHERE u.created_at < :cursor
            ORDER BY u.created_at DESC
            LIMIT :limit OFFSET :offset
        """)
        result = db.session.execute(sql, {'cursor': cursor, 'limit': limit, 'offset': offset})
        return [row[0] for row in result.fetchall()].scalars().all()

    @staticmethod
    def find_by_google_id(google_id: str):
        return db.session.query(User).filter(User.google_id == google_id).first()