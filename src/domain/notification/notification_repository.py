from sqlalchemy import and_, text
from src.extensions import db
from .notification import Notification
import datetime
from typing import List

class NotificationRepository:
    @ staticmethod
    def find_by_id(id):
        return db.session.query(Notification).filter(Notification.id==id).first()


    @staticmethod
    def mark_all_as_seen(receiver_id: int)->int:
        sql = text("UPDATE notification n SET n.seen = true WHERE n.receiver_id = :receiver_id AND n.seen = false")
        result = db.session.execute(sql,{"receiver_id":receiver_id})
        return result

    
    @staticmethod
    def find_unseen_notification_ids(receiver_id: int)-> List[int]:
        sql = text("SELECT n.id FROM notification n WHERE n.receiver_id = :receiver_id AND n.seen = false")
        result = db.session.execute(sql,{"receiver_id": receiver_id})
        return result
    
    @staticmethod
    def exists_by_sender_id_receiver_id_type_reference_text(sender_id: int, receiver_id: int, type: str, reference_id: int, text: str)->bool:
        return db.session.query(
            db.session.query(Notification).filter(
                and_(Notification.sender_id == sender_id,
                    Notification.receiver_id == receiver_id,
                    Notification.type == type,
                    Notification.reference_id == reference_id,
                    Notification.text == text
                    )
            ).exists()
        ).scalar()
   
    @staticmethod
    def find_by_sender_id_receiver_id_type_reference_text(sender_id: int, receiver_id: int, type: str, reference_id: int, text: str)->Notification:
        return db.session.query().filter(  
                Notification.sender_id == sender_id,
                Notification.receiver_id == receiver_id,
                Notification.type == type,
                Notification.reference_id == reference_id,
                Notification.text == text
                ).first()
   
    @staticmethod
    def find_by_sender_id_receiver_id_type_reference_id(sender_id: int, receiver_id: int, type: str, reference_id: int)-> Notification:
        return db.session.query().filter(  
                Notification.sender_id == sender_id,
                Notification.receiver_id == receiver_id,
                Notification.type == type,
                Notification.reference_id == reference_id,
                ).first()
    
    @staticmethod
    def find_paginated_notification_ids_by_time(user_id: int, cursor: datetime, limit: int, offset: int)->List[int]:
        sql = text("""SELECT n.id
                FROM notification n
                WHERE n.receiver_id = :user_id AND n.created_at < :cursor 
                ORDER BY n.created_at DESC
                LIMIT :limit OFFSET :offset
                """)
        result = db.session.execute(sql, {"user_id": user_id, "cursor": cursor, "limit":limit, "offset":offset})
        return result
 
    @staticmethod
    def delete_by_reference_id_where_type_is_not_follow():
        pass
    
    @staticmethod
    def find_by_reference_id_where_type_is_not_follow(id: int)->List[Notification]:
        sql = text("""
                SELECT n
                FROM notification n 
                WHERE n.reference_id = :id AND n.type <> 'follow'
                """)
        result = db.session.execute(sql, {"id": id})
        return result
    
    @staticmethod
    def exists_by_id(id : int):
        return db.session.query(db.session.query(Notification).filter(Notification.id == id).exists).scalar()

    @staticmethod
    def find_all_by_id(ids):
        # Fetch all notifications with given IDs
        notifications = Notification.query.filter(Notification.id.in_(ids)).all()
        return notifications