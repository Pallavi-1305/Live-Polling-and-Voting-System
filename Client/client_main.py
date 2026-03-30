import socket
import threading
import time
import random
from client_config import SERVER_PORT, TIMEOUT
from client_crypto import encrypt_message
from client_utils import validate_client_id

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(TIMEOUT)

LOSS_PROBABILITY = 0.4   # 40% packet loss simulation
running = True

server_ip = input("Enter server IP address: ").strip()
server_address = (server_ip, SERVER_PORT)

# Handshake
client.sendto(b"HELLO", server_address)

try:
    data, _ = client.recvfrom(1024)
except socket.timeout:
    print("Server not responding.")
    client.close()
    exit()
except ConnectionResetError:
    print("Connection reset. Make sure server is running.")
    client.close()
    exit()

if data.decode() != "READY":
    print("Server not ready")
    client.close()
    exit()

print("Secure connection established")

print("\nVote for your party:")
print("1. BJP\n2. Congress\n3. JDS")

vote = input("Enter vote (1/2/3): ").strip()
client_id = input("Enter Client ID: ").strip()

# Only validate client ID here
if not validate_client_id(client_id):
    print("Invalid Client ID format")
    client.close()
    exit()

# Step 1: Notify server that one vote attempt is happening
attempt_message = f"ATTEMPT|{client_id}"
client.sendto(attempt_message.encode(), server_address)

message = client_id + "|" + vote
encrypted = encrypt_message(message)

# Start response time measurement
start_time = time.time()

# Step 2: Simulate packet loss for actual vote packet
if random.random() < LOSS_PROBABILITY:
    print("\n⚠ Simulated Packet Loss: Vote packet was dropped and NOT sent to server.")
else:
    client.sendto(encrypted, server_address)
    print("Encrypted vote sent...")

    # First receive vote response separately
    try:
        response, _ = client.recvfrom(4096)
        end_time = time.time()

        print("\n[SERVER RESPONSE]")
        print(response.decode())
        print(f"Response Time: {(end_time - start_time) * 1000:.2f} ms")

    except socket.timeout:
        print("No response from server (packet may be lost).")
    except ConnectionResetError:
        print("Connection reset while waiting for server response.")

# Function to keep receiving broadcasts AFTER vote is sent / dropped
def receive_messages():
    global running
    while running:
        try:
            response, _ = client.recvfrom(4096)
            print("\n[SERVER MESSAGE]")
            print(response.decode())
        except socket.timeout:
            continue
        except OSError:
            break
        except ConnectionResetError:
            print("\nConnection reset. Server may have stopped.")
            break
        except:
            break

receiver_thread = threading.Thread(target=receive_messages, daemon=True)
receiver_thread.start()

print("\nWaiting for periodic result broadcasts... Press Ctrl+C to exit.\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClient closed.")
    running = False
    try:
        client.close()
    except:
        pass