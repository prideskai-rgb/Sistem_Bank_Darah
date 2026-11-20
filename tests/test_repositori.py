"""Tes penyimpanan: memori dan JSON harus berperilaku sama."""
from datetime import date

import pytest

from models.hasil_pendonoran import HasilPendonoran
from models.komponen_darah import Plasma
from models.status import StatusKantong
from repositori.json_file import RepositoriJSON
from repositori.memori import RepositoriMemori
from tests.data_uji import HARI, donor_contoh, kantong_contoh


def isi(repositori):
    donor = donor_contoh()
    donor.tambah_riwayat(HARI)
    kantong = kantong_contoh(komponen=Plasma())
    repositori.simpan_donor(donor)
    repositori.simpan_kantong(kantong)
    repositori.simpan_pendonoran(HasilPendonoran("P001", "D001", HARI, "Plasma", kantong=kantong))
    repositori.simpan_pendonoran(HasilPendonoran("P002", "D001", HARI, "Plasma", ["Hb rendah"]))


@pytest.fixture(params=["memori", "json"])
def repositori(request, tmp_path):
    return RepositoriMemori() if request.param == "memori" else RepositoriJSON(tmp_path / "utd.json")


def test_simpan_dan_cari(repositori):
    isi(repositori)
    assert repositori.cari_donor("D001").nama == "Donor Uji"
    assert repositori.cari_kantong("K001").komponen.nama == "Plasma"
    assert repositori.cari_pendonoran("P001").layak
    assert repositori.cari_donor("D999") is None
    assert len(repositori.semua_pendonoran()) == 2


def test_kosongkan(repositori):
    isi(repositori)
    repositori.kosongkan()
    assert repositori.semua_donor() == [] and repositori.semua_kantong() == []


def test_json_bertahan_setelah_dibuka_ulang(tmp_path):
    lokasi = tmp_path / "data" / "utd.json"
    awal = RepositoriJSON(lokasi)
    isi(awal)
    kantong = awal.cari_kantong("K001")
    kantong.tandai_digunakan()
    awal.simpan_kantong(kantong)

    baru = RepositoriJSON(lokasi)                    # seolah program dijalankan ulang
    assert baru.cari_donor("D001").riwayat_donor == (HARI,)
    assert baru.cari_kantong("K001").status == StatusKantong.TERPAKAI
    assert baru.cari_pendonoran("P001").kantong.id_kantong == "K001"
    ditolak = baru.cari_pendonoran("P002")
    assert not ditolak.layak and ditolak.alasan_penolakan == ("Hb rendah",)
    assert baru.cari_donor("D001").tanggal_lahir == date(2000, 1, 1)