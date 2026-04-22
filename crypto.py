from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# ---------------- RSA ---------------- #

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key


def encrypt_aes_key(aes_key, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(aes_key)


def decrypt_aes_key(encrypted_key, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_key)


# ---------------- AES ---------------- #

def encrypt_message(message: bytes, aes_key: bytes) -> bytes:
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext)


def decrypt_message(encrypted_message: bytes, aes_key: bytes) -> bytes:
    raw = base64.b64decode(encrypted_message)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)
________________________________________
