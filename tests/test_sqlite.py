"""Tes RepositoriSQLite: harus berperilaku sama dengan memori dan JSON."""
from datetime import date

from models.golongan_darah import GolonganDarah as G
from models.status import JenisKelamin, StatusKantong
from repositori.sqlite import RepositoriSQLite
from services.sistem_utd import SistemUTD
from tests.data_uji import HARI, pemeriksaan_sehat
from tests.test_repositori import isi
from web import rakit_sistem


def test_sqlite_simpan_dan_cari(tmp_path):
    repositori = RepositoriSQLite(tmp_path / "utd.db")
    isi(repositori)
    assert repositori.cari_donor("D001").nama == "Donor Uji"
    assert repositori.cari_kantong("K001").komponen.nama == "Plasma"
    assert repositori.cari_pendonoran("P001").layak
    assert repositori.cari_donor("D999") is None
    assert len(repositori.semua_pendonoran()) == 2


def test_sqlite_bertahan_setelah_dibuka_ulang(tmp_path):
    lokasi = tmp_path / "data" / "utd.db"
    awal = RepositoriSQLite(lokasi)
    isi(awal)
    kantong = awal.cari_kantong("K001")
    kantong.tandai_digunakan()
    awal.simpan_kantong(kantong)

    baru = RepositoriSQLite(lokasi)                  # seolah program dijalankan ulang
    assert baru.cari_donor("D001").riwayat_donor == (HARI,)
    assert baru.cari_donor("D001").tanggal_lahir == date(2000, 1, 1)
    assert baru.cari_kantong("K001").status == StatusKantong.TERPAKAI
    assert baru.cari_pendonoran("P001").kantong.id_kantong == "K001"
    ditolak = baru.cari_pendonoran("P002")
    assert not ditolak.layak and ditolak.alasan_penolakan == ("Hb rendah",)


def test_sqlite_kosongkan_juga_menghapus_isi_database(tmp_path):
    lokasi = tmp_path / "utd.db"
    repositori = RepositoriSQLite(lokasi)
    isi(repositori)
    repositori.kosongkan()
    baru = RepositoriSQLite(lokasi)
    assert baru.semua_donor() == [] and baru.semua_kantong() == []
    assert baru.semua_pendonoran() == []


def test_sistem_dengan_sqlite_bertahan_setelah_restart(tmp_path):
    lokasi = tmp_path / "utd.db"
    sistem = SistemUTD(RepositoriSQLite(lokasi))
    donor = sistem.daftarkan_donor("Donor Uji", date(2000, 1, 1), JenisKelamin.LAKI_LAKI, 65, G.O_NEGATIF)
    sistem.catat_pendonoran(donor.id_donor, "Sel Darah Merah", pemeriksaan_sehat(), HARI)
    sistem.ajukan_permintaan(G.O_POSITIF, "Sel Darah Merah", 1, HARI)

    baru = SistemUTD(RepositoriSQLite(lokasi))       # program dijalankan ulang
    assert len(baru.daftar_donor()) == 1 and len(baru.semua_kantong()) == 1
    assert baru.ringkasan(HARI)["jumlah_tersedia"] == 0   # kantong tetap berstatus terpakai


def test_rakit_sistem_memilih_sqlite_dari_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_SQLITE", str(tmp_path / "web.db"))
    monkeypatch.delenv("DATA_JSON", raising=False)
    sistem = rakit_sistem()
    assert isinstance(sistem._repositori, RepositoriSQLite)
    assert (tmp_path / "web.db").exists()