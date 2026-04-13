import socket
import threading
from utils.protocol import decode_message

HOST = '127.0.0.1'
PORT = 5050

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            decoded = decode_message(data)
            print(f"{decoded['user']}: {decoded['msg']}")
            
            broadcast(data, conn)
        
        except:
            break

    clients.remove(conn)
    conn.close()
    print(f"Disconnected: {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
