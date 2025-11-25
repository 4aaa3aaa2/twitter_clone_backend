class NewNotification:
    sender_id: int
    receiver_id: int
    reference_id: int
    type: str
    text: str

    def __init__(self, sender_id, receiver_id, reference_id, type, text):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.reference_id = reference_id
        self.type = type
        self.text = text