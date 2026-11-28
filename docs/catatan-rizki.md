# Catatan Rizki

Bagian: aturan kelayakan, parameter, dan kejujuran data medis.
Dokumen sumber: Permenkes No. 91 Tahun 2015 tentang Standar Pelayanan Transfusi Darah (Berita Negara RI 2016 No. 36)
Diverifikasi oleh: Rizki Amalina Harahap, dibaca dari PDF resmi dengan bantuan Claude (AI)
Tanggal verifikasi: 27 November 2026

## Verifikasi parameter (R-2)

| Parameter | Satuan | Nilai demo | Nilai resmi | Sumber (pasal/halaman) | Status |
|---|---|---|---|---|---|
| usia_minimal | tahun | 17 | 17 | Lampiran Bab III 3.2.2 C.1, hal. 56 | terverifikasi |
| usia_maksimal | tahun | 60 | tidak ada batas tunggal | Lampiran Bab III 3.2.2 C.1, hal. 56 | tetap demo |
| berat_minimal | kg | 45 | 55 (450 mL) atau 45 (350 mL) | Lampiran Bab III 3.2.2 C.1, hal. 56-57 | tetap demo |
| hb_minimal | g/dL | 12.5 | 12,5 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| hb_maksimal | g/dL | 17.0 | 17 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| sistolik_minimal | mmHg | 90 | 90 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| sistolik_maksimal | mmHg | 160 | 160 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| diastolik_minimal | mmHg | 60 | 60 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| diastolik_maksimal | mmHg | 100 | 100 | Lampiran Bab III 3.2.2 C.1, hal. 57 | terverifikasi |
| interval_donor_hari | hari | 60 | 2 bulan (dikonversi 60 hari) | Lampiran Bab III 3.2.2 C.6, hal. 64 | terverifikasi |
| masa_simpan_sel_darah_merah | hari | 35 | tidak diverifikasi pada R-2 | - | tetap demo |
| masa_simpan_plasma | hari | 365 | tidak diverifikasi pada R-2 | - | tetap demo |

Status diisi: terverifikasi, atau tetap demo (kalau tidak ditemukan di sumber).

## Yang masih demo / perlu dibahas dengan tim
- usia_maksimal: sumber tidak punya batas atas tunggal. Donor pertama di atas 60 tahun dan donor ulang di atas 65 tahun hanya boleh dengan pertimbangan medis khusus.
- berat_minimal: batasnya tergantung volume pengambilan (55 kg untuk 450 mL, 45 kg untuk 350 mL). Tim perlu memutuskan volume yang dipakai simulasi.
- interval_donor_hari: sumber memakai satuan bulan (2 bulan), kode memakai hari (dikonversi 60 hari).
- Syarat yang ada di sumber tetapi belum ada di kode: denyut nadi 50 sampai 100 kali per menit, suhu tubuh 36,5 sampai 37,5 derajat C, selisih sistolik dan diastolik lebih dari 20 mmHg.

- masa_simpan_sel_darah_merah dan masa_simpan_plasma: belum dicocokkan dengan sumber, tetap nilai demo.

## Catatan pribadi (R-4)

### 1. Ringkasan bagianku
Bagianku adalah aturan kelayakan donor dan parameter aturan. Aku membuat class AturanKelayakanStandar yang memeriksa usia, berat badan, jeda donasi, hemoglobin, dan tekanan darah, lalu mengembalikan daftar alasan penolakan. Semua angka aturan tidak ditulis di class, melainkan dibaca dari aturan/parameter.py. Aku membuat halaman /parameter supaya status tiap angka terlihat, dan mencocokkan delapan parameter dengan Permenkes No. 91 Tahun 2015. Parameter yang belum bisa dipastikan dari sumber sengaja ditandai nilai demo, tidak diklaim benar.

### 2. Jawaban pertanyaan pemahaman
- Mengapa parameter diberi dua penanda, sumber dan terverifikasi, bukan satu?
  Sumber menjawab dari mana angka itu berasal, sedangkan terverifikasi menjawab apakah angka itu sudah dicek. Keduanya perlu karena angka bisa punya sumber tetapi belum dicek. Ada juga tes yang memastikan angka bertanda terverifikasi wajib punya sumber.
- Bagaimana jika sumber memberi batas berbeda untuk laki-laki dan perempuan?
  Parameter perlu dipisah per jenis kelamin, dan aturan membaca batas sesuai jenis kelamin donor. Karena itu mengubah struktur parameter.py dan tesnya, hal ini harus dibahas dengan tim dulu. Untuk interval donor darah lengkap, sumber memberi nilai yang sama untuk keduanya (2 bulan).
- Apa yang kutulis di laporan jika ada angka yang tidak berhasil diverifikasi?
  Aku menulis bahwa angka itu masih nilai demo dan tidak menyebutnya sesuai Permenkes. Halaman /parameter juga menandainya dengan jelas.
- Mengapa tes tidak memakai nilai langsung dari parameter.py?
  Supaya tes tidak rusak saat angka diganti hasil verifikasi. Tes memberi angkanya sendiri lewat konstruktor, sesuai prinsip DIP.
- Apa yang diuji test_nilai_tepat_di_batas_masih_layak, dan mengapa kasus batas penting?
  Tes ini memastikan donor yang nilainya persis di batas tetap layak. Kesalahan yang paling sering terjadi ada di batas, misalnya salah memakai lebih kecil dari dan lebih kecil sama dengan.
- Tes mana yang gagal bila _cek_rentang memakai <= bukan <?
  test_nilai_tepat_di_batas_masih_layak akan gagal, karena nilai yang persis di batas akan ditolak padahal seharusnya layak.

### 3. Satu hal yang sulit dan cara mengatasinya
Yang paling sulit adalah alur Git dan terminal, karena beberapa kali muncul error: venv gagal dibuat karena perintahnya kurang satu kata, aktivasi diblokir kebijakan skrip Windows, dan perintah Select-String salah ketik. Aku mengatasinya dengan membaca pesan error sampai habis, memperbaiki perintahnya, lalu mencoba lagi.

### 4. Satu hal yang kupelajari
Angka di sistem yang menyangkut kesehatan tidak boleh diisi dari tebakan. Tiap angka harus punya sumber tertulis dan statusnya harus jujur. Aku juga belajar bahwa memisahkan angka aturan dari kode membuat perubahan lebih aman.

