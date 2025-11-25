from src.domain.feed.feed_entry import FeedEntry
from src.domain.feed.post_rank import PostRank
from src.domain.post.post import Post

from typing import List

class EdgeRankUtils:
    def generate_feed_entries_list(user_id: int, feed: List[PostRank])->List[FeedEntry]:
        feed_entries: List[FeedEntry] = []
        for i in range(len(feed)):
            pr = feed[i]
            feed_entry = FeedEntry()
            feed_entry.user_id = user_id
            feed_entry.post_id = pr.post.id
            feed_entry.score = pr.total_score
            feed_entry.position = i
            feed_entries.append(feed_entry)
        return feed_entries
    
    def generate_post_rank_list(posts: List[Post])->List[PostRank]:
        post_ranks: List[PostRank] = []
        for post in posts:
            post_ranks.append(PostRank(post))
        return post_ranks