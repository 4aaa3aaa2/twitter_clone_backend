from datetime import datetime
from src.extensions import db

class PostMedia(db.Model):
    __tablename__ = "post_media"
    
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id: int = db.Column(db.Integer, nullable = False)
    file_name: str = db.Column(db.String(255), nullable = False)
    mime_type: str = db.Column(db.String(100), nullable = False)
    url: str = db.Column(db.String(512), nullable = False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self,post_id: int, file_name: str, mime_type: str, url: str):
        self.post_id = post_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.url = url
    
    def __repr__(self):
        return f"<post id={self.post_id}, file name={self.file_name},url={self.url}>"