# 🔐 ChainSecureX – Secure Communication System

ChainSecureX is a multi-phase project that implements a **secure, real-time communication system** using networking, modern GUI, and advanced cryptographic techniques.

---

## 🚀 Features

### 🟢 Phase 1: Networking (CLI)
- TCP socket-based communication
- Multi-client chat using threading
- Real-time message broadcasting

### 🟢 Phase 2: GUI Interface
- Built using CustomTkinter
- Chat window with message bubbles
- Timestamped messages
- User-friendly interface

### 🔴 Phase 3: Secure Communication Layer
- AES encryption for message confidentiality
- RSA for secure key exchange
- Hybrid cryptography model

### 🟠 Phase 4: Integrity & Data Protection
- SHA-256 hashing for message integrity
- Tamper detection
- Ensures message authenticity

### 🟣 Phase 5: Identity & Authentication
- Username-based identity system
- RSA digital signatures for message authentication
- Verified sender identity

---

## 💻 Tech Stack

- Python
- Socket Programming
- Threading
- CustomTkinter
- AES (Symmetric Encryption)
- RSA (Asymmetric Encryption)
- SHA-256 (Hashing)

---

## 📁 Project Structure
ChainSecureX/
│── client/
│ └── client.py
│
│── server/
│ └── server.py
│
│── utils/
│ ├── crypto.py
│ ├── protocol.py
│ └── diffie_hellman.py

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

- AES ensures encrypted message transmission
- RSA secures AES key exchange
- SHA-256 ensures message integrity
- Digital signatures verify message authenticity
- Server only relays encrypted data

---

## 🧠 Cryptography Concepts Implemented

- Symmetric Encryption (AES)
- Asymmetric Encryption (RSA)
- Hashing (SHA-256)
- Digital Signatures
- Hybrid Cryptographic Model

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

Phase 4 and 5:-
1.Server and Clients
<img width="1007" height="736" alt="image" src="https://github.com/user-attachments/assets/d950fca2-2d05-46f6-8d65-b3f9845cd341" />

2.Login
<img width="770" height="647" alt="image" src="https://github.com/user-attachments/assets/8202f9f5-5df7-4479-af75-53fb00977752" />

<img width="777" height="632" alt="image" src="https://github.com/user-attachments/assets/492961ae-4efe-463d-8b63-6849b7d93d0c" />


## 🔐 Upcoming Phases
- Storage Layer(Database)
- Message Hashing & Integrity
- Blockchain-based Message Chaining
