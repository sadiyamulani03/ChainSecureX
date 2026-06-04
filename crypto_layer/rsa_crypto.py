from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


KEY_SIZE = 2048


def generate_rsa_keys():
    key = RSA.generate(KEY_SIZE)

    private_key = key.export_key()

    public_key = key.publickey().export_key()

    return private_key, public_key


def encrypt_key(aes_key: bytes, public_key: bytes):
    rsa_key = RSA.import_key(public_key)

    cipher = PKCS1_OAEP.new(rsa_key)

    encrypted_key = cipher.encrypt(aes_key)

    return base64.b64encode(encrypted_key).decode()


def decrypt_key(encrypted_key: str, private_key: bytes):
    rsa_key = RSA.import_key(private_key)

    cipher = PKCS1_OAEP.new(rsa_key)

    decrypted_key = cipher.decrypt(
        base64.b64decode(encrypted_key)
    )

    return decrypted_key