import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


class AesCipher:
    OPENSSL_CIPHER_NAME = "aes-128-ecb"
    CIPHER_KEY_LEN = 16  # 128 bits

    @staticmethod
    def create_keyhash(keybank):
        keybankhash = hashlib.sha256(keybank.encode()).digest()
        return keybankhash

    @staticmethod
    def fix_key(key):
        if len(key) < AesCipher.CIPHER_KEY_LEN:
            key = key.ljust(AesCipher.CIPHER_KEY_LEN, b"\0")
        elif len(key) > AesCipher.CIPHER_KEY_LEN:
            key = key[: AesCipher.CIPHER_KEY_LEN]
        return key

    @staticmethod
    def encrypt(key):
        cipher = AES.new(AesCipher.fix_key(key), AES.MODE_ECB)
        encrypted_data = cipher.encrypt(pad("752".encode(), AesCipher.CIPHER_KEY_LEN))
        encoded_encrypted_data = b64encode(encrypted_data).decode("utf-8")
        return encoded_encrypted_data

    @staticmethod
    def decrypt(key, data):
        cipher = AES.new(AesCipher.fix_key(key), AES.MODE_ECB)
        decrypted_data = unpad(
            cipher.decrypt(b64decode(data)), AesCipher.CIPHER_KEY_LEN
        ).decode("utf-8")
        return decrypted_data
