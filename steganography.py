!pip install pillow

from PIL import Image
import numpy as np

# 🧠 Convert text to binary
def to_bin(data):
    return ''.join(format(ord(char), '08b') for char in data)

def encode_image(image_path, secret_message, output_path="encoded_image.png"):
    image = Image.open(image_path)
    binary_msg = to_bin(secret_message) + '1111111111111110'  # EOF marker
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    
    if len(binary_msg) > len(flat_pixels):
        raise ValueError("Message too large to encode in image.")

    for i in range(len(binary_msg)):
        flat_pixels[i] = (flat_pixels[i] & ~1) | int(binary_msg[i])

    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_image = Image.fromarray(encoded_pixels.astype('uint8'))
    encoded_image.save(output_path)
    print(f"✅ Message encoded into {output_path}")

def decode_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image).flatten()
    binary_data = ''.join(str(pixel & 1) for pixel in pixels)

    bytes_list = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ''
    for byte in bytes_list:
        if byte == '11111110':  # EOF
            break
        decoded_text += chr(int(byte, 2))
    return decoded_text
