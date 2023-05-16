import os
import cv2
import numpy as np
from Crypto.Cipher import AES
import secrets
from Crypto.Util.Padding import pad
# read video file


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """Decrypts a file using AES (CBC mode) with the given key."""
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    # Open the input and output files
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            # Read the IV from the input file
            iv = infile.read(AES.block_size)

            # Create the AES cipher object
            cipher = AES.new(key, AES.MODE_CBC, iv)

            

            # Decrypt the file in chunks
            while True:
                chunk = infile.read(chunksize)
                padded_data = pad(chunk, AES.block_size)
                if len(chunk) == 0:
                    break
                outfile.write(cipher.decrypt(padded_data))

            # # Remove PKCS#7 padding from the decrypted data
            # padding_size = outfile.tell() % 16
            # if padding_size != 0:
            #     padding_size = 16 - padding_size
            # padding = bytes([padding_size] * padding_size)
            # outfile.seek(-padding_size, os.SEEK_END)
            # actual_padding = outfile.read(padding_size)
            # if actual_padding != padding:
            #     raise ValueError("Invalid padding")
            # outfile.seek(-padding_size, os.SEEK_END)
            # outfile.truncate()


# # open output text file in write mode
# fileName = 'temp.txt_229504.avi'
# cap = cv2.VideoCapture(fileName)
# out_file_name = "out_"+fileName.split('_')[0]
# padding = int(fileName.split('_')[1].split('.')[0])
# output_file = open(out_file_name, 'w')
# f = 0
# # read video frame by frame
# while True:
#     ret, frame = cap.read()

#     # check if end of video file
#     if not ret:
#         output_file.seek(0, 2)
#         # get the current position of the file pointer
#         pos = output_file.tell()

#         # truncate the file at the given position
#         output_file.truncate(pos - int(padding/8))
#         break

    

#     # convert frame to binary string
#     binary_string = ''
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     for row in gray_frame:
#         for pixel in row:
#             if pixel >= 128:  # white pixel
#                 binary_string += '1'
#             else:  # black pixel
#                 binary_string += '0'

#     # write binary string to output file
#     text = ''
#     for i in range(0, len(binary_string), 8):
#         chunk = binary_string[i:i+8]  # take 8 characters at a time
#         decimal = int(chunk, 2)  # convert binary to decimal
#         text += chr(decimal)  # convert decimal to string and append to string
#     # text = ''.join(chr(int(binary_string[i*8:i*8+8],2)) for i in range(len(binary_string)//8))

#     # write packed data to output file
#     output_file.write(text)
#     f += 1
#     print(f"reading frame {f}")

# # close files and release video capture
# output_file.close()
# cap.release()

with open('key.txt', 'rb') as key_file:
    key = key_file.read()

decrypted_filename = 'decrypted.txt'
decrypt_file(key, "temp.txt.enc", decrypted_filename)
