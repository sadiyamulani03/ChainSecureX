import socket
import threading
from Crypto.Random import get_random_bytes
from utils.crypto import encrypt_aes_key

HOST = '127.0.0.1'
PORT = 5051

clients = []

# 🔐 SINGLE shared AES key
GLOBAL_AES_KEY = get_random_bytes(16)


def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)


def handle_client(conn, addr):
    print(f"Connected: {addr}")

    try:
        from Crypto.PublicKey import RSA

        # Receive public key
        client_pub_key_data = conn.recv(4096)
        client_pub_key = RSA.import_key(client_pub_key_data)

        # Encrypt SAME AES key for every client
        encrypted_aes_key = encrypt_aes_key(GLOBAL_AES_KEY, client_pub_key)

        conn.send(encrypted_aes_key)

    except Exception as e:
        print("Handshake Error:", e)
        return

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break

            broadcast(data, conn)

        except:
            break

    if conn in clients:
        clients.remove(conn)

    conn.close()
    print(f"Disconnected: {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)

        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
