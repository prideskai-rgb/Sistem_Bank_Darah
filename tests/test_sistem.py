"""Tes terpadu SistemUTD: alur donor sampai permintaan, penelusuran, OCP, JSON."""
from datetime import date, timedelta

import pytest

from aturan.aturan_standar import AturanKelayakanStandar
from models.golongan_darah import GolonganDarah as G
from models.hasil_pemeriksaan import HasilPemeriksaan
from models.status import JenisKelamin, StatusPermintaan
from repositori.json_file import RepositoriJSON
from repositori.memori import RepositoriMemori
from services.sistem_utd import SistemUTD
from tests.data_uji import HARI, pemeriksaan_sehat


def daftar(sistem, golongan=G.O_POSITIF):
    return sistem.daftarkan_donor("Donor Uji", date(2000, 1, 1), JenisKelamin.LAKI_LAKI, 65, golongan)


def test_alur_lengkap_donor_sampai_permintaan(sistem):
    donor = daftar(sistem, G.O_NEGATIF)
    hasil = sistem.catat_pendonoran(donor.id_donor, "Sel Darah Merah", pemeriksaan_sehat(), HARI)
    assert hasil.layak and sistem.ringkasan(HARI)["jumlah_tersedia"] == 1
    permintaan = sistem.ajukan_permintaan(G.AB_POSITIF, "Sel Darah Merah", 1, HARI)
    assert permintaan.status == StatusPermintaan.DIPENUHI
    assert sistem.ringkasan(HARI)["jumlah_tersedia"] == 0


def test_penelusuran_dari_kantong_ke_donor(sistem):
    donor = daftar(sistem)
    hasil = sistem.catat_pendonoran(donor.id_donor, "Plasma", pemeriksaan_sehat(), HARI)
    kantong, pendonoran, asal = sistem.telusuri_kantong(hasil.kantong.id_kantong)
    assert pendonoran.id_pendonoran == hasil.id_pendonoran and asal is donor
    assert sistem.telusuri_kantong("K999") == (None, None, None)


def test_donor_ditolak_dicatat_tetapi_tanpa_kantong(sistem):
    donor = daftar(sistem)
    hasil = sistem.catat_pendonoran(donor.id_donor, "Plasma",
                                    HasilPemeriksaan(5.0, 120, 80), HARI)
    assert not hasil.layak and sistem.semua_kantong() == []
    assert len(sistem.daftar_pendonoran()) == 1 and donor.riwayat_donor == ()


def test_jeda_donor_terbaca_pada_donasi_berikutnya(sistem):
    donor = daftar(sistem)
    sistem.catat_pendonoran(donor.id_donor, "Sel Darah Merah", pemeriksaan_sehat(), HARI)
    ulang = sistem.catat_pendonoran(donor.id_donor, "Sel Darah Merah", pemeriksaan_sehat(),
                                    HARI + timedelta(days=5))
    assert not ulang.layak and "jeda" in ulang.alasan_penolakan[0]


def test_donor_tidak_ditemukan(sistem):
    with pytest.raises(ValueError):
        sistem.catat_pendonoran("D999", "Plasma", pemeriksaan_sehat(), HARI)


def test_ocp_aturan_baru_tanpa_mengubah_sistem():
    """Aturan baru = subclass baru. SistemUTD dan Pendonoran tidak diubah."""
    class AturanKetat(AturanKelayakanStandar):
        def periksa(self, donor, hasil_pemeriksaan, tanggal):
            alasan = super().periksa(donor, hasil_pemeriksaan, tanggal)
            if hasil_pemeriksaan.hemoglobin < 15:
                alasan.append("Aturan ketat: hemoglobin minimal 15.")
            return alasan

    sistem = SistemUTD(RepositoriMemori(), aturan=AturanKetat())
    donor = daftar(sistem)
    assert not sistem.catat_pendonoran(donor.id_donor, "Plasma", pemeriksaan_sehat(), HARI).layak


def test_data_demo_memuat_semua_kondisi_stok(sistem):
    sistem.isi_data_demo(date.today())
    ringkasan = sistem.ringkasan(date.today())
    assert ringkasan["jumlah_donor"] == 6
    assert ringkasan["hampir_kedaluwarsa"] and ringkasan["sudah_kedaluwarsa"]
    assert ringkasan["jumlah_tersedia"] == 5


def test_sistem_dengan_json_bertahan_setelah_restart(tmp_path):
    lokasi = tmp_path / "utd.json"
    sistem = SistemUTD(RepositoriJSON(lokasi))
    donor = daftar(sistem, G.O_NEGATIF)
    sistem.catat_pendonoran(donor.id_donor, "Sel Darah Merah", pemeriksaan_sehat(), HARI)
    sistem.ajukan_permintaan(G.O_POSITIF, "Sel Darah Merah", 1, HARI)

    baru = SistemUTD(RepositoriJSON(lokasi))             # program dijalankan ulang
    assert len(baru.daftar_donor()) == 1 and len(baru.semua_kantong()) == 1
    assert baru.ringkasan(HARI)["jumlah_tersedia"] == 0   # kantong tetap berstatus terpakai


def test_kosongkan(sistem):
    sistem.isi_data_demo(date.today())
    sistem.kosongkan()
    assert sistem.daftar_donor() == [] and sistem.semua_kantong() == []