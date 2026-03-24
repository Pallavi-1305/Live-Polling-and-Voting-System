import socket
from client_config import SERVER_PORT, TIMEOUT
from client_crypto import encrypt_message
from client_utils import validate_client_id

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(TIMEOUT)

server_ip = input("Enter server IP address: ").strip()
server_address = (server_ip, SERVER_PORT)

# Handshake
client.sendto(b"HELLO", server_address)

try:
    data, _ = client.recvfrom(1024)
except socket.timeout:
    print("Server not responding.")
    exit()

if data.decode() != "READY":
    print("Server not ready")
    exit()

print("Secure connection established")

print("\nVote for your party:")
print("1. BJP\n2. Congress\n3. JDS")

vote = input("Enter vote (1/2/3): ").strip()
client_id = input("Enter Client ID: ").strip()

# ❗ Only validate client ID (NOT vote)
if not validate_client_id(client_id):
    print("Invalid Client ID")
    exit()

# ✅ Always send vote (even if invalid)
message = client_id + "|" + vote
encrypted = encrypt_message(message)

client.sendto(encrypted, server_address)
print("Encrypted vote sent...")

try:
    response, _ = client.recvfrom(4096)
    print(response.decode())
except socket.timeout:
    print("No response from server")

client.close()