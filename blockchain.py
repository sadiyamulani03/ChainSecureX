import hashlib

def calculate_hash(username, message, timestamp, prev_hash):
    data = f"{username}{message}{timestamp}{prev_hash}".encode()
    return hashlib.sha256(data).hexdigest()