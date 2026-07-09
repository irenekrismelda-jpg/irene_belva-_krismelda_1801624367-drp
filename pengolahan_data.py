# ============================================================
# Tugas 13: Pengolahan Data Sederhana
# Kelompok 15 - Aplikasi Konseling Psikologi
#
# Insight yang dikomputasi:
# 1. Jumlah konsultasi per kategori masalah
#    -> kategori masalah apa yang paling banyak dikonsultasikan
# 2. Rata-rata konsultasi per hari
# 3. Psikolog dengan jumlah booking terbanyak
# 4. Persentase status booking (dipesan/selesai/dibatalkan)
# ============================================================

import sqlite3

DB_NAME = "konseling.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ------------------------------------------------------------
# 1. Jumlah konsultasi per kategori masalah
# ------------------------------------------------------------
def konsultasi_per_kategori():
    conn = get_connection()
    rows = conn.execute("""
        SELECT km.nama_kategori, COUNT(k.id_konsultasi) AS jumlah
        FROM kategori_masalah km
        LEFT JOIN konsultasi k ON k.id_kategori = km.id_kategori
        GROUP BY km.id_kategori
        ORDER BY jumlah DESC
    """).fetchall()
    conn.close()

    print("\n--- Jumlah Konsultasi per Kategori Masalah ---")
    if not rows:
        print(">> Belum ada data kategori.")
        return
    for nama, jumlah in rows:
        print(f"{nama:<25} : {jumlah} konsultasi")
    print(f"\n>> Kategori paling banyak dikonsultasikan: {rows[0][0]} ({rows[0][1]} konsultasi)")


# ------------------------------------------------------------
# 2. Rata-rata konsultasi per hari
# ------------------------------------------------------------
def rata_rata_konsultasi_per_hari():
    conn = get_connection()
    hasil = conn.execute("""
        SELECT COUNT(*) * 1.0 / COUNT(DISTINCT DATE(tanggal))
        FROM konsultasi
    """).fetchone()[0]
    total = conn.execute("SELECT COUNT(*) FROM konsultasi").fetchone()[0]
    conn.close()

    print("\n--- Rata-rata Konsultasi per Hari ---")
    if not total:
        print(">> Belum ada data konsultasi.")
        return
    print(f"Total konsultasi : {total}")
    print(f"Rata-rata        : {hasil:.2f} konsultasi/hari")


# ------------------------------------------------------------
# 3. Psikolog dengan booking terbanyak
# ------------------------------------------------------------
def psikolog_terpopuler():
    conn = get_connection()
    rows = conn.execute("""
        SELECT ps.nama, COUNT(j.id_jadwal) AS jumlah
        FROM psikolog ps
        LEFT JOIN jadwal_konseling j ON j.id_psikolog = ps.id_psikolog
        GROUP BY ps.id_psikolog
        ORDER BY jumlah DESC
    """).fetchall()
    conn.close()

    print("\n--- Jumlah Booking per Psikolog ---")
    if not rows:
        print(">> Belum ada data psikolog.")
        return
    for nama, jumlah in rows:
        print(f"{nama:<25} : {jumlah} booking")
    print(f"\n>> Psikolog dengan booking terbanyak: {rows[0][0]} ({rows[0][1]} booking)")


# ------------------------------------------------------------
# 4. Persentase status booking
# ------------------------------------------------------------
def persentase_status_booking():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM jadwal_konseling").fetchone()[0]
    rows = conn.execute("""
        SELECT status_booking, COUNT(*)
        FROM jadwal_konseling
        GROUP BY status_booking
    """).fetchall()
    conn.close()

    print("\n--- Persentase Status Booking ---")
    if not total:
        print(">> Belum ada data jadwal konseling.")
        return
    for status, jumlah in rows:
        persen = jumlah / total * 100
        print(f"{status:<15} : {jumlah} ({persen:.1f}%)")


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------
def menu_pengolahan_data():
    while True:
        print("\n===== MENU PENGOLAHAN DATA =====")
        print("1. Jumlah konsultasi per kategori masalah")
        print("2. Rata-rata konsultasi per hari")
        print("3. Psikolog dengan booking terbanyak")
        print("4. Persentase status booking")
        print("0. Kembali")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            konsultasi_per_kategori()
        elif pilihan == "2":
            rata_rata_konsultasi_per_hari()
        elif pilihan == "3":
            psikolog_terpopuler()
        elif pilihan == "4":
            persentase_status_booking()
        elif pilihan == "0":
            break
        else:
            print(">> Pilihan tidak valid!")


if __name__ == "__main__":
    menu_pengolahan_data()
