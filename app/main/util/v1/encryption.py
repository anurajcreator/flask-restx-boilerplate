from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from app.main.config import DATABASE_KEY_PAIR_DIR, RESPONSE_KEY_PAIR_DIR

class Encryption:

    def encrypt_data(data):

        if not type(data) == bytes:
            data = data.encode("utf-8")

        recipient_key = RSA.import_key(open(f"{DATABASE_KEY_PAIR_DIR}/db_receiver.pem").read())
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key, hashAlgo='Crypto.Hash.SHA256')
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(pad(data,AES.block_size))

        return enc_session_key, ciphertext, cipher_aes.nonce, tag


    def decrypt_data(ciphertext, enc_session_key, nonce, tag):
        private_key = RSA.import_key(open(f"{DATABASE_KEY_PAIR_DIR}/db_private.pem").read())

        cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo='Crypto.Hash.SHA256')
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = unpad(cipher_aes.decrypt_and_verify(ciphertext, tag), AES.block_size)

        return data.decode("utf-8")


    def encrypt_response(data):

        if not type(data) == bytes:
            data = data.encode("utf-8")

        recipient_key = RSA.import_key(open(f"{RESPONSE_KEY_PAIR_DIR}/rp_receiver.pem").read())
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key, hashAlgo='Crypto.Hash.SHA256')
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(pad(data,AES.block_size))

        return enc_session_key, ciphertext, cipher_aes.nonce, tag

        

