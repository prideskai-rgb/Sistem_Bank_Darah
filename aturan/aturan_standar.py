"""AturanKelayakanStandar: aturan kelayakan donor berdasarkan parameter."""
from aturan import parameter
from aturan.aturan_kelayakan import AturanKelayakan


class AturanKelayakanStandar(AturanKelayakan):
    def __init__(self, nilai=parameter.nilai):
        # DIP: sumber angka disuntikkan, jadi tes bisa memakai angka sendiri.
        self._nilai = nilai

    def periksa(self, donor, hasil_pemeriksaan, tanggal):
        """LSP: mengembalikan daftar alasan penolakan; kosong berarti layak."""
        alasan = []
        alasan += self._cek_usia(donor, tanggal)
        alasan += self._cek_berat(donor)
        alasan += self._cek_interval(donor, tanggal)
        alasan += self._cek_rentang("Hemoglobin", hasil_pemeriksaan.hemoglobin,
                                    "hb_minimal", "hb_maksimal", "g/dL")
        alasan += self._cek_rentang("Tekanan sistolik", hasil_pemeriksaan.sistolik,
                                    "sistolik_minimal", "sistolik_maksimal", "mmHg")
        alasan += self._cek_rentang("Tekanan diastolik", hasil_pemeriksaan.diastolik,
                                    "diastolik_minimal", "diastolik_maksimal", "mmHg")
        return alasan

    def _cek_usia(self, donor, tanggal):
        umur = donor.umur_pada(tanggal)
        minimal, maksimal = self._nilai("usia_minimal"), self._nilai("usia_maksimal")
        if umur < minimal or umur > maksimal:
            return [f"Usia {umur} tahun di luar rentang {minimal}-{maksimal} tahun."]
        return []

    def _cek_berat(self, donor):
        minimal = self._nilai("berat_minimal")
        if donor.berat_badan < minimal:
            return [f"Berat badan {donor.berat_badan} kg kurang dari {minimal} kg."]
        return []

    def _cek_interval(self, donor, tanggal):
        terakhir = donor.donasi_terakhir()
        jeda = self._nilai("interval_donor_hari")
        if terakhir is not None and (tanggal - terakhir).days < jeda:
            return [f"Donasi terakhir {terakhir:%d/%m/%Y}; jeda minimal {jeda} hari belum terpenuhi."]
        return []

    def _cek_rentang(self, nama, nilai, kunci_min, kunci_maks, satuan):
        minimal, maksimal = self._nilai(kunci_min), self._nilai(kunci_maks)
        if nilai < minimal or nilai > maksimal:
            return [f"{nama} {nilai} {satuan} di luar rentang {minimal}-{maksimal} {satuan}."]
        return []