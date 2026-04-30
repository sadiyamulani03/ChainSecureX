import json
import base64

def encode_message(username, message, msg_hash, signature):
    return json.dumps({
        "user": username,
        "msg": message,
        "hash": msg_hash,
        "sig": base64.b64encode(signature).decode()
    }).encode()

def decode_message(data):
    decoded = json.loads(data.decode())
    decoded["sig"] = base64.b64decode(decoded["sig"])
    return decoded

