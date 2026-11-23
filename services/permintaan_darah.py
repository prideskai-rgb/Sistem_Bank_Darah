"""PermintaanDarah: memenuhi permintaan dari stok dengan urutan FEFO."""
from models.status import StatusPermintaan


class PermintaanDarah:
    def __init__(self, id_permintaan, golongan_penerima, komponen, jumlah, tanggal):
        if isinstance(jumlah, bool) or not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah kantong harus bilangan bulat lebih dari 0.")
        self._id_permintaan = id_permintaan
        self._golongan_penerima = golongan_penerima
        self._komponen = komponen
        self._jumlah = jumlah
        self._tanggal = tanggal
        self._status = StatusPermintaan.MENUNGGU
        self._kantong_terkumpul = []

    @property
    def id_permintaan(self):
        return self._id_permintaan

    @property
    def golongan_penerima(self):
        return self._golongan_penerima

    @property
    def komponen(self):
        return self._komponen

    @property
    def jumlah(self):
        return self._jumlah

    @property
    def status(self):
        return self._status

    @property
    def kantong_terkumpul(self):
        return tuple(self._kantong_terkumpul)

    def penuhi(self, stok):
        """Ambil kantong cocok satu per satu (FEFO) sampai jumlah terpenuhi atau habis.
        Penyederhanaan: pada hasil SEBAGIAN, kantong yang sudah diambil tetap terpakai.
        """
        if self._status != StatusPermintaan.MENUNGGU:
            raise ValueError("Permintaan ini sudah diproses.")
        while len(self._kantong_terkumpul) < self._jumlah:
            kantong = stok.ambil_fefo(self._golongan_penerima, self._komponen, self._tanggal)
            if kantong is None:
                break
            stok.keluarkan(kantong)
            self._kantong_terkumpul.append(kantong)
        self._status = self._tentukan_status()
        return list(self._kantong_terkumpul)

    def _tentukan_status(self):
        if len(self._kantong_terkumpul) == self._jumlah:
            return StatusPermintaan.DIPENUHI
        if self._kantong_terkumpul:
            return StatusPermintaan.SEBAGIAN
        return StatusPermintaan.TIDAK_TERPENUHI