# Bahan presentasi Rizki: Aturan dan Parameter

## 5 poin bicara
1. Aturan kelayakan memutuskan donor boleh mendonor atau tidak, lewat periksa() yang mengembalikan daftar alasan penolakan. Daftar kosong berarti layak.
2. Semua angka aturan disimpan terpusat di aturan/parameter.py, bukan tertanam di class. Mengganti angka tidak mengubah kode aturan.
3. Tiap angka medis punya status: terverifikasi dengan sumber tertulis, atau nilai demo. Statusnya terlihat di halaman /parameter.
4. AturanKelayakanStandar menerima sumber angka lewat konstruktor, jadi tes memakai angka sendiri dan tidak rusak saat angka diganti.
5. Aturan baru ditambah dengan membuat subclass AturanKelayakan, tanpa mengubah kode lama.

## Demo
- S4 (Pendonoran ditolak): daftarkan donor, lalu proses pendonoran dengan Hb 10. Tunjukkan bahwa sistem menampilkan alasan penolakan. Lalu coba donor yang sama lagi di tanggal yang berdekatan untuk menunjukkan penolakan karena jeda donasi.
- S9 (Parameter): buka halaman /parameter, tunjukkan status verifikasi tiap angka, lalu kembali ke beranda dan klik Reset data demo.

## Tanya jawab
- LSP (Liskov Substitution Principle): subclass harus bisa menggantikan induknya tanpa merusak. Buktinya, periksa() di semua aturan selalu mengembalikan list alasan, jadi pemanggil tidak perlu tahu aturan mana yang dipakai.
- OCP (Open/Closed Principle): terbuka untuk penambahan, tertutup untuk perubahan. Buktinya, aturan baru cukup subclass AturanKelayakan tanpa mengubah AturanKelayakanStandar.
- DIP (Dependency Inversion Principle): modul bergantung pada abstraksi, bukan detail. Buktinya, AturanKelayakanStandar(nilai) menerima fungsi nilai dari luar, jadi sumber angka bisa diganti.
- Apakah angka medisnya benar? Delapan parameter sudah dicocokkan dengan Permenkes No. 91 Tahun 2015 dan punya sumber tertulis di parameter.py. Empat lainnya (usia maksimal, berat minimal, dua masa simpan) belum, dan ditandai nilai demo di halaman /parameter. Ini simulasi pembelajaran dengan data fiktif, bukan untuk keputusan klinis.
- Mengapa usia maksimal dan berat minimal belum diverifikasi? Sumbernya tidak memberi satu angka tunggal. Usia di atas 60 atau 65 hanya boleh dengan pertimbangan medis khusus, dan berat minimal tergantung volume pengambilan (55 kg untuk 450 mL, 45 kg untuk 350 mL). Keputusannya ada di tim.