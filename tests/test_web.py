"""Tes lapisan web milik Iqral: beranda, donor, reset, galat, dan asap semua halaman."""
import pytest

HALAMAN = ["/", "/donor", "/pendonoran", "/stok", "/permintaan", "/penelusuran", "/parameter"]


@pytest.mark.parametrize("alamat", HALAMAN)
def test_semua_halaman_terbuka(klien, alamat):
    assert klien.get(alamat).status_code == 200


@pytest.mark.parametrize("alamat", HALAMAN)
def test_semua_halaman_terbuka_saat_data_kosong(klien_kosong, alamat):
    assert klien_kosong.get(alamat).status_code == 200


def test_beranda_menampilkan_ringkasan_dan_peringatan(klien):
    halaman = klien.get("/").get_data(as_text=True)
    assert "Donor terdaftar" in halaman and "Hampir kedaluwarsa" in halaman
    assert "Kedaluwarsa, tidak dipakai" in halaman


def test_banner_batasan_selalu_tampil(klien):
    assert "bukan untuk keputusan klinis" in klien.get("/").get_data(as_text=True)


def test_registrasi_donor(klien_kosong):
    halaman = klien_kosong.post("/donor", data={
        "nama": "Tes Satu", "tanggal_lahir": "2000-01-01", "jenis_kelamin": "LAKI_LAKI",
        "berat_badan": "60", "golongan_darah": "B_POSITIF"}, follow_redirects=True).get_data(as_text=True)
    assert "terdaftar dengan ID D001" in halaman and "Tes Satu" in halaman


@pytest.mark.parametrize("ubah,pesan", [
    ({"nama": " "}, "Nama donor tidak boleh kosong"),
    ({"berat_badan": "-5"}, "lebih dari 0"),
    ({"berat_badan": "abc"}, "angka"),
    ({"tanggal_lahir": "2999-01-01"}, "Tanggal lahir tidak sah"),
    ({"tanggal_lahir": "bukan-tanggal"}, "Tanggal tidak sah"),
    ({"golongan_darah": "XX"}, "Golongan darah tidak dikenal"),
    ({"jenis_kelamin": "XX"}, "Jenis kelamin tidak dikenal")])
def test_registrasi_donor_menolak_data_salah(klien_kosong, ubah, pesan):
    data = {"nama": "Tes", "tanggal_lahir": "2000-01-01", "jenis_kelamin": "LAKI_LAKI",
            "berat_badan": "60", "golongan_darah": "B_POSITIF"}
    data.update(ubah)
    halaman = klien_kosong.post("/donor", data=data, follow_redirects=True).get_data(as_text=True)
    assert pesan in halaman and "Daftar donor (0)" in halaman


def test_reset_mengembalikan_data_demo(klien_kosong):
    halaman = klien_kosong.post("/reset", follow_redirects=True).get_data(as_text=True)
    assert "Data demo dikembalikan" in halaman
    assert "Donor terdaftar" in halaman


def test_reset_tidak_bisa_lewat_get(klien):
    assert klien.get("/reset").status_code in (404, 405)      # hanya POST yang menghapus data


def test_halaman_tidak_ada(klien):
    assert klien.get("/tidak-ada").status_code == 404


def test_css_tersedia(klien):
    assert klien.get("/style.css").status_code == 200