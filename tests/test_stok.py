"""Tes StokDarah: FEFO, pencocokan, peringatan kedaluwarsa."""
from datetime import timedelta

import pytest

from models.golongan_darah import GolonganDarah as G
from models.komponen_darah import Plasma, SelDarahMerah
from repositori.memori import RepositoriMemori
from services.stok_darah import StokDarah
from tests.data_uji import HARI, kantong_contoh

BATAS = 7


@pytest.fixture
def stok():
    return StokDarah(RepositoriMemori(), BATAS)


def hari(n):
    return HARI + timedelta(days=n)


def test_urutan_fefo_yang_paling_cepat_kedaluwarsa_di_depan(stok):
    stok.tambah_kantong(kantong_contoh("K001", ambil=hari(0)))
    stok.tambah_kantong(kantong_contoh("K002", ambil=hari(-10)))
    stok.tambah_kantong(kantong_contoh("K003", ambil=hari(-5)))
    urutan = [k.id_kantong for k in stok.daftar_tersedia(hari(0))]
    assert urutan == ["K002", "K003", "K001"]


def test_ambil_fefo_memilih_yang_cocok_dan_paling_cepat_kedaluwarsa(stok):
    stok.tambah_kantong(kantong_contoh("K001", G.A_POSITIF, ambil=hari(-1)))   # tidak cocok ke O
    stok.tambah_kantong(kantong_contoh("K002", G.O_POSITIF, ambil=hari(-2)))
    stok.tambah_kantong(kantong_contoh("K003", G.O_NEGATIF, ambil=hari(-9)))
    assert stok.ambil_fefo(G.O_POSITIF, SelDarahMerah(), hari(0)).id_kantong == "K003"
    assert stok.ambil_fefo(G.A_POSITIF, SelDarahMerah(), hari(0)).id_kantong == "K003"
    assert stok.ambil_fefo(G.O_NEGATIF, SelDarahMerah(), hari(0)).id_kantong == "K003"


def test_ambil_fefo_menghormati_jenis_komponen(stok):
    stok.tambah_kantong(kantong_contoh("K001", G.O_POSITIF, komponen=Plasma()))
    assert stok.ambil_fefo(G.O_POSITIF, SelDarahMerah(), HARI) is None
    assert stok.ambil_fefo(G.O_POSITIF, Plasma(), HARI).id_kantong == "K001"


def test_kantong_kedaluwarsa_tidak_diambil_tetapi_dilaporkan(stok):
    lama = kantong_contoh("K001", ambil=hari(-100))
    stok.tambah_kantong(lama)
    assert stok.ambil_fefo(G.O_POSITIF, SelDarahMerah(), hari(0)) is None
    assert stok.kantong_sudah_kedaluwarsa(hari(0)) == [lama]
    assert stok.daftar_tersedia(hari(0)) == []


def test_keluarkan_menandai_terpakai(stok):
    kantong = kantong_contoh()
    stok.tambah_kantong(kantong)
    stok.keluarkan(kantong)
    assert stok.daftar_tersedia(HARI) == []
    assert stok.ambil_fefo(G.O_POSITIF, SelDarahMerah(), HARI) is None


def test_peringatan_hampir_kedaluwarsa(stok):
    masa = SelDarahMerah().masa_simpan()
    hampir = kantong_contoh("K001", ambil=hari(-(masa - BATAS)))       # sisa tepat batas
    aman = kantong_contoh("K002", ambil=hari(-(masa - BATAS - 1)))      # sisa batas + 1
    stok.tambah_kantong(hampir)
    stok.tambah_kantong(aman)
    assert stok.kantong_hampir_kedaluwarsa(hari(0)) == [hampir]


def test_jumlah_per_golongan(stok):
    stok.tambah_kantong(kantong_contoh("K001", G.A_POSITIF))
    stok.tambah_kantong(kantong_contoh("K002", G.A_POSITIF))
    stok.tambah_kantong(kantong_contoh("K003", G.B_NEGATIF, komponen=Plasma()))
    assert stok.jumlah_per_golongan(HARI) == {G.A_POSITIF: 2, G.B_NEGATIF: 1}
    assert stok.jumlah_per_golongan(HARI, "Plasma") == {G.B_NEGATIF: 1}