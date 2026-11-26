
# Catatan Pengujian Pendonoran

## 1. Tujuan
Pengujian ini dilakukan untuk memastikan proses pendonoran darah berjalan sesuai dengan fungsi yang telah dibuat pada kelas Pendonoran.

## 2. Skenario Pengujian

| No. | Skenario Pengujian | Hasil |
|---|---|---|
| 1 | Pendonoran berhasil menghasilkan kantong darah | Berhasil |
| 2 | Riwayat donor ditambahkan setelah pendonoran berhasil | Berhasil |
| 3 | Pendonoran ditolak jika berat badan kurang dari batas minimum | Berhasil |
| 4 | Pendonoran yang ditolak tidak menambahkan riwayat donor | Berhasil |

## 3. Hasil Pengujian
Pengujian dilakukan menggunakan perintah:

`python -m pytest tests/test_pendonoran.py -v`

Hasil pengujian menunjukkan bahwa seluruh 4 skenario berhasil dijalankan dengan status PASSED.

## 4. Kesimpulan
Berdasarkan hasil pengujian, proses pendonoran sudah berjalan sesuai dengan skenario yang diuji. Sistem dapat menghasilkan kantong darah ketika donor dinyatakan layak dan memberikan penolakan ketika donor tidak memenuhi aturan kelayakan.

## 5. Catatan
Pengujian menggunakan parameter medis demo yang masih berstatus belum terverifikasi. Nilai tersebut tidak dimaksudkan sebagai acuan keputusan medis.
