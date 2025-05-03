from utils.csv_handler import read_csv, write_csv
from utils.bst import BST
from utils.queue import Queue

JADWAL_FILE = "jadwal_dokter.csv"
DOKTER_FILE = "dokter.csv"
PENDAFTARAN_FILE = "pendaftaran.csv"

antrian = Queue()

def run(user):
    while True:
        print(f"\n=== Menu Pasien ({user['username']}) ===")
        print("1. Lihat Semua Jadwal")
        print("2. Cari Jadwal Dokter")
        print("3. Daftar Konsultasi")
        print("4. Ajukan Perubahan Jadwal")
        print("5. Lihat Status Pendaftaran")
        print("6. Lihat Riwayat Pendaftaran")
        print("7. Batalkan Pendaftaran")
        print("0. Logout")
        choice = input("Pilih menu: ")

        if choice == "1":
            lihat_semua_jadwal()
        elif choice == "2":
            cari_jadwal_dokter()
        elif choice == "3":
            daftar_konsultasi(user)
        elif choice == "4":
            ubah_jadwal(user)
        elif choice == "5":
            lihat_status(user)
        elif choice == "6":
            riwayat_pendaftaran(user)
        elif choice == "7":
            batalkan_pendaftaran(user)

        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid.")

def lihat_semua_jadwal():
    jadwal = read_csv(JADWAL_FILE)
    print("\n--- Semua Jadwal Dokter ---")
    for j in jadwal:
        print(f"{j['id_jadwal']} | Dokter: {j['id_dokter']} | Hari: {j['hari']} | Jam: {j['jam']} | Kapasitas: {j['kapasitas']}")

def cari_jadwal_dokter():
    keyword = input("Masukkan nama atau spesialisasi dokter: ").lower()
    
    dokter_data = read_csv("dokter.csv")
    jadwal_data = read_csv("jadwal_dokter.csv")

    # Buat BST berdasarkan nama_dokter dan spesialisasi
    bst = BST()
    for d in dokter_data:
        key = d["nama_dokter"].lower()
        bst.insert(key, d["id_dokter"])
        bst.insert(d["spesialisasi"].lower(), d["id_dokter"])

    hasil_id_dokter = bst.search(keyword)
    if not hasil_id_dokter:
        print("Dokter tidak ditemukan.")
        return

    # Tampilkan jadwal dari dokter yang ditemukan
    print("\n--- Jadwal yang Ditemukan ---")
    ditemukan = False
    for j in jadwal_data:
        if j["id_dokter"] == hasil_id_dokter:
            print(f"ID Jadwal: {j['id_jadwal']} | Hari: {j['hari']} | Jam: {j['jam']} | Kapasitas: {j['kapasitas']}")
            ditemukan = True
    if not ditemukan:
        print("Dokter ditemukan tapi belum memiliki jadwal.")


def daftar_konsultasi(user):
    lihat_semua_jadwal()
    id_jadwal = input("Masukkan ID Jadwal yang ingin didaftarkan: ")
    
    daftar = read_csv(PENDAFTARAN_FILE)
    daftar.append({
        "id_pasien": user["id"],
        "nama": user["username"],
        "id_jadwal": id_jadwal,
        "status": "terdaftar"
    })
    write_csv(PENDAFTARAN_FILE, daftar, ["id_pasien", "nama", "id_jadwal", "status"])
    antrian.enqueue(user["id"])
    print("Pendaftaran berhasil! Kamu masuk dalam antrean konsultasi.")

def ubah_jadwal(user):
    daftar = read_csv(PENDAFTARAN_FILE)
    found = False
    for d in daftar:
        if d["id_pasien"] == user["id"]:
            print(f"Jadwal saat ini: {d['id_jadwal']}")
            new_id = input("Masukkan ID Jadwal baru: ")
            d["id_jadwal"] = new_id
            d["status"] = "menunggu persetujuan"
            found = True
            break
    if found:
        write_csv(PENDAFTARAN_FILE, daftar, ["id_pasien", "nama", "id_jadwal", "status"])
        print("Permintaan perubahan jadwal diajukan.")
    else:
        print("Belum ada pendaftaran ditemukan.")

def lihat_status(user):
    daftar = read_csv(PENDAFTARAN_FILE)
    print("\n--- Status Pendaftaran ---")
    for d in daftar:
        if d["id_pasien"] == user["id"]:
            print(f"Jadwal: {d['id_jadwal']} | Status: {d['status']}")

def riwayat_pendaftaran(user):
    daftar = read_csv(PENDAFTARAN_FILE)
    print("\n--- Riwayat Pendaftaran ---")
    count = 0
    for d in daftar:
        if d["id_pasien"] == user["id"]:
            print(f"- Jadwal: {d['id_jadwal']} | Status: {d['status']}")
            count += 1
    if count == 0:
        print("Belum ada riwayat pendaftaran.")

def batalkan_pendaftaran(user):
    daftar = read_csv(PENDAFTARAN_FILE)
    new_daftar = [d for d in daftar if d["id_pasien"] != user["id"]]
    if len(new_daftar) < len(daftar):
        write_csv(PENDAFTARAN_FILE, new_daftar, ["id_pasien", "nama", "id_jadwal", "status"])
        print("Pendaftaran berhasil dibatalkan.")
    else:
        print("Tidak ada pendaftaran yang bisa dibatalkan.")
