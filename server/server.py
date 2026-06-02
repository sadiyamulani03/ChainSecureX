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

    for conn in clients.values():
        try:
            conn.sendall(
                len(payload).to_bytes(4, 'big') + payload
            )

        except Exception as e:
            logger.error(f"User list broadcast error: {e}")


def handle_client(conn, addr):

    username = None

    try:
        # Receive username
        username_len = int.from_bytes(
            recv_fixed(conn, 4),
            'big'
        )

        username = recv_fixed(
            conn,
            username_len
        ).decode()

        # Receive public key
        key_len = int.from_bytes(
            recv_fixed(conn, 4),
            'big'
        )

        key_data = recv_fixed(conn, key_len)

        client_pub_key = RSA.import_key(key_data)

        # Encrypt and send AES key
        encrypted_aes = encrypt_aes_key(
            GLOBAL_AES_KEY,
            client_pub_key
        )

        conn.sendall(
            len(encrypted_aes).to_bytes(4, 'big') +
            encrypted_aes
        )

        # Store client
        clients[username] = conn

        print(f"{username} connected")

        logger.info(
            f"Client connected: {username} | {addr}"
        )

        broadcast_user_list()

    except Exception as e:

        print(f"[Handshake Error] {addr}: {e}")

        logger.error(
            f"Handshake error from {addr}: {e}"
        )

        conn.close()
        return

    while True:

        try:
            # Receive header safely
            header = recv_fixed(conn, 4)

            if not header:
                break

            data_len = int.from_bytes(header, 'big')

            data = recv_fixed(conn, data_len)

            if not data:
                break

            logger.info(
                f"Encrypted message received from {username}"
            )

            # Wrap encrypted data
            message_packet = json.dumps({
                "type": "chat",
                "id": str(uuid.uuid4()),
                "data": data.hex()
            }).encode()

            # Broadcast to other clients
            for user, client in list(clients.items()):

                if client != conn:

                    try:
                        client.sendall(
                            len(message_packet).to_bytes(4, 'big') +
                            message_packet
                        )

                    except Exception as e:

                        print(f"[Broadcast Error] to {user}: {e}")

                        logger.error(
                            f"Broadcast error to {user}: {e}"
                        )

            # Send seen ACK
            ack = json.dumps({
                "type": "seen"
            }).encode()

            conn.sendall(
                len(ack).to_bytes(4, 'big') + ack
            )

        except Exception as e:

            print(f"[Receive Error] {username}: {e}")

            logger.error(
                f"Receive error from {username}: {e}"
            )

            break

    # Disconnect cleanup
    if username and username in clients:

        del clients[username]

        print(f"{username} disconnected")

        logger.info(
            f"Client disconnected: {username}"
        )

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

    print("Server running...")

    logger.info("Server started")

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()


    if __name__ == "__main__":
        start_server()