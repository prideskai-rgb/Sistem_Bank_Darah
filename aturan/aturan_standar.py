"""TODO Rizki (R-1): AturanKelayakanStandar."""
from aturan.aturan_kelayakan import AturanKelayakan


class AturanKelayakanStandar(AturanKelayakan):
    def __init__(self, nilai=None):
        pass

    def periksa(self, donor, hasil_pemeriksaan, tanggal):
        raise NotImplementedError("Tugas R-1 Rizki")