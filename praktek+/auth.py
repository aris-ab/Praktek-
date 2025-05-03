# auth.py
USERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "dr_andi", "password": "dokter123", "role": "dokter", "id": "D001"},
    {"username": "pasien1", "password": "pas123", "role": "pasien", "id": "P001"}
]

def login():
    print("=== Login Praktek+ ===")
    username = input("Username: ")
    password = input("Password: ")
    for user in USERS:
        if user["username"] == username and user["password"] == password:
            return user
    return None