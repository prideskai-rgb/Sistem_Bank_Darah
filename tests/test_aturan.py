"""Tes AturanKelayakanStandar dan halaman parameter (Rizki)."""
from datetime import date, timedelta

import pytest

from aturan import parameter
from aturan.aturan_kelayakan import AturanKelayakan
from aturan.aturan_standar import AturanKelayakanStandar
from models.hasil_pemeriksaan import HasilPemeriksaan
from tests.data_uji import HARI, donor_contoh, pemeriksaan_sehat

# Angka uji sendiri: tes tidak bergantung pada nilai di aturan/parameter.py.
ANGKA = {"usia_minimal": 17, "usia_maksimal": 60, "berat_minimal": 45,
         "hb_minimal": 12.5, "hb_maksimal": 17.0, "sistolik_minimal": 90,
         "sistolik_maksimal": 160, "diastolik_minimal": 60, "diastolik_maksimal": 100,
         "interval_donor_hari": 60}


@pytest.fixture
def aturan():
    return AturanKelayakanStandar(nilai=lambda kunci: ANGKA[kunci])


def test_donor_sehat_layak(aturan):
    assert aturan.periksa(donor_contoh(), pemeriksaan_sehat(), HARI) == []


def test_adalah_aturan_kelayakan(aturan):
    assert isinstance(aturan, AturanKelayakan)      # LSP: bisa dipakai di mana pun


@pytest.mark.parametrize("donor_kw,kata", [
    ({"lahir": date(2015, 1, 1)}, "Usia"),            # terlalu muda
    ({"lahir": date(1950, 1, 1)}, "Usia"),            # terlalu tua
    ({"berat": 40}, "Berat"),
])
def test_ditolak_karena_data_donor(aturan, donor_kw, kata):
    alasan = aturan.periksa(donor_contoh(**donor_kw), pemeriksaan_sehat(), HARI)
    assert len(alasan) == 1 and kata in alasan[0]


@pytest.mark.parametrize("hasil,kata", [
    (HasilPemeriksaan(10.0, 120, 80), "Hemoglobin"),
    (HasilPemeriksaan(18.0, 120, 80), "Hemoglobin"),
    (HasilPemeriksaan(14.0, 80, 70), "sistolik"),
    (HasilPemeriksaan(14.0, 170, 80), "sistolik"),
    (HasilPemeriksaan(14.0, 120, 50), "diastolik"),
    (HasilPemeriksaan(14.0, 150, 110), "diastolik"),
])
def test_ditolak_karena_pemeriksaan(aturan, hasil, kata):
    alasan = aturan.periksa(donor_contoh(), hasil, HARI)
    assert len(alasan) == 1 and kata in alasan[0]


def test_nilai_tepat_di_batas_masih_layak(aturan):
    donor = donor_contoh(berat=45, lahir=date(2009, 6, 1))     # tepat 17 tahun pada HARI
    hasil = HasilPemeriksaan(12.5, 90, 60)
    assert aturan.periksa(donor, hasil, HARI) == []


def test_interval_donor(aturan):
    donor = donor_contoh()
    donor.tambah_riwayat(HARI - timedelta(days=59))
    assert "jeda" in aturan.periksa(donor, pemeriksaan_sehat(), HARI)[0]
    assert aturan.periksa(donor, pemeriksaan_sehat(), HARI + timedelta(days=1)) == []


def test_alasan_bisa_lebih_dari_satu(aturan):
    alasan = aturan.periksa(donor_contoh(berat=30), HasilPemeriksaan(9.0, 120, 80), HARI)
    assert len(alasan) == 2


def test_parameter_default_terbaca_dari_file_parameter():
    assert AturanKelayakanStandar().periksa(donor_contoh(), pemeriksaan_sehat(), HARI) == []
    with pytest.raises(KeyError):
        parameter.nilai("tidak_ada")


def test_halaman_parameter(klien):
    halaman = klien.get("/parameter").get_data(as_text=True)
    assert "usia_minimal" in halaman and "Belum terverifikasi" in halaman


def test_parameter_terverifikasi_harus_punya_sumber():
    """Guna R-2: nilai medis boleh bertanda terverifikasi hanya bila sumbernya disebut."""
    for kunci, isi in parameter.PARAMETER.items():
        if isi["medis"] and isi["terverifikasi"]:
            assert isi["sumber"] != parameter.SUMBER_DEMO, kunci


def test_penanda_parameter_belum_terverifikasi_konsisten():
    ada = any(i["medis"] and not i["terverifikasi"] for i in parameter.PARAMETER.values())
    assert parameter.ada_yang_belum_terverifikasi() == ada
    