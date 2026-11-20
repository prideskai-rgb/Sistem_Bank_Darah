"""HasilPemeriksaan: hasil pemeriksaan fisik donor (diterima sebagai masukan)."""


def _angka_positif(nilai, nama):
    if isinstance(nilai, bool) or not isinstance(nilai, (int, float)) or nilai <= 0:
        raise ValueError(f"{nama} harus berupa angka lebih dari 0.")
    return nilai


class HasilPemeriksaan:
    def __init__(self, hemoglobin, sistolik, diastolik):
        self._hemoglobin = _angka_positif(hemoglobin, "Hemoglobin")
        self._sistolik = _angka_positif(sistolik, "Tekanan sistolik")
        self._diastolik = _angka_positif(diastolik, "Tekanan diastolik")
        if self._sistolik <= self._diastolik:
            raise ValueError("Tekanan sistolik harus lebih besar dari diastolik.")

    @property
    def hemoglobin(self):
        return self._hemoglobin

    @property
    def sistolik(self):
        return self._sistolik

    @property
    def diastolik(self):
        return self._diastolik