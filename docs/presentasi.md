\# Bahan Presentasi - Bagian Pendonoran dan Penelusuran



\## 1. Gambaran Umum Proyek



Proyek ini merupakan Sistem Manajemen Donor dan Stok Kantong Darah yang dibuat menggunakan Python dan Flask dengan pendekatan Object-Oriented Programming (OOP) serta prinsip SOLID.



Sistem ini dibuat untuk membantu proses pengelolaan data donor, pendonoran darah, stok kantong darah, permintaan darah, dan penelusuran kantong darah.



Bagian yang saya kerjakan adalah fitur pendonoran dan penelusuran kantong darah.



\## 2. K-1: Implementasi Kelas Pendonoran



Kelas `Pendonoran` terdapat pada file `services/pendonoran.py`.



Tugas utama kelas ini adalah memproses satu kegiatan pendonoran darah dan menentukan apakah donor memenuhi aturan kelayakan.



Alur kerjanya:

1\. Menerima data pendonoran, donor, tanggal, aturan, komponen darah, dan ID kantong.

2\. Memeriksa kelayakan donor melalui metode `periksa()` pada aturan kelayakan.

3\. Jika donor tidak layak, sistem mengembalikan hasil penolakan beserta alasannya.

4\. Jika donor layak, sistem membuat objek kantong darah.

5\. Riwayat donor ditambahkan setelah pendonoran berhasil.



Dengan adanya kelas ini, proses pendonoran memiliki tanggung jawab yang jelas dan tidak dicampur dengan tampilan halaman web.



\## 3. K-2: Implementasi Halaman Pendonoran



Halaman pendonoran terdapat pada:

\- `web/views\_pendonoran.py`

\- `web/templates/pendonoran.html`



Fitur ini digunakan untuk memasukkan data pendonoran dan hasil pemeriksaan donor.



Data yang dimasukkan meliputi:

\- Nama atau ID donor.

\- Tanggal pendonoran.

\- Komponen darah.

\- Nilai hemoglobin.

\- Tekanan darah sistolik.

\- Tekanan darah diastolik.



Alur kerjanya:

1\. Pengguna memilih donor yang sudah terdaftar.

2\. Pengguna mengisi tanggal, komponen darah, dan hasil pemeriksaan.

3\. Sistem memvalidasi input dan membuat objek `HasilPemeriksaan`.

4\. Sistem memanggil proses pendonoran melalui `catat\_pendonoran()`.

5\. Jika donor layak, sistem menampilkan ID pendonoran dan ID kantong darah.

6\. Jika donor tidak layak, sistem menampilkan alasan penolakan.



\## 4. K-3: Implementasi Halaman Penelusuran



Halaman penelusuran terdapat pada:

\- `web/views\_penelusuran.py`

\- `web/templates/penelusuran.html`



Fitur ini digunakan untuk mencari informasi berdasarkan ID kantong darah.



Alur kerjanya:

1\. Pengguna membuka menu Penelusuran.

2\. Pengguna memasukkan ID kantong darah.

3\. Sistem mencari data menggunakan metode `telusuri\_kantong()`.

4\. Sistem mengambil informasi kantong darah, hasil pendonoran, dan data donor.

5\. Hasil pencarian ditampilkan pada halaman web.



Jika ID kantong tidak ditemukan, sistem dapat menampilkan informasi bahwa data tidak ditemukan.



Fitur ini membantu pengguna mengetahui asal-usul kantong darah dan informasi yang berkaitan dengan proses pendonorannya.



\## 5. K-4: Pengujian dan Dokumentasi



Pengujian pendonoran dilakukan menggunakan library `pytest`.



Terdapat empat skenario pengujian:

1\. Pendonoran berhasil menghasilkan kantong darah.

2\. Riwayat donor ditambahkan setelah pendonoran berhasil.

3\. Pendonoran ditolak jika berat badan kurang dari batas minimum.

4\. Pendonoran yang ditolak tidak menambahkan riwayat donor.



Hasil pengujian:

\- Pengujian khusus pendonoran: 4 skenario berhasil (`PASSED`).

\- Pengujian keseluruhan pada branch K-4: 93 tes berhasil.



Dokumentasi pengujian disimpan dalam file `docs/catatan.md`.



\## 6. Hubungan dengan Prinsip OOP dan SOLID



Pada bagian pendonoran, konsep OOP diterapkan dengan menggunakan kelas `Pendonoran` untuk mengelola proses pendonoran sebagai sebuah objek.



Salah satu penerapan prinsip SOLID yang terlihat adalah SRP (Single Responsibility Principle). Kelas `Pendonoran` berfokus pada proses pendonoran, sedangkan halaman web menangani interaksi dengan pengguna.



Dengan pemisahan tersebut, kode menjadi lebih terstruktur dan lebih mudah dikembangkan.



\## 7. Rencana Demonstrasi Aplikasi



Saat presentasi, demonstrasi dapat dilakukan dengan urutan berikut:



1\. Membuka aplikasi Sistem Bank Darah.

2\. Membuka menu Pendonoran.

3\. Memilih donor yang sudah terdaftar.

4\. Mengisi formulir pendonoran menggunakan data simulasi.

5\. Menunjukkan hasil pendonoran berhasil atau ditolak.

6\. Membuka menu Penelusuran.

7\. Memasukkan ID kantong darah yang dihasilkan.

8\. Menunjukkan informasi kantong darah dan data pendonor.



\## 8. Kesimpulan



Berdasarkan fitur yang telah dibuat, proses pendonoran dapat dilakukan melalui halaman web dan hasilnya dapat ditelusuri menggunakan ID kantong darah.



Pengujian juga menunjukkan bahwa skenario pendonoran yang dibuat dapat berjalan sesuai dengan fungsi yang diharapkan.



Dengan adanya fitur pendonoran dan penelusuran, sistem dapat membantu pengelolaan informasi donor dan kantong darah secara lebih terstruktur.



\## 9. Catatan Penting



Aplikasi ini menggunakan data fiktif untuk keperluan pembelajaran. Parameter medis yang digunakan masih berupa nilai demo dan belum terverifikasi, sehingga hasil aplikasi tidak boleh digunakan sebagai acuan keputusan medis.

