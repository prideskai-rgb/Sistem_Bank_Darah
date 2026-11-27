"""Tes PermintaanDarah, halaman stok, dan halaman permintaan (Fadhilah)."""
from datetime import date, timedelta
import pytest
from models.golongan_darah import GolonganDarah as G
from models.komponen_darah import Plasma, SelDarahMerah
from models.status import StatusKantong, StatusPermintaan
from repositori.memori import RepositoriMemori
from services.permintaan_darah import PermintaanDarah
from services.stok_darah import StokDarah
from tests.data_uji import HARI, kantong_contoh


@pytest.fixture
def stok():
    return StokDarah(RepositoriMemori(), 7)


def minta(jumlah, golongan=G.O_POSITIF, komponen=None):
    return PermintaanDarah("R001", golongan, komponen or SelDarahMerah(), jumlah, HARI)


def test_permintaan_dipenuhi_dan_kantong_terpakai(stok):
    for i in (1, 2, 3):
        stok.tambah_kantong(kantong_contoh(f"K00{i}"))
    permintaan = minta(2)
    diambil = permintaan.penuhi(stok)
    assert permintaan.status == StatusPermintaan.DIPENUHI and len(diambil) == 2
    assert all(k.status == StatusKantong.TERPAKAI for k in diambil)
    assert len(stok.daftar_tersedia(HARI)) == 1


def test_urutan_fefo_dipakai_saat_memenuhi(stok):
    stok.tambah_kantong(kantong_contoh("K001", ambil=HARI))
    stok.tambah_kantong(kantong_contoh("K002", ambil=HARI - timedelta(days=20)))
    diambil = minta(1).penuhi(stok)
    assert [k.id_kantong for k in diambil] == ["K002"]


def test_permintaan_sebagian(stok):
    stok.tambah_kantong(kantong_contoh("K001"))
    permintaan = minta(3)
    permintaan.penuhi(stok)
    assert permintaan.status == StatusPermintaan.SEBAGIAN
    assert len(permintaan.kantong_terkumpul) == 1


def test_permintaan_tidak_terpenuhi_dan_stok_tidak_berubah(stok):
    stok.tambah_kantong(kantong_contoh("K001", G.A_POSITIF))          # tidak cocok ke O+
    permintaan = minta(1)
    assert permintaan.penuhi(stok) == []
    assert permintaan.status == StatusPermintaan.TIDAK_TERPENUHI
    assert len(stok.daftar_tersedia(HARI)) == 1


def test_kantong_kedaluwarsa_tidak_dipakai(stok):
    stok.tambah_kantong(kantong_contoh("K001", ambil=HARI - timedelta(days=100)))
    assert minta(1).penuhi(stok) == []


def test_jenis_komponen_dihormati(stok):
    stok.tambah_kantong(kantong_contoh("K001", komponen=Plasma()))
    assert minta(1, komponen=SelDarahMerah()).penuhi(stok) == []
    assert len(minta(1, komponen=Plasma()).penuhi(stok)) == 1


def test_permintaan_tidak_bisa_diproses_dua_kali(stok):
    permintaan = minta(1)
    permintaan.penuhi(stok)
    with pytest.raises(ValueError):
        permintaan.penuhi(stok)


@pytest.mark.parametrize("jumlah", [0, -1, 1.5, "2", True])
def test_jumlah_tidak_sah(jumlah):
    with pytest.raises(ValueError):
        minta(jumlah)


# --- halaman -----------------------------------------------------------------

def ajukan(klien, **ubah):
    data = {"golongan_penerima": "AB_POSITIF", "komponen": "Sel Darah Merah",
            "jumlah": "1", "tanggal": date.today().isoformat()}
    data.update(ubah)
    return klien.post("/permintaan", data=data, follow_redirects=True).get_data(as_text=True)


def test_halaman_stok_dan_filter(klien):
    assert klien.get("/stok").status_code == 200
    assert "Plasma" in klien.get("/stok?komponen=Plasma").get_data(as_text=True)
    assert klien.get("/stok?komponen=ngawur").status_code == 200


def test_permintaan_dipenuhi_lewat_web(klien):
    assert "Dipenuhi" in ajukan(klien)


def test_permintaan_tidak_terpenuhi_lewat_web(klien):
    assert "Dipenuhi" in ajukan(klien, golongan_penerima="O_NEGATIF")      # menghabiskan O-
    assert "Tidak terpenuhi" in ajukan(klien, golongan_penerima="O_NEGATIF")


def test_permintaan_sebagian_lewat_web(klien):
    assert "Sebagian" in ajukan(klien, jumlah="99")


def test_permintaan_input_salah(klien):
    assert "angka" in ajukan(klien, jumlah="abc")
    assert "lebih dari 0" in ajukan(klien, jumlah="0")
    assert "Tanggal tidak sah" in ajukan(klien, tanggal="x")
    assert "Golongan darah tidak dikenal" in ajukan(klien, golongan_penerima="XYZ")