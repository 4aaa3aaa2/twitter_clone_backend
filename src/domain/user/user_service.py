from src.extensions import  db
import uuid
from typing import List
from werkzeug.datastructures import FileStorage
import datetime
from sqlalchemy import func


from .user_repository import UserRepository
from src.domain.follow.follow import Follow
from src.domain.post.post_service import PostService
from src.domain.bookmark.bookmark_service import BookmarkService
from src.domain.like.like_service import LikeService
from src.domain.retweet.retweet_service import RetweetService
#from src.domain.feed.edge_rank import EdgeRank
from src.storage.cloud_storage_service import CloudStorageService
from src.domain.follow.follow_repository import FollowRepository


from src.constants.banned import BANNED


from .user import User
from .user_dto import UserDTO

user_repository = UserRepository()
post_service = PostService()
bookmark_service = BookmarkService()
like_service = LikeService()
retweet_service = RetweetService()
follow_repository = FollowRepository()
#edge_rank = EdgeRank()
cloud_storage_service = CloudStorageService()

#initialize the imported models


class UserService:
    @staticmethod
    def create_userDTO( user:User)->UserDTO:
        user_posts :List[int] = post_service.find_all_posts_by_user_id(user.id)
        user_bookmarks : List[int]  = bookmark_service.get_all_user_bookmarked_ids(user.id)
        user_likes : List[int] = like_service.get_all_user_likes(user.id)
        user_following : List[Follow]  = follow_repository.find_all_by_follower_id(user.id)
        user_following_ids = []
        for follow in user_following:
            user_following_ids.append(follow.followed_id)
        user_follower_ids : List[int] = []
        user_followers : List[Follow] = follow_repository.find_all_by_followed_id(user.id)
        for follow in user_followers:
            user_follower_ids.append(follow.follower_id)
        user_replies : List[int] = post_service.find_all_replies_by_user_id(user.id)
        user_retweets : List[int] = retweet_service.get_all_retweeted_posts_by_user_id(user.id)
        return UserDTO(user, user_posts, user_bookmarks, user_likes, user_follower_ids, user_following_ids,
                       user_replies, user_retweets)
    
    @staticmethod
    def update_user_profile( user_id:int, profile_pic:FileStorage, banner_img:FileStorage,
                             display_name:str, username:str, bio:str):
        user : User = user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("user not found")
        
        for banned in BANNED.words:
            if banned in display_name.lower() or banned in username.lower() or banned in bio.lower():
                raise ValueError("do not use banned words")
        
        if user_repository.exists_user_by_username(username):
            to_check : User = user_repository.find_by_username(username)
            if to_check.id != user_id:
                raise ValueError("user name already exists")
        
        if username != None:
            user.username = username
        
        user.display_name = display_name

        if user.bio == None or user.bio == "":
            user.bio = " "
        
        user.bio = bio

        if profile_pic and profile_pic.filename:
            file_name : str = f"{uuid.uuid4()}_{profile_pic.filename}"
            mime_type : str = profile_pic.content_type()
            url : str = cloud_storage_service.upload(file_name, profile_pic.stream, mime_type)
            user.profile_picture_url = url
        
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def generate_user_dto_by_user_id(id: int)-> UserDTO:
        user = user_repository.find_by_id(id)
        if user:
            return UserService.create_userDTO(user)
        else:
            return None
        
    @staticmethod
    def get_paginated_top_users( cursor:int, limit:int)->dict:
        cursor_timestamp : datetime = datetime.datetime.fromtimestamp(cursor/1000)
        user_ids : List[int] = UserRepository.find_user_ids_by_created_at_custom(cursor_timestamp,limit)
        next_cursor : int = None

        if user_ids and len(user_ids) == limit:
            last_user_id : int = user_ids[-1]
            last_user = user_repository.find_by_id(last_user_id)
            if last_user:
                next_cursor = int(last_user.created_at.timestamp()*1000)
            else:
                raise ValueError("user id not exists")
        
        print(f"user length is {len(user_ids)}")

        response = {"users": user_ids, "next_cursor": next_cursor}

        return response
    
    @staticmethod
    def search_users_by_name( query:str)->List[int]:
        user_list : List[User] = user_repository.search_by_username_or_display_name(query)
        user_ids : List[int] = []
        for user in user_list:
            user_ids.append(user.id)
        return user_ids
    
    @staticmethod
    def find_all_user_dto_by_ids( ids : List[int]) -> List[UserDTO]:
        users = user_repository.find_all_by_ids(ids)
        return [UserService.create_userDTO(user) for user in users]
    
    @staticmethod
    def find_by_id( id : int):
        user = user_repository.find_by_id(id)
        if user:
            return user
        else:
            return None
        
    @staticmethod    
    def generate_feed( user_id : int):
        from src.domain.feed.edge_rank import EdgeRank
        edge_rank = EdgeRank()
        edge_rank.generate_feed(user_id)
        
