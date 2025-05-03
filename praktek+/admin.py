# admin.py
from utils.bst import BST
from utils.csv_handler import read_csv, write_csv

DOKTER_FILE = "dokter.csv"
JADWAL_FILE = "jadwal_dokter.csv"

def cari_jadwal_dengan_bst():
    dokter_data = read_csv(DOKTER_FILE)
    jadwal_data = read_csv(JADWAL_FILE)

    # Buat BST berdasarkan nama dokter
    bst_nama = BST()
    for d in dokter_data:
        id_dokter = d["id_dokter"]
        nama = d["nama"]
        spesialisasi = d["spesialisasi"]
        jadwal_dokter = [j for j in jadwal_data if j["id_dokter"] == id_dokter]
        bst_nama.insert(nama.lower(), jadwal_dokter)

    nama_dicari = input("Masukkan nama dokter: ").lower()
    hasil = bst_nama.search(nama_dicari)
    if hasil:
        print(f"\nJadwal untuk {nama_dicari.title()}:")
        for j in hasil:
            print(f"  - Hari: {j['hari']} | Jam: {j['jam']} | Kapasitas: {j['kapasitas']}")
    else:
        print("Dokter tidak ditemukan.")

def run():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat Semua Jadwal")
        print("2. Tambah Jadwal")
        print("3. Ubah Jadwal")
        print("4. Hapus Jadwal")
        print("5. Kelola Data Pasien")
        print("6. Cari Jadwal Dokter")

        print("0. Logout")
        choice = input("Pilih menu: ")

        if choice == "1":
            lihat_semua_jadwal()
        elif choice == "2":
            tambah_jadwal()
        elif choice == "3":
            ubah_jadwal()
        elif choice == "4":
            hapus_jadwal()
        elif choice == "5":
            print("(Fitur kelola pasien belum dibuat)")
        elif choice == "6":
            cari_jadwal_dengan_bst()

        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid")


def lihat_semua_jadwal():
    jadwal = read_csv(JADWAL_FILE)
    print("\n--- Semua Jadwal Dokter ---")
    for j in jadwal:
        print(f"ID: {j['id_jadwal']} | Dokter: {j['id_dokter']} | Hari: {j['hari']} | Jam: {j['jam']} | Kapasitas: {j['kapasitas']}")


def tambah_jadwal():
    id_jadwal = input("ID Jadwal: ")
    id_dokter = input("ID Dokter: ")
    hari = input("Hari: ")
    jam = input("Jam: ")
    kapasitas = input("Kapasitas: ")

    jadwal = read_csv(JADWAL_FILE)
    jadwal.append({
        "id_jadwal": id_jadwal,
        "id_dokter": id_dokter,
        "hari": hari,
        "jam": jam,
        "kapasitas": kapasitas
    })
    write_csv(JADWAL_FILE, jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
    print("Jadwal berhasil ditambahkan.")


def ubah_jadwal():
    jadwal = read_csv(JADWAL_FILE)
    id_jadwal = input("Masukkan ID Jadwal yang ingin diubah: ")
    for j in jadwal:
        if j['id_jadwal'] == id_jadwal:
            j['hari'] = input(f"Hari baru ({j['hari']}): ") or j['hari']
            j['jam'] = input(f"Jam baru ({j['jam']}): ") or j['jam']
            j['kapasitas'] = input(f"Kapasitas baru ({j['kapasitas']}): ") or j['kapasitas']
            write_csv(JADWAL_FILE, jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
            print("Jadwal berhasil diubah.")
            return
    print("Jadwal tidak ditemukan.")


def hapus_jadwal():
    jadwal = read_csv(JADWAL_FILE)
    id_jadwal = input("Masukkan ID Jadwal yang ingin dihapus: ")
    new_jadwal = [j for j in jadwal if j['id_jadwal'] != id_jadwal]
    if len(new_jadwal) < len(jadwal):
        write_csv(JADWAL_FILE, new_jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
        print("Jadwal berhasil dihapus.")
    else:
        print("Jadwal tidak ditemukan.")