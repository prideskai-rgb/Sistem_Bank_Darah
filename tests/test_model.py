"""Tes model: GolonganDarah, Donor, HasilPemeriksaan, KomponenDarah, KantongDarah."""
from datetime import date, timedelta

import pytest

from models.golongan_darah import GolonganDarah
from models.hasil_pemeriksaan import HasilPemeriksaan
from models.komponen_darah import KOMPONEN_TERSEDIA, Plasma, SelDarahMerah, buat_komponen
from models.status import JenisKelamin, StatusKantong
from tests.data_uji import HARI, donor_contoh, kantong_contoh

SEMUA = {g.label: g for g in GolonganDarah}

# Aturan kecocokan: BELUM TERVERIFIKASI dari sumber resmi (tugas R-2).
SEL_MERAH = {"O-": "O- O+ A- A+ B- B+ AB- AB+", "O+": "O+ A+ B+ AB+",
             "A-": "A- A+ AB- AB+", "A+": "A+ AB+", "B-": "B- B+ AB- AB+",
             "B+": "B+ AB+", "AB-": "AB- AB+", "AB+": "AB+"}
PLASMA = {"AB-": "ALL", "AB+": "ALL", "A-": "A- A+ O- O+", "A+": "A- A+ O- O+",
          "B-": "B- B+ O- O+", "B+": "B- B+ O- O+", "O-": "O- O+", "O+": "O- O+"}


def penerima_cocok(komponen, label):
    return {p for p, g in SEMUA.items() if komponen.bisa_diberikan_ke(SEMUA[label], g)}


@pytest.mark.parametrize("label,harapan", SEL_MERAH.items())
def test_kecocokan_sel_darah_merah(label, harapan):
    assert penerima_cocok(SelDarahMerah(), label) == set(harapan.split())


@pytest.mark.parametrize("label,harapan", PLASMA.items())
def test_kecocokan_plasma(label, harapan):
    semua = set(SEMUA) if harapan == "ALL" else set(harapan.split())
    assert penerima_cocok(Plasma(), label) == semua


def test_lsp_semua_komponen_mengikuti_kontrak():
    for nama in KOMPONEN_TERSEDIA:
        komponen = buat_komponen(nama)
        assert komponen.masa_simpan() > 0
        for a in GolonganDarah:
            for b in GolonganDarah:
                assert isinstance(komponen.bisa_diberikan_ke(a, b), bool)


def test_komponen_tidak_dikenal():
    with pytest.raises(ValueError):
        buat_komponen("Trombosit")


def test_label_golongan():
    assert GolonganDarah.AB_NEGATIF.label == "AB-"
    assert GolonganDarah.O_POSITIF.label == "O+"


def test_donor_valid_dan_umur():
    donor = donor_contoh(lahir=date(2000, 6, 15))
    assert donor.umur_pada(date(2026, 6, 14)) == 25
    assert donor.umur_pada(date(2026, 6, 15)) == 26


@pytest.mark.parametrize("galat", [
    {"nama": "  "}, {"berat_badan": -5}, {"berat_badan": 0}, {"berat_badan": "60"},
    {"tanggal_lahir": date.today() + timedelta(days=1)}, {"golongan_darah": "O+"},
    {"jenis_kelamin": "L"}])
def test_donor_menolak_data_tidak_sah(galat):
    donor = donor_contoh()
    with pytest.raises(ValueError):
        for atribut, nilai in galat.items():
            setattr(donor, atribut, nilai)


def test_riwayat_terurut_dan_tidak_bisa_diubah_dari_luar():
    donor = donor_contoh()
    donor.tambah_riwayat(date(2026, 3, 1))
    donor.tambah_riwayat(date(2026, 1, 1))
    assert donor.riwayat_donor == (date(2026, 1, 1), date(2026, 3, 1))
    assert donor.donasi_terakhir() == date(2026, 3, 1)
    assert isinstance(donor.riwayat_donor, tuple)


def test_hasil_pemeriksaan_validasi():
    HasilPemeriksaan(14, 120, 80)
    for argumen in [(0, 120, 80), (14, -1, 80), (14, 80, 120), ("a", 120, 80)]:
        with pytest.raises(ValueError):
            HasilPemeriksaan(*argumen)


def test_kantong_kedaluwarsa_dan_sisa_hari():
    kantong = kantong_contoh(ambil=HARI)
    batas = kantong.tanggal_kedaluwarsa()
    assert batas == HARI + timedelta(days=SelDarahMerah().masa_simpan())
    assert not kantong.sudah_kedaluwarsa(batas)            # hari terakhir masih layak
    assert kantong.sudah_kedaluwarsa(batas + timedelta(days=1))
    assert kantong.sisa_hari(batas - timedelta(days=3)) == 3


def test_kantong_terpakai_tidak_layak_dan_tidak_bisa_dipakai_dua_kali():
    kantong = kantong_contoh()
    assert kantong.layak_diberikan(HARI)
    kantong.tandai_digunakan()
    assert kantong.status == StatusKantong.TERPAKAI
    assert not kantong.layak_diberikan(HARI)
    with pytest.raises(ValueError):
        kantong.tandai_digunakan()


def test_kantong_bertanya_ke_komponennya():
    kantong = kantong_contoh(golongan=GolonganDarah.A_POSITIF)
    assert kantong.bisa_diberikan_ke(GolonganDarah.AB_POSITIF)
    assert not kantong.bisa_diberikan_ke(GolonganDarah.O_POSITIF)