import socket
import threading
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

from utils.crypto import encrypt_aes_key

HOST = '127.0.0.1'
PORT = 5051

clients = []

GLOBAL_AES_KEY = get_random_bytes(16)

def recv_fixed(conn, size):
    data = b''
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

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
        username_len = int.from_bytes(conn.recv(4), 'big')
        username = recv_fixed(conn, username_len).decode()

        key_len = int.from_bytes(conn.recv(4), 'big')
        key_data = recv_fixed(conn, key_len)

        client_pub_key = RSA.import_key(key_data)

        encrypted_aes = encrypt_aes_key(GLOBAL_AES_KEY, client_pub_key)

        conn.send(len(encrypted_aes).to_bytes(4, 'big'))
        conn.send(encrypted_aes)

        print(f"{username} authenticated")

    except Exception as e:
        print("Handshake Error:", e)
        return

    while True:
        try:
            data_len_bytes = conn.recv(4)
            if not data_len_bytes:
                break

            data_len = int.from_bytes(data_len_bytes, 'big')
            data = recv_fixed(conn, data_len)

            broadcast(data_len_bytes + data, conn)

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
