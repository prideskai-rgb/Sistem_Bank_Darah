"""HasilPendonoran: catatan satu peristiwa pendonoran (diterima atau ditolak)."""


class HasilPendonoran:
    def __init__(self, id_pendonoran, id_donor, tanggal, nama_komponen,
                 alasan_penolakan=(), kantong=None):
        self._id_pendonoran = id_pendonoran
        self._id_donor = id_donor
        self._tanggal = tanggal
        self._nama_komponen = nama_komponen
        self._alasan_penolakan = tuple(alasan_penolakan)
        self._kantong = kantong

    @property
    def id_pendonoran(self):
        return self._id_pendonoran

    @property
    def id_donor(self):
        return self._id_donor

    @property
    def tanggal(self):
        return self._tanggal

    @property
    def nama_komponen(self):
        return self._nama_komponen

    @property
    def alasan_penolakan(self):
        return self._alasan_penolakan

    @property
    def kantong(self):
        return self._kantong

    @property
    def layak(self):
        return self._kantong is not None