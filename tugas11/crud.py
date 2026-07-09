"""
crud.py
Berisi fungsi Create, Read, Update, Delete untuk setiap entitas pada ERD.

Catatan sesuai instruksi Tugas 11:
- Kolom id_* (primary key)      -> otomatis (AUTOINCREMENT dari SQLite), TIDAK diminta dari user
- tanggal_daftar (Pengguna)      -> otomatis pakai datetime.now(), TIDAK diminta dari user
- tanggal (Konsultasi)           -> otomatis pakai datetime.now(), TIDAK diminta dari user
- tanggal_publish (Info Psikologis) -> otomatis pakai datetime.now(), TIDAK diminta dari user
- status (Konsultasi)            -> otomatis diisi default "Menunggu" saat create
- status_booking (Jadwal Konseling) -> otomatis diisi default "Menunggu Konfirmasi" saat create
- Kolom lain                     -> diminta dari user (lewat parameter fungsi/input())
"""

from datetime import datetime
from database import get_connection


def _now():
    """Helper untuk generate timestamp otomatis, menggantikan input manual dari user."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =========================================================
# 1. PENGGUNA
# =========================================================
def create_pengguna(nama, email, password, pekerjaan):
    conn = get_connection()
    conn.execute(
        """INSERT INTO pengguna (nama, email, password, pekerjaan, tanggal_daftar)
           VALUES (?, ?, ?, ?, ?)""",
        (nama, email, password, pekerjaan, _now())  # tanggal_daftar otomatis
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_pengguna(id_user=None):
    conn = get_connection()
    if id_user is None:
        rows = conn.execute("SELECT * FROM pengguna").fetchall()
    else:
        rows = conn.execute("SELECT * FROM pengguna WHERE id_user = ?", (id_user,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_pengguna(id_user, nama=None, email=None, password=None, pekerjaan=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM pengguna WHERE id_user = ?", (id_user,)).fetchone()
    if not current:
        conn.close()
        return False
    nama = nama if nama is not None else current["nama"]
    email = email if email is not None else current["email"]
    password = password if password is not None else current["password"]
    pekerjaan = pekerjaan if pekerjaan is not None else current["pekerjaan"]
    conn.execute(
        """UPDATE pengguna SET nama=?, email=?, password=?, pekerjaan=? WHERE id_user=?""",
        (nama, email, password, pekerjaan, id_user)
    )
    conn.commit()
    conn.close()
    return True


def delete_pengguna(id_user):
    conn = get_connection()
    conn.execute("DELETE FROM pengguna WHERE id_user = ?", (id_user,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0


# =========================================================
# 2. KATEGORI MASALAH
# =========================================================
def create_kategori(nama_kategori, deskripsi):
    conn = get_connection()
    conn.execute(
        "INSERT INTO kategori_masalah (nama_kategori, deskripsi) VALUES (?, ?)",
        (nama_kategori, deskripsi)
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_kategori(id_kategori=None):
    conn = get_connection()
    if id_kategori is None:
        rows = conn.execute("SELECT * FROM kategori_masalah").fetchall()
    else:
        rows = conn.execute("SELECT * FROM kategori_masalah WHERE id_kategori = ?", (id_kategori,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_kategori(id_kategori, nama_kategori=None, deskripsi=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM kategori_masalah WHERE id_kategori = ?", (id_kategori,)).fetchone()
    if not current:
        conn.close()
        return False
    nama_kategori = nama_kategori if nama_kategori is not None else current["nama_kategori"]
    deskripsi = deskripsi if deskripsi is not None else current["deskripsi"]
    conn.execute(
        "UPDATE kategori_masalah SET nama_kategori=?, deskripsi=? WHERE id_kategori=?",
        (nama_kategori, deskripsi, id_kategori)
    )
    conn.commit()
    conn.close()
    return True


def delete_kategori(id_kategori):
    conn = get_connection()
    conn.execute("DELETE FROM kategori_masalah WHERE id_kategori = ?", (id_kategori,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0


# =========================================================
# 3. KONSULTASI
# =========================================================
def create_konsultasi(id_user, isi_konsultasi, id_kategori):
    conn = get_connection()
    conn.execute(
        """INSERT INTO konsultasi (id_user, isi_konsultasi, id_kategori, tanggal, status)
           VALUES (?, ?, ?, ?, ?)""",
        (id_user, isi_konsultasi, id_kategori, _now(), "Menunggu")  # tanggal & status otomatis
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_konsultasi(id_konsultasi=None):
    conn = get_connection()
    if id_konsultasi is None:
        rows = conn.execute("SELECT * FROM konsultasi").fetchall()
    else:
        rows = conn.execute("SELECT * FROM konsultasi WHERE id_konsultasi = ?", (id_konsultasi,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_konsultasi(id_konsultasi, isi_konsultasi=None, id_kategori=None, status=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM konsultasi WHERE id_konsultasi = ?", (id_konsultasi,)).fetchone()
    if not current:
        conn.close()
        return False
    isi_konsultasi = isi_konsultasi if isi_konsultasi is not None else current["isi_konsultasi"]
    id_kategori = id_kategori if id_kategori is not None else current["id_kategori"]
    status = status if status is not None else current["status"]
    conn.execute(
        "UPDATE konsultasi SET isi_konsultasi=?, id_kategori=?, status=? WHERE id_konsultasi=?",
        (isi_konsultasi, id_kategori, status, id_konsultasi)
    )
    conn.commit()
    conn.close()
    return True


def delete_konsultasi(id_konsultasi):
    conn = get_connection()
    conn.execute("DELETE FROM konsultasi WHERE id_konsultasi = ?", (id_konsultasi,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0


# =========================================================
# 4. INFO PSIKOLOGIS
# =========================================================
def create_info(judul, isi_konten, id_kategori):
    conn = get_connection()
    conn.execute(
        """INSERT INTO info_psikologis (judul, isi_konten, id_kategori, tanggal_publish)
           VALUES (?, ?, ?, ?)""",
        (judul, isi_konten, id_kategori, _now())  # tanggal_publish otomatis
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_info(id_info=None):
    conn = get_connection()
    if id_info is None:
        rows = conn.execute("SELECT * FROM info_psikologis").fetchall()
    else:
        rows = conn.execute("SELECT * FROM info_psikologis WHERE id_info = ?", (id_info,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_info(id_info, judul=None, isi_konten=None, id_kategori=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM info_psikologis WHERE id_info = ?", (id_info,)).fetchone()
    if not current:
        conn.close()
        return False
    judul = judul if judul is not None else current["judul"]
    isi_konten = isi_konten if isi_konten is not None else current["isi_konten"]
    id_kategori = id_kategori if id_kategori is not None else current["id_kategori"]
    conn.execute(
        "UPDATE info_psikologis SET judul=?, isi_konten=?, id_kategori=? WHERE id_info=?",
        (judul, isi_konten, id_kategori, id_info)
    )
    conn.commit()
    conn.close()
    return True


def delete_info(id_info):
    conn = get_connection()
    conn.execute("DELETE FROM info_psikologis WHERE id_info = ?", (id_info,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0


# =========================================================
# 5. PSIKOLOG
# =========================================================
def create_psikolog(nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik):
    conn = get_connection()
    conn.execute(
        """INSERT INTO psikolog (nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik)
           VALUES (?, ?, ?, ?, ?)""",
        (nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik)
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_psikolog(id_psikolog=None):
    conn = get_connection()
    if id_psikolog is None:
        rows = conn.execute("SELECT * FROM psikolog").fetchall()
    else:
        rows = conn.execute("SELECT * FROM psikolog WHERE id_psikolog = ?", (id_psikolog,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_psikolog(id_psikolog, nama=None, spesialisasi=None, nomor_lisensi=None, kontak=None, lokasi_praktik=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM psikolog WHERE id_psikolog = ?", (id_psikolog,)).fetchone()
    if not current:
        conn.close()
        return False
    nama = nama if nama is not None else current["nama"]
    spesialisasi = spesialisasi if spesialisasi is not None else current["spesialisasi"]
    nomor_lisensi = nomor_lisensi if nomor_lisensi is not None else current["nomor_lisensi"]
    kontak = kontak if kontak is not None else current["kontak"]
    lokasi_praktik = lokasi_praktik if lokasi_praktik is not None else current["lokasi_praktik"]
    conn.execute(
        """UPDATE psikolog SET nama=?, spesialisasi=?, nomor_lisensi=?, kontak=?, lokasi_praktik=?
           WHERE id_psikolog=?""",
        (nama, spesialisasi, nomor_lisensi, kontak, lokasi_praktik, id_psikolog)
    )
    conn.commit()
    conn.close()
    return True


def delete_psikolog(id_psikolog):
    conn = get_connection()
    conn.execute("DELETE FROM psikolog WHERE id_psikolog = ?", (id_psikolog,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0


# =========================================================
# 6. JADWAL KONSELING
# =========================================================
def create_jadwal(id_psikolog, id_user, tanggal, jam):
    # tanggal & jam booking TETAP diminta dari user karena ini jadwal pilihan user,
    # bukan waktu sistem seperti tanggal_daftar/tanggal_publish
    conn = get_connection()
    conn.execute(
        """INSERT INTO jadwal_konseling (id_psikolog, id_user, tanggal, jam, status_booking)
           VALUES (?, ?, ?, ?, ?)""",
        (id_psikolog, id_user, tanggal, jam, "Menunggu Konfirmasi")  # status_booking otomatis
    )
    conn.commit()
    new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return new_id


def read_jadwal(id_jadwal=None):
    conn = get_connection()
    if id_jadwal is None:
        rows = conn.execute("SELECT * FROM jadwal_konseling").fetchall()
    else:
        rows = conn.execute("SELECT * FROM jadwal_konseling WHERE id_jadwal = ?", (id_jadwal,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_jadwal(id_jadwal, tanggal=None, jam=None, status_booking=None):
    conn = get_connection()
    current = conn.execute("SELECT * FROM jadwal_konseling WHERE id_jadwal = ?", (id_jadwal,)).fetchone()
    if not current:
        conn.close()
        return False
    tanggal = tanggal if tanggal is not None else current["tanggal"]
    jam = jam if jam is not None else current["jam"]
    status_booking = status_booking if status_booking is not None else current["status_booking"]
    conn.execute(
        "UPDATE jadwal_konseling SET tanggal=?, jam=?, status_booking=? WHERE id_jadwal=?",
        (tanggal, jam, status_booking, id_jadwal)
    )
    conn.commit()
    conn.close()
    return True


def delete_jadwal(id_jadwal):
    conn = get_connection()
    conn.execute("DELETE FROM jadwal_konseling WHERE id_jadwal = ?", (id_jadwal,))
    conn.commit()
    changed = conn.total_changes
    conn.close()
    return changed > 0
