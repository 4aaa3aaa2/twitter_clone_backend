from src.twitter_clone_app import db
from datetime import datetime
import math

from src.util.edge_rank_utils import EdgeRankUtils
from .feed_entry_repository import FeedEntryRepository
from .feed_entry import FeedEntry
from src.domain.like.like import Like
from src.domain.like.like_repository import LikeRepository
from .post_rank import PostRank
from src.domain.post.post import Post
from src.domain.post.post_repository import PostRepository
from src.domain.post.post_media_repository import PostMediaRepository
from src.domain.user.user import User
from src.domain.user.user_dto import UserDTO 
from src.domain.user.user_service import UserService

from typing import List, Optional

post_repository = PostRepository()
post_media_repository = PostMediaRepository()
like_repository = LikeRepository()
user_service = UserService()
feed_entry_repository = FeedEntryRepository()


class EdgeRank:

    def generate_feed(user_id: int):
        post_ranks: List[PostRank] = EdgeRank.build_and_get_new_feed(user_id)
        EdgeRank.save_feed(user_id, post_ranks)

    def build_and_get_new_feed( user_id: int)->List[PostRank]:
        user_dto: UserDTO = user_service.generate_user_dto_by_user_id(user_id)
        posts: List[Post] = post_repository.find_all_top_level_posts()
        post_ranks: List[PostRank] = EdgeRankUtils.generate_post_rank_list(posts)
        EdgeRank.compute_total_score(post_ranks, user_dto)
        post_ranks.sort(key=lambda pr: pr.total_score, reverse=True)
        return post_ranks

    def save_feed(user_id: int, feed: List[PostRank]):
        feed_entry_repository.delete_by_user_id(user_id)
        feed_entries: List[FeedEntry] = EdgeRankUtils.generate_feed_entries_list(user_id, feed)
        
        db.session.add_all(feed_entries)
        db.session.commit()

    def compute_total_score( post_ranks: List[PostRank], feed_user: UserDTO):
        for post_rank in post_ranks:
            if not EdgeRank.calculate_if_own_recent_post(post_rank, feed_user):
                EdgeRank.compute_affinity(post_rank, feed_user)
                EdgeRank.compute_weights(post_rank)
            EdgeRank.compute_time_decay_value(post_rank)
            post_rank.compute_total_score()

    def compute_time_decay_value( post_rank: PostRank):
        post_rank.time_decay += EdgeRank.compute_time_decay(post_rank.post)

    def compute_affinity( post_to_rank:PostRank, feed_user: UserDTO):
        post_ids_by_other: List[int] = post_repository.find_post_ids_by_author(post_to_rank.post.user_id)
        post_ids_by_other_set: set[int] = set(post_ids_by_other)
        post_to_rank.affinity += EdgeRank.compute_following_affinity(feed_user, post_to_rank.post.user_id)
        post_to_rank.affinity += EdgeRank.compute_has_like_affinity(feed_user, post_ids_by_other_set)
        post_to_rank.affinity += EdgeRank.compute_has_replied_affinity(feed_user, post_ids_by_other_set)


    def compute_weights( post_to_rank: PostRank):
        post_to_rank.weight += EdgeRank.compute_has_media_affinity(post_to_rank)
        post_to_rank.weight += EdgeRank.compute_like_weights(post_to_rank)

    def compute_has_media_affinity( post_to_rank: PostRank):
        if post_media_repository.find_all_by_post_id(post_to_rank.post.id)==None:
            return 0
        else:
            return 0.4

    def calculate_if_own_recent_post( post_rank: PostRank, feed_user: UserDTO)-> bool:
        is_own_recent_post: bool = (post_rank.post.user_id==feed_user.id) and ((datetime.now() - post_rank.post.created_at).total_seconds() / 3600)<=6
        if is_own_recent_post:
            post_rank.affinity += 2000 + post_rank.post.id
            post_rank.weight += 2000 + post_rank.post.id
            return True
        else:
            return False
        

    def compute_like_weights( post_to_rank: PostRank)->float:
        likes: List[Like] = like_repository.find_all_by_liked_post_id(post_to_rank.post.id)
        return  float(math.log(len(likes) + 1))

    def compute_time_decay( post: Post)->float:
        created_at: datetime = post.created_at
        hours_since =  (datetime.now() - created_at).total_seconds() / 3600.0
        return 1.0 / math.pow(hours_since + 1, 4.0)

    def compute_following_affinity( feed_user: UserDTO, post_owner_id: int)->float:
        if post_owner_id in feed_user.following:
            return 2.0
        else: 
            return 1.0

    def compute_has_like_affinity( feed_user: UserDTO, post_ids_by_other_set: set[int])-> float:
        if any(post_id in post_ids_by_other_set for post_id in feed_user.liked_posts):
            return 0.5
        else:
            return 0.0


    def compute_has_replied_affinity( feed_user: UserDTO, post_ids_by_other_set: set[int])-> float:
        if any(post_id in post_ids_by_other_set for post_id in feed_user.replies):
            return 0.5
        else: 
            return 0.0