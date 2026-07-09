"""
main.py
Menu CLI untuk mengelola aplikasi Konsultasi Psikologi (Kelompok 15).
Menjalankan mekanisme Create, Read, Update, Delete (CRUD) untuk 6 entitas ERD.

Cara menjalankan:
    python main.py
"""

import database
import crud


def cetak_tabel(rows, kolom_kosong="(tidak ada data)"):
    if not rows:
        print(kolom_kosong)
        return
    for row in rows:
        print("-" * 50)
        for key, value in row.items():
            print(f"{key:<18}: {value}")
    print("-" * 50)


def input_opsional(label):
    """Untuk update: enter kosong berarti field tidak diubah."""
    val = input(f"{label} (kosongkan jika tidak diubah): ").strip()
    return val if val != "" else None


# =========================================================
# MENU: PENGGUNA
# =========================================================
def menu_pengguna():
    while True:
        print("\n=== MENU PENGGUNA ===")
        print("1. Tambah Pengguna (Create)")
        print("2. Lihat Pengguna (Read)")
        print("3. Ubah Pengguna (Update)")
        print("4. Hapus Pengguna (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            nama = input("Nama: ")
            email = input("Email: ")
            password = input("Password: ")
            pekerjaan = input("Pekerjaan: ")
            new_id = crud.create_pengguna(nama, email, password, pekerjaan)
            print(f"Pengguna berhasil ditambahkan dengan id_user={new_id}")
            print("(tanggal_daftar otomatis diisi oleh sistem)")

        elif pilihan == "2":
            id_user = input("Masukkan id_user (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_pengguna(int(id_user) if id_user else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_user = int(input("id_user yang ingin diubah: "))
            nama = input_opsional("Nama baru")
            email = input_opsional("Email baru")
            password = input_opsional("Password baru")
            pekerjaan = input_opsional("Pekerjaan baru")
            ok = crud.update_pengguna(id_user, nama, email, password, pekerjaan)
            print("Berhasil diubah." if ok else "id_user tidak ditemukan.")

        elif pilihan == "4":
            id_user = int(input("id_user yang ingin dihapus: "))
            ok = crud.delete_pengguna(id_user)
            print("Berhasil dihapus." if ok else "Gagal / id_user tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU: KATEGORI MASALAH
# =========================================================
def menu_kategori():
    while True:
        print("\n=== MENU KATEGORI MASALAH ===")
        print("1. Tambah Kategori (Create)")
        print("2. Lihat Kategori (Read)")
        print("3. Ubah Kategori (Update)")
        print("4. Hapus Kategori (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            nama_kategori = input("Nama kategori: ")
            deskripsi = input("Deskripsi: ")
            new_id = crud.create_kategori(nama_kategori, deskripsi)
            print(f"Kategori berhasil ditambahkan dengan id_kategori={new_id}")

        elif pilihan == "2":
            id_kategori = input("Masukkan id_kategori (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_kategori(int(id_kategori) if id_kategori else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_kategori = int(input("id_kategori yang ingin diubah: "))
            nama_kategori = input_opsional("Nama kategori baru")
            deskripsi = input_opsional("Deskripsi baru")
            ok = crud.update_kategori(id_kategori, nama_kategori, deskripsi)
            print("Berhasil diubah." if ok else "id_kategori tidak ditemukan.")

        elif pilihan == "4":
            id_kategori = int(input("id_kategori yang ingin dihapus: "))
            ok = crud.delete_kategori(id_kategori)
            print("Berhasil dihapus." if ok else "Gagal / id_kategori tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU: KONSULTASI
# =========================================================
def menu_konsultasi():
    while True:
        print("\n=== MENU KONSULTASI ===")
        print("1. Tambah Konsultasi (Create)")
        print("2. Lihat Konsultasi (Read)")
        print("3. Ubah Konsultasi (Update)")
        print("4. Hapus Konsultasi (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            id_user = int(input("id_user (pemilik konsultasi): "))
            isi_konsultasi = input("Isi konsultasi: ")
            id_kategori = input("id_kategori (kosongkan jika tidak ada): ").strip()
            new_id = crud.create_konsultasi(
                id_user, isi_konsultasi, int(id_kategori) if id_kategori else None
            )
            print(f"Konsultasi berhasil ditambahkan dengan id_konsultasi={new_id}")
            print("(tanggal & status='Menunggu' otomatis diisi oleh sistem)")

        elif pilihan == "2":
            id_konsultasi = input("Masukkan id_konsultasi (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_konsultasi(int(id_konsultasi) if id_konsultasi else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_konsultasi = int(input("id_konsultasi yang ingin diubah: "))
            isi_konsultasi = input_opsional("Isi konsultasi baru")
            id_kategori = input_opsional("id_kategori baru")
            status = input_opsional("Status baru (mis. Menunggu/Diproses/Selesai)")
            ok = crud.update_konsultasi(
                id_konsultasi, isi_konsultasi,
                int(id_kategori) if id_kategori else None, status
            )
            print("Berhasil diubah." if ok else "id_konsultasi tidak ditemukan.")

        elif pilihan == "4":
            id_konsultasi = int(input("id_konsultasi yang ingin dihapus: "))
            ok = crud.delete_konsultasi(id_konsultasi)
            print("Berhasil dihapus." if ok else "Gagal / id_konsultasi tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU: INFO PSIKOLOGIS
# =========================================================
def menu_info():
    while True:
        print("\n=== MENU INFO PSIKOLOGIS ===")
        print("1. Tambah Info (Create)")
        print("2. Lihat Info (Read)")
        print("3. Ubah Info (Update)")
        print("4. Hapus Info (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            judul = input("Judul: ")
            isi_konten = input("Isi konten: ")
            id_kategori = input("id_kategori (kosongkan jika tidak ada): ").strip()
            new_id = crud.create_info(judul, isi_konten, int(id_kategori) if id_kategori else None)
            print(f"Info berhasil ditambahkan dengan id_info={new_id}")
            print("(tanggal_publish otomatis diisi oleh sistem)")

        elif pilihan == "2":
            id_info = input("Masukkan id_info (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_info(int(id_info) if id_info else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_info = int(input("id_info yang ingin diubah: "))
            judul = input_opsional("Judul baru")
            isi_konten = input_opsional("Isi konten baru")
            id_kategori = input_opsional("id_kategori baru")
            ok = crud.update_info(
                id_info, judul, isi_konten, int(id_kategori) if id_kategori else None
            )
            print("Berhasil diubah." if ok else "id_info tidak ditemukan.")

        elif pilihan == "4":
            id_info = int(input("id_info yang ingin dihapus: "))
            ok = crud.delete_info(id_info)
            print("Berhasil dihapus." if ok else "Gagal / id_info tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU: PSIKOLOG
# =========================================================
def menu_psikolog():
    while True:
        print("\n=== MENU PSIKOLOG ===")
        print("1. Tambah Psikolog (Create)")
        print("2. Lihat Psikolog (Read)")
        print("3. Ubah Psikolog (Update)")
        print("4. Hapus Psikolog (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            nama = input("Nama: ")
            spesialisasi = input("Spesialisasi: ")
            nomor_lisensi = input("Nomor lisensi: ")
            kontak = input("Kontak: ")
            lokasi_praktik = input("Lokasi praktik: ")
            new_id = crud.create_psikolog(nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik)
            print(f"Psikolog berhasil ditambahkan dengan id_psikolog={new_id}")

        elif pilihan == "2":
            id_psikolog = input("Masukkan id_psikolog (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_psikolog(int(id_psikolog) if id_psikolog else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_psikolog = int(input("id_psikolog yang ingin diubah: "))
            nama = input_opsional("Nama baru")
            spesialisasi = input_opsional("Spesialisasi baru")
            nomor_lisensi = input_opsional("Nomor lisensi baru")
            kontak = input_opsional("Kontak baru")
            lokasi_praktik = input_opsional("Lokasi praktik baru")
            ok = crud.update_psikolog(
                id_psikolog, nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik
            )
            print("Berhasil diubah." if ok else "id_psikolog tidak ditemukan.")

        elif pilihan == "4":
            id_psikolog = int(input("id_psikolog yang ingin dihapus: "))
            ok = crud.delete_psikolog(id_psikolog)
            print("Berhasil dihapus." if ok else "Gagal / id_psikolog tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU: PEMILIHAN JADWAL KONSELING
# =========================================================
def menu_jadwal():
    while True:
        print("\n=== MENU JADWAL KONSELING ===")
        print("1. Tambah Jadwal (Create)")
        print("2. Lihat Jadwal (Read)")
        print("3. Ubah Jadwal (Update)")
        print("4. Hapus Jadwal (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            id_psikolog = int(input("id_psikolog: "))
            id_user = int(input("id_user: "))
            tanggal = input("Tanggal booking (YYYY-MM-DD): ")
            jam = input("Jam booking (HH:MM): ")
            new_id = crud.create_jadwal(id_psikolog, id_user, tanggal, jam)
            print(f"Jadwal berhasil ditambahkan dengan id_jadwal={new_id}")
            print("(status_booking otomatis diisi 'Menunggu Konfirmasi')")

        elif pilihan == "2":
            id_jadwal = input("Masukkan id_jadwal (kosongkan untuk lihat semua): ").strip()
            rows = crud.read_jadwal(int(id_jadwal) if id_jadwal else None)
            cetak_tabel(rows)

        elif pilihan == "3":
            id_jadwal = int(input("id_jadwal yang ingin diubah: "))
            tanggal = input_opsional("Tanggal baru")
            jam = input_opsional("Jam baru")
            status_booking = input_opsional("Status booking baru")
            ok = crud.update_jadwal(id_jadwal, tanggal, jam, status_booking)
            print("Berhasil diubah." if ok else "id_jadwal tidak ditemukan.")

        elif pilihan == "4":
            id_jadwal = int(input("id_jadwal yang ingin dihapus: "))
            ok = crud.delete_jadwal(id_jadwal)
            print("Berhasil dihapus." if ok else "Gagal / id_jadwal tidak ditemukan.")

        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")


# =========================================================
# MENU UTAMA
# =========================================================
def main():
    database.create_tables()
    while True:
        print("\n===================================")
        print(" APLIKASI KONSULTASI PSIKOLOGI")
        print(" Tugas 11 - Implementasi CRUD")
        print("===================================")
        print("1. Kelola Pengguna")
        print("2. Kelola Kategori Masalah")
        print("3. Kelola Konsultasi")
        print("4. Kelola Info Psikologis")
        print("5. Kelola Psikolog")
        print("6. Kelola Jadwal Konseling")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            menu_pengguna()
        elif pilihan == "2":
            menu_kategori()
        elif pilihan == "3":
            menu_konsultasi()
        elif pilihan == "4":
            menu_info()
        elif pilihan == "5":
            menu_psikolog()
        elif pilihan == "6":
            menu_jadwal()
        elif pilihan == "0":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
