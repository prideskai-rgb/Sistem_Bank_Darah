"""SistemUTD: perakit objek dan pintu masuk untuk lapisan tampilan.

Lapisan web hanya bicara dengan class ini (tampilan bisa diganti tanpa mengubah logika).
"""
from datetime import date, timedelta

from aturan import parameter
from aturan.aturan_standar import AturanKelayakanStandar
from models.donor import Donor
from models.golongan_darah import GolonganDarah
from models.hasil_pendonoran import HasilPendonoran
from models.kantong_darah import KantongDarah
from models.komponen_darah import buat_komponen
from models.status import JenisKelamin
from services.pendonoran import Pendonoran
from services.permintaan_darah import PermintaanDarah
from services.stok_darah import StokDarah


class SistemUTD:
    def __init__(self, repositori, aturan=None):
        self._repositori = repositori
        # DIP + OCP: aturan kelayakan boleh diganti dari luar tanpa mengubah class ini.
        self._aturan = aturan or AturanKelayakanStandar()
        self.stok = StokDarah(repositori, parameter.nilai("batas_peringatan_hari"))
        self._jumlah_permintaan = 0

    # --- donor -------------------------------------------------------------
    def daftarkan_donor(self, nama, tanggal_lahir, jenis_kelamin, berat_badan, golongan_darah):
        donor = Donor(self._buat_id("D", self._repositori.semua_donor()), nama,
                      tanggal_lahir, jenis_kelamin, berat_badan, golongan_darah)
        self._repositori.simpan_donor(donor)
        return donor

    def daftar_donor(self):
        return self._repositori.semua_donor()

    def cari_donor(self, id_donor):
        return self._repositori.cari_donor(id_donor)

    # --- pendonoran --------------------------------------------------------
    def catat_pendonoran(self, id_donor, nama_komponen, hasil_pemeriksaan, tanggal):
        donor = self._repositori.cari_donor(id_donor)
        if donor is None:
            raise ValueError("Donor tidak ditemukan.")
        pendonoran = Pendonoran(
            self._buat_id("P", self._repositori.semua_pendonoran()), donor, tanggal,
            self._aturan, buat_komponen(nama_komponen),
            self._buat_id("K", self._repositori.semua_kantong()))
        hasil = pendonoran.proses(hasil_pemeriksaan)
        self._repositori.simpan_pendonoran(hasil)
        if hasil.layak:
            self._repositori.simpan_donor(donor)          # riwayat donor berubah
            self.stok.tambah_kantong(hasil.kantong)
        return hasil

    def daftar_pendonoran(self):
        return self._repositori.semua_pendonoran()

    # --- permintaan --------------------------------------------------------
    def ajukan_permintaan(self, golongan_penerima, nama_komponen, jumlah, tanggal):
        self._jumlah_permintaan += 1
        permintaan = PermintaanDarah(f"R{self._jumlah_permintaan:03d}", golongan_penerima,
                                     buat_komponen(nama_komponen), jumlah, tanggal)
        permintaan.penuhi(self.stok)
        return permintaan

    # --- penelusuran dan ringkasan ----------------------------------------
    def semua_kantong(self):
        return self._repositori.semua_kantong()

    def telusuri_kantong(self, id_kantong):
        """Kembalikan (kantong, hasil_pendonoran, donor); None bila tidak ketemu."""
        kantong = self._repositori.cari_kantong(id_kantong)
        if kantong is None:
            return None, None, None
        hasil = self._repositori.cari_pendonoran(kantong.id_pendonoran)
        donor = self._repositori.cari_donor(hasil.id_donor) if hasil else None
        return kantong, hasil, donor

    def ringkasan(self, tanggal):
        return {"jumlah_donor": len(self._repositori.semua_donor()),
                "jumlah_tersedia": len(self.stok.daftar_tersedia(tanggal)),
                "hampir_kedaluwarsa": self.stok.kantong_hampir_kedaluwarsa(tanggal),
                "sudah_kedaluwarsa": self.stok.kantong_sudah_kedaluwarsa(tanggal)}

    # --- data demo ---------------------------------------------------------
    def isi_data_demo(self, hari_ini):
        """Isi data fiktif: ada kantong aman, hampir kedaluwarsa, dan sudah kedaluwarsa."""
        masa_sel = buat_komponen("Sel Darah Merah").masa_simpan()
        masa_plasma = buat_komponen("Plasma").masa_simpan()
        contoh = [  # nama, golongan, jenis kelamin, berat, komponen, hari sejak donor
            ("Andi Wijaya", GolonganDarah.O_POSITIF, JenisKelamin.LAKI_LAKI, 68, "Sel Darah Merah", 5),
            ("Sari Lestari", GolonganDarah.A_POSITIF, JenisKelamin.PEREMPUAN, 55, "Sel Darah Merah", masa_sel - 3),
            ("Budi Hartono", GolonganDarah.B_POSITIF, JenisKelamin.LAKI_LAKI, 72, "Sel Darah Merah", masa_sel + 4),
            ("Dewi Anggraini", GolonganDarah.AB_POSITIF, JenisKelamin.PEREMPUAN, 58, "Plasma", 10),
            ("Rahmat Hidayat", GolonganDarah.O_NEGATIF, JenisKelamin.LAKI_LAKI, 75, "Sel Darah Merah", 12),
            ("Maya Putri", GolonganDarah.A_NEGATIF, JenisKelamin.PEREMPUAN, 52, "Plasma", masa_plasma - 4),
        ]
        for nama, golongan, kelamin, berat, nama_komponen, hari_lalu in contoh:
            lahir = date(hari_ini.year - 26, 6, 15)
            donor = self.daftarkan_donor(nama, lahir, kelamin, berat, golongan)
            tanggal = hari_ini - timedelta(days=hari_lalu)
            # Dibuat langsung (tanpa Pendonoran/aturan) agar data demo tidak bergantung pada kode lain.
            kantong = KantongDarah(self._buat_id("K", self._repositori.semua_kantong()),
                                   self._buat_id("P", self._repositori.semua_pendonoran()),
                                   golongan, tanggal, buat_komponen(nama_komponen))
            donor.tambah_riwayat(tanggal)
            self._repositori.simpan_donor(donor)
            self._repositori.simpan_pendonoran(
                HasilPendonoran(kantong.id_pendonoran, donor.id_donor, tanggal, nama_komponen, kantong=kantong))
            self.stok.tambah_kantong(kantong)

    def kosongkan(self):
        self._repositori.kosongkan()
        self._jumlah_permintaan = 0

    # --- bantu -------------------------------------------------------------
    @staticmethod
    def _buat_id(awalan, daftar):
        return f"{awalan}{len(daftar) + 1:03d}"