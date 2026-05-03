import socket
import threading
import json
import uuid
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from utils.crypto import encrypt_aes_key

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
            conn.sendall(len(payload).to_bytes(4, 'big') + payload)
        except:
            pass

def handle_client(conn, addr):
    username = None
    try:
        # Username
        username_len = int.from_bytes(recv_fixed(conn, 4), 'big')  # FIX: use recv_fixed for header
        username = recv_fixed(conn, username_len).decode()

        # Public key
        key_len = int.from_bytes(recv_fixed(conn, 4), 'big')       # FIX: use recv_fixed for header
        key_data = recv_fixed(conn, key_len)
        client_pub_key = RSA.import_key(key_data)

        # Send AES key
        encrypted_aes = encrypt_aes_key(GLOBAL_AES_KEY, client_pub_key)
        conn.sendall(len(encrypted_aes).to_bytes(4, 'big') + encrypted_aes)  # FIX: sendall avoids partial sends

        clients[username] = conn
        print(f"{username} connected")
        broadcast_user_list()

    except Exception as e:
        print(f"[Handshake Error] {addr}: {e}")
        conn.close()
        return

    while True:
        try:
            # FIX: use recv_fixed for the 4-byte length header — conn.recv(4) can return 1-3 bytes
            header = recv_fixed(conn, 4)
            if not header:
                break

            data_len = int.from_bytes(header, 'big')
            data = recv_fixed(conn, data_len)

            if not data:
                break

            # FIX: Store data as hex so it survives JSON serialization regardless of content type.
            # This works for BOTH encrypted chat messages AND encrypted file payloads —
            # the server never needs to inspect the content, just forward it blindly.
            message_packet = json.dumps({
                "type": "chat",
                "id": str(uuid.uuid4()),
                "data": data.hex()
            }).encode()

            # Broadcast to all other clients
            for user, client in list(clients.items()):
                if client != conn:
                    try:
                        client.sendall(len(message_packet).to_bytes(4, 'big') + message_packet)
                    except Exception as e:
                        print(f"[Broadcast Error] to {user}: {e}")

            # Send seen ACK back to sender
            ack = json.dumps({"type": "seen"}).encode()
            conn.sendall(len(ack).to_bytes(4, 'big') + ack)

        except Exception as e:
            print(f"[Receive Error] {username}: {e}")
            break

    # Clean up disconnected user
    if username and username in clients:
        del clients[username]
        print(f"{username} disconnected")
        broadcast_user_list()

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # FIX: allows quick restart without "address in use" error
    server.bind((HOST, PORT))
    server.listen()
    print("Server running...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
