from dataclasses import dataclass
from typing import Optional
import time
import json


@dataclass
class Packet:
    packet_type: str
    sender: str
    payload: str
    timestamp: float = time.time()
    signature: Optional[str] = None
    nonce: Optional[str] = None

    def to_dict(self):
        return {
            "packet_type": self.packet_type,
            "sender": self.sender,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "nonce": self.nonce
        }

    def to_json(self):
        return json.dumps(self.to_dict())