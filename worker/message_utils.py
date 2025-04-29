
import json
import uuid

def create_message(sender_id, content, message_type="generic"):
    return {
        "id": str(uuid.uuid4()),
        "sender": sender_id,
        "type": message_type,
        "payload": content
    }

def serialize_message(message):
    return json.dumps(message)

def deserialize_message(message_str):
    return json.loads(message_str)
