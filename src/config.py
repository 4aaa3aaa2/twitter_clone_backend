import os

class Config:
    # App name (not always used directly in Flask, but you can keep it)
    APP_NAME = "twitter_clone"

    # Database / JPA related settings
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')  # You can set your MySQL DB URI here or via env var
    #SQLALCHEMY_TRACK_MODIFICATIONS = False  # Flask-SQLAlchemy equivalent to disable overhead
    
    # Hibernate settings don't have direct Flask equivalent, but you can control SQL echo:
    SQLALCHEMY_ECHO = False  # corresponds to spring.jpa.show-sql=false

    # File upload limits
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB max request size

    # GCS bucket name
    GCS_BUCKET = "twitter_clone_media"

    # JWT secrets from environment variables (recommended to keep secrets out of code)
    JWT_SECRET = os.getenv('JWT_SECRET', "your-default-jwt-secret")
    X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN', '')

    # Logging levels can be set up in your app's logging config (see below)