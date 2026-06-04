from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64


def sign_data(data: str, private_key: bytes):
    key = RSA.import_key(private_key)

    hashed_data = SHA256.new(data.encode())

    signature = pkcs1_15.new(key).sign(
        hashed_data
    )

    return base64.b64encode(signature).decode()


def verify_signature(
    data: str,
    signature: str,
    public_key: bytes
):
    try:
        key = RSA.import_key(public_key)

        hashed_data = SHA256.new(data.encode())

        decoded_signature = base64.b64decode(
            signature
        )

        pkcs1_15.new(key).verify(
            hashed_data,
            decoded_signature
        )

        return True

    except Exception:
        return False
