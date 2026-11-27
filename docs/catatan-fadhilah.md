# Catatan Fadhilah

## 1. Ringkasan bagianku
Bagianku adalah permintaan darah. Kelas PermintaanDarah mengurus satu permintaan dari rumah sakit. Kelas ini meminta kantong yang cocok ke stok, satu per satu, sampai jumlahnya cukup atau stok habis. Kantong yang diambil selalu yang paling cepat kedaluwarsa (FEFO). Hasilnya ada tiga: Dipenuhi, Sebagian, atau Tidak terpenuhi. Aku juga membuat dua halaman web, yaitu Stok dan Permintaan, serta tes untuk semuanya.

## 2. Jawaban pertanyaan pemahaman

### F-1 Kelas PermintaanDarah
1. **Kenapa penuhi tidak mencari kantong sendiri, tapi memanggil stok.ambil_fefo?**
   Karena urusan memilih kantong (urutan FEFO dan kecocokan golongan) sudah dikerjakan oleh StokDarah. PermintaanDarah cukup mengurus satu permintaan. Ini prinsip SRP: satu kelas, satu tugas. Selain itu stok diberikan dari luar ke penuhi(stok), jadi kelasnya tidak membuat stok sendiri. Ini prinsip DIP, dan membuat kelas ini mudah dites dengan stok palsu.

2. **Kenapa jumlah=True ditolak? Apa yang terjadi kalau pengecekan isinstance(jumlah, bool) dihapus?**
   Di Python, True dianggap sama dengan angka 1. Jadi tanpa pengecekan khusus, jumlah=True akan lolos dan dianggap minta 1 kantong, padahal itu input yang tidak masuk akal. Kalau pengecekan itu dihapus, permintaan dengan True atau False bisa diterima dengan diam-diam.

3. **Apa dampaknya kalau penuhi dipanggil dua kali, dan bagaimana kode mencegahnya?**
   Kalau dipanggil dua kali, permintaan yang sama bisa mengambil kantong lagi, jadi stok terpakai dua kali untuk satu permintaan. Kode mencegahnya dengan mengecek status di awal. Kalau status sudah bukan MENUNGGU, kode melempar ValueError "Permintaan ini sudah diproses."

### F-2 Halaman Stok
1. **Kenapa nilai komponen dari alamat dicek dengan in KOMPONEN_TERSEDIA?**
   Karena alamat bisa diketik siapa saja, misalnya /stok?komponen=ngawur. Kalau nilainya langsung dipakai, bisa muncul error atau hasil kosong yang aneh. Dengan pengecekan, nilai yang tidak dikenal diubah menjadi None (semua komponen), jadi halaman tetap tampil normal.

2. **Kantong mana yang ada di baris paling atas, dan kenapa?**
   Kantong yang tanggal kedaluwarsanya paling dekat. Waktu aku coba, itu K002. Alasannya FEFO (First Expired, First Out): yang paling cepat kedaluwarsa dipakai lebih dulu supaya tidak terbuang.

### F-3 Halaman Permintaan
1. **Apa yang terjadi kalau pengguna mengisi jumlah abc?**
   Muncul pesan "Jumlah harus berupa angka yang sah.", bukan halaman error. Galatnya dibuat di fungsi ambil_angka (web/bantu.py), yang melempar ValueError saat abc gagal diubah menjadi angka. Galat itu ditangkap oleh try/except di views_permintaan.py, lalu ditampilkan lewat flash sebagai pesan merah.

2. **Kenapa ada redirect setelah POST?**
   Supaya kalau pengguna menekan refresh, browser tidak mengirim ulang formulir yang sama. Tanpa redirect, refresh akan membuat permintaan yang sama terkirim lagi dan mengambil kantong lagi. Pola ini disebut Post/Redirect/Get.

3. **Kenapa KATEGORI memakai StatusPermintaan sebagai kunci, bukan teks?**
   Karena Enum lebih aman daripada teks yang diketik ulang. Kalau salah ketik teks, tidak ada peringatan. Kalau salah nama Enum, Python langsung memberi error. Jadi kalau ada status baru, kita tahu persis bagian mana yang harus ditambah.

### F-4 Tes
1. **Apa gunanya @pytest.mark.parametrize pada test_jumlah_tidak_sah?**
   Satu fungsi tes dijalankan berulang dengan banyak nilai (0, -1, 1.5, "2", True), jadi tidak perlu menulis lima tes yang hampir sama. Kalau satu nilai gagal, kita langsung tahu nilai yang mana.

2. **Kenapa ada tes yang memastikan stok tidak berubah saat permintaan tidak terpenuhi?**
   Untuk memastikan permintaan yang gagal tidak mengambil atau merusak kantong. Kalau stok berubah padahal tidak ada darah yang diberikan, datanya jadi salah.

3. **Tes mana yang gagal kalau penuhi lupa memanggil stok.keluarkan?**
   Tanpa keluarkan, kantong tidak ditandai terpakai, jadi stok mengembalikan kantong yang sama berulang kali. Akibatnya beberapa tes gagal. Yang paling jelas adalah test_permintaan_dipenuhi_dan_kantong_terpakai, karena memeriksa status TERPAKAI dan sisa stok. test_permintaan_sebagian juga gagal, karena hasilnya jadi Dipenuhi, bukan Sebagian.

## 3. Satu hal yang sulit dan cara mengatasinya
Yang paling sulit buatku adalah mengatur branch di Git. Branch F-3 awalnya dibuat dari main yang belum berisi kode F-1, jadi halaman Permintaan belum bisa jalan. Aku mengatasinya dengan menggabungkan branch F-1 ke branch F-3 memakai git merge. Aku juga sempat bingung kenapa file stok.html hilang waktu pindah branch. Ternyata Git memang mengganti isi folder sesuai branch, dan filenya aman di branch F-2.

## 4. Satu hal yang kupelajari
Aku belajar bahwa tiap kelas sebaiknya punya satu tugas saja (SRP). PermintaanDarah hanya mengurus satu permintaan, StokDarah mengurus pemilihan kantong, dan halaman web hanya menampilkan data. Dengan begitu kodenya lebih mudah dites dan diubah.