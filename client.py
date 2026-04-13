import socket
import threading
from utils.protocol import encode_message, decode_message

HOST = '127.0.0.1'
PORT = 5050

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            data = client.recv(1024)
            if data:
                decoded = decode_message(data)
                print(f"\n{decoded['user']}: {decoded['msg']}")
        except:
            break

def send():
    while True:
        message = input()
        data = encode_message(username, message)
        client.send(data)

threading.Thread(target=receive).start()
threading.Thread(target=send).start()
