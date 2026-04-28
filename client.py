import socket
import threading
import customtkinter as ctk
from datetime import datetime

from utils.protocol import encode_message, decode_message
from utils.crypto import (
    generate_rsa_keys,
    decrypt_aes_key,
    encrypt_message,
    decrypt_message,
    generate_hash,
    verify_hash,
    sign_message
)
from utils.database import init_db, save_message, load_messages

HOST = '127.0.0.1'
PORT = 5051


def recv_fixed(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChainSecureX Chat")
        self.root.geometry("500x600")

        self.username = input("Enter username: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        self.private_key, self.public_key = generate_rsa_keys()

        # Send username
        username_bytes = self.username.encode()
        self.client.send(len(username_bytes).to_bytes(4, 'big'))
        self.client.send(username_bytes)

        # Send public key
        key_bytes = self.public_key.export_key()
        self.client.send(len(key_bytes).to_bytes(4, 'big'))
        self.client.send(key_bytes)

        # Receive AES key
        aes_len = int.from_bytes(self.client.recv(4), 'big')
        encrypted_aes = recv_fixed(self.client, aes_len)

        self.aes_key = decrypt_aes_key(encrypted_aes, self.private_key)

        print("Secure connection established")

        # Database init
        init_db()

        self.setup_ui()
        self.load_old_messages()

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def setup_ui(self):
        self.chat_frame = ctk.CTkScrollableFrame(self.root, width=480, height=500)
        self.chat_frame.pack(padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.root, width=350)
        self.entry.pack(side="left", padx=(10, 5), pady=10)

        self.send_button = ctk.CTkButton(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=(5, 10), pady=10)

    def load_old_messages(self):
        messages = load_messages()

        for user, msg, time in messages:
            self.add_message(f"{user}: {msg}", time)

    def add_message(self, message, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M")

        frame = ctk.CTkFrame(self.chat_frame)
        frame.pack(anchor="w", pady=5)

        label = ctk.CTkLabel(frame, text=f"{message}\n{timestamp}")
        label.pack(padx=10, pady=5)

    def send_message(self):
        msg = self.entry.get()
        if not msg:
            return

        msg_bytes = msg.encode()
        msg_hash = generate_hash(msg_bytes)
        signature = sign_message(msg_bytes, self.private_key)

        data = encode_message(self.username, msg, msg_hash, signature)
        encrypted = encrypt_message(data, self.aes_key)

        self.client.send(len(encrypted).to_bytes(4, 'big'))
        self.client.send(encrypted)

        timestamp = datetime.now().strftime("%H:%M")

        save_message(self.username, msg, timestamp)

        self.add_message(f"You: {msg}", timestamp)
        self.entry.delete(0, "end")

    def receive_messages(self):
        while True:
            try:
                data_len_bytes = self.client.recv(4)
                if not data_len_bytes:
                    break

                data_len = int.from_bytes(data_len_bytes, 'big')
                encrypted = recv_fixed(self.client, data_len)

                decrypted = decrypt_message(encrypted, self.aes_key)
                decoded = decode_message(decrypted)

                msg = decoded["msg"]
                sender = decoded["user"]

                if verify_hash(msg.encode(), decoded["hash"]):
                    display_msg = f"{sender}: {msg}"
                else:
                    display_msg = "Message tampered"

                timestamp = datetime.now().strftime("%H:%M")

                save_message(sender, msg, timestamp)

                self.add_message(display_msg, timestamp)

            except Exception as e:
                print("Error:", e)
                break


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = ChatApp(root)
    root.mainloop()
