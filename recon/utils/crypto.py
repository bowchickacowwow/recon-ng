from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def aes_decrypt(ciphertext, key, iv):
    decoded = ciphertext.decode('base64')
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv.encode('utf-8')), default_backend())
    decryptor = cipher.decryptor()
    password = decryptor.update(decoded) + decryptor.finalize()
    return unicode(password, 'utf-8')
