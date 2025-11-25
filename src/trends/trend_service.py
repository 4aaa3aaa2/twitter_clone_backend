from .trend_entity import TrendEntity
from .trend_repository import TrendRepository
import os
import requests
from src.twitter_clone_app import db

trend_repository = TrendRepository()
bearer_token = os.getenv("X_BEARER_TOKEN")

class TrendService:

    def fetch_and_store_trends():
        url = "https://api.example.com/trends"  # replace with actual endpoint
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch trends: {response.status_code}")

        data = response.json()
        trends = data.get("trends", [])

        # Save to DB (you can clear old ones first if needed)
        db.session.add(trends)
        db.session.commit()