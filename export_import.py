# ============================================================
# Tugas 12: Implementasi Fitur Export/Import Data JSON
# Kelompok 15 - Aplikasi Konseling Psikologi
# ============================================================

import json
import sqlite3
from datetime import datetime

DB_NAME = "konseling.db"

# Daftar tabel yang akan di-export/import
TABEL = [
    "pengguna",
    "psikolog",
    "kategori_masalah",
    "konsultasi",
    "jadwal_konseling",
    "info_psikologis",
]


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ------------------------------------------------------------
# EXPORT: Database -> File JSON
# ------------------------------------------------------------
def export_json():
    conn = get_connection()
    conn.row_factory = sqlite3.Row  # supaya hasil query bisa jadi dictionary

    data = {}
    for tabel in TABEL:
        rows = conn.execute(f"SELECT * FROM {tabel}").fetchall()
        data[tabel] = [dict(row) for row in rows]
    conn.close()

    nama_file = input("Nama file export (enter = otomatis): ").strip()
    if not nama_file:
        nama_file = "export_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    if not nama_file.endswith(".json"):
        nama_file += ".json"

    with open(nama_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    total = sum(len(records) for records in data.values())
    print(f">> Export berhasil! {total} record tersimpan di '{nama_file}'")


# ------------------------------------------------------------
# IMPORT: File JSON -> Database
# ------------------------------------------------------------
def import_json():
    nama_file = input("Nama file JSON yang mau di-import: ").strip()

    try:
        with open(nama_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f">> File '{nama_file}' tidak ditemukan.")
        return
    except json.JSONDecodeError:
        print(">> File bukan JSON yang valid.")
        return

    conn = get_connection()
    total_masuk = 0
    total_lewat = 0

    for tabel in TABEL:
        records = data.get(tabel, [])
        for record in records:
            kolom = ", ".join(record.keys())
            tanda = ", ".join("?" for _ in record)
            try:
                # INSERT OR IGNORE: record dengan id yang sudah ada akan dilewati
                cur = conn.execute(
                    f"INSERT OR IGNORE INTO {tabel} ({kolom}) VALUES ({tanda})",
                    tuple(record.values()),
                )
                if cur.rowcount:
                    total_masuk += 1
                else:
                    total_lewat += 1
            except sqlite3.Error as e:
                print(f">> Gagal import record di tabel {tabel}: {e}")

    conn.commit()
    conn.close()
    print(f">> Import selesai! {total_masuk} record masuk, {total_lewat} dilewati (sudah ada).")


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------
def menu_export_import():
    while True:
        print("\n===== MENU EXPORT/IMPORT JSON =====")
        print("1. Export data ke file JSON")
        print("2. Import data dari file JSON")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            export_json()
        elif pilihan == "2":
            import_json()
        elif pilihan == "0":
            break
        else:
            print(">> Pilihan tidak valid!")


if __name__ == "__main__":
    menu_export_import()
