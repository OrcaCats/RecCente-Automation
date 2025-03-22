import os
import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class StringEncryptor:
    def __init__(self, password, regenSalt, salt=None):
        """Initializes the StringEncryptor with a password and optional salt."""
        self.password = password.encode()
        if salt is None or regenSalt == 'true':
            salt = os.urandom(16) 
            saltf = open('salt.txt', 'w')
            print('success create salt')
            saltf.write(base64.urlsafe_b64encode(salt).decode('utf-8'))
        self.salt = salt
        self.key = self._derive_key(self.password, self.salt)
        self.fernet = Fernet(self.key)

    def _derive_key(self, password, salt):
        """Derives a key from the password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, plain_text):
        """Encrypts a string and returns the ciphertext in base64-encoded string format."""
        encrypted_bytes = self.fernet.encrypt(plain_text.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode()

    def decrypt(self, cipher_text):
        """Decrypts a base64-encoded ciphertext string and returns the plaintext."""
        decoded_bytes = base64.urlsafe_b64decode(cipher_text.encode())
        return self.fernet.decrypt(decoded_bytes).decode()

    def get_salt(self):
        """Returns the salt used for key derivation as a base64-encoded string."""
        return base64.urlsafe_b64encode(self.salt).decode()
