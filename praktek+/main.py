## Struktur Awal Proyek "Praktek+"

# main.py
from auth import login

def main():
    user = login()
    if not user:
        print("Login gagal.")
        return

    role = user["role"]
    if role == "admin":
        import admin
        admin.run()
    elif role == "dokter":
        import dokter
        dokter.run(user)
    elif role == "pasien":
        import pasien
        pasien.run(user)

if __name__ == "__main__":
    main()




