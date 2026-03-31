#  UDP-Based Live Polling and Voting System

##  Overview
This project is a **real-time voting system** implemented using **UDP socket programming in Python**.  
It supports multiple clients and demonstrates key networking concepts such as:

- unreliable communication (UDP)
- packet loss analysis
- retransmission mechanisms
- secure communication using encryption

The system enables clients to cast votes, while the server processes them and broadcasts live results.

---

## Key Features

### 🔹 Networking
- UDP-based client-server communication
- Custom communication protocol (`HELLO`, `ATTEMPT`, etc.)
- Multi-client handling using threading

### 🔹 Reliability & Analysis
- Statistical packet loss analysis
- Simulated packet loss for testing
- Automatic retransmission of lost packets
- Separate tracking of:
  - initial packet loss
  - recovered transmissions

### 🔹 Functionality
- Live vote counting
- Duplicate vote detection
- Invalid input handling
- Periodic broadcasting of results

### 🔹 Security
- Application-layer encryption using **Fernet (symmetric encryption)**

### 🔹 Performance
- Response time measurement
- Multi-client interaction testing

---

## Technologies Used
- **Python**
- **Socket Programming (UDP)**
- **Threading**
- **Cryptography (Fernet)**

---

##  Project Structure

```text
UDP-Voting-System/
│
├── client/
│   ├── client_config.py
│   ├── client_crypto.py
│   ├── client_utils.py
│   └── client_main.py
│
├── server/
│   ├── server_config.py
│   ├── server_crypto.py
│   ├── server_handler.py
│   └── server_main.py
│
└── README.md