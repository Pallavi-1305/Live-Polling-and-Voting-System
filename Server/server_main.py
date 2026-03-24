import socket
import threading
from server_config import HOST, PORT
from server_handler import handle_packet

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("Server started...")
print("Waiting for votes...\n")

lock = threading.Lock()

while True:
    data, addr = server.recvfrom(4096)

    print(f"Packet received from {addr}")   # 👈 DEBUG LINE

    t = threading.Thread(
        target=handle_packet,
        args=(server, data, addr, lock)
    )
    t.start()