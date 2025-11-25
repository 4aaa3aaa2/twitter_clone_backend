
class MessageParser:
    @staticmethod 
    def parse_message(message: str)->dict[str:str]:
        return {"message:":message}