REQUIRED_FIELDS = [
    "packet_type",
    "sender",
    "payload",
    "timestamp"
]


def validate_packet(packet_dict):
    for field in REQUIRED_FIELDS:
        if field not in packet_dict:
            return False

    return True