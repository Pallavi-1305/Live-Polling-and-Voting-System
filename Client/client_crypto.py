from cryptography.fernet import Fernet

key = b'TGZMwocgeSyxa-vyxohlylteCF4s7lsCLeBYS61LQuQ='
cipher = Fernet(key)

def encrypt_message(message):
    return cipher.encrypt(message.encode())