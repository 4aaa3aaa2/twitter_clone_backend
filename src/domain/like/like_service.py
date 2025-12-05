from .like import Like
from .like_repository import LikeRepository
from src.domain.notification.new_notification import NewNotification
from src.domain.notification.notification_service import NotificationService
from src.domain.post.post import Post
from src.domain.post.post_dto import PostDTO
from src.domain.post.post_service import PostService
from typing import Optional, List
from src.extensions import db


like_repository = LikeRepository()
notification_service = NotificationService()
post_service = PostService()

class LikeService:
    
    @staticmethod
    def get_all_user_likes( liker_id: int)-> List[int]:
        like_ids = []
        likes: List[int] = like_repository.find_all_by_liker_id(liker_id)
        for like in likes:
            like: Like
            like_ids.append(like.post_id)
        return like_ids
    
    @staticmethod    
    def add_new_like(liker_id: int, liked_post_id: int)-> PostDTO:
        if like_repository.exists_by_liker_id_and_liked_post_id(liker_id, liked_post_id):
            raise ValueError("like exists")
        
        like = Like()
        like.post_id = liked_post_id
        like.liker_id = liker_id
        db.session.add(like)
        db.session.commit()

        notification_service.create_new_notification_from_type(liker_id, liked_post_id, "like")
        
        post_dto = post_service.find_post_dto_by_id(liked_post_id)
        if post_dto==None: 
            raise ValueError("post doesnt exist")
        return post_dto
    
    @staticmethod  
    def delete_like( liker_id: int, liked_post_id: int)-> PostDTO:
        to_delete: Optional[Like] = like_repository.find_by_liker_id_and_liked_post_id(liker_id, liked_post_id)
        if not to_delete:
            raise ValueError("like to delete not exist")
        
        db.session.delete(to_delete)
        db.session.commit()

        post_dto: PostDTO = post_service.find_post_dto_by_id(liked_post_id)
        if post_dto == None:
            raise ValueError("post not exist")
        return post_dto
