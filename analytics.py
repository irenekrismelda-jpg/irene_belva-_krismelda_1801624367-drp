"""
analytics.py
Implementasi fitur Pengolahan Data Sederhana (Tugas 13).

Modul ini mengolah data yang sudah tersimpan di basis data aplikasi
Konsultasi Psikologi menjadi beberapa insight/kesimpulan sederhana:

1. statistik_konsultasi_per_kategori()
   -> Menghitung jumlah konsultasi per kategori masalah, untuk mengetahui
      kategori masalah apa yang paling banyak dikeluhkan pengguna.

2. statistik_status_konsultasi()
   -> Menghitung jumlah dan persentase konsultasi berdasarkan status
      (Menunggu / Diproses / Selesai), untuk mengukur kinerja penanganan
      konsultasi oleh psikolog/admin.

3. rata_rata_konsultasi_per_hari()
   -> Menghitung rata-rata jumlah konsultasi yang masuk per hari,
      dihitung dari rentang tanggal konsultasi pertama sampai terakhir.

4. ranking_psikolog_terbooking()
   -> Meranking psikolog berdasarkan jumlah booking pada jadwal_konseling,
      untuk mengetahui psikolog yang paling diminati.

5. pertumbuhan_pengguna_per_bulan()
   -> Menghitung jumlah pengguna baru yang mendaftar per bulan,
      untuk melihat tren pertumbuhan jumlah pengguna aplikasi.
"""

from collections import Counter, defaultdict
from datetime import datetime
from database import get_connection


# =========================================================
# 1. STATISTIK KONSULTASI PER KATEGORI MASALAH
# =========================================================
def statistik_konsultasi_per_kategori():
    """
    Mengembalikan list of dict berisi nama_kategori dan jumlah_konsultasi,
    diurutkan dari yang paling banyak.
    Konsultasi tanpa kategori (id_kategori NULL) dikelompokkan sebagai
    "Tanpa Kategori".
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT COALESCE(k.nama_kategori, 'Tanpa Kategori') AS nama_kategori,
               COUNT(kon.id_konsultasi) AS jumlah_konsultasi
        FROM konsultasi kon
        LEFT JOIN kategori_masalah k ON kon.id_kategori = k.id_kategori
        GROUP BY nama_kategori
        ORDER BY jumlah_konsultasi DESC
        """
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =========================================================
# 2. STATISTIK STATUS KONSULTASI (+ PERSENTASE)
# =========================================================
def statistik_status_konsultasi():
    """
    Mengembalikan dict:
    {
        "total": int,
        "detail": [
            {"status": "Menunggu", "jumlah": 5, "persentase": 41.67},
            ...
        ]
    }
    """
    conn = get_connection()
    rows = conn.execute(
        "SELECT status, COUNT(*) AS jumlah FROM konsultasi GROUP BY status ORDER BY jumlah DESC"
    ).fetchall()
    conn.close()

    total = sum(r["jumlah"] for r in rows)
    detail = []
    for r in rows:
        persentase = (r["jumlah"] / total * 100) if total > 0 else 0
        detail.append({
            "status": r["status"],
            "jumlah": r["jumlah"],
            "persentase": round(persentase, 2)
        })

    return {"total": total, "detail": detail}


# =========================================================
# 3. RATA-RATA KONSULTASI MASUK PER HARI
# =========================================================
def rata_rata_konsultasi_per_hari():
    """
    Menghitung rata-rata jumlah konsultasi yang masuk per hari,
    dihitung dari selisih tanggal konsultasi paling awal sampai
    paling akhir yang tercatat di database.

    Mengembalikan dict:
    {
        "total_konsultasi": int,
        "tanggal_pertama": str,
        "tanggal_terakhir": str,
        "jumlah_hari": int,
        "rata_rata_per_hari": float
    }
    Mengembalikan None jika belum ada data konsultasi.
    """
    conn = get_connection()
    rows = conn.execute("SELECT tanggal FROM konsultasi").fetchall()
    conn.close()

    if not rows:
        return None

    tanggal_list = []
    for r in rows:
        # tanggal disimpan format "%Y-%m-%d %H:%M:%S", ambil bagian tanggalnya saja
        tgl_str = r["tanggal"].split(" ")[0]
        tanggal_list.append(datetime.strptime(tgl_str, "%Y-%m-%d"))

    tanggal_pertama = min(tanggal_list)
    tanggal_terakhir = max(tanggal_list)
    jumlah_hari = (tanggal_terakhir - tanggal_pertama).days + 1  # inklusif
    total_konsultasi = len(rows)
    rata_rata = total_konsultasi / jumlah_hari

    return {
        "total_konsultasi": total_konsultasi,
        "tanggal_pertama": tanggal_pertama.strftime("%Y-%m-%d"),
        "tanggal_terakhir": tanggal_terakhir.strftime("%Y-%m-%d"),
        "jumlah_hari": jumlah_hari,
        "rata_rata_per_hari": round(rata_rata, 2)
    }


# =========================================================
# 4. RANKING PSIKOLOG BERDASARKAN JUMLAH BOOKING
# =========================================================
def ranking_psikolog_terbooking(limit=None):
    """
    Meranking psikolog berdasarkan jumlah booking (jadwal_konseling)
    yang diterima, dari yang paling banyak.

    Parameter:
        limit -> jika diisi, hanya mengembalikan N psikolog teratas.

    Mengembalikan list of dict:
    [{"nama": ..., "spesialisasi": ..., "jumlah_booking": ...}, ...]
    """
    conn = get_connection()
    query = """
        SELECT p.nama, p.spesialisasi, COUNT(j.id_jadwal) AS jumlah_booking
        FROM psikolog p
        LEFT JOIN jadwal_konseling j ON p.id_psikolog = j.id_psikolog
        GROUP BY p.id_psikolog
        ORDER BY jumlah_booking DESC
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    hasil = [dict(r) for r in rows]
    if limit is not None:
        hasil = hasil[:limit]
    return hasil


# =========================================================
# 5. PERTUMBUHAN JUMLAH PENGGUNA PER BULAN
# =========================================================
def pertumbuhan_pengguna_per_bulan():
    """
    Menghitung jumlah pengguna baru yang mendaftar tiap bulan
    (berdasarkan tanggal_daftar), diurutkan secara kronologis.

    Mengembalikan list of dict:
    [{"bulan": "2026-06", "jumlah_pengguna_baru": 3}, ...]
    """
    conn = get_connection()
    rows = conn.execute("SELECT tanggal_daftar FROM pengguna").fetchall()
    conn.close()

    if not rows:
        return []

    counter = Counter()
    for r in rows:
        bulan = r["tanggal_daftar"].split(" ")[0][:7]  # ambil "YYYY-MM"
        counter[bulan] += 1

    hasil = [
        {"bulan": bulan, "jumlah_pengguna_baru": jumlah}
        for bulan, jumlah in sorted(counter.items())
    ]
    return hasil


# =========================================================
# RINGKASAN GABUNGAN
# =========================================================
def ringkasan_lengkap():
    """
    Mengembalikan dict berisi seluruh insight sekaligus,
    supaya bisa ditampilkan sebagai satu laporan utuh.
    """
    return {
        "konsultasi_per_kategori": statistik_konsultasi_per_kategori(),
        "status_konsultasi": statistik_status_konsultasi(),
        "rata_rata_konsultasi_per_hari": rata_rata_konsultasi_per_hari(),
        "ranking_psikolog": ranking_psikolog_terbooking(),
        "pertumbuhan_pengguna": pertumbuhan_pengguna_per_bulan(),
    }
