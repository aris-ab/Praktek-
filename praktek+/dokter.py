from utils.queue import Queue
from utils.csv_handler import read_csv, write_csv

JADWAL_FILE = "jadwal_dokter.csv"
PENDAFTARAN_FILE = "pendaftaran.csv"

def run(user):
    while True:
        print("\n=== Menu Dokter ===")
        print("1. Lihat Jadwal Saya")
        print("2. Tambah Jadwal")
        print("3. Ubah Jadwal")
        print("4. Hapus Jadwal")
        print("5. Lihat Pasien Terdaftar")
        print("6. Ubah Status Pasien")
        print("7. Lihat Laporan Pasien")
        print("8. Lihat Antrean Pasien")
        print("9. Panggil Pasien Berikutnya")
        print("0. Logout")
        choice = input("Pilih menu: ")

        if choice == "1":
            lihat_jadwal(user)
        elif choice == "2":
            tambah_jadwal(user)
        elif choice == "3":
            ubah_jadwal(user)
        elif choice == "4":
            hapus_jadwal(user)
        elif choice == "5":
            lihat_pasien(user)
        elif choice == "6":
            ubah_status_pasien(user)
        elif choice == "7":
            laporan_pasien(user)
        elif choice == "4":
            jadwal_id = input("Masukkan ID Jadwal: ")
            lihat_antrean(jadwal_id)
        elif choice == "5":
            jadwal_id = input("Masukkan ID Jadwal: ")
            panggil_pasien(jadwal_id)

        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid.")

def lihat_jadwal(user):
    jadwal = read_csv(JADWAL_FILE)
    print("\n--- Jadwal Praktik Saya ---")
    for j in jadwal:
        if j["id_dokter"] == user["id"]:
            print(f"ID Jadwal: {j['id_jadwal']} | Hari: {j['hari']} | Jam: {j['jam']} | Kapasitas: {j['kapasitas']}")

def tambah_jadwal(user):
    id_jadwal = input("ID Jadwal: ")
    hari = input("Hari: ")
    jam = input("Jam: ")
    kapasitas = input("Kapasitas: ")

    jadwal = read_csv(JADWAL_FILE)
    jadwal.append({
        "id_jadwal": id_jadwal,
        "id_dokter": user["id"],
        "hari": hari,
        "jam": jam,
        "kapasitas": kapasitas
    })
    write_csv(JADWAL_FILE, jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
    print("Jadwal berhasil ditambahkan.")

def ubah_jadwal(user):
    jadwal = read_csv(JADWAL_FILE)
    id_jadwal = input("ID Jadwal yang ingin diubah: ")
    for j in jadwal:
        if j['id_jadwal'] == id_jadwal and j['id_dokter'] == user["id"]:
            j['hari'] = input(f"Hari baru ({j['hari']}): ") or j['hari']
            j['jam'] = input(f"Jam baru ({j['jam']}): ") or j['jam']
            j['kapasitas'] = input(f"Kapasitas baru ({j['kapasitas']}): ") or j['kapasitas']
            write_csv(JADWAL_FILE, jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
            print("Jadwal berhasil diubah.")
            return
    print("Jadwal tidak ditemukan atau bukan milik Anda.")

def hapus_jadwal(user):
    jadwal = read_csv(JADWAL_FILE)
    id_jadwal = input("ID Jadwal yang ingin dihapus: ")
    new_jadwal = [j for j in jadwal if not (j['id_jadwal'] == id_jadwal and j['id_dokter'] == user["id"])]
    if len(new_jadwal) < len(jadwal):
        write_csv(JADWAL_FILE, new_jadwal, ["id_jadwal", "id_dokter", "hari", "jam", "kapasitas"])
        print("Jadwal berhasil dihapus.")
    else:
        print("Jadwal tidak ditemukan atau bukan milik Anda.")

def lihat_pasien(user):
    jadwal = read_csv(JADWAL_FILE)
    daftar = read_csv(PENDAFTARAN_FILE)

    # Ambil semua ID jadwal milik dokter ini
    id_jadwal_dokter = [j["id_jadwal"] for j in jadwal if j["id_dokter"] == user["id"]]

    print("\n--- Pasien Terdaftar ---")
    found = False
    for d in daftar:
        if d["id_jadwal"] in id_jadwal_dokter:
            print(f"Pasien: {d['nama']} | Jadwal: {d['id_jadwal']} | Status: {d['status']}")
            found = True
    if not found:
        print("Belum ada pasien terdaftar.")

def ubah_status_pasien(user):
    pendaftaran = read_csv(PENDAFTARAN_FILE)
    jadwal = read_csv(JADWAL_FILE)

    # Ambil ID jadwal milik dokter
    id_jadwal_dokter = [j["id_jadwal"] for j in jadwal if j["id_dokter"] == user["id"]]

    print("\n--- Daftar Pasien Anda ---")
    for p in pendaftaran:
        if p["id_jadwal"] in id_jadwal_dokter:
            print(f"ID Pasien: {p['id_pasien']} | Nama: {p['nama']} | Jadwal: {p['id_jadwal']} | Status: {p['status']}")

    target_id = input("Masukkan ID Pasien yang ingin diubah statusnya: ")
    new_status = input("Status baru (Menunggu/Selesai/Batal): ").capitalize()

    updated = False
    for p in pendaftaran:
        if p["id_pasien"] == target_id and p["id_jadwal"] in id_jadwal_dokter:
            p["status"] = new_status
            updated = True
            break

    if updated:
        write_csv(PENDAFTARAN_FILE, pendaftaran, ["id_pasien", "nama", "id_jadwal", "status"])
        print("Status pasien berhasil diubah.")
    else:
        print("Data pasien tidak ditemukan.")

def laporan_pasien(user):
    pendaftaran = read_csv(PENDAFTARAN_FILE)
    jadwal = read_csv(JADWAL_FILE)

    id_jadwal_dokter = [j["id_jadwal"] for j in jadwal if j["id_dokter"] == user["id"]]

    laporan = {"Menunggu": 0, "Selesai": 0, "Batal": 0}

    for p in pendaftaran:
        if p["id_jadwal"] in id_jadwal_dokter:
            status = p["status"].capitalize()
            if status in laporan:
                laporan[status] += 1

    print("\n--- Laporan Pasien ---")
    for status, jumlah in laporan.items():
        print(f"{status}: {jumlah} pasien")

def lihat_antrean(jadwal_id):
    pendaftar = read_csv("pendaftaran.csv")
    antrean = Queue()

    for p in pendaftar:
        if p["id_jadwal"] == jadwal_id and p["status"] == "terdaftar":
            antrean.enqueue(p)

    if antrean.is_empty():
        print("Belum ada pasien dalam antrean.")
    else:
        print("\n--- Antrean Pasien ---")
        for idx, pasien in enumerate(antrean.get_all(), 1):
            print(f"{idx}. {pasien['nama']} (ID Pasien: {pasien['id_pasien']})")

def panggil_pasien(jadwal_id):
    pendaftar = read_csv("pendaftaran.csv")
    antrean = Queue()
    for p in pendaftar:
        if p["id_jadwal"] == jadwal_id and p["status"] == "terdaftar":
            antrean.enqueue(p)

    if antrean.is_empty():
        print("Tidak ada pasien dalam antrean.")
        return

    next_patient = antrean.dequeue()
    print(f"Memanggil pasien: {next_patient['nama']} (ID: {next_patient['id_pasien']})")
