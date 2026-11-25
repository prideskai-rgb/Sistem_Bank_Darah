
"""Pendonoran: satu peristiwa donor. Periksa kelayakan, lalu hasilkan kantong."""

from models.hasil_pendonoran import HasilPendonoran
from models.kantong_darah import KantongDarah


class Pendonoran:
    def __init__(self, id_pendonoran, donor, tanggal, aturan, komponen, id_kantong):
         # Aturan diberikan dari luar agar class lebih fleksibel
        self._id_pendonoran = id_pendonoran
        self._donor = donor
        self._tanggal = tanggal
        self._aturan = aturan
        self._komponen = komponen
        self._id_kantong = id_kantong

    def proses(self, hasil_pemeriksaan):
         # Memeriksa apakah donor memenuhi aturan kelayakan
        alasan = self._aturan.periksa(
            self._donor,
            hasil_pemeriksaan,
            self._tanggal
        )

        # Jika ada alasan penolakan, pendonoran tidak menghasilkan kantong
        if alasan:
            return HasilPendonoran(
                self._id_pendonoran,
                self._donor.id_donor,
                self._tanggal,
                self._komponen.nama,
                alasan
            )

        # Jika donor layak, buat kantong darah
        kantong = KantongDarah(
            self._id_kantong,
            self._id_pendonoran,
            self._donor.golongan_darah,
            self._tanggal,
            self._komponen
        )

        # Riwayat donor hanya ditambahkan jika donor layak
        self._donor.tambah_riwayat(self._tanggal)

        return HasilPendonoran(
            self._id_pendonoran,
            self._donor.id_donor,
            self._tanggal,
            self._komponen.nama,
            kantong=kantong
        )
