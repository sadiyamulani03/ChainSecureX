🔐 ChainSecureX

A multi-phase Python project building a secure, real-time chat system from the ground up — layering TCP networking, an encrypted GUI, cryptographic security, digital identity, persistent storage, and a blockchain-verified message chain.

📌 Overview
ChainSecureX is built phase-by-phase, with each phase adding a new security or feature layer on top of the last. Starting from a basic TCP chat server, the project evolves into a full cryptographic communication system where every message is encrypted, authenticated, signed, stored, and recorded on a tamper-evident blockchain chain.
This project covers concepts from networking, applied cryptography, GUI development, and blockchain — built entirely in Python.

🚀 Phase-by-Phase Features

🟢 Phase 1 — TCP Networking (CLI)

Multi-client chat server using Python sockets and threading
Real-time message broadcasting to all connected clients

🟡 Phase 2 — GUI Interface

Built with CustomTkinter
Chat bubbles with timestamps and a clean user-friendly layout

🔴 Phase 3 — Encrypted Communication

AES (symmetric) for fast message encryption
RSA (asymmetric) for secure AES key exchange
Hybrid cryptography model — server never sees plaintext

🟠 Phase 4 — Message Integrity

SHA-256 hashing on every message
Tamper detection — altered messages are flagged automatically

🟣 Phase 5 — Identity & Authentication

Username-based login system
RSA digital signatures to verify sender identity on every message

🟤 Phase 6 — Persistent Storage

SQLite database integration
Chat history is saved and automatically loaded on reconnect

🔵 Phase 7 — Blockchain Layer

Every message is hashed and linked to the previous message's hash
Creates a tamper-evident chain — any modification breaks the chain
Full blockchain-style integrity verification for chat history


🔐 Security Architecture
Client A                        Server                        Client B
   │                               │                               │
   │──── RSA Key Exchange ────────>│<──── RSA Key Exchange ───────│
   │                               │                               │
   │──── AES-Encrypted Message ───>│──── AES-Encrypted Message ──>│
   │      + SHA-256 Hash           │      (server never decrypts)  │
   │      + RSA Digital Signature  │                               │
   │                               │                               │
   └── Blockchain records each message with hash linkage ──────────┘
LayerTechnologyPurposeEncryptionAES-256Confidential message transmissionKey ExchangeRSA / Diffie-HellmanSecure AES key distributionIntegritySHA-256Detect message tamperingAuthenticationRSA Digital SignaturesVerify sender identityStorageSQLitePersist encrypted chat historyAudit TrailBlockchain (SHA-256 chain)Tamper-evident message log

💻 Tech Stack
Language: Python 3.10, Networkingsocket ,threading

GUI custom tkinter

Cryptography pycryptodome (AES, RSA, SHA-256)

Database sqlite3

Key Exchange Diffie-Hellman


▶️ Getting Started
1. Clone the repo
bashgit clone https://github.com/sadiyamulani03/ChainSecureX.git
cd ChainSecureX
2. Install dependencies
bashpip install customtkinter pycryptodome
3. Start the server
bashpython server.py
4. Launch client(s) — open in separate terminals
bashpython client.py
Multiple clients can connect simultaneously. Each gets a unique identity and encrypted session.# 🔐 ChainSecureX – Secure Communication System

ChainSecureX is a multi-phase project that implements a **secure, real-time communication system** using networking, modern GUI, and advanced cryptographic techniques.

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
│ ├── database.py
| ├── diffie_hellman.py
│ └── blockchain.py

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
- SQLite ensures persistent storage

---

## 🧠 Cryptography Concepts Implemented

- Symmetric Encryption (AES)
- Asymmetric Encryption (RSA)
- Hashing (SHA-256)
- Digital Signatures
- Hybrid Cryptographic Model
- Database Persistence

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

Phase 6:-
1. Before Database
   <img width="956" height="510" alt="image" src="https://github.com/user-attachments/assets/fcbc23d6-23c1-4211-a472-713e63e9d824" />

2. After Database
   <img width="978" height="518" alt="image" src="https://github.com/user-attachments/assets/eebcea14-7cc1-4fce-aa30-7d2380283b23" />
 
Phase 7:-
   <img width="936" height="1138" alt="image" src="https://github.com/user-attachments/assets/b051713a-39cd-4276-8638-bf35deb2bef2" />

Phase 8:-
   <img width="936" height="1138" alt="image" src="https://github.com/user-attachments/assets/1331aafe-a06b-45ca-9702-b34430e47a4e" />
