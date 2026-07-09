# ============================================================
# Tugas 11: Implementasi CRUD menggunakan SQLite
# Kelompok 15 - Aplikasi Konseling Psikologi
# Jesse Martua Alesika (1801624243)
# Nayla Putri Anandhita (1801624350)
# Irene Belva Krismelda (1801624367)
# ============================================================

import sqlite3
from datetime import datetime

from export_import import menu_export_import      # Tugas 12
from pengolahan_data import menu_pengolahan_data  # Tugas 13

DB_NAME = "konseling.db"


# ------------------------------------------------------------
# SETUP DATABASE
# ------------------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pengguna (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            pekerjaan TEXT,
            tanggal_daftar TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS psikolog (
            id_psikolog INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            spesialisasi TEXT,
            nomor_lisensi TEXT,
            kontak TEXT,
            lokasi_praktik TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kategori_masalah (
            id_kategori INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kategori TEXT NOT NULL,
            deskripsi TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS konsultasi (
            id_konsultasi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            isi_konsultasi TEXT NOT NULL,
            id_kategori INTEGER,
            tanggal TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'menunggu',
            FOREIGN KEY (id_user) REFERENCES pengguna(id_user),
            FOREIGN KEY (id_kategori) REFERENCES kategori_masalah(id_kategori)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS jadwal_konseling (
            id_jadwal INTEGER PRIMARY KEY AUTOINCREMENT,
            id_psikolog INTEGER NOT NULL,
            id_user INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            jam TEXT NOT NULL,
            status_booking TEXT NOT NULL DEFAULT 'dipesan',
            FOREIGN KEY (id_psikolog) REFERENCES psikolog(id_psikolog),
            FOREIGN KEY (id_user) REFERENCES pengguna(id_user)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS info_psikologis (
            id_info INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            isi_konten TEXT,
            id_kategori INTEGER,
            tanggal_publish TEXT NOT NULL,
            FOREIGN KEY (id_kategori) REFERENCES kategori_masalah(id_kategori)
        )
    """)

    conn.commit()
    conn.close()


# ------------------------------------------------------------
# UTILITAS
# ------------------------------------------------------------
def tampilkan_tabel(rows, headers):
    if not rows:
        print(">> Data masih kosong.")
        return
    print("-" * 80)
    print(" | ".join(headers))
    print("-" * 80)
    for row in rows:
        print(" | ".join(str(kolom) for kolom in row))
    print("-" * 80)


def input_angka(pesan):
    while True:
        try:
            return int(input(pesan))
        except ValueError:
            print(">> Masukkan angka yang valid!")


# ------------------------------------------------------------
# CRUD PENGGUNA
# ------------------------------------------------------------
def create_pengguna():
    nama = input("Nama: ")
    email = input("Email: ")
    password = input("Password: ")
    pekerjaan = input("Pekerjaan: ")
    tanggal_daftar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # otomatis

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO pengguna (nama, email, password, pekerjaan, tanggal_daftar) VALUES (?, ?, ?, ?, ?)",
            (nama, email, password, pekerjaan, tanggal_daftar),
        )
        conn.commit()
        print(">> Pengguna berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        print(">> Gagal: email sudah terdaftar.")
    conn.close()


def read_pengguna():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM pengguna").fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "Nama", "Email", "Password", "Pekerjaan", "Tgl Daftar"])


def update_pengguna():
    read_pengguna()
    id_user = input_angka("ID pengguna yang mau diubah: ")
    nama = input("Nama baru: ")
    email = input("Email baru: ")
    pekerjaan = input("Pekerjaan baru: ")

    conn = get_connection()
    cur = conn.execute(
        "UPDATE pengguna SET nama = ?, email = ?, pekerjaan = ? WHERE id_user = ?",
        (nama, email, pekerjaan, id_user),
    )
    conn.commit()
    conn.close()
    print(">> Data berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_pengguna():
    read_pengguna()
    id_user = input_angka("ID pengguna yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM pengguna WHERE id_user = ?", (id_user,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# CRUD PSIKOLOG
# ------------------------------------------------------------
def create_psikolog():
    nama = input("Nama: ")
    spesialisasi = input("Spesialisasi: ")
    nomor_lisensi = input("Nomor lisensi: ")
    kontak = input("Kontak: ")
    lokasi_praktik = input("Lokasi praktik: ")

    conn = get_connection()
    conn.execute(
        "INSERT INTO psikolog (nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik) VALUES (?, ?, ?, ?, ?)",
        (nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik),
    )
    conn.commit()
    conn.close()
    print(">> Psikolog berhasil ditambahkan!")


def read_psikolog():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM psikolog").fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "Nama", "Spesialisasi", "No Lisensi", "Kontak", "Lokasi"])


def update_psikolog():
    read_psikolog()
    id_psikolog = input_angka("ID psikolog yang mau diubah: ")
    spesialisasi = input("Spesialisasi baru: ")
    kontak = input("Kontak baru: ")
    lokasi_praktik = input("Lokasi praktik baru: ")

    conn = get_connection()
    cur = conn.execute(
        "UPDATE psikolog SET spesialisasi = ?, kontak = ?, lokasi_praktik = ? WHERE id_psikolog = ?",
        (spesialisasi, kontak, lokasi_praktik, id_psikolog),
    )
    conn.commit()
    conn.close()
    print(">> Data berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_psikolog():
    read_psikolog()
    id_psikolog = input_angka("ID psikolog yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM psikolog WHERE id_psikolog = ?", (id_psikolog,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# CRUD KATEGORI MASALAH
# ------------------------------------------------------------
def create_kategori():
    nama_kategori = input("Nama kategori: ")
    deskripsi = input("Deskripsi: ")
    conn = get_connection()
    conn.execute(
        "INSERT INTO kategori_masalah (nama_kategori, deskripsi) VALUES (?, ?)",
        (nama_kategori, deskripsi),
    )
    conn.commit()
    conn.close()
    print(">> Kategori berhasil ditambahkan!")


def read_kategori():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM kategori_masalah").fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "Nama Kategori", "Deskripsi"])


def update_kategori():
    read_kategori()
    id_kategori = input_angka("ID kategori yang mau diubah: ")
    nama_kategori = input("Nama kategori baru: ")
    deskripsi = input("Deskripsi baru: ")
    conn = get_connection()
    cur = conn.execute(
        "UPDATE kategori_masalah SET nama_kategori = ?, deskripsi = ? WHERE id_kategori = ?",
        (nama_kategori, deskripsi, id_kategori),
    )
    conn.commit()
    conn.close()
    print(">> Data berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_kategori():
    read_kategori()
    id_kategori = input_angka("ID kategori yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM kategori_masalah WHERE id_kategori = ?", (id_kategori,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# CRUD KONSULTASI
# ------------------------------------------------------------
def create_konsultasi():
    read_pengguna()
    id_user = input_angka("ID user: ")
    isi_konsultasi = input("Isi konsultasi: ")
    read_kategori()
    id_kategori = input_angka("ID kategori masalah: ")
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # otomatis
    status = "menunggu"  # otomatis

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO konsultasi (id_user, isi_konsultasi, id_kategori, tanggal, status) VALUES (?, ?, ?, ?, ?)",
            (id_user, isi_konsultasi, id_kategori, tanggal, status),
        )
        conn.commit()
        print(">> Konsultasi berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        print(">> Gagal: ID user / kategori tidak ditemukan.")
    conn.close()


def read_konsultasi():
    conn = get_connection()
    rows = conn.execute("""
        SELECT k.id_konsultasi, p.nama, k.isi_konsultasi, km.nama_kategori, k.tanggal, k.status
        FROM konsultasi k
        JOIN pengguna p ON k.id_user = p.id_user
        LEFT JOIN kategori_masalah km ON k.id_kategori = km.id_kategori
    """).fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "User", "Isi", "Kategori", "Tanggal", "Status"])


def update_konsultasi():
    read_konsultasi()
    id_konsultasi = input_angka("ID konsultasi yang mau diubah: ")
    status = input("Status baru (menunggu/diproses/selesai): ")
    conn = get_connection()
    cur = conn.execute(
        "UPDATE konsultasi SET status = ? WHERE id_konsultasi = ?",
        (status, id_konsultasi),
    )
    conn.commit()
    conn.close()
    print(">> Status berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_konsultasi():
    read_konsultasi()
    id_konsultasi = input_angka("ID konsultasi yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM konsultasi WHERE id_konsultasi = ?", (id_konsultasi,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# CRUD JADWAL KONSELING
# ------------------------------------------------------------
def create_jadwal():
    read_psikolog()
    id_psikolog = input_angka("ID psikolog: ")
    read_pengguna()
    id_user = input_angka("ID user: ")
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    jam = input("Jam (HH:MM): ")
    status_booking = "dipesan"  # otomatis

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO jadwal_konseling (id_psikolog, id_user, tanggal, jam, status_booking) VALUES (?, ?, ?, ?, ?)",
            (id_psikolog, id_user, tanggal, jam, status_booking),
        )
        conn.commit()
        print(">> Jadwal berhasil ditambahkan!")
    except sqlite3.IntegrityError:
        print(">> Gagal: ID psikolog / user tidak ditemukan.")
    conn.close()


def read_jadwal():
    conn = get_connection()
    rows = conn.execute("""
        SELECT j.id_jadwal, ps.nama, p.nama, j.tanggal, j.jam, j.status_booking
        FROM jadwal_konseling j
        JOIN psikolog ps ON j.id_psikolog = ps.id_psikolog
        JOIN pengguna p ON j.id_user = p.id_user
    """).fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "Psikolog", "User", "Tanggal", "Jam", "Status"])


def update_jadwal():
    read_jadwal()
    id_jadwal = input_angka("ID jadwal yang mau diubah: ")
    status_booking = input("Status baru (dipesan/selesai/dibatalkan): ")
    conn = get_connection()
    cur = conn.execute(
        "UPDATE jadwal_konseling SET status_booking = ? WHERE id_jadwal = ?",
        (status_booking, id_jadwal),
    )
    conn.commit()
    conn.close()
    print(">> Status berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_jadwal():
    read_jadwal()
    id_jadwal = input_angka("ID jadwal yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM jadwal_konseling WHERE id_jadwal = ?", (id_jadwal,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# CRUD INFO PSIKOLOGIS
# ------------------------------------------------------------
def create_info():
    judul = input("Judul: ")
    isi_konten = input("Isi konten: ")
    read_kategori()
    id_kategori = input_angka("ID kategori: ")
    tanggal_publish = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # otomatis

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO info_psikologis (judul, isi_konten, id_kategori, tanggal_publish) VALUES (?, ?, ?, ?)",
            (judul, isi_konten, id_kategori, tanggal_publish),
        )
        conn.commit()
        print(">> Info berhasil dipublikasikan!")
    except sqlite3.IntegrityError:
        print(">> Gagal: ID kategori tidak ditemukan.")
    conn.close()


def read_info():
    conn = get_connection()
    rows = conn.execute("""
        SELECT i.id_info, i.judul, i.isi_konten, km.nama_kategori, i.tanggal_publish
        FROM info_psikologis i
        LEFT JOIN kategori_masalah km ON i.id_kategori = km.id_kategori
    """).fetchall()
    conn.close()
    tampilkan_tabel(rows, ["ID", "Judul", "Isi", "Kategori", "Tgl Publish"])


def update_info():
    read_info()
    id_info = input_angka("ID info yang mau diubah: ")
    judul = input("Judul baru: ")
    isi_konten = input("Isi konten baru: ")
    conn = get_connection()
    cur = conn.execute(
        "UPDATE info_psikologis SET judul = ?, isi_konten = ? WHERE id_info = ?",
        (judul, isi_konten, id_info),
    )
    conn.commit()
    conn.close()
    print(">> Data berhasil diubah!" if cur.rowcount else ">> ID tidak ditemukan.")


def delete_info():
    read_info()
    id_info = input_angka("ID info yang mau dihapus: ")
    conn = get_connection()
    cur = conn.execute("DELETE FROM info_psikologis WHERE id_info = ?", (id_info,))
    conn.commit()
    conn.close()
    print(">> Data berhasil dihapus!" if cur.rowcount else ">> ID tidak ditemukan.")


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------
def menu_crud(nama_tabel, fungsi_create, fungsi_read, fungsi_update, fungsi_delete):
    while True:
        print(f"\n===== MENU {nama_tabel.upper()} =====")
        print("1. Tambah data (Create)")
        print("2. Lihat data (Read)")
        print("3. Ubah data (Update)")
        print("4. Hapus data (Delete)")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            fungsi_create()
        elif pilihan == "2":
            fungsi_read()
        elif pilihan == "3":
            fungsi_update()
        elif pilihan == "4":
            fungsi_delete()
        elif pilihan == "0":
            break
        else:
            print(">> Pilihan tidak valid!")


def main():
    setup_database()
    while True:
        print("\n========================================")
        print("   APLIKASI KONSELING PSIKOLOGI")
        print("   Kelompok 15")
        print("========================================")
        print("1. Kelola Pengguna")
        print("2. Kelola Psikolog")
        print("3. Kelola Kategori Masalah")
        print("4. Kelola Konsultasi")
        print("5. Kelola Jadwal Konseling")
        print("6. Kelola Info Psikologis")
        print("7. Export/Import Data (JSON)")
        print("8. Pengolahan Data")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            menu_crud("Pengguna", create_pengguna, read_pengguna, update_pengguna, delete_pengguna)
        elif pilihan == "2":
            menu_crud("Psikolog", create_psikolog, read_psikolog, update_psikolog, delete_psikolog)
        elif pilihan == "3":
            menu_crud("Kategori Masalah", create_kategori, read_kategori, update_kategori, delete_kategori)
        elif pilihan == "4":
            menu_crud("Konsultasi", create_konsultasi, read_konsultasi, update_konsultasi, delete_konsultasi)
        elif pilihan == "5":
            menu_crud("Jadwal Konseling", create_jadwal, read_jadwal, update_jadwal, delete_jadwal)
        elif pilihan == "6":
            menu_crud("Info Psikologis", create_info, read_info, update_info, delete_info)
        elif pilihan == "7":
            menu_export_import()
        elif pilihan == "8":
            menu_pengolahan_data()
        elif pilihan == "0":
            print("Terima kasih! Program selesai.")
            break
        else:
            print(">> Pilihan tidak valid!")


if __name__ == "__main__":
    main()
