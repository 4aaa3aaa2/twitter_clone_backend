from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .user import User

@dataclass
class UserDTO:
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    display_name: Optional[str]
    posts: List[int]
    bookmarked_posts: List[int]
    liked_posts: List[int]
    followers: List[int]
    following: List[int]
    created_at: Optional[datetime]
    replies: List[int]
    retweets: List[int]
    profile_picture_url: Optional[str]
    banner_image_url: Optional[str]
    pinned_post_id: Optional[int]
    verified: Optional[bool]

    def __init__(self, user:User, posts, bookmarked_posts, liked_posts, followers, following, replies, retweets):
        self.id = user.id
        self.username = user.username
        self.verified = user.verified
        self.email = user.email
        self.bio = user.bio
        self.pinned_post_id = user.pinned_post_id
        self.profile_picture_url = user.profile_picture_url
        self.banner_image_url = user.banner_image_url
        self.display_name = user.display_name
        self.posts = posts
        self.bookmarked_posts = bookmarked_posts
        self.liked_posts = liked_posts
        self.followers = followers
        self.following = following
        self.created_at = user.created_at
        self.replies = replies
        self.retweets = retweets