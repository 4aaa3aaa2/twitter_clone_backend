from src.domain.post.poll.poll import Poll
from datetime import datetime,timedelta
from typing import List

class POllUtils:
    @staticmethod
    def check_poll_expiry(poll: Poll)->bool:
        return poll.expired_at<= datetime.now()
    
    @staticmethod
    def parse_poll_expiry_to_timestamp(poll_expiry: List[str]) -> datetime:
        """
        Convert [days, hours, minutes] into a datetime expiration.
        Equivalent to Java's LocalDateTime.now().plusDays(...).plusHours(...).plusMinutes(...).
        """
        days = int(poll_expiry[0])
        hours = int(poll_expiry[1])
        minutes = int(poll_expiry[2])

        expiration = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
        return expiration