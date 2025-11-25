from src.twitter_clone_app import db
from typing import List
from .post_media import PostMedia

class PostMediaRepository:
    @staticmethod 
    def find_all_by_post_id(post_id: int)->List[PostMedia]:
        return db.session.query(PostMedia).filter(PostMedia.post_id == post_id).all()