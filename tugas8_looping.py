def tampilkan_papan_catur():
    print("\n=== Layout Papan Catur (8x8) ===")
    ukuran = 8

    for baris in range(ukuran):
        baris_papan = ""
        for kolom in range(ukuran):
            if (baris + kolom) % 2 == 0:
                baris_papan += "⬜"
            else:
                baris_papan += "⬛"
        print(baris_papan)


def catat_aktivitas():
    print("\n=== Pencatat Aktivitas Harian ===")
    print("Ketik 'selesai' pada nama aktivitas jika sudah tidak ingin menambah data.\n")

    daftar_aktivitas = []

    while True:
        nama_aktivitas = input("Masukkan aktivitas: ").strip()

        if nama_aktivitas.lower() == "selesai":
            break

        if nama_aktivitas == "":
            print("Aktivitas tidak boleh kosong, coba lagi.")
            continue

        prioritas = input("Masukkan tingkat prioritas (Tinggi/Sedang/Rendah): ").strip().title()
        durasi = input("Perkiraan durasi aktivitas (misal: 30 menit, 2 jam): ").strip()

        aktivitas = {
            "nama": nama_aktivitas,
            "prioritas": prioritas,
            "durasi": durasi
        }
        daftar_aktivitas.append(aktivitas)
        print(f"'{nama_aktivitas}' berhasil ditambahkan.\n")

    print("\n=== Daftar Aktivitas Kamu ===")

    if len(daftar_aktivitas) == 0:
        print("Belum ada aktivitas yang tercatat.")
        return

    for nomor, aktivitas in enumerate(daftar_aktivitas, start=1):
        print(f"{nomor}. {aktivitas['nama']}")
        print(f"   Prioritas : {aktivitas['prioritas']}")
        print(f"   Durasi    : {aktivitas['durasi']}")

    total_tinggi = sum(1 for a in daftar_aktivitas if a["prioritas"] == "Tinggi")
    print(f"\nTotal aktivitas: {len(daftar_aktivitas)}")
    print(f"Jumlah aktivitas prioritas Tinggi: {total_tinggi}")


def main():
    tampilkan_papan_catur()
    catat_aktivitas()


if __name__ == "__main__":
    main()
