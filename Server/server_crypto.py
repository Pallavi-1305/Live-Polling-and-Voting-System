from cryptography.fernet import Fernet

key = b'TGZMwocgeSyxa-vyxohlylteCF4s7lsCLeBYS61LQuQ='
cipher = Fernet(key)

def decrypt_message(data):
    return cipher.decrypt(data).decode()