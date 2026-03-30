import socket
import threading
import time
from server_config import HOST, PORT
from server_handler import handle_packet, votes, known_clients, stats

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print("Server started...")
print("Waiting for votes...\n")

lock = threading.Lock()

# Periodic result broadcasting
def broadcast_results():
    while True:
        time.sleep(10)

        with lock:
            result_message = (
                f"BROADCAST RESULTS\n"
                f"BJP: {votes['BJP']}\n"
                f"Congress: {votes['Congress']}\n"
                f"JDS: {votes['JDS']}\n"
            )

        print("\n[Broadcasting Results to Clients]")
        print(result_message)

        for client_addr in list(known_clients):
            try:
                server.sendto(result_message.encode(), client_addr)
            except:
                pass

# Statistical loss analysis
def print_statistics():
    while True:
        time.sleep(15)

        with lock:
            expected_packets = stats["total_vote_attempts"]
            actual_packets = stats["total_packets_received"]
            lost_packets = expected_packets - actual_packets
            loss_percentage = (lost_packets / expected_packets) * 100 if expected_packets > 0 else 0

            print("\n========== STATISTICAL LOSS ANALYSIS ==========")
            print(f"Total Vote Attempts: {stats['total_vote_attempts']}")
            print(f"Total Packets Received: {stats['total_packets_received']}")
            print(f"Valid Votes: {stats['valid_votes']}")
            print(f"Duplicate Votes: {stats['duplicate_votes']}")
            print(f"Invalid Packets: {stats['invalid_packets']}")
            print(f"Estimated Lost Packets: {lost_packets}")
            print(f"Packet Loss Percentage: {loss_percentage:.2f}%")
            print("===============================================\n")

threading.Thread(target=broadcast_results, daemon=True).start()
threading.Thread(target=print_statistics, daemon=True).start()

while True:
    try:
        data, addr = server.recvfrom(4096)
        print(f"Packet received from {addr}")

        t = threading.Thread(
            target=handle_packet,
            args=(server, data, addr, lock)
        )
        t.start()

    except ConnectionResetError:
        print("⚠ Ignored UDP reset from closed client.")
        continue
    except KeyboardInterrupt:
        print("\nServer stopped.")
        break
    except Exception as e:
        print(f"Server error: {e}")
        continue

server.close()