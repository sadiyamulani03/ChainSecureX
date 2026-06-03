from shared.packets.protocol import Packet
from shared.packets.serializer import (
    serialize_packet,
    deserialize_packet
)


def test_packet_serialization():
    packet = Packet(
        packet_type="message",
        sender="Alice",
        payload="Hello"
    )

    serialized = serialize_packet(packet)
    deserialized = deserialize_packet(serialized)

    assert deserialized.sender == "Alice"
    assert deserialized.payload == "Hello"