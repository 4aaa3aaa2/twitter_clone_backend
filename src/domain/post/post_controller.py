
from flask import request, jsonify, Blueprint
from src.security.jwt_service import JwtService
from src.util.get_auth_user_id import GetAuthUserId

from .post import Post
from .post_dto import PostDTO
from .post_repository import PostRepository
from .post_service import PostService
from .poll.poll_service import PollService
from src.domain.user.user import User
from src.domain.user.user_dto import UserDTO
from src.domain.user.user_service import UserService
from src.domain.notification.notification_service import NotificationService

post_bp = Blueprint("post_bp", __name__, url_prefix="/api/posts")


post_service = PostService()
notification_service = NotificationService()
post_repository = PostRepository()
user_service = UserService()
poll_service = PollService()

class PostController:
    
    @post_bp.route("/get-posts", methods=["POST"])
    @staticmethod
    def get_post():
        ids = request.get_json()
        print("received request to retrieve posts")

        result = post_service.find_all_post_dto_by_ids(ids)
        return jsonify(result)
    
    @post_bp.route("/get-post/<int:post_id>",methods=["GET"])
    @staticmethod
    def get_single_post(post_id):
        result = post_service.find_post_dto_by_id(post_id)
        return jsonify(result)
    
    @post_bp.route("/delete", methods=["POST"])
    @staticmethod
    def delete_post():
        post_id = request.get_json()
        auth_user_id = GetAuthUserId.get_auth_user_id()
        print("reveived request to delete post")
        print(auth_user_id)
        post_service.delete_post(post_id,auth_user_id)
        return jsonify(success=True)
    

    @post_bp.route("/pin",methods=["POST"])
    @staticmethod
    def pin_post():
        post_id = request.args.get("post_id", type = int)
        auth_user_id = GetAuthUserId.get_auth_user_id()
        print(f"jwt user id {auth_user_id}")
        print(f"post id {post_id}")
        to_return: User = post_service.handle_pin_post(post_id, auth_user_id, delete=False)
        user_to_return: UserDTO = user_service.generate_user_dto_by_user_id(to_return.id)
        return jsonify(user_to_return)
    
    @post_bp.route("/unpin", methods=["POST"])
    @staticmethod
    def unpin_post():
        post_id = request.args.get("post_id", type = int)
        auth_user_id = GetAuthUserId.get_auth_user_id()
        print(f"jwt user id {auth_user_id}")
        print(f"post id {post_id}")

        to_return: User = post_service.handle_pin_post(post_id, auth_user_id, delete=True)
        user_to_return: UserDTO = user_service.generate_user_dto_by_user_id(to_return.id)
        return jsonify(user_to_return)
    
    @post_bp.route("/create", methods=["POST"])
    @staticmethod
    def create_post():
        text = request.form.get("text", type = str)
        parent_id = request.form.get("parent_id", type = int)
        images = request.files.get("images", type = list)
        poll_choices = request.form.get("poll_choices",type = int)
        poll_expiry = request.form.get("poll_expiry", type = int)
        auth_user_id = GetAuthUserId.get_auth_user_id()
    
        post: Post = post_service.create_post_entity(auth_user_id, text, parent_id)

        if len(text)<1 and images == None:
            raise ValueError("text or images are madatory")
        
        if poll_choices != None and parent_id == None and poll_expiry != None:
            poll_service.create_new_poll_for_post(post.id, poll_choices, poll_expiry)
        
        if images != None:
            post_service.save_post_images(post.id, images)

        if parent_id != None:
            notification_service.create_new_notification_from_type(auth_user_id, post.id, type="reply")
        
        to_return: PostDTO = post_service.find_post_dto_by_id(post.id)
        return jsonify(to_return)    



