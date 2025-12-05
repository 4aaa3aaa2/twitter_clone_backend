from src.extensions import db

from src.domain.post.post import Post
from src.domain.post.post_repository import PostRepository
from .notification_repository import NotificationRepository
from .new_notification import NewNotification
from .notification import Notification
from .notification_dto import NotificationDTO
from typing import Optional,List

post_repository = PostRepository()
notification_repository = NotificationRepository()


class NotificationService:
    
    @staticmethod    
    def check_existing_notification(new_notification: NewNotification)-> bool:
        if NotificationRepository.exists_by_sender_id_receiver_id_type_reference_text(
            new_notification.sender_id, new_notification.receiver_id,
            new_notification.type, new_notification.reference_id,
            new_notification.text
        ):
            return True
        else: 
            return False
    
    @staticmethod
    def add_notification( new_notification: NewNotification)-> bool:
        if NotificationService.check_existing_notification: 
            return False
        elif new_notification.sender_id == new_notification.receiver_id:
            return False
        
        notification = Notification()
        notification.sender_id = new_notification.sender_id
        notification.receiver_id = new_notification.receiver_id
        notification.receiver_id = new_notification.receiver_id
        notification.seen = False
        notification.text = new_notification.text
        notification.reference_id = new_notification.reference_id
        notification.type = new_notification.type
        
        db.session.add(notification)
        db.session.commit()

        if NotificationRepository.exists_by_id(notification.id):
            return True
        else:
            return False
        
    
    @staticmethod    
    def create_reply_notification_template(sender_id: int, reply_post_id: int)->NewNotification:
        reply: Optional[Post] = PostRepository.find_by_id(reply_post_id)
        if not reply:
            return None
        
        parent_post_id: int = reply.parent_id
        if parent_post == None:
            return None
        
        parent_post: Optional[Post] = PostRepository.find_by_id(parent_post_id)
        if not parent_post:
            return None
        
        new_notification = NewNotification()
        new_notification.sender_id = sender_id
        new_notification.receiver_id = parent_post.user_id
        new_notification.reference_id = reply.id
        new_notification.text = reply.text
        new_notification.type = "reply"

        return new_notification
    
    @staticmethod    
    def create_new_notification_from_type( sender_id: int, reference_id: int, type: str):
        if type == "reply":
            to_create = NotificationService.create_reply_notification_template(sender_id,reference_id)
        elif type == "follow":
            to_create = NotificationService.create_follow_notification_template(sender_id, reference_id, type)
        else:
            to_create = NotificationService.create_new_notification_template_from_post(sender_id, reference_id, type)
        NotificationService.add_notification(to_create)
    
    @staticmethod
    def delete_notification_from_type( sender_id: int, reference_id: int, type: str):
        if type == "follow":
            notification: Notification = NotificationService.get_follow_notification(sender_id, reference_id, type)
        else:
            notification: Notification = NotificationService.get_notification_from_sender_and_post(sender_id, reference_id, type)
        
        if notification:
            db.session.delete(notification)
            db.session.commit()
    
    @staticmethod
    def delete_all_non_follow_notifications_by_reference_id( reference_id:int):
        to_delete = notification_repository.find_by_reference_id_where_type_is_not_follow(reference_id)
        for notification in to_delete:
            db.session.delete(notification)
        db.session.commit()

    
    @staticmethod
    def create_new_notification_template_from_post( sender_id: int, post_id: int, type: str):
        new_notification = NewNotification()
        new_notification.sender_id = sender_id
        new_notification.type = type
        post: Optional[Post] = PostRepository.find_by_id(post_id)

        if not post: 
            return None
        else:
            new_notification.text = post.text
            new_notification.receiver_id = post.user_id
            new_notification.reference_id = post.id
        
        return new_notification
    
    @staticmethod
    def get_notification_from_sender_and_post( sender_id: int, post_id: int, type: str):
        new_notification = NewNotification()
        new_notification.sender_id = sender_id 
        new_notification.type = type
        post: Optional[Post] = PostRepository.find_by_id(post_id)
        if not post:
            return None
        
        new_notification.text = post.text
        new_notification.receiver_id = post.user_id
        new_notification.reference_id = post.id
        notification: Notification = NotificationRepository.find_by_sender_id_receiver_id_type_reference_text(
            new_notification.sender_id,
            new_notification.receiver_id,
            new_notification.type,
            new_notification.reference_id,
            new_notification.text
        )
        return notification
    
    @staticmethod
    def create_follow_notification_template( follower_id: int, following_id:int, type: int):
        new_notification = Notification()
        new_notification.sender_id = follower_id
        new_notification.type = type
        new_notification.receiver_id = following_id
        new_notification.reference_id = follower_id
        new_notification.text = "" 
        return new_notification 
    
    @staticmethod
    def get_follow_notification( follower_id: int, following_id: int, type: str):
        notiication: Notification = NotificationRepository.find_by_sender_id_receiver_id_type_reference_id(follower_id, following_id,type, follower_id)
        return notiication
    
    @staticmethod
    def find_all_notification_dtos_by_id( ids: List[int]):
        notifications = NotificationRepository.find_all_by_id(ids)
        notification_dtos: List[NotificationDTO] = []
        for notification in notifications:
            notification_dtos.append(NotificationDTO(notification))

        return notification_dtos
    
    @staticmethod
    def get_user_unseen_ids_and_mark_all_as_seen( receiver_id: int):
        print("getting and refreshing unseen ids")
        unseen_ids: List[int] = NotificationRepository.find_unseen_notification_ids(receiver_id)
        print(f"unseen size is {len(unseen_ids)}")
        NotificationRepository.mark_all_as_seen(receiver_id)
        print(f"new unseen size is {len(unseen_ids)}")
        return unseen_ids