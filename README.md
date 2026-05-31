🔐 ChainSecureX

A multi-phase Python project building a secure, real-time communication system from the ground up — combining TCP networking, GUI development, cryptographic security, digital identity verification, persistent storage, and blockchain-based message integrity.

<br>
📌 Overview

ChainSecureX is built phase-by-phase, with each phase introducing a new layer of functionality and security on top of the previous implementation.

Starting from a basic TCP socket chat server, the project evolves into a complete cryptographic communication platform where every message is:

encrypted
authenticated
digitally signed
integrity verified
persistently stored
blockchain chained

The project combines concepts from:

Computer Networks
Cybersecurity
Applied Cryptography
Blockchain Concepts
GUI Development
Database Systems
Software Engineering

All implemented entirely in Python.

---
🎯 Purpose

ChainSecureX was created to explore how modern secure communication systems combine networking, cryptography, authentication, storage, and blockchain-inspired integrity verification into a unified architecture.

The project focuses on practical implementation of security concepts rather than theoretical demonstrations.

----
🚀 Phase-by-Phase Features

🟢 Phase 1 — TCP Networking (CLI)
Multi-client chat server using Python sockets and threading
Real-time message broadcasting
Client connection handling
Concurrent communication support

🟡 Phase 2 — GUI Interface
Built using CustomTkinter
Modern chat interface
Chat bubbles with timestamps
Improved user interaction
Better visual communication experience

🔴 Phase 3 — Encrypted Communication
AES symmetric encryption for message confidentiality
RSA asymmetric encryption for secure AES key exchange
Hybrid cryptographic communication model
End-to-end encrypted workflow
Server relays encrypted data without accessing plaintext

🟠 Phase 4 — Message Integrity
SHA-256 hashing for every transmitted message
Integrity verification mechanisms
Tamper detection system
Automatic validation of message authenticity

🟣 Phase 5 — Identity & Authentication
Username-based authentication system
RSA digital signatures
Sender identity verification
Authenticated communication workflow

🟤 Phase 6 — Persistent Storage
SQLite database integration
Encrypted chat history storage
Automatic message loading on reconnect
Persistent communication records

🔵 Phase 7 — Blockchain Layer
Blockchain-inspired message chaining
Each message linked to previous message hash
Tamper-evident audit trail
Chain integrity validation
Immutable-style communication history

----
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

  --- 
🛡️ Security Layers
Layer	Technology	Purpose

Encryption	AES-256	Confidential message transmission

Key Exchange	RSA / Diffie-Hellman	Secure AES key distribution

Integrity	SHA-256	Detect message tampering

Authentication	RSA Digital Signatures	Verify sender identity

Storage	SQLite	Persist encrypted chat history

Audit Trail	Blockchain Hash Chain	Tamper-evident message logging

---
💻 Tech Stack
Category	Technology

Language	Python 3.10

Networking	socket, threading

GUI	CustomTkinter

Cryptography	pycryptodome

Encryption	AES, RSA

Hashing	SHA-256

Database	SQLite3

Key Exchange	Diffie-Hellman

CI/CD	GitHub Actions

---
📚 Concepts Explored

Socket Programming

Concurrent Networking

Hybrid Cryptography

AES Encryption

RSA Encryption

SHA-256 Hashing

Digital Signatures

Blockchain Hash Chaining

Secure Authentication

Database Persistence

GUI Application Development

CI/CD Pipelines

Modular Software Architecture

---
📂 Project Structure
ChainSecureX/
│
├── client/
│   └── client.py
│
├── server/
│   └── server.py
│
├── utils/
│   ├── crypto.py
│   ├── protocol.py
│   ├── database.py
│   ├── diffie_hellman.py
│   └── blockchain.py
│
├── tests/
├── docs/
├── logs/
├── .github/
│
├── requirements.txt
├── README.md
└── LICENSE


▶️ Getting Started
1️⃣ Clone the Repository
git clone https://github.com/sadiyamulani03/ChainSecureX.git

cd ChainSecureX
2️⃣ Install Dependencies
pip install -r requirements.txt

Or manually:

pip install customtkinter pycryptodome
3️⃣ Start the Server
python -m server.server
4️⃣ Start Client(s)
python -m client.client

Multiple clients can connect simultaneously with secure encrypted sessions.


🔄 CI/CD Integration

This project uses GitHub Actions for Continuous Integration.

Automated workflows currently include:

Dependency installation
Multi-version Python testing
Workflow validation
Project verification
CI pipeline automation

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
-------
👨‍💻 Author

Sadiya Mulani

Built as a practical exploration of secure communication systems, applied cryptography, networking, and blockchain-inspired integrity verification using Python.
