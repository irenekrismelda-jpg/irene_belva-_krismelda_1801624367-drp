"""
database.py
Membuat koneksi ke SQLite dan membuat semua tabel sesuai ERD Tugas 10
Kelompok 15 - Aplikasi Konsultasi Psikologi
"""

import sqlite3

DB_NAME = "konsultasi_psikologi.db"


def get_connection():
    """Membuka koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")  # aktifkan constraint foreign key
    conn.row_factory = sqlite3.Row  # supaya hasil query bisa diakses seperti dict
    return conn


def create_tables():
    """Membuat seluruh tabel sesuai ERD (jika belum ada)."""
    conn = get_connection()
    cur = conn.cursor()

    # 1. Tabel Pengguna
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

    # 2. Tabel Kategori Masalah
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kategori_masalah (
            id_kategori INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kategori TEXT NOT NULL,
            deskripsi TEXT
        )
    """)

    # 3. Tabel Konsultasi (FK ke pengguna & kategori_masalah)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS konsultasi (
            id_konsultasi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            isi_konsultasi TEXT NOT NULL,
            id_kategori INTEGER,
            tanggal TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES pengguna(id_user) ON DELETE CASCADE,
            FOREIGN KEY (id_kategori) REFERENCES kategori_masalah(id_kategori) ON DELETE SET NULL
        )
    """)

    # 4. Tabel Info Psikologis (kategori mengacu ke kategori_masalah)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS info_psikologis (
            id_info INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            isi_konten TEXT NOT NULL,
            id_kategori INTEGER,
            tanggal_publish TEXT NOT NULL,
            FOREIGN KEY (id_kategori) REFERENCES kategori_masalah(id_kategori) ON DELETE SET NULL
        )
    """)

    # 5. Tabel Psikolog
    cur.execute("""
        CREATE TABLE IF NOT EXISTS psikolog (
            id_psikolog INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            spesialisasi TEXT,
            nomor_lisensi TEXT NOT NULL UNIQUE,
            kontak TEXT,
            lokasi_praktik TEXT
        )
    """)

    # 6. Tabel Jadwal Konseling (FK ke psikolog & pengguna)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jadwal_konseling (
            id_jadwal INTEGER PRIMARY KEY AUTOINCREMENT,
            id_psikolog INTEGER NOT NULL,
            id_user INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            jam TEXT NOT NULL,
            status_booking TEXT NOT NULL,
            FOREIGN KEY (id_psikolog) REFERENCES psikolog(id_psikolog) ON DELETE CASCADE,
            FOREIGN KEY (id_user) REFERENCES pengguna(id_user) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print(f"Database '{DB_NAME}' dan semua tabel berhasil dibuat.")
