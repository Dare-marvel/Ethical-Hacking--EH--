import os
import random
import string
import tkinter as tk
from tkinter import simpledialog, messagebox

def generate_key(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        content = file.read()
    encrypted_content = bytearray()
    for byte in content:
        encrypted_content.append(byte ^ key)  # Simple XOR encryption
    with open(file_path + ".locked", 'wb') as file:
        file.write(encrypted_content)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        content = file.read()
    decrypted_content = bytearray()
    for byte in content:
        decrypted_content.append(byte ^ key)  # Simple XOR decryption
    with open(file_path[:-7], 'wb') as file:
        file.write(decrypted_content)

def lock_files(file_paths, key):
    for file_path in file_paths:
        encrypt_file(file_path, ord(key[0]))  # Using the ASCII value of the first character of the key
        os.remove(file_path)  # Delete the original file

def unlock_files(file_paths, key):
    for file_path in file_paths:
        if file_path.endswith(".locked"):
            decrypt_file(file_path, ord(key[0]))  # Using the ASCII value of the first character of the key
            os.remove(file_path)  # Remove the encrypted file

# Function to prompt user for password
def prompt_for_password(file_path, key):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt user for password
    password = simpledialog.askstring("Password", "Enter password to unlock the file: ", show='*')

    # Check if password is correct
    if password == key:
        decrypt_file(file_path, ord(key[0]))  # Using the ASCII value of the first character of the key
        os.remove(file_path)
        messagebox.showinfo("Success", "File unlocked successfully!")
    else:
        messagebox.showerror("Error", "Incorrect password!")

def convert_to_double_backslashes(file_path):
    # Replace single backslashes with double backslashes
    return file_path.replace('\\', '\\\\')

# Get key from user input
key = input("Enter encryption key: ")

# Taking file path input from the user
file_path = input("Enter the file path (e.g., B:\\AIML\\FileToBeLocked.pdf): ")

# Converting file path to desired format
file_path = convert_to_double_backslashes(file_path)
# print(file_path)

# Usage Example:
# Lock files at specified locations
lock_files([file_path], key)

# Example usage to unlock file
file_path = file_path + '.locked'

# Prompt for password if file is accessed
prompt_for_password(file_path, key)
