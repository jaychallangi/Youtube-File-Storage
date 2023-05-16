# define PY_SSIZE_T_CLEAN
import os
import cv2
import numpy as np
from Crypto.Cipher import AES
import secrets

# Define the encryption function


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """Encrypts a file using AES (CBC mode) with the given key."""
    if not out_filename:
        out_filename = in_filename + '.enc'

    # Generate a random IV (initialization vector)
    iv = os.urandom(AES.block_size)

    # Create the AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open the input and output files
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            # Write the IV to the output file
            outfile.write(iv)

            # Encrypt the file in chunks
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    # Pad the last chunk if it's not a multiple of the block size
                    chunk += b' ' * (AES.block_size - len(chunk) %
                                     AES.block_size)

                # Encrypt the chunk and write it to the output file
                outfile.write(cipher.encrypt(chunk))

# Define the function to convert a file to a binary string


def file_to_binary(filename):
    """Reads a file and returns its contents as a binary string."""
    with open(filename, 'rb') as file:
        binary_string = ''
        while True:
            byte = file.read(1)
            if not byte:
                break
            # Convert the byte to binary and append it to the binary string
            binary_string += bin(ord(byte))[2:].zfill(8)
        file = open("binarystring.txt", "w")
        file.write(binary_string)
        file.close()
        return binary_string


# Define the video dimensions
width = 640
height = 480

# Generate a strong random key
key = secrets.token_bytes(32)

# Save the key to a file
with open('key.txt', 'wb') as key_file:
    key_file.write(key)

# Define the input file
in_filename = 'temp.txt'

# Encrypt the file
encrypt_file(key, in_filename)

# Convert the encrypted file to a binary string
encrypted_filename = in_filename + '.enc'
encrypted_binary = file_to_binary(encrypted_filename)
print(len(encrypted_binary))
padding_length = width*height - (len(encrypted_binary) % (width*height))
encrypted_binary += '0' * padding_length
print(len(encrypted_binary))
# Convert the binary string to a numpy array
binary_array = np.array(list(encrypted_binary),
                        dtype=np.uint8).reshape((-1, width))

# Create a grayscale image from the binary array
image = [np.zeros((height, width), dtype=np.uint8)for frame in range((len(binary_array)//height))]
# image = [np.zeros((height, width)*(len(binary_array)//height), dtype=np.uint8)]
# image = [[[0 for w in range(width)]for h in range(height)]for frames in range((len(binary_array)//height))]

i = 0
for frame in range(len(image)):
    for h in range(height):
        for w in range(width):
            # print(binary_array[i][w])
            image[frame][h][w] = 255 if binary_array[i][w] == 1 else 0
        i += 1
    print(f"formating video frame {frame}/{len(image)}")
    

# Define the output video filename with the full path
video_filename = in_filename+f"_{padding_length}.avi"
print(f"saving file with name {video_filename}")
# Create a video writer object and write the image frames to a video file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
writer = cv2.VideoWriter(video_filename, fourcc, 30.0, (width, height), False)
for i in range(len(image)):
    writer.write(image[i])

# Release the writer object
writer.release()
