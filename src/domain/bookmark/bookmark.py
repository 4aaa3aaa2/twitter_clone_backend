
from datetime import datetime
from src.extensions import db


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    bookmarked_by = db.Column(db.Integer)
    bookmarked_post = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, bookmarked_by, bookmarked_post):
        self.bookmarked_by = bookmarked_by
        self.bookmarked_post = bookmarked_post

    def to_dict(self):
        """Convert model instance to dictionary (useful for JSON responses)."""
        return {
            "id": self.id,
            "bookmarked_by": self.bookmarked_by,
            "bookmarked_post": self.bookmarked_post,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Bookmark id={self.id} by={self.bookmarked_by} post={self.bookmarked_post}>"