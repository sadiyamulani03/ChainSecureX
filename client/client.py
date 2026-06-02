```python
import socket
import threading
import json
import uuid
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from utils.crypto import encrypt_aes_key
from utils.logger import logger

HOST = '127.0.0.1'
PORT = 5051

clients = {}
GLOBAL_AES_KEY = get_random_bytes(16)

def recv_fixed(conn, size):
    data = b''

    while len(data) < size:
        packet = conn.recv(size - len(data))

        if not packet:
            return None

        data += packet

    return data

def broadcast_user_list():
    user_list = list(clients.keys())

    payload = json.dumps({
        "type": "users",
        "users": user_list
    }).encode()

    for username, conn in list(clients.items()):
        try:
            conn.sendall(len(payload).to_bytes(4, 'big') + payload)

        except Exception as e:
            logger.error(f"[Broadcast Error] {username}: {e}")

def handle_client(conn, addr):
    username = None

    try:
        logger.info(f"New connection from {addr}")

        # ─────────────────────────────────────────────
        # Receive username
        # ─────────────────────────────────────────────
        username_len = int.from_bytes(
            recv_fixed(conn, 4),
            'big'
        )

        username = recv_fixed(
            conn,
            username_len
        ).decode()

        logger.info(f"Username received: {username}")

        # ─────────────────────────────────────────────
        # Receive public key
        # ─────────────────────────────────────────────
        key_len = int.from_bytes(
            recv_fixed(conn, 4),
            'big'
        )

        key_data = recv_fixed(conn, key_len)

        client_pub_key = RSA.import_key(key_data)

        logger.info(f"RSA public key received from {username}")

        # ─────────────────────────────────────────────
        # Encrypt AES key with client RSA key
        # ─────────────────────────────────────────────
        encrypted_aes = encrypt_aes_key(
            GLOBAL_AES_KEY,
            client_pub_key
        )

        conn.sendall(
            len(encrypted_aes).to_bytes(4, 'big')
            + encrypted_aes
        )

        logger.info(f"AES session key sent securely to {username}")

        # ─────────────────────────────────────────────
        # Add client
        # ─────────────────────────────────────────────
        clients[username] = conn

        logger.info(f"{username} connected successfully")

        broadcast_user_list()

    except Exception as e:
        logger.error(f"[Handshake Error] {addr}: {e}")

        conn.close()
        return

    # ─────────────────────────────────────────────────
    # Main receive loop
    # ─────────────────────────────────────────────────
    while True:
        try:
            header = recv_fixed(conn, 4)

            if not header:
                logger.warning(f"{username} disconnected unexpectedly")
                break

            data_len = int.from_bytes(header, 'big')

            data = recv_fixed(conn, data_len)

            if not data:
                logger.warning(f"No data received from {username}")
                break

            logger.info(
                f"Encrypted packet received from {username} "
                f"({data_len} bytes)"
            )

            # ─────────────────────────────────────────
            # Server NEVER decrypts message
            # It only forwards encrypted payload
            # ─────────────────────────────────────────
            message_packet = json.dumps({
                "type": "chat",
                "id": str(uuid.uuid4()),
                "data": data.hex()
            }).encode()

            # ─────────────────────────────────────────
            # Broadcast to other clients
            # ─────────────────────────────────────────
            for user, client in list(clients.items()):

                if client != conn:

                    try:
                        client.sendall(
                            len(message_packet).to_bytes(4, 'big')
                            + message_packet
                        )

                        logger.info(
                            f"Forwarded encrypted packet "
                            f"from {username} to {user}"
                        )

                    except Exception as e:
                        logger.error(
                            f"[Broadcast Error] "
                            f"{username} -> {user}: {e}"
                        )

            # ─────────────────────────────────────────
            # Send seen acknowledgment
            # ─────────────────────────────────────────
            ack = json.dumps({
                "type": "seen"
            }).encode()

            conn.sendall(
                len(ack).to_bytes(4, 'big')
                + ack
            )

            logger.info(f"Seen ACK sent to {username}")

        except Exception as e:
            logger.error(f"[Receive Error] {username}: {e}")
            break

    # ─────────────────────────────────────────────────
    # Cleanup
    # ─────────────────────────────────────────────────
    if username and username in clients:

        del clients[username]

        logger.warning(f"{username} disconnected")

        broadcast_user_list()

    conn.close()

def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    server.listen()

    logger.info(f"Server started on {HOST}:{PORT}")

    print(f"Server running on {HOST}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()

            logger.info(f"Accepted connection from {addr}")

            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()

        except Exception as e:
            logger.error(f"[Server Error] {e}")

if __name__ == "__main__":
    start_server()
```
