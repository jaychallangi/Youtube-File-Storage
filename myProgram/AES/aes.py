import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt


class myAES:
    def __init__(self, in_fileName, out_fileName, password):
        self.password = password
        self.in_fileName = in_fileName
        self.out_fileName = out_fileName

    def encrypt(self):
        password = self.password

        input_filename = self.in_fileName
        output_filename = self.out_fileName

        # Open files
        # rb = read bytes. Required to read non-text files
        file_in = open(input_filename, 'rb')
        # wb = write bytes. Required to write the encrypted data
        file_out = open(output_filename, 'wb')

        salt = get_random_bytes(32)  # Generate salt
        # Generate a key using the password and salt
        key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)
        file_out.write(salt)  # Write the salt to the top of the output file

        # Create a cipher object to encrypt data
        cipher = AES.new(key, AES.MODE_GCM)
        # Write out the nonce to the output file under the salt
        file_out.write(cipher.nonce)

        # Read, encrypt and write the data
        BUFFER_SIZE = 1024 * 1024
        data = file_in.read(BUFFER_SIZE)  # Read in some of the file
        while len(data) != 0:  # Check if we need to encrypt anymore data
            encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
            # Write the encrypted data to the output file
            file_out.write(encrypted_data)
            # Read some more of the file to see if there is any more left
            data = file_in.read(BUFFER_SIZE)

        # Get and write the tag for decryption verification
        tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
        file_out.write(tag)

        # Close both files
        file_in.close()
        file_out.close()
        print("encrypted file")

    def decrypt(self):
        password = self.password

        input_filename = self.in_fileName
        output_filename = self.out_fileName
        file_in = open(input_filename, 'rb')
        file_out = open(output_filename, 'wb')

        # Read salt and generate key
        salt = file_in.read(32)  # The salt we generated was 32 bits long
        # Generate a key using the password and salt again
        key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)

        # Read nonce and create cipher
        nonce = file_in.read(16)  # The nonce is 16 bytes long
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # Identify how many bytes of encrypted there is
        # We know that the salt (32) + the nonce (16) + the data (?) + the tag (16) is in the file
        # So some basic algebra can tell us how much data we need to read to decrypt
        file_in_size = os.path.getsize(input_filename)
        # Total - salt - nonce - tag = encrypted data
        encrypted_data_size = file_in_size - 32 - 16 - 16

        # Read, decrypt and write the data
        BUFFER_SIZE = 1024 * 1024

        # Identify how many loops of full buffer reads we need to do
        for _ in range(int(encrypted_data_size / BUFFER_SIZE)):
            # Read in some data from the encrypted file
            data = file_in.read(BUFFER_SIZE)
            decrypted_data = cipher.decrypt(data)  # Decrypt the data
            # Write the decrypted data to the output file
            file_out.write(decrypted_data)
        # Read whatever we have calculated to be left of encrypted data
        data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))
        decrypted_data = cipher.decrypt(data)  # Decrypt the data
        # Write the decrypted data to the output file
        file_out.write(decrypted_data)

        # Verify encrypted file was not tampered with
        tag = file_in.read(16)
        # try:
        #     cipher.verify(tag)
        # except ValueError as e:
        #     # If we get a ValueError, there was an error when decrypting so delete the file we created
        #     file_in.close()
        #     file_out.close()
        #     os.remove(output_filename)
        #     raise e

        # If everything was ok, close the files
        file_in.close()
        file_out.close()


# if __name__ == "__main__":
#     # aes = myAES('temp.txt', 'enc_temp.txt', "securePassword1")
#     # aes.encrypt()

#     aes = myAES('enc_temp.txt', 'out.txt', 'securePassword1')
#     aes.decrypt()
