from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def verify_signature(message, signature, public_key):
    try:
        h = SHA256.new(message)
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False