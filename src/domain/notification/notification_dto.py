import datetime
from .notification import Notification

class NotificationDTO:
    def __init__(self, notification: Notification):
        self.id = notification.id
        self.sender_id = notification.sender_id
        self.receiver_id = notification.receiver_id
        self.reference_id = notification.reference_id
        self.type = notification.type
        self.text = notification.text
        self.created_at = notification.created_at
        self.seen = notification.seen
    
    