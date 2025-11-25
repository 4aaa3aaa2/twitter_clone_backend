
from flask import request, jsonify, Blueprint
from .feed_service import FeedService
from src.util.get_auth_user_id import GetAuthUserId

feed_bp = Blueprint("feed_bp", __name__, url_prefix="/api/feed")

feed_service = FeedService()

class FeedController:

    @feed_bp.route("/get-feed-page", methods=["GET"])
    def get_feed_page(self):
        feed_type = request.args.get('type', default='ForYou', type=str)
        cursor = request.args.get('cursor', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        user_id = request.args.get('userId', type=int)  # optional

        requires_auth: bool = feed_type.lower() in  ["bookmarks", "notifications", "foryou", "following"]
        if requires_auth:
            try: 
                user_id = GetAuthUserId.get_auth_user_id()
            except ValueError:
                return jsonify(error=f"Login required for feed type: {feed_type}"),401
        print(f"Received request for type {feed_type} cursor {cursor} limit {limit}")
        result = feed_service.get_paginated_post_ids(cursor, limit, user_id, type)
        return jsonify(result)