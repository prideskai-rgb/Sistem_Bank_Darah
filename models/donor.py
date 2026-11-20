"""Donor: data donor dengan enkapsulasi dan validasi."""
from datetime import date

from models.golongan_darah import GolonganDarah
from models.status import JenisKelamin


class Donor:
    def __init__(self, id_donor, nama, tanggal_lahir, jenis_kelamin,
                 berat_badan, golongan_darah, riwayat_donor=None):
        self._id_donor = id_donor
        self.nama = nama                  # setter di bawah memvalidasi
        self.tanggal_lahir = tanggal_lahir
        self.jenis_kelamin = jenis_kelamin
        self.berat_badan = berat_badan
        self.golongan_darah = golongan_darah
        self._riwayat_donor = []
        for tanggal in riwayat_donor or []:
            self.tambah_riwayat(tanggal)

    @property
    def id_donor(self):
        return self._id_donor

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Nama donor tidak boleh kosong.")
        self._nama = nilai.strip()

    @property
    def tanggal_lahir(self):
        return self._tanggal_lahir

    @tanggal_lahir.setter
    def tanggal_lahir(self, nilai):
        if not isinstance(nilai, date) or nilai > date.today():
            raise ValueError("Tanggal lahir tidak sah.")
        self._tanggal_lahir = nilai

    @property
    def jenis_kelamin(self):
        return self._jenis_kelamin

    @jenis_kelamin.setter
    def jenis_kelamin(self, nilai):
        if not isinstance(nilai, JenisKelamin):
            raise ValueError("Jenis kelamin tidak dikenal.")
        self._jenis_kelamin = nilai

    @property
    def berat_badan(self):
        return self._berat_badan

    @berat_badan.setter
    def berat_badan(self, nilai):
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)) or nilai <= 0:
            raise ValueError("Berat badan harus berupa angka lebih dari 0.")
        self._berat_badan = nilai

    @property
    def golongan_darah(self):
        return self._golongan_darah

    @golongan_darah.setter
    def golongan_darah(self, nilai):
        if not isinstance(nilai, GolonganDarah):
            raise ValueError("Golongan darah tidak dikenal.")
        self._golongan_darah = nilai

    @property
    def riwayat_donor(self):
        return tuple(self._riwayat_donor)   # salinan: tidak bisa diubah dari luar

    def umur_pada(self, tanggal):
        """Umur dalam tahun penuh pada tanggal tertentu."""
        belum_ulang_tahun = (tanggal.month, tanggal.day) < (self._tanggal_lahir.month,
                                                            self._tanggal_lahir.day)
        return tanggal.year - self._tanggal_lahir.year - int(belum_ulang_tahun)

    def tambah_riwayat(self, tanggal):
        if not isinstance(tanggal, date):
            raise ValueError("Tanggal riwayat tidak sah.")
        self._riwayat_donor.append(tanggal)
        self._riwayat_donor.sort()

    def donasi_terakhir(self):
        return self._riwayat_donor[-1] if self._riwayat_donor else None