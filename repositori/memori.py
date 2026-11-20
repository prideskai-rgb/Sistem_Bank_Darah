"""RepositoriMemori: data disimpan di memori (hilang saat program berhenti)."""
from repositori.kontrak import RepositoriDonor, RepositoriKantong, RepositoriPendonoran


class RepositoriMemori(RepositoriDonor, RepositoriPendonoran, RepositoriKantong):
    """Satu class memenuhi tiga kontrak kecil sekaligus."""

    def __init__(self):
        self._donor = {}
        self._pendonoran = {}
        self._kantong = {}

    def simpan_donor(self, donor):
        self._donor[donor.id_donor] = donor

    def cari_donor(self, id_donor):
        return self._donor.get(id_donor)

    def semua_donor(self):
        return list(self._donor.values())

    def simpan_pendonoran(self, hasil):
        self._pendonoran[hasil.id_pendonoran] = hasil

    def cari_pendonoran(self, id_pendonoran):
        return self._pendonoran.get(id_pendonoran)

    def semua_pendonoran(self):
        return list(self._pendonoran.values())

    def simpan_kantong(self, kantong):
        self._kantong[kantong.id_kantong] = kantong

    def cari_kantong(self, id_kantong):
        return self._kantong.get(id_kantong)

    def semua_kantong(self):
        return list(self._kantong.values())

    def kosongkan(self):
        self._donor.clear()
        self._pendonoran.clear()
        self._kantong.clear()