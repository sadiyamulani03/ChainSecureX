from crypto_layer.aes_crypto import (
    generate_aes_key,
    encrypt_message,
    decrypt_message
)

from crypto_layer.rsa_crypto import (
    generate_rsa_keys,
    encrypt_key,
    decrypt_key
)

from crypto_layer.signatures import (
    sign_data,
    verify_signature
)


def test_aes_encryption():
    key = generate_aes_key()
    message = "ChainSecureX"

    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)

    assert decrypted == message


def test_rsa_encryption():
    private_key, public_key = generate_rsa_keys()

    aes_key = generate_aes_key()

    encrypted = encrypt_key(aes_key, public_key)
    decrypted = decrypt_key(encrypted, private_key)

    assert decrypted == aes_key


def test_signature_verification():
    private_key, public_key = generate_rsa_keys()

    message = "Secure Packet"

    signature = sign_data(message, private_key)

    valid = verify_signature(
        message,
        signature,
        public_key
    )

    assert valid is True
