from src.extensions import db
from src.domain.user.user_dto import UserDTO
from src.domain.user.user_service import UserService
from src.domain.notification.notification_service import NotificationService

from typing import List, Optional

from .follow_repository import FollowRepository
from .follow import Follow

follow_repository = FollowRepository()
notification_service = NotificationService()
user_service = UserService()
class FollowService:
    
    @staticmethod
    def add_new_follow( follower_id: int, followed_id: int):
        if follow_repository.exists_by_followed_id_and_follower_id(followed_id, follower_id):
            raise ValueError("follow exists")
        
        follow = Follow()
        follow.follower_id = follower_id
        follow.followed_id = followed_id

        db.session.add(follow)
        db.session.commit()

        notification_service.create_new_notification_from_type(follower_id, followed_id, type="follow")
        return user_service.generate_user_dto_by_user_id(followed_id)
        
    @staticmethod
    def delete_follow( follower_id: int, followed_id: int)->UserDTO:
        to_delete_follow: Optional[Follow] = follow_repository.find_by_followed_id_and_follower_id(followed_id, follower_id)
        if to_delete_follow:
            db.session.delete(to_delete_follow)
            notification_service.delete_notification_from_type(follower_id,followed_id,type="follow")
            return user_service.generate_user_dto_by_user_id(followed_id)
        else:
            raise ValueError("follow doesnt exist")
        