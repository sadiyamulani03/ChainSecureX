from utils.crypto import (
    generate_rsa_keys,
    sign_message,
    verify_signature
)

def test_digital_signature_verification():
    private_key, public_key = generate_rsa_keys()

    message = b"Hello ChainSecureX"

    signature = sign_message(message, private_key)

    result = verify_signature(
        message,
        signature,
        public_key
    )

    assert result == True