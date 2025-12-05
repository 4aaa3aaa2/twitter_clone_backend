from flask import Flask
from flask_cors import CORS 
import json
from src.extensions import db
from .security.jwt_auth_filter import JwtAuthMiddleware

import os
app = Flask(__name__)

jwt_middleware = JwtAuthMiddleware()
jwt_middleware.register_middleware(app)

CORS(app, origins="http://localhost:5173",supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:****@localhost:3306/***?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max request size
app.config['GCS_BUCKET'] = os.getenv("GCS_BUCKET")
app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', "your-default-jwt-secret")
app.config['X_BEARER_TOKEN'] = X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN', '')
app.config["TESTING"] = True
db.init_app(app)

with open("C:/****.apps.googleusercontent.com.json") as f:
    google_creds = json.load(f)
GOOGLE_CLIENT_ID = google_creds["web"]["client_id"]
GOOGLE_CLIENT_SECRET = google_creds["web"]["client_secret"]
#GOOGLE_REDIRECT_URI = google_creds["web"]["redirect_uris"][0]
GOOGLE_REDIRECT_URI ="http://localhost:8080/oauth2callback"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:/***.json"
from src.domain.auth.auth_controller import auth_bp
from src.domain.bookmark.bookmark_controller import bookmark_bp
from src.domain.feed.feed_controller import feed_bp
from src.domain.feedback.feedback_controller import feedback_bp
from src.domain.follow.follow_controller import follow_bp
from src.domain.like.like_controller import like_bp
from src.domain.notification.notification_controller import notification_bp
from src.domain.post.post_controller import post_bp
from src.domain.retweet.retweet_controller import retweet_bp
from src.domain.user.user_controller import user_bp
from src.trends.trend_controller import trend_bp
from src.running_test.health import health_bp

app.register_blueprint(auth_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(follow_bp)
app.register_blueprint(like_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(post_bp)
app.register_blueprint(retweet_bp)
app.register_blueprint(user_bp)
app.register_blueprint(trend_bp)
app.register_blueprint(health_bp)


if __name__ == '__main__':
    app.run(debug=True)
