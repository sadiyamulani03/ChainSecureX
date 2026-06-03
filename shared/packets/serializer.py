import json
from shared.packets.protocol import Packet


def serialize_packet(packet: Packet):
    return packet.to_json().encode()


def deserialize_packet(data: bytes):
    packet_dict = json.loads(data.decode())

    return Packet(
        packet_type=packet_dict["packet_type"],
        sender=packet_dict["sender"],
        payload=packet_dict["payload"],
        timestamp=packet_dict["timestamp"],
        signature=packet_dict.get("signature"),
        nonce=packet_dict.get("nonce")
    )