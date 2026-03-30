from server_crypto import decrypt_message

votes = {"BJP": 0, "Congress": 0, "JDS": 0}
voted_clients = set()
known_clients = set()

stats = {
    "total_vote_attempts": 0,
    "total_packets_received": 0,
    "valid_votes": 0,
    "duplicate_votes": 0,
    "invalid_packets": 0
}

def handle_packet(server, data, addr, lock):
    known_clients.add(addr)

    # Handshake
    if data == b"HELLO":
        print(f"Handshake from {addr}")
        server.sendto(b"READY", addr)
        return

    # Attempt packet
    try:
        text_data = data.decode()
        if text_data.startswith("ATTEMPT|"):
            with lock:
                stats["total_vote_attempts"] += 1
            print(f"Vote attempt registered from {addr}")
            return
    except:
        pass

    with lock:
        stats["total_packets_received"] += 1

    # Decrypt message
    try:
        decrypted = decrypt_message(data)
        client_id, vote = decrypted.split("|")
    except Exception as e:
        print(f"Invalid packet from {addr}: {e}")
        with lock:
            stats["invalid_packets"] += 1
        server.sendto(b"ERROR|Invalid packet", addr)
        return

    # Validate client ID
    if not client_id.startswith("C"):
        print(f"Invalid Client ID: {client_id}")
        with lock:
            stats["invalid_packets"] += 1
        server.sendto(b"ERROR|Invalid Client ID", addr)
        return

    with lock:
        # Duplicate vote check
        if client_id in voted_clients:
            print(f"Duplicate vote from {client_id}")
            stats["duplicate_votes"] += 1
            server.sendto(b"ERROR|Duplicate vote", addr)
            return

        # Vote validation
        party_map = {"1": "BJP", "2": "Congress", "3": "JDS"}

        if vote not in party_map:
            print("Invalid vote option")
            stats["invalid_packets"] += 1
            server.sendto(b"ERROR|Invalid vote", addr)
            return

        party = party_map[vote]
        votes[party] += 1
        voted_clients.add(client_id)
        stats["valid_votes"] += 1

    print(f"\nVote accepted from: {client_id} -> {party}")
    print(f"Current Vote Count: {votes}")
    print("----------------------------")

    result = f"VOTE_ACCEPTED|{party}|BJP:{votes['BJP']}|Congress:{votes['Congress']}|JDS:{votes['JDS']}"
    server.sendto(result.encode(), addr)