"""Fixture bersama: sistem kosong, sistem berisi data demo, dan klien web."""
from datetime import date

import pytest

from repositori.memori import RepositoriMemori
from services.sistem_utd import SistemUTD
from web import buat_app


@pytest.fixture
def sistem():
    return SistemUTD(RepositoriMemori())


@pytest.fixture
def klien():
    """Klien web dengan data demo (tanggal hari ini)."""
    sistem_demo = SistemUTD(RepositoriMemori())
    sistem_demo.isi_data_demo(date.today())
    return buat_app(sistem_demo).test_client()


@pytest.fixture
def klien_kosong():
    return buat_app(SistemUTD(RepositoriMemori())).test_client()