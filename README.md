# Sistem Manajemen Donor dan Stok Kantong Darah

Proyek ISP132 Pemrograman Berorientasi Objek, Universitas Jambi. Python + Flask, OOP + SOLID.
Data fiktif. Angka medis di `aturan/parameter.py` adalah NILAI DEMO belum terverifikasi; bukan untuk keputusan klinis.

## Menjalankan (Windows PowerShell)
```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m flask --app app run --debug
python -m pytest -q
```

## Struktur
`models/` entitas · `aturan/` aturan kelayakan + parameter · `repositori/` penyimpanan ·
`services/` logika · `web/` halaman Flask · `tests/` pytest · `docs/` panduan tim.

## Peta SOLID
| Prinsip | Lokasi |
|---|---|
| SRP | satu class satu tugas: `StokDarah`, `Pendonoran`, `PermintaanDarah` |
| OCP | `KOMPONEN_TERSEDIA`, subclass `AturanKelayakan` baru tanpa ubah service |
| LSP | semua `KomponenDarah` / `AturanKelayakan` bisa dipakai bergantian (`tests/test_model.py`) |
| ISP | tiga kontrak kecil di `repositori/kontrak.py` |
| DIP | service bergantung pada abstraksi, bukan `RepositoriMemori`/`RepositoriJSON` |