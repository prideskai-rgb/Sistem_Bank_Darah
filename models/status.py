"""Enum untuk pilihan tetap, supaya tidak ada teks 'ajaib' tersebar di kode."""
from enum import Enum


class JenisKelamin(Enum):
    LAKI_LAKI = "Laki-laki"
    PEREMPUAN = "Perempuan"


class StatusKantong(Enum):
    TERSEDIA = "Tersedia"
    TERPAKAI = "Terpakai"


class StatusPermintaan(Enum):
    MENUNGGU = "Menunggu"
    DIPENUHI = "Dipenuhi"
    SEBAGIAN = "Sebagian"
    TIDAK_TERPENUHI = "Tidak terpenuhi"