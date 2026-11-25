
"""Pengujian proses pendonoran."""

from datetime import date

from aturan.aturan_standar import AturanKelayakanStandar
from models.komponen_darah import SelDarahMerah
from services.pendonoran import Pendonoran
from tests.data_uji import donor_contoh, pemeriksaan_sehat, HARI


def test_pendonoran_berhasil_menghasilkan_kantong():
    donor = donor_contoh()
    pendonoran = Pendonoran(
        "P001", donor, HARI,
        AturanKelayakanStandar(),
        SelDarahMerah(),
        "K001"
    )

    hasil = pendonoran.proses(pemeriksaan_sehat())

    assert hasil.layak is True
    assert hasil.kantong is not None
    assert hasil.kantong.id_kantong == "K001"
    assert hasil.id_donor == donor.id_donor


def test_pendonoran_berhasil_menambahkan_riwayat_donor():
    donor = donor_contoh()
    pendonoran = Pendonoran(
        "P001", donor, HARI,
        AturanKelayakanStandar(),
        SelDarahMerah(),
        "K001"
    )

    pendonoran.proses(pemeriksaan_sehat())

    assert HARI in donor.riwayat_donor
    assert donor.donasi_terakhir() == HARI


def test_pendonoran_ditolak_jika_berat_badan_kurang():
    donor = donor_contoh(berat=40)
    pendonoran = Pendonoran(
        "P001", donor, HARI,
        AturanKelayakanStandar(),
        SelDarahMerah(),
        "K001"
    )

    hasil = pendonoran.proses(pemeriksaan_sehat())

    assert hasil.layak is False
    assert hasil.kantong is None
    assert len(hasil.alasan_penolakan) > 0
    assert donor.riwayat_donor == ()


def test_pendonoran_ditolak_tidak_menambahkan_riwayat():
    donor = donor_contoh(berat=40)
    pendonoran = Pendonoran(
        "P001", donor, HARI,
        AturanKelayakanStandar(),
        SelDarahMerah(),
        "K001"
    )

    pendonoran.proses(pemeriksaan_sehat())

    assert len(donor.riwayat_donor) == 0
