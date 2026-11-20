"""RepositoriJSON: sama seperti RepositoriMemori, tetapi tersimpan di file JSON.

OCP: cara simpan baru cukup berupa class baru; service tidak berubah.
"""
import json
from datetime import date
from pathlib import Path

from models.donor import Donor
from models.golongan_darah import GolonganDarah
from models.hasil_pendonoran import HasilPendonoran
from models.kantong_darah import KantongDarah
from models.komponen_darah import buat_komponen
from models.status import JenisKelamin, StatusKantong
from repositori.memori import RepositoriMemori


def _donor_ke_dict(d):
    return {"id": d.id_donor, "nama": d.nama, "lahir": d.tanggal_lahir.isoformat(),
            "kelamin": d.jenis_kelamin.name, "berat": d.berat_badan,
            "golongan": d.golongan_darah.name,
            "riwayat": [t.isoformat() for t in d.riwayat_donor]}


def _donor_dari_dict(x):
    return Donor(x["id"], x["nama"], date.fromisoformat(x["lahir"]),
                 JenisKelamin[x["kelamin"]], x["berat"], GolonganDarah[x["golongan"]],
                 [date.fromisoformat(t) for t in x["riwayat"]])


def _kantong_ke_dict(k):
    return {"id": k.id_kantong, "pendonoran": k.id_pendonoran,
            "golongan": k.golongan_darah.name, "ambil": k.tanggal_ambil.isoformat(),
            "komponen": k.komponen.nama, "status": k.status.name}


def _kantong_dari_dict(x):
    return KantongDarah(x["id"], x["pendonoran"], GolonganDarah[x["golongan"]],
                        date.fromisoformat(x["ambil"]), buat_komponen(x["komponen"]),
                        StatusKantong[x["status"]])


def _pendonoran_ke_dict(h):
    return {"id": h.id_pendonoran, "donor": h.id_donor, "tanggal": h.tanggal.isoformat(),
            "komponen": h.nama_komponen, "alasan": list(h.alasan_penolakan),
            "kantong": h.kantong.id_kantong if h.kantong else None}


class RepositoriJSON(RepositoriMemori):
    def __init__(self, lokasi_file):
        super().__init__()
        self._file = Path(lokasi_file)
        if self._file.exists():
            self._muat()

    def _muat(self):
        isi = json.loads(self._file.read_text(encoding="utf-8"))
        for x in isi["donor"]:
            super().simpan_donor(_donor_dari_dict(x))
        for x in isi["kantong"]:
            super().simpan_kantong(_kantong_dari_dict(x))
        for x in isi["pendonoran"]:
            kantong = self.cari_kantong(x["kantong"]) if x["kantong"] else None
            super().simpan_pendonoran(HasilPendonoran(
                x["id"], x["donor"], date.fromisoformat(x["tanggal"]),
                x["komponen"], x["alasan"], kantong))

    def _tulis(self):
        isi = {"donor": [_donor_ke_dict(d) for d in self.semua_donor()],
               "kantong": [_kantong_ke_dict(k) for k in self.semua_kantong()],
               "pendonoran": [_pendonoran_ke_dict(h) for h in self.semua_pendonoran()]}
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(json.dumps(isi, indent=2, ensure_ascii=False), encoding="utf-8")

    def simpan_donor(self, donor):
        super().simpan_donor(donor)
        self._tulis()

    def simpan_pendonoran(self, hasil):
        super().simpan_pendonoran(hasil)
        self._tulis()

    def simpan_kantong(self, kantong):
        super().simpan_kantong(kantong)
        self._tulis()

    def kosongkan(self):
        super().kosongkan()
        self._tulis()