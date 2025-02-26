import cv2
import hashlib
import numpy as np
import csv

# Decoding dictionary
c = {i: chr(i) for i in range(255)}

def load_metadata():
    """Load encryption metadata from CSV file."""
    try:
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                return row[0], int(row[1])  # Return (key, length)
    except FileNotFoundError:
        print("Error: Metadata file not found!")
        return None, None

def get_steg_key():
    """Prompt user for a secure decryption key."""
    key = input("Enter Steganography key: ")
    return hashlib.md5(key.encode()).hexdigest()

def decrypt_image():
    """Decrypts and retrieves the secret message from an encrypted image."""
    key = get_steg_key()
    saved_key, msg_len = load_metadata()

    if key is None or saved_key is None or msg_len is None:
        print("Error: Missing metadata. Decryption failed.")
        return

    if key != saved_key:
        print("Error: Incorrect key! Decryption failed.")
        return

    try:
        img = np.load('encrypted_img.npy')  # Load NumPy array
        decrypted_msg = ""
        kl = 0  # Key index
        x, y, z = 0, 0, 0  # Pixel indices

        for _ in range(msg_len):
            decrypted_msg += c[img[x, y, z] ^ ord(key[kl % len(key)])]
            x = (x + 1) % img.shape[0]
            y = (y + 1) % img.shape[1]
            z = (z + 1) % 3
            kl += 1

        print(f"Decryption successful! Secret message: {decrypted_msg}")

    except Exception as e:
        print(f"Error during decryption: {e}")

if __name__ == "__main__":
    decrypt_image()
