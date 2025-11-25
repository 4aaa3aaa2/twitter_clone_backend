from .edge_rank import EdgeRank
from .feed_entry import FeedEntry
from .feed_entry_repository import FeedEntryRepository
from .post_rank import PostRank
from src.domain.post.post import Post 
from src.domain.post.post_repository import PostRepository

from src.domain.bookmark.bookmark_repository import BookmarkRepository
from src.domain.like.like_repository import LikeRepository
from src.domain.notification.notification import Notification
from src.domain.notification.notification_repository import NotificationRepository
from src.domain.user.user_repository import UserRepository
from src.domain.user.user_dto import UserDTO
from src.domain.post.post_media_repository import PostMediaRepository
from src.domain.user.user_service import UserService
from datetime import datetime,timezone
from typing import Optional, List

post_repository = PostRepository()
like_repository = LikeRepository()
bookmark_repository = BookmarkRepository()
feed_entry_repository = FeedEntryRepository()
edge_rank = EdgeRank()
user_repository = UserRepository()
user_service = UserService()
post_media_repository = PostMediaRepository()
notification_repository = NotificationRepository()


class FeedService:

    @staticmethod
    def get_paginated_post_ids(cursor: int, limit: int, user_id: int, type: str)-> dict[str:str]:
        ids: List = FeedService.get_paginated_feed(type, user_id, cursor, limit)
        print(f"Got paginated post ids: {ids} size: {len(ids)} cursor: {cursor} limit: {limit} user: {user_id} type: {type}")

        last_post_id: Optional[int] = None

        if not ids or ids == []:
            last_post_id = None
        elif type == "For You" and user_id is not None:
            # For You: cursor represents a feed position, not a timestamp
            last_post_id_int: int = ids[-1]
            feed_entry: FeedEntry = feed_entry_repository.find_by_post_id_and_user_id(last_post_id_int, user_id)
            last_post_id = int(feed_entry.position) if feed_entry else None
        else:
            # For other feeds: cursor is a timestamp or ID depending on type
            last_post_id_int: int = None if len(ids) < limit else ids[-1]
            if last_post_id_int is not None:
                if type == "Notifications" and user_id is not None:
                    notification: Optional[Notification] = notification_repository.find_by_id(last_post_id_int)
                    if notification:
                        # nextCursor is a millisecond timestamp
                        last_post_id = int(notification.created_at.timestamp() * 1000)
                    else:
                        raise ValueError("NotificationId doesn't exist")
                else:
                    post: Optional[Post] = post_repository.find_by_id(last_post_id_int)
                    if post:
                        last_post_id = int(post.created_at.timestamp() * 1000)
                    else:
                        raise ValueError("PostId doesn't exist")

        response = {
            "posts": ids,
            "nextCursor": last_post_id,
        }
        print(f"Returned: {ids} cursor: {last_post_id} limit: {limit} user: {user_id} type: {type}")
        return response
    
    @staticmethod
    def get_paginated_feed(
        self,
        feed_type: str,
        user_id: Optional[int],
        cursor: int,
        limit: int,
    ) -> List[int]:
        # Java used Timestamp(cursor). Here cursor is epoch millis; convert to aware datetime
        cursor_ts = datetime.fromtimestamp(cursor / 1000, tz=timezone.utc)

        t = feed_type.lower()
        if t == "for you":
            return FeedService.get_users_for_you_feed(user_id, cursor, limit)
        elif t == "following":
            user = user_service.generate_user_dto_by_user_id(user_id)
            return post_repository.find_paginated_post_ids_from_followed_users_by_time(user.following, cursor_ts, limit)
        elif t == "tweets":
            if user_id is None:
                raise ValueError("userId required for tweets feed")
            return post_repository.find_post_ids_by_user_and_reposts(user_id, cursor_ts, limit)
        elif t == "liked":
            if user_id is None:
                raise ValueError("userId required for liked feed")
            return like_repository.find_paginated_liked_post_ids_by_time(user_id, cursor_ts, limit)
        elif t == "replies":
            if user_id is None:
                raise ValueError("userId required for replies feed")
            return post_repository.find_paginated_reply_ids_by_user_id_by_time(user_id, cursor_ts, limit)
        elif t == "bookmarks":
            if user_id is None:
                raise ValueError("userId required for bookmarks feed")
            return bookmark_repository.find_paginated_bookmarked_post_ids_by_time(user_id, cursor_ts, limit)
        elif t == "media":
            if user_id is None:
                raise ValueError("userId required for media feed")
            return post_repository.find_paginated_post_ids_with_media_by_user_id_by_time(user_id, cursor_ts, limit)
        elif t == "notifications":
            if user_id is None:
                raise ValueError("userId required for notifications feed")
            return notification_repository.find_paginated_notification_ids_by_time(user_id, cursor_ts, limit)
        else:
            raise ValueError(f"Unknown feed type: {feed_type}")
    
    @staticmethod
    def get_users_for_you_feed(user_id: Optional[int], cursor: int, limit: int) -> List[int]:
        if user_id is None:
            print("userId required for you feed, getting generic")
            cursor_ts = datetime.fromtimestamp(cursor / 1000, tz=timezone.utc)
            return post_repository.find_next_paginated_post_ids_by_time(cursor_ts, limit)

        # If user refreshes or logs in fresh (cursor == 0), create a new feed
        ids: List[int]
        if cursor == 0:
            print(f"Creating NEW feed for user: {user_id}")
            post_ranks: List[PostRank] = edge_rank.build_and_get_new_feed(user_id)
            edge_rank.save_feed(user_id, post_ranks)
            ids = feed_entry_repository.get_feed_post_ids_custom(user_id, cursor, limit)
            print(f"New Feed Generated: {ids}")
        else:
            ids = feed_entry_repository.get_feed_post_ids_custom(user_id, cursor, limit)
            print(f"Old ids is: {ids}")
            if not ids:
                post_ranks = edge_rank.build_and_get_new_feed(user_id)
                edge_rank.save_feed(user_id, post_ranks)
                ids = feed_entry_repository.get_feed_post_ids_custom(user_id, cursor, limit)
        return ids
      
    @staticmethod
    def print_feed(feed_entries: List[FeedEntry], user_id: int) -> None:
        user = user_service.generate_user_dto_by_user_id(user_id)
        print(f"GENERATED FEED FOR USER: {user.username}")
        print("--------------------------------------------------------------")
        print(f"| {'PostId':<7} | {'UserId':<7} | {'Score':<9} | {'Position':<9} |")
        print("--------------------------------------------------------------")
        for entry in feed_entries:
            print(f"| {entry.post_id:<7d} | {entry.user_id:<7d} | {entry.score:<9.4f} | {entry.position:<9d} |")
        print("--------------------------------------------------------------")
