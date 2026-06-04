import secrets


def generate_nonce(length=16):
    return secrets.token_hex(length)