from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from config import KEY_PAIR_DIR, initialization_vector

class Encryption:

    def generate_key_pair():
        """
        Generate Public and Private Key Pair for Initial Setup
        """
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open(f"{KEY_PAIR_DIR}/private.pem", "wb")
        file_out.write(private_key)
        file_out.close()

        public_key = key.publickey().export_key()
        file_out = open(f"{KEY_PAIR_DIR}/receiver.pem", "wb")
        file_out.write(public_key)
        file_out.close()

    def encrypt_data(data):
        data = data.encode("utf-8")

        recipient_key = RSA.import_key(open("receiver.pem").read())
        session_key = get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(pad(data,AES.block_size))

        return f"{enc_session_key.decode('utf-8')}|{ciphertext.decode('utf-8')}"


    def decrypt_data(ciphertext):
        ciphertext = str.split(ciphertext,"|")
        private_key = RSA.import_key(open(f"{KEY_PAIR_DIR}/private.pem").read())

        cipher = ciphertext[1].encode("utf-8")
        enc_session_key = ciphertext[0].encode("utf-8")
        ciphertext = cipher

        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        data = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)

        return data.decode("utf-8")

        

