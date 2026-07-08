"""
Tugas 7 - If Statement
Aplikasi Manajemen Aktivitas Sederhana
"""

from datetime import datetime

def cek_sarapan():
    bahan_tersedia = ["telur", "ikan", "nugget"]

    print("\n--- MENU SARAPAN ---")
    menu = input("Menu sarapan apa yang kamu inginkan? ").strip().lower()

    if menu in bahan_tersedia:
        print(f"\n[INFO] Bahan '{menu}' tersedia di lokasi kamu.")
        print(f"[PROSES] Sedang memasak {menu}...")
        print(f"[SELESAI] {menu.capitalize()} siap disantap. Selamat sarapan!")
    else:
        print(f"\n[INFO] Bahan '{menu}' tidak tersedia di lokasi kamu.")
        print(f"[TINDAKAN] Kamu perlu membeli bahan '{menu}' terlebih dahulu sebelum bisa memasaknya.")


def cek_berangkat_kerja():
    jam_masuk = datetime.strptime("08:00", "%H:%M").time()
    waktu_sekarang = datetime.now()
    jam_sekarang = waktu_sekarang.time()

    print("\n--- CEK JADWAL KERJA ---")
    print(f"Waktu sekarang: {waktu_sekarang.strftime('%H:%M:%S')}")
    print("Jadwal masuk kerja: 08:00")

    if jam_sekarang > jam_masuk:
        selisih = datetime.combine(waktu_sekarang.date(), jam_sekarang) - datetime.combine(waktu_sekarang.date(), jam_masuk)
        menit_terlambat = int(selisih.total_seconds() // 60)
        print(f"[PERINGATAN] Kamu SUDAH TERLAMBAT sekitar {menit_terlambat} menit. Segera berangkat!")
    elif jam_sekarang == jam_masuk:
        print("[NOTIFIKASI] Ini waktunya tepat jam masuk kerja. Segera berangkat sekarang!")
    else:
        selisih = datetime.combine(waktu_sekarang.date(), jam_masuk) - datetime.combine(waktu_sekarang.date(), jam_sekarang)
        menit_tersisa = int(selisih.total_seconds() // 60)
        print(f"[NOTIFIKASI] Kamu masih punya waktu sekitar {menit_tersisa} menit sebelum jam masuk kerja. Aman!")


def main():
    print("=== APLIKASI MANAJEMEN AKTIVITAS SEDERHANA ===")
    print("Aktivitas yang tersedia: sarapan, berangkat kerja")

    aktivitas = input("\nAktivitas apa yang ingin kamu lakukan? ").strip().lower()

    if aktivitas == "sarapan":
        cek_sarapan()
    elif aktivitas in ["berangkat kerja", "kerja", "berangkat"]:
        cek_berangkat_kerja()
    else:
        print(f"\n[INFO] Aktivitas '{aktivitas}' belum dikenali oleh sistem.")
        print("[SARAN] Coba ketik 'sarapan' atau 'berangkat kerja'.")

    print("\n=== PROGRAM SELESAI ===")


if __name__ == "__main__":
    main()
