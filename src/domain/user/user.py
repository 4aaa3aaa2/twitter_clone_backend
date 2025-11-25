
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from src.twitter_clone_app import db

class User(db.Model):
    __tablename__ = "users"
        
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(400))
    google_id = db.Column(db.String, unique=True)
    email = db.Column(db.String(45), nullable=False, unique=True)
    display_name = db.Column(db.String(45), nullable=False)
    profile_picture_url = db.Column(db.String)
    banner_image_url = db.Column(db.String)
    verified = db.Column(db.Boolean)
    bio = db.Column(db.String(180))
    created_at = db.Column(db.DateTime, default=datetime.now)
    pinned_post_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "profile_picture_url": self.profile_picture_url,
            "banner_image_url": self.banner_image_url,
            "verified": self.verified,
            "bio": self.bio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "pinned_post_id": self.pinned_post_id,
            "google_id": self.google_id,
        }

    


 