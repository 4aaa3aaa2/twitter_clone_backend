from src.twitter_clone_app import db
from .trend_entity import TrendEntity
from sqlalchemy import text
from typing import List

class TrendRepository:
    @staticmethod
    def find_top_5_by_tweet_volume():
        sql = text("SELECT * FROM trends ORDER BY tweet_volume DESC LIMIT 5")
        result = db.session.execute(sql)
        return [dict(row) for row in result.fetchall()]
     
    @staticmethod
    def find_all():
        sql = text("SELECT * FROM trends")
        result = db.session.execute(sql)
        return [dict(row) for row in result.fetchall()]