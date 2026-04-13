import json

def encode_message(username, message):
    return json.dumps({
        "user": username,
        "msg": message
    }).encode()

def decode_message(data):
    return json.loads(data.decode())
