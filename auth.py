import hashlib
import os
import json
USER_FILE = "users.json"

#Creates json file
def create_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            json.dump({}, file)

#Hashes passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Gets users from json file
def load_users():
    create_user_file()
    with open(USER_FILE, "r") as file:
        return json.load(file)

#Save users    
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

#Signup function which loads users, checks if name is in users, hashes the password then saves as a new user
def signup(username, password):

    users = load_users()

    if username in users:
        return False

    users[username] = {
        "password": hash_password(password),
        "role": "student"
    }
    save_users(users)

    return True

#Login function
def login(username, password):
    users = load_users()
    if username not in users:
        return None
    hashed = hash_password(password)
    if hashed == users[username]["password"]:
        return users[username]["role"]

    return None

