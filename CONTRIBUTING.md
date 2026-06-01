# Contributing to ChainSecureX

Thank you for your interest in contributing to ChainSecureX 🔐

This project focuses on secure communication systems, cryptography, networking, authentication, and blockchain-based message verification.

---

# 📌 Project Goals

ChainSecureX aims to provide:

* Secure encrypted communication
* Real-time networking
* Message integrity verification
* Blockchain-style tamper detection
* Persistent secure storage
* Modular cybersecurity architecture

---

# ⚙️ Project Setup

## 1. Clone Repository

```bash
git clone https://github.com/sadiyamulani03/ChainSecureX.git
cd ChainSecureX
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Start Server

```bash
python -m server.server
```

## Start Client

Open another terminal:

```bash
python -m client.client
```

You can launch multiple clients simultaneously.

---

# 🧪 Running Tests

Run all tests:

```bash
pytest
```

Future test coverage includes:

* AES encryption/decryption
* RSA key exchange
* SHA-256 hashing
* Blockchain integrity verification
* Authentication validation

---

# 🧹 Coding Guidelines

Please follow these practices:

* Write clean and modular Python code
* Use meaningful variable and function names
* Add comments for important logic
* Keep cryptographic functions isolated in `utils/`
* Avoid hardcoding secrets or credentials

---

# 📂 Recommended Project Structure

```plaintext
client/
server/
utils/
tests/
docs/
```

---

# 🔀 Pull Request Process

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

Example:

```bash
git checkout -b feature/add-authentication
```

---

# 🚨 Security Notes

Because this project involves cryptography and secure communication:

* Never expose private keys
* Never commit `.env` files
* Never upload production secrets
* Validate all incoming network data

---

Thank you for helping improve ChainSecureX 🚀
