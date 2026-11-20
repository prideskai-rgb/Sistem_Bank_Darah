"""Data dan fungsi bantu bersama untuk semua tes."""
from datetime import date

from models.donor import Donor
from models.golongan_darah import GolonganDarah
from models.hasil_pemeriksaan import HasilPemeriksaan
from models.kantong_darah import KantongDarah
from models.komponen_darah import SelDarahMerah
from models.status import JenisKelamin

HARI = date(2026, 6, 1)


def donor_contoh(id_donor="D001", golongan=GolonganDarah.O_POSITIF, berat=60,
                 kelamin=JenisKelamin.LAKI_LAKI, lahir=date(2000, 1, 1)):
    return Donor(id_donor, "Donor Uji", lahir, kelamin, berat, golongan)


def pemeriksaan_sehat():
    return HasilPemeriksaan(hemoglobin=14.0, sistolik=120, diastolik=80)


def kantong_contoh(id_kantong="K001", golongan=GolonganDarah.O_POSITIF, komponen=None,
                   ambil=HARI, id_pendonoran="P001"):
    return KantongDarah(id_kantong, id_pendonoran, golongan, ambil, komponen or SelDarahMerah())