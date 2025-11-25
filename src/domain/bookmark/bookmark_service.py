from src.twitter_clone_app import db
import uuid
from typing import List
from .bookmark import Bookmark
from .bookmark_repository import BookmarkRepository
from src.domain.post.post_dto import PostDTO
from src.domain.post.post_service import PostService

post_service = PostService()
bookmark_repository = BookmarkRepository()

class BookmarkService:        
    
    @staticmethod
    def get_all_user_bookmarked_ids(user_id: int)-> List[int]:
        bookmark_ids: List[int] = []
        bookmarks: List[Bookmark] = bookmark_repository.find_all_by_bookmarked_by(user_id)
        for bookmark in bookmarks:
            bookmark_ids.append(bookmark.id)
        return bookmark_ids
    
    @staticmethod
    def add_new_bookmark(user_id: int, bookmarked_post: int)->PostDTO:
        if bookmark_repository.exists_by_bookmarked_by_and_bookmarked_post(user_id, bookmarked_post):
            raise ValueError('bookmark exists')
        bookmark: Bookmark = Bookmark()
        bookmark.bookmarked_by = user_id
        bookmark.bookmarked_post = bookmarked_post
        
        db.session.add(bookmark)
        db.session.commit()

        post_dto: PostDTO = post_service.find_post_dto_by_id(bookmarked_post)
        if post_dto is None:
            raise ValueError("post doesnt exist")
        return post_dto
        
    @staticmethod
    def delete_bookmark( user_id: int, bookmarked_post: int)-> PostDTO:
        to_delete = bookmark_repository.exists_by_bookmarked_by_and_bookmarked_post(user_id, bookmarked_post)
        if not to_delete:
            raise ValueError("bookmark not exist")
        
        db.session.delete(to_delete)
        db.session.commit()

        post_dto: PostDTO = post_service.find_post_dto_by_id(bookmarked_post)
        if not post_dto or post_dto is None:
            raise ValueError("post does not exist")
        return post_dto