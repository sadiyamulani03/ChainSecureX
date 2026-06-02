from utils.blockchain import calculate_hash

def test_hash_consistency():
    hash1 = calculate_hash(
        "Sadiya",
        "Hello",
        "2026-05-30",
        "previoushash"
    )

    hash2 = calculate_hash(
        "Sadiya",
        "Hello",
        "2026-05-30",
        "previoushash"
    )

    assert hash1 == hash2


def test_tamper_detection():
    original_hash = calculate_hash(
        "Sadiya",
        "Hello",
        "2026-05-30",
        "previoushash"
    )

    tampered_hash = calculate_hash(
        "Sadiya",
        "Hacked Message",
        "2026-05-30",
        "previoushash"
    )

    assert original_hash != tampered_hash