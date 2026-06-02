from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64


# AES Encryption
def encrypt_message(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_CBC)

    ciphertext = cipher.encrypt(
        pad(message.encode(), AES.block_size)
    )

    return base64.b64encode(
        cipher.iv + ciphertext
    )


# AES Decryption
def decrypt_message(encrypted_message, aes_key):
    encrypted_message = base64.b64decode(encrypted_message)

    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]

    cipher = AES.new(aes_key, AES.MODE_CBC, iv)

    decrypted = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return decrypted.decode()


# RSA Key Generation
def generate_rsa_keys():
    key = RSA.generate(2048)

    private_key = key
    public_key = key.publickey()

    return private_key, public_key


# RSA Encryption
def encrypt_aes_key(aes_key, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)

    return cipher_rsa.encrypt(aes_key)


# RSA Decryption
def decrypt_aes_key(encrypted_key, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)

    return cipher_rsa.decrypt(encrypted_key)


# Digital Signature
def sign_message(message, private_key):
    h = SHA256.new(message)

    signature = pkcs1_15.new(private_key).sign(h)

    return signature


# Signature Verification
def verify_signature(message, signature, public_key):
    try:
        h = SHA256.new(message)

        pkcs1_15.new(public_key).verify(h, signature)

        return True

    except (ValueError, TypeError):
        return False