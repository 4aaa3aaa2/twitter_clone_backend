from src.twitter_clone_app import db
from src.domain.feed.edge_rank import EdgeRank
from src.domain.user.user import User
from src.domain.user.user_repository import UserRepository
import random
from src.constants.default_name_contents import default_name_contents
from datetime import datetime
from src.util.user_identity_utils import UserIdentityUtils
from typing import Optional, List

user_repository = UserRepository()
edge_rank = EdgeRank()


class AuthService:

    @staticmethod
    def register_temp_user()-> User:
        new_user = User()
        firstname: str = random.choice(default_name_contents.default_adjs)
        last_name: str = random.choice(default_name_contents.default_nouns)
        defalut_pfp: str = random.choice(default_name_contents.default_profile_urls)

        suffix: int = random.randint(10000,99999)
        use_name: str = f"user{suffix}"
        
        new_user.display_name = f"{firstname} {last_name}"
        new_user.username = use_name
        new_user.email = f"{use_name}@gmail.com"
        new_user.created_at = datetime.now()
        new_user.profile_picture_url = defalut_pfp
        #TODO
        new_user.banner_image_url = " NOT SET YET !!!"
        #TODO
        new_user.verified = False
        return new_user
    
    @staticmethod
    def authenicate_google_user(access_token: str)-> User:
        user_info: dict = UserIdentityUtils.parse_google_user_info(access_token)
        if user_info == None or "sub" not in user_info:
            raise ValueError("could not find user")
        
        user: Optional[User] = user_repository.find_by_google_id(user_info["sub"])

        if user:
            to_return: User = user
            return to_return
        else:
            return AuthService.create_new_google_user(user_info)
        
    @staticmethod
    def create_new_google_user( user_info: dict)->User:
        google_id: str = user_info["sub"]
        email: str = user_info["email"]
        picture_url: str = user_info["picture"]
        first_name: str = user_info["given_name"]
        last_name: str = user_info["family_name"]

        new_user = User()
        new_user.google_id = google_id

        suffix: int = random.randint(10000,99999)

        new_user.username = UserIdentityUtils.parse_google_user_name(first_name, last_name, suffix)
        new_user.display_name = UserIdentityUtils.parse_google_display_name(first_name,last_name, suffix)
        new_user.verified = False
        new_user.email = email
        new_user.created_at = datetime.now()
        new_user.profile_picture_url = picture_url
        new_user.banner_image_url = " NOT SET YET!!!  "

        db.session.add(new_user)
        db.session.commit()
        edge_rank.generate_feed(new_user.id)

        return new_user
        
    
    @staticmethod 
    def create_test_user(email: str)->User:
        new_test_user = User()
        new_test_user.email = email
        new_test_user.username = "test_user"
        new_test_user.display_name = email.split("@")[0]
        new_test_user.google_id = None
        new_test_user.profile_picture_url = None

        db.session.add(new_test_user)
        db.session.commit()

        return new_test_user




        

