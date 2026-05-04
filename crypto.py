from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import hashlib
import os

# ---------------- RSA ----------------
def generate_rsa_keys():
    key = RSA.generate(2048)
    return key, key.publickey()

def encrypt_aes_key(aes_key, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(aes_key)

def decrypt_aes_key(encrypted_key, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_key)

# ---------------- SIGNATURE ----------------
def sign_message(message: bytes, private_key):
    h = SHA256.new(message)
    return pkcs1_15.new(private_key).sign(h)

# ---------------- AES ENCRYPT ----------------
def encrypt_message(message, aes_key: bytes) -> bytes:
    """
    FIX: Now accepts str or bytes input, always returns bytes.
    Previously returned a str (base64), which caused:
      - socket.send(enc) → TypeError: a bytes-like object is required
      - len(enc).to_bytes() → calculated wrong length (chars vs bytes)
    """
    if isinstance(message, str):
        message = message.encode('utf-8')

    iv = os.urandom(16)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    raw = iv + ciphertext

    # Return bytes — callers (socket.send) need bytes, not str
    return base64.b64encode(raw)

# ---------------- AES DECRYPT ----------------
def decrypt_message(encrypted_message, aes_key: bytes) -> bytes:
    """
    FIX: Accepts both bytes and str input gracefully.
    Previously had a risky .decode("utf-8", errors="ignore") which could
    silently corrupt base64 data containing non-UTF8 bytes.
    """
    if isinstance(encrypted_message, bytes):
        # Try decoding as UTF-8 string first (base64 is always ASCII-safe)
        try:
            encrypted_message = encrypted_message.decode('ascii')
        except UnicodeDecodeError:
            raise ValueError("Encrypted message contains non-ASCII bytes — likely not base64")

    try:
        raw = base64.b64decode(encrypted_message)
    except Exception:
        raise ValueError("Invalid base64 encrypted data")

    if len(raw) < 16:
        raise ValueError("Invalid encrypted payload (too short)")

    iv = raw[:16]
    ciphertext = raw[16:]

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)

# ---------------- HASHING ----------------
def generate_hash(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()

def verify_hash(message: bytes, received_hash: str) -> bool:
    return generate_hash(message) == received_hash
