from src.twitter_clone_app import db
from src.domain.notification.notification_service import NotificationService
from src.domain.post.post_dto import PostDTO
from src.domain.post.post_service import PostService

from .retweet import Retweet
from .retweet_repository import RetweetRepository
from .new_retweet import NewRetweet

from typing import List

notification_service = NotificationService()
retweet_repository = RetweetRepository()
post_service = PostService()

class RetweetService:
    
    @staticmethod
    def get_all_retweeted_posts_by_user_id( retweeter_id: int)-> List[int]:
        retweets: List[Retweet] = retweet_repository.find_all_by_retweeter_id(retweeter_id)
        reference_ids: List[int] = []
        for retweet in retweets:
            reference_ids.append(retweet.reference_id)
        return reference_ids
    
    @staticmethod
    def create_retweet( retweeter_id: int, new_retweet: NewRetweet)->PostDTO:
        if retweet_repository.exists_by_retweeter_id_and_reference_id(retweeter_id,new_retweet.reference_id):
            raise ValueError("retweet exists")
        retweet: Retweet = Retweet()
        retweet.retweeter_id = retweeter_id
        retweet.reference_id = new_retweet.reference_id
        retweet.type = new_retweet.type
        db.session.add(retweet)
        db.session.commit()

        notification_service.create_new_notification_from_type(retweeter_id,new_retweet.reference_id, "repost")
        post_dto: PostDTO = post_service.find_post_dto_by_id(new_retweet.reference_id)
        if post_dto ==None:
            raise ValueError("post not exist")
        return post_dto
    
    @staticmethod
    def delete_retweet( retweeter_id: int, new_retweet: NewRetweet)-> PostDTO:
        to_delete: Retweet = retweet_repository.find_by_retweeter_id_and_reference_id(retweeter_id, new_retweet.reference_id)
        if to_delete:
            notification_service.delete_notification_from_type(retweeter_id,new_retweet.reference_id,"repost")
            db.session.delete(to_delete)
            db.session.commit()

            post_dto: PostDTO = post_service.find_post_dto_by_id(new_retweet.reference_id)
            if not post_dto:
                raise ValueError("post not exist")
            return post_dto
        else:
            raise LookupError("post not found")
    