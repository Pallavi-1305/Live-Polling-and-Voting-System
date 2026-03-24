def validate_vote(vote):
    return vote in ["1", "2", "3"]

def validate_client_id(client_id):
    return client_id.startswith("C")