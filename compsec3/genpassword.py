import hashlib
import getpass
import os
from datetime import datetime

def correctid(user_id):
    return user_id.islower()

def correctpasswd(passwd):
    return len(passwd) >= 8

def computehash(passwd):
    hashedpasswd = hashlib.sha256(passwd.encode()).hexdigest()
    return hashedpasswd

def id_exists(file_path, user_id):
    if not os.path.isfile(file_path):
        return False
    with open(file_path, 'r') as file:
        for line in file:
            stored_id, _, _, _= line.strip().split(' ')
            if stored_id == user_id:
                return True
    return False

def Main():
    file_path = 'hashpasswd'
    
    while True:
        user_id = input("Enter your ID: ")
        if not correctid(user_id):
            print("The ID should only contain lowercase letters")
            continue

        if id_exists(file_path, user_id):
            print("The ID already exists")
            another_entry = input("Would you like to enter another ID (Y/N)? ").strip().lower()
            if another_entry != 'y':
                break
            continue

        passwd = getpass.getpass("Enter your passwd: ")
        if not correctpasswd(passwd):
            print("The passwd should contain at least 8 characters")
            continue

        hashedpasswd = computehash(passwd)
        
        with open(file_path, 'a' if os.path.isfile(file_path) else 'w') as file:
            file.write(f"{user_id} {hashedpasswd} {datetime.now()}\n")

        print("User information saved to hashpasswd file")

        another_entry = input("Would you like to enter another ID (Y/N)? ").strip().lower()
        if another_entry != 'y':
            break

if __name__ == "__main__":
    Main()