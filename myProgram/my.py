# define PY_SSIZE_T_CLEAN
import os
import cv2
import numpy as np
import secrets
from PIL import Image

from AES.aes import myAES


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



# Define the input file
in_filename = 'temp.txt'

# Encrypt the file
aes = myAES(in_filename, in_filename+".enc", "password")
myAES.encrypt(aes)

# Convert the encrypted file to a binary string
encrypted_filename = in_filename + '.enc'
encrypted_binary = file_to_binary(encrypted_filename)
print(len(encrypted_binary))
padding_length = 320*180 - (len(encrypted_binary) % (320*180))
encrypted_binary += '0' * padding_length

print(len(encrypted_binary))
binary_string = encrypted_binary


# Pad the binary string with zeros at the beginning to make it a multiple of 4
while len(binary_string) % 4 != 0:
    binary_string = '0' + binary_string

# Calculate the number of images needed
num_images = (len(binary_string) // (320 * 180))


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(
    f'{in_filename}_{padding_length}.mp4', fourcc, 25, (1280, 720), isColor=False)

# Loop through the binary string and generate images
for i in range(num_images):
    # Create a 1280x720 image with all white pixels
    image_data = np.zeros((720, 1280), dtype=np.uint8) + 255

    # Set up counters to keep track of current row and column
    current_row = 0
    current_col = 0

    # Loop through the binary string and update the pixels of the image
    for j in range(i*320*180, (i+1)*320*180, 4):
        chunk = binary_string[j:j+4]
        if (chunk != ''):
            for k in range(4):
                pixel_value = 255 - int(chunk[k])*255  # 0 -> white, 1 -> black
                image_data[current_row:current_row+4,
                           current_col:current_col+4] = pixel_value
                current_col += 4
                if current_col == 1280:  # Move to the next row if we have reached the end of the current row
                    current_row += 4
                    current_col = 0
    # Save the final image
    final_image = Image.fromarray(image_data, mode='L')
    # final_image.save(f"binary_image_{i}.png")
    video_writer.write(np.array(image_data))
    print(f"generating frame {i}/{num_images}")

print(f"created video {in_filename}_{padding_length}.mp4")
video_writer.release()
