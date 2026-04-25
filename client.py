import socket
import threading
import customtkinter as ctk
from datetime import datetime

from utils.protocol import encode_message, decode_message
from utils.crypto import (
    generate_rsa_keys,
    decrypt_aes_key,
    encrypt_message,
    decrypt_message
)
from utils.diffie_hellman import generate_private_key, generate_public_key, generate_shared_key

HOST = '127.0.0.1'
PORT = 5051


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChainSecureX Chat")
        self.root.geometry("500x600")

        self.username = input("Enter your username: ")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # ---------------- RSA ---------------- #
        self.private_key, self.public_key = generate_rsa_keys()
        self.client.send(self.public_key.export_key())

        encrypted_aes = self.client.recv(4096)
        self.aes_key = decrypt_aes_key(encrypted_aes, self.private_key)

        print("Secure connection established")

        # ---------------- DIFFIE-HELLMAN ---------------- #
        client_private = generate_private_key()
        client_public = generate_public_key(client_private)

        # Receive server public key
        server_public = int(self.client.recv(1024).decode())

        # Send client public key
        self.client.send(str(client_public).encode())

        shared_key = generate_shared_key(server_public, client_private)

        print(f"DH Shared Key (Client): {shared_key}")

        # ---------------- UI ---------------- #
        self.setup_ui()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def setup_ui(self):
        self.chat_frame = ctk.CTkScrollableFrame(self.root, width=480, height=500)
        self.chat_frame.pack(padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.root, width=350)
        self.entry.pack(side="left", padx=(10, 5), pady=10)

        self.send_button = ctk.CTkButton(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side="right", padx=(5, 10), pady=10)

    def add_message(self, message, sender="other"):
        time = datetime.now().strftime("%H:%M")

        frame = ctk.CTkFrame(self.chat_frame)
        frame.pack(anchor="e" if sender == "me" else "w", pady=5)

        label = ctk.CTkLabel(frame, text=f"{message}\n{time}")
        label.pack(padx=10, pady=5)

    def send_message(self):
        msg = self.entry.get()
        if not msg:
            return

        data = encode_message(self.username, msg)
        encrypted = encrypt_message(data, self.aes_key)

        self.client.send(encrypted)

        self.add_message(msg, "me")
        self.entry.delete(0, "end")

    def receive_messages(self):
        while True:
            try:
                encrypted = self.client.recv(4096)
                if not encrypted:
                    break

                decrypted = decrypt_message(encrypted, self.aes_key)
                decoded = decode_message(decrypted)

                if decoded["user"] != self.username:
                    self.add_message(f"{decoded['user']}: {decoded['msg']}")

            except Exception as e:
                print("Error:", e)
                break


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = ChatApp(root)
    root.mainloop()
