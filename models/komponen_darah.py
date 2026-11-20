"""KomponenDarah (abstrak) dan jenis-jenisnya.

Aturan kecocokan hidup di sini (polimorfisme), bukan di class lain.
"""
from abc import ABC, abstractmethod

from aturan import parameter


class KomponenDarah(ABC):
    def __init__(self, nama, kunci_masa_simpan):
        self._nama = nama
        self._kunci_masa_simpan = kunci_masa_simpan

    @property
    def nama(self):
        return self._nama

    def masa_simpan(self):
        """Masa simpan (hari), dibaca dari parameter."""
        return parameter.nilai(self._kunci_masa_simpan)

    @abstractmethod
    def bisa_diberikan_ke(self, golongan_kantong, golongan_penerima):
        """LSP: semua subclass wajib mengembalikan True/False dengan arti sama."""


class SelDarahMerah(KomponenDarah):
    """Yang dilihat adalah antigen pada sel donor: tidak boleh asing bagi penerima."""

    def __init__(self):
        super().__init__("Sel Darah Merah", "masa_simpan_sel_darah_merah")

    def bisa_diberikan_ke(self, golongan_kantong, golongan_penerima):
        return ((not golongan_kantong.punya_antigen_a or golongan_penerima.punya_antigen_a)
                and (not golongan_kantong.punya_antigen_b or golongan_penerima.punya_antigen_b)
                and (not golongan_kantong.rhesus_positif or golongan_penerima.rhesus_positif))


class Plasma(KomponenDarah):
    """Arah kebalikan: yang dilihat adalah antibodi dalam plasma donor. Rhesus diabaikan."""

    def __init__(self):
        super().__init__("Plasma", "masa_simpan_plasma")

    def bisa_diberikan_ke(self, golongan_kantong, golongan_penerima):
        return ((golongan_kantong.punya_antigen_a or not golongan_penerima.punya_antigen_a)
                and (golongan_kantong.punya_antigen_b or not golongan_penerima.punya_antigen_b))


# OCP: jenis komponen baru = subclass baru + satu baris di sini. Class lain tidak diubah.
KOMPONEN_TERSEDIA = {kelas().nama: kelas for kelas in (SelDarahMerah, Plasma)}


def buat_komponen(nama):
    """Buat objek komponen dari namanya (dipakai form web dan penyimpanan JSON)."""
    if nama not in KOMPONEN_TERSEDIA:
        raise ValueError(f"Jenis komponen '{nama}' tidak dikenal.")
    return KOMPONEN_TERSEDIA[nama]()