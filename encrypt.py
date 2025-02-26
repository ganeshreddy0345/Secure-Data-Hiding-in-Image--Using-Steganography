import cv2
import hashlib
import numpy as np
import csv

# Encoding dictionary
d = {chr(i): i for i in range(255)}

def save_metadata(hashkey, length):
    """Save encryption metadata to a CSV file."""
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([hashkey, length])

def get_steg_key():
    """Prompt user for a secure encryption key."""
    key = input("Enter Steganography key: ")
    confirm_key = input("Re-enter Steganography key: ")
    
    if key != confirm_key:
        print("Keys do not match! Please try again.")
        return get_steg_key()
    
    print("Key verified! Proceeding with encryption.")
    return hashlib.md5(key.encode()).hexdigest()

def encrypt_image(image_path, secret_message):
    """Encrypts a secret message into an image."""
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found! Please check the path.")
        return

    key = get_steg_key()
    
    h, w, _ = img.shape
    msg_len = len(secret_message)
    kl = 0  # Key index
    x, y, z = 0, 0, 0  # Pixel indices

    for i in range(msg_len):
        img[x, y, z] = d[secret_message[i]] ^ ord(key[kl % len(key)])
        x = (x + 1) % h
        y = (y + 1) % w
        z = (z + 1) % 3
        kl += 1

    np.save('encrypted_img.npy', img)  # Save encrypted NumPy array
    save_metadata(key, msg_len)
    cv2.imwrite("encrypted_img.jpg", img)
    print("Encryption successful! Encrypted image saved as 'encrypted_img.jpg'.")

if __name__ == "__main__":
    img_path = input("Enter the image path: ")
    secret_msg = input("Enter secret message: ")
    encrypt_image(img_path, secret_msg)
