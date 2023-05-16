import os
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

# Define the filename of the file to encrypt
filename = "temp.txt"

# Generate a random encryption key and initialization vector (IV)
key = os.urandom(32)
iv = os.urandom(16)

# Save the encryption key and IV to files
with open("key.txt", "wb") as key_file:
    key_file.write(key)
with open("iv.txt", "wb") as iv_file:
    iv_file.write(iv)

# Encrypt the file using AES CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)
with open(filename, "rb") as file:
    plaintext = file.read()
    padded_plaintext = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)

# Convert the encrypted data to binary
binary_data = "".join(format(byte, "08b") for byte in ciphertext)

# Define the size of each frame (in bits)
frame_size = 10000

# Split the binary data into frames
frames = [binary_data[i:i+frame_size] for i in range(0, len(binary_data), frame_size)]

# Convert each frame to an image
width = 100
height = int(frame_size / width) + 1
images = []
for frame in frames:
    img = Image.new("1", (width, height), "white")
    pixels = img.load()
    for i in range(len(frame)):
        row = int(i / width)
        col = i % width
        if frame[i] == "1":
            pixels[col, row] = 0
    images.append(img)

# Calculate the frame duration for a 30 FPS video (in seconds)
frame_duration = 1 / 30

# Save the images as an MP4 video
clip = ImageSequenceClip(images, fps=30)
clip.write_videofile("video.mp4", fps=30)
