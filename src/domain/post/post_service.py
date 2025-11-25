from src.twitter_clone_app import db
from src.domain.bookmark.bookmark import Bookmark
from src.domain.bookmark.bookmark_repository import BookmarkRepository
#from src.domain.feed.edge_rank import EdgeRank
from src.domain.like.like import Like
from src.domain.like.like_repository import LikeRepository
from src.domain.notification.notification_service import NotificationService
from src.domain.post.poll.poll import Poll
from src.domain.post.poll.polls_repository import PollsRepository
from src.domain.retweet.retweet import Retweet
from src.domain.retweet.retweet_repository import RetweetRepository
from src.domain.user.user import User
from src.domain.user.user_repository import UserRepository
from .post_repository import PostRepository
from .post_media_repository import PostMediaRepository
from src.storage.cloud_storage_service import CloudStorageService
from .post_dto import PostDTO
from .post import Post
from .post_media import PostMedia

from flask import abort
from datetime import datetime
from typing import List, Optional
import uuid
from werkzeug.datastructures import FileStorage

post_repository = PostRepository()
like_repository = LikeRepository()
bookmark_repository = BookmarkRepository()
notification_service = NotificationService()
retweet_repository = RetweetRepository()
post_media_repository = PostMediaRepository()
#edge_rank = EdgeRank()
cloud_storage = CloudStorageService()
user_repository = UserRepository()
polls_repository = PollsRepository()


class PostService:
    
    @staticmethod    
    def find_post_dto_by_id( id: int)-> PostDTO:
        post: Optional[Post] = polls_repository.find_by_post_id(id)
        if post:
            post_entity: Post = post
            return PostService.create_post_dto(post_entity)
        else: 
            return None
    
    @staticmethod        
    def find_all_post_dto_by_ids( ids: List[int])-> List[PostDTO]:
        post_dtos: List[PostDTO] = []
        posts = post_repository.find_all_by_id(ids)
        for post in posts:
            post_dtos.append(PostService.create_post_dto(post))
        return post_dtos
    
    @staticmethod
    def create_post_dto( post: Post)-> PostDTO:
        liked_by: List[Like] = like_repository.find_all_by_liked_post_id(post.id)
        liked_by_ids: List[int] = []
        bookmarks: List[Bookmark] = bookmark_repository.find_all_by_bookmarked_post(post.id)
        bookmark_ids: List[int] = []
        replies: List[Post] = post_repository.find_all_by_parent_id(post.id)
        reply_ids: List[int] = []
        retweets: List[Retweet] = retweet_repository.find_all_by_reference_id(post.id)
        retweeters: List[int]  = []
        post_media: List[PostMedia] = post_media_repository.find_all_by_post_id(post.id)

        poll_id: int = None
        poll_expiry_time: datetime  = None

        if polls_repository.exits_by_post_id(post.id):
            post_poll: Optional[Poll] = polls_repository.find_by_post_id(post.id)
            if post_poll:
                poll_id = post_poll.id
                poll_expiry_time = post_poll.expired_at
            else:
                raise ValueError(f"poll with id {post.id} not found")

        for like in liked_by:
            liked_by_ids.append(like.liker_id)
        
        for bookmark in bookmarks:
            bookmark_ids.append(bookmark.id)
            
        for reply in replies:
            reply_ids.append(reply.id)
            
        for retweet in retweets:
            retweeters.append(retweet.retweeter_id)
        
        return PostDTO(post, liked_by_ids, bookmark_ids, reply_ids, retweeters, post_media, poll_id, poll_expiry_time)

    
    @staticmethod
    def find_all_posts_by_user_id( id: int)->List[int]:
        posts: Optional[List[Post]] = post_repository.find_all_by_user_id(id)
        ids = []

        if posts:
            for post in posts:
                if post.parent_id ==None:
                    ids.append(post.id)
        return ids
    
    @staticmethod
    def find_all_replies_by_user_id( id: int)-> List[int]:
        posts: Optional[List[Post]] = post_repository.find_all_by_user_id(id)
        ids: List[int] = []
        if posts:
            for post in posts:
                if post.parent_id !=None:
                    ids.append(post.id)
        return ids
    
    @staticmethod
    def create_post_entity( user_id: int, text: str, parent_id: int)-> Post:
        post = Post()
        post.user_id = user_id
        post.text = text

        if parent_id != None:
            post.parent_id = parent_id

        print("saving post by", user_id)
        db.session.add(post)
        db.session.commit()  # commits transaction and assigns ID
        return post
    
    @staticmethod
    def handle_pin_post( post_id: int, pinner_id: int, delete: bool)-> User:
        post: Optional[Post] = post_repository.find_by_id(post_id)
        if post == None:
            raise ValueError("post not found")
        retrieved_post: Post = post
        print("retriving post by id", retrieved_post.id)
        print("retriving post by user id", retrieved_post.user_id)
        if retrieved_post.user_id!=pinner_id:
            abort(403, "not post owner")
        user: User = user_repository.find_by_id(pinner_id)
        if not user: 
            abort (404, "user not found")

        if delete:
            user.pinned_post_id = None
        else:
            user.pinned_post_id = post_id
        db.session.commit()

        return user
    
    @staticmethod
    def delete_post( post_id: int, deleter_id: int):
        post: Optional[Post] = post_repository.find_by_id(post_id)
        if not post:
            raise LookupError("post not found")
        
        post_entity: Post = post
        to_delete_id: int = post_id

        print("deleting post by", post_entity.user_id)
        print("deleter id", deleter_id)
        if deleter_id != post_entity.user_id:
            raise ValueError("failed, not owner")
        notification_service.delete_all_non_follow_notifications_by_reference_id(to_delete_id)
        PostService.delete_replies(post_entity)
        db.session.delete(post_entity)
        db.session.commit()
        print("deleted post by", post_id)

    
    @staticmethod
    def delete_replies( post: Post):
        children: List[Post] = post_repository.find_all_by_parent_id(post.id)
        for child in children:
            PostService.delete_replies(child)
            notification_service.delete_all_non_follow_notifications_by_reference_id(child.id)
            db.session.delete(child)
        db.session.commit()
            
    
    @staticmethod
    def save_post_images( post_id: int, images: List[FileStorage]):
        for file in images: 
            file_name: str = f"{uuid.uuid4}_{file_name}"
            mime_type = file.mimetype
            print(f"MINE: {mime_type}, len: {file.filename}")
            url: str = cloud_storage.upload(file_name, file.stream, mime_type)
            media: PostMedia = PostMedia(post_id, file.filename, mime_type, url)
            db.session.add(media)
            db.session.commit()