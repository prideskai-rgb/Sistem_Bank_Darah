# Bahan Presentasi Fadhilah
Bagian: Stok dan Permintaan (skenario S5, S6, S7)

## Lima poin bicara
1. **Apa itu FEFO.** FEFO artinya First Expired, First Out: kantong darah yang paling cepat kedaluwarsa dipakai lebih dulu. Tujuannya supaya darah yang terbuang karena kedaluwarsa lebih sedikit.
2. **Pencocokan golongan darah.** Kantong yang diambil harus cocok dengan golongan penerima. Aturan kecocokannya ditentukan oleh jenis komponen, karena sel darah merah dan plasma aturannya berbeda.
3. **Cara kerja permintaan.** Kelas PermintaanDarah mengurus satu permintaan. Ia meminta kantong ke StokDarah satu per satu, lalu mengeluarkannya dari stok, sampai jumlahnya cukup atau stok habis.
4. **Tiga hasil permintaan.** Dipenuhi (semua kantong didapat), Sebagian (hanya sebagian yang didapat), atau Tidak terpenuhi (tidak ada kantong cocok).
5. **Batasan yang kuakui.** Kalau hasilnya Sebagian, kantong yang sudah diambil tetap terpakai dan tidak dikembalikan. Aplikasi ini juga belum menangani dua permintaan yang datang bersamaan.

## Demo
Sebelum mulai: klik Reset data demo di Beranda.

| Kode | Halaman | Langkah | Yang kujelaskan |
|---|---|---|---|
| S5 | Stok | Lihat urutan kantong, lalu filter Plasma | Kantong yang kedaluwarsanya paling dekat ada di atas (FEFO) |
| S6 | Permintaan | Golongan A+, Sel Darah Merah, jumlah 1 | Sistem mencocokkan golongan lalu mengambil kantong paling cepat kedaluwarsa, hasilnya Dipenuhi |
| S7 | Permintaan | Jumlah 99 | Stok tidak cukup, hasilnya Sebagian atau Tidak terpenuhi |

## Jawaban tanya jawab
**SRP (satu class punya satu alasan untuk berubah).**
Di bagianku: PermintaanDarah hanya mengurus satu permintaan. Memilih kantong (urutan FEFO dan kecocokan golongan) dikerjakan StokDarah. Halaman web (views_stok dan views_permintaan) hanya meminta data dan menampilkannya, tanpa menghitung stok.

**ISP (klien tidak dipaksa bergantung pada metode yang tidak dipakai).**
Penyimpanan data dipecah menjadi tiga kontrak kecil di repositori/kontrak.py (donor, pendonoran, kantong). StokDarah hanya butuh kontrak untuk kantong (RepositoriKantong), jadi tidak ikut bergantung pada urusan donor atau pendonoran.

**Pertanyaan lain yang mungkin muncul**
- *Kenapa FEFO?* Supaya kantong yang paling cepat kedaluwarsa dipakai lebih dulu dan yang terbuang lebih sedikit.
- *Bagaimana kalau dua permintaan datang bersamaan?* Belum ditangani, karena belum ada penguncian atau transaksi database. Ini batasan yang kami akui.
- *Apakah angka medisnya benar?* Tidak diklaim. Semua angka adalah nilai demo yang belum terverifikasi. Aplikasi ini simulasi pembelajaran.