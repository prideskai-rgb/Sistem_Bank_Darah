"""Fungsi bantu lapisan web: membaca input form dan mengambil SistemUTD."""
import math
from datetime import date, datetime

from flask import current_app

from models.golongan_darah import GolonganDarah


def sistem():
    return current_app.extensions["sistem"]


def hari_ini():
    return date.today()


def ambil_tanggal(teks):
    try:
        return datetime.strptime(teks, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("Tanggal tidak sah (format tahun-bulan-hari).")


def ambil_angka(teks, nama, tipe=float):
    try:
        hasil = tipe(teks)
    except (TypeError, ValueError):
        raise ValueError(f"{nama} harus berupa angka yang sah.")
    if not math.isfinite(hasil):
        raise ValueError(f"{nama} harus berupa angka yang sah.")
    return hasil


def ambil_golongan(teks):
    try:
        return GolonganDarah[teks]
    except KeyError:
        raise ValueError("Golongan darah tidak dikenal.")