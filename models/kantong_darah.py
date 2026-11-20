"""KantongDarah: satu kantong hasil pendonoran, memiliki satu komponen."""
from datetime import timedelta

from models.status import StatusKantong


class KantongDarah:
    def __init__(self, id_kantong, id_pendonoran, golongan_darah, tanggal_ambil,
                 komponen, status=StatusKantong.TERSEDIA):
        self._id_kantong = id_kantong
        self._id_pendonoran = id_pendonoran      # asal donor ditelusuri lewat sini
        self._golongan_darah = golongan_darah
        self._tanggal_ambil = tanggal_ambil
        self._komponen = komponen
        self._status = status

    @property
    def id_kantong(self):
        return self._id_kantong

    @property
    def id_pendonoran(self):
        return self._id_pendonoran

    @property
    def golongan_darah(self):
        return self._golongan_darah

    @property
    def tanggal_ambil(self):
        return self._tanggal_ambil

    @property
    def komponen(self):
        return self._komponen

    @property
    def status(self):
        return self._status

    def tanggal_kedaluwarsa(self):
        return self._tanggal_ambil + timedelta(days=self._komponen.masa_simpan())

    def sudah_kedaluwarsa(self, tanggal):
        return tanggal > self.tanggal_kedaluwarsa()

    def sisa_hari(self, tanggal):
        return (self.tanggal_kedaluwarsa() - tanggal).days

    def layak_diberikan(self, tanggal):
        return self._status == StatusKantong.TERSEDIA and not self.sudah_kedaluwarsa(tanggal)

    def bisa_diberikan_ke(self, golongan_penerima):
        # Kantong tidak tahu aturan kecocokan; ia bertanya ke komponennya.
        return self._komponen.bisa_diberikan_ke(self._golongan_darah, golongan_penerima)

    def tandai_digunakan(self):
        if self._status == StatusKantong.TERPAKAI:
            raise ValueError("Kantong sudah terpakai.")
        self._status = StatusKantong.TERPAKAI