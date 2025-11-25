from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .post import Post
from .post_media import PostMedia

@dataclass
class PostDTO:
    id: int
    user_id: int
    text: str
    created_at: datetime
    liked_by: List[int]
    bookmarked_by: List[int]
    replies: List[int]
    parent_id: int
    retweeted_by: List[int]
    post_media: List[PostMedia]
    poll_id: int
    poll_expiry_time_stamp: datetime

    def __init__(self, post: Post, liked_by, bookmarked_by, replies,
                 retweeted_by, post_media, poll_id, poll_expiry_time_stamp):
        self.id = post.id
        self.user_id = post.user_id
        self.text = post.text
        self.liked_by = liked_by
        self.bookmarked_by = bookmarked_by
        self.created_at = post.created_at
        self.parent_id = post.parent_id
        self.replies = replies
        self.retweeted_by = retweeted_by
        self.post_media = post_media
        self.poll_id = poll_id
        self.poll_expiry_time_stamp = poll_expiry_time_stamp

        