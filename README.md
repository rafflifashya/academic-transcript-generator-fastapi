# Sistem Manajemen Nilai & Transkrip Akademik (UAS)

Project ini dikembangkan untuk memenuhi kriteria UAS Modul Nilai & Transkrip. Sistem ini mengelola input nilai mahasiswa, perhitungan IPK otomatis, hingga pelacakan audit perubahan data.

## Identitas Mahasiswa
- **Nama**: Raffli Islami Fashya
- **NIM**: 24360003

## Fitur Utama
Sistem ini dibangun berdasarkan spesifikasi teknis berikut:
* [cite_start]**Grade Management (30%)**: Konversi nilai huruf (A-E) ke angka bobot (4.0-0.0)[cite: 10, 11].
* [cite_start]**GPA Calculator (30%)**: Menghitung IPK dengan aturan $IPK = \Sigma(SKS \times Nilai~Angka) / \Sigma(SKS)$[cite: 12, 13, 27].
* **Business Rules (10%)**: 
    * [cite_start]Presensi mahasiswa wajib $\ge 75\%$ untuk penginputan nilai[cite: 20].
    * [cite_start]Hanya menghitung MK yang sudah lulus (nilai $\ge$ D)[cite: 28].
    * [cite_start]Mengambil nilai tertinggi jika mata kuliah diulang[cite: 29].
* [cite_start]**PDF Generator (25%)**: Struktur transkrip mencakup header logo, tabel nilai per semester, dan predikat kelulusan (Cum Laude, dll)[cite: 15, 17, 23, 40].
* [cite_start]**Audit Trail**: Melacak riwayat perubahan nilai mahasiswa (ID, lama, baru, pengubah, waktu, alasan)[cite: 42, 43, 44].

## Tech Stack
* **Framework**: FastAPI
* **Data Validation**: Pydantic
* **Documentation**: Swagger UI (OpenAPI)

## Cara Menjalankan
1. Clone repositori ini.
2. Install dependencies: `pip install fastapi uvicorn`.
3. Jalankan server: `uvicorn main:app --reload`.
4. Buka Swagger UI di: `http://127.0.0.1:8000/docs`.

## Kriteria Sukses Terpenuhi
- [x] [cite_start]Input nilai via form web/API[cite: 46].
- [x] [cite_start]IPK ter-update otomatis[cite: 47].
- [x] [cite_start]Audit trail lengkap untuk setiap perubahan[cite: 49].
