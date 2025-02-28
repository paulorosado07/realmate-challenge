from datetime import datetime
import pytz
import uuid
from urllib.parse import urlparse

def generate_timestamp():
    timezone = pytz.timezone("America/Sao_Paulo")
    timestamp = datetime.now(timezone).isoformat()
    return timestamp

def generate_conversation_id():
    unique_id = str(uuid.uuid4())
    return unique_id


def generate_new_message(direction_message, content, conversation_id):
    timestamp = generate_timestamp()
    message_id = generate_conversation_id()


    new_message = {
        "type": "NEW_MESSAGE",
        "timestamp": timestamp,
        "data": {
            "id": message_id,
            "direction": direction_message,
            "content": content,
            "conversation_id": conversation_id
        }
    }


    return new_message


def get_base_url(url):
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return domain