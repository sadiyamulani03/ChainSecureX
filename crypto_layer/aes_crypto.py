from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


AES_KEY_SIZE = 32


def generate_aes_key():
    return get_random_bytes(AES_KEY_SIZE)


def encrypt_message(message: str, key: bytes):
    cipher = AES.new(key, AES.MODE_CBC)

    ciphertext = cipher.encrypt(
        pad(message.encode(), AES.block_size)
    )

    return {
        "iv": base64.b64encode(cipher.iv).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }


def decrypt_message(encrypted_data, key: bytes):
    iv = base64.b64decode(encrypted_data["iv"])

    ciphertext = base64.b64decode(
        encrypted_data["ciphertext"]
    )

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return plaintext.decode()