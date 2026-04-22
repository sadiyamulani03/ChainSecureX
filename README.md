# 🔐 ChainSecureX – Secure Communication System

ChainSecureX is a multi-phase project focused on building a **secure and user-friendly communication system** using networking, modern UI, and advanced cryptography.

---

## 🚀 Features Implemented:-

### 🔹 Phase 1: Multi-Client Chat System (CLI)
- TCP socket-based communication
- Multi-client support using threading
- Real-time message broadcasting

### 🔹 Phase 2: Modern GUI Interface
- Built using CustomTkinter
- Scrollable chat window
- Message bubbles
- Timestamped messages
- Interactive input field

### 🔹 Phase 3: Secure Communication Layer (Hybrid Cryptography)
- AES-based message encryption
- RSA-based secure key exchange
- Hybrid encryption model (AES + RSA)
- End-to-end encrypted communication

---

## 💻 Tech Stack
- Python
- Socket Programming
- Threading
- CustomTkinter (GUI)
- AES Encryption (PyCryptodome)
- RSA Cryptography

---

## 📁 Project Structure

ChainSecureX/
│── server/
│   └── server.py
│
│── client/
│   └── client.py
│
│── utils/
│   ├── protocol.py
│   └── crypto.py

---

## ▶️ How to Run

### 1. Install dependencies
pip install customtkinter pycryptodome

### 2. Start server
python -m server.server

### 3. Start client(s)
python -m client.client

---

## 🔐 Security Overview
- AES is used for fast message encryption
- RSA is used for secure AES key exchange
- Messages are encrypted end-to-end
- Server only relays encrypted data

---
## 📸Demo

Phase 1:-
1. Server
<img width="1043" height="722" alt="image" src="https://github.com/user-attachments/assets/0ffdf400-0a7b-4feb-a703-cfd27b7b09ec" />

2.Client1
<img width="1041" height="453" alt="image" src="https://github.com/user-attachments/assets/0d62fc46-8dc4-4d43-b416-8a519f4d162b" />

3.Client2
<img width="950" height="545" alt="image" src="https://github.com/user-attachments/assets/28154cd1-ca90-4c54-95d5-914af7440821" />

Phase 2:-
1. Server
   <img width="935" height="563" alt="image" src="https://github.com/user-attachments/assets/3bed5169-4d14-4ab2-baa6-291fe41af0d7" />

2. Clients
   <img width="1911" height="995" alt="Screenshot 2026-04-11 214201" src="https://github.com/user-attachments/assets/2d409930-e770-4dd4-ba7d-43faa927043b" />

Phase 3:-
<img width="992" height="705" alt="image" src="https://github.com/user-attachments/assets/6e13c502-1060-4a9e-8e2c-c3f11e1c3418" />


## 🔐 Upcoming Phases
- Diffie-Hellman Secure Key Generation
- Message Hashing & Integrity
- Authentication System
- Blockchain-based Message Chaining
