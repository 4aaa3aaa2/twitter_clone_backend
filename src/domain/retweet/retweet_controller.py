
from flask import request, jsonify, Blueprint
#from src.security.jwt_service import JwtService
from src.util.get_auth_user_id import GetAuthUserId

#from src.domain.post.post import Post
from src.domain.post.post_dto import PostDTO
#from src.domain.post.post_service import PostService
#from .retweet import Retweet
from .new_retweet import NewRetweet
#from .retweet_repository import RetweetRepository
from .retweet_service import RetweetService

retweet_bp = Blueprint("retweet_bp",__name__, url_prefix="/api/retweets")


retweet_service = RetweetService()
class RetweetController:
    
    @retweet_bp.route("/create", methods=["POST"])
    def new_retweet():
        new_retweet: NewRetweet = request.get_json()
        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        try: 
            post_to_return: PostDTO = retweet_service.create_retweet(auth_user_id, new_retweet)
            return jsonify(post_to_return)
        except ValueError as e:
            return jsonify(str(e))
    
    @retweet_bp.route("/delete", methods=["POST"])
    def delete_retweet():
        new_retweet: NewRetweet = request.get_json()
        auth_user_id: int = GetAuthUserId.get_auth_user_id()
        try: 
            post_to_return: PostDTO = retweet_service.delete_retweet(auth_user_id, new_retweet)
            return jsonify(post_to_return)
        except ValueError as e:
            return jsonify(str(e))
    