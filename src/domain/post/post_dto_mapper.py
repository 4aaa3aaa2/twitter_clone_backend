from src.domain.bookmark.bookmark import Bookmark
from src.domain.bookmark.bookmark_repository import BookmarkRepository
from src.domain.like.like import Like
from src.domain.like.like_repository import LikeRepository
from src.domain.post.poll.poll import Poll
from src.domain.post.poll.polls_repository import PollsRepository
from src.domain.retweet.retweet import Retweet
from src.domain.retweet.retweet_repository import RetweetRepository
from .post import Post
from .post_repository import PostRepository
from .post_media_repository import PostMediaRepository
from .post_dto import PostDTO
from .post_media import PostMedia

from typing import Optional, List

like_repository = LikeRepository()
bookmark_repository = BookmarkRepository()
post_repository = PostRepository()
retweet_repository = RetweetRepository()
post_media_repository = PostMediaRepository()
polls_repository = PollsRepository()

class PostDTOMapper:

    def from_post_id( id: int)->PostDTO:
        found_post: PostDTO = post_repository.find_by_id(id)
        if not found_post:
            raise LookupError()
        return PostDTOMapper.from_post(found_post)
    
    def from_post(post: Post)->PostDTO:
        liked_by_ids: List[int] = [like.liker_id for like in like_repository.find_all_by_liked_post_id(post.id)]
        bookmark_ids: List[int]  =[bookmark.bookmarked_by for bookmark in bookmark_repository.find_all_by_bookmarked_post(post.id)]
        reply_ids: List[int] = [post.id for post in post_repository.find_all_by_parent_id(post.id)]
        retweeters: List[int] = [retweet.retweeter_id for retweet in retweet_repository.find_all_by_reference_id(post.id)]
        post_media: List[PostMedia] = post_media_repository.find_all_by_post_id(post.id)

        poll_id: int = None
        poll_expiry: int = None

        if polls_repository.exits_by_post_id(post.id):
            poll: Optional[Poll] = polls_repository.find_by_post_id(post.id)
            if poll:
                poll_id = poll.id
                poll_expiry = poll.expired_at
            else:
                raise  LookupError(f"poll with id {post.id} not found")
            
        return PostDTO(post,liked_by_ids,bookmark_ids,reply_ids,retweeters,post_media,poll_id, poll_expiry)



        