import socket
import threading
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

from utils.crypto import encrypt_aes_key
from utils.diffie_hellman import generate_private_key, generate_public_key, generate_shared_key

HOST = '127.0.0.1'
PORT = 5051

clients = []

# Shared AES key (Hybrid crypto)
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
        # ---------------- RSA HANDSHAKE ---------------- #
        client_pub_key_data = conn.recv(4096)
        client_pub_key = RSA.import_key(client_pub_key_data)

        encrypted_aes_key = encrypt_aes_key(GLOBAL_AES_KEY, client_pub_key)
        conn.send(encrypted_aes_key)

        # ---------------- DIFFIE-HELLMAN ---------------- #
        server_private = generate_private_key()
        server_public = generate_public_key(server_private)

        # Send server public key
        conn.send(str(server_public).encode())

        # Receive client public key
        client_public = int(conn.recv(1024).decode())

        # Generate shared key
        shared_key = generate_shared_key(client_public, server_private)

        print(f"DH Shared Key (Server): {shared_key}")

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
