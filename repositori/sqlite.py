"""RepositoriSQLite: data tersimpan di satu file database SQLite.

OCP: cara simpan baru cukup berupa class baru; service tidak berubah.
Sama seperti RepositoriJSON, class ini turunan RepositoriMemori: data dimuat dari
database saat dibuka, lalu setiap perubahan langsung ditulis ke database.
"""
import json
import sqlite3
from datetime import date
from pathlib import Path

from models.donor import Donor
from models.golongan_darah import GolonganDarah
from models.hasil_pendonoran import HasilPendonoran
from models.kantong_darah import KantongDarah
from models.komponen_darah import buat_komponen
from models.status import JenisKelamin, StatusKantong
from repositori.memori import RepositoriMemori

_SKEMA = """
CREATE TABLE IF NOT EXISTS donor (
    id TEXT PRIMARY KEY, nama TEXT NOT NULL, lahir TEXT NOT NULL,
    kelamin TEXT NOT NULL, berat REAL NOT NULL, golongan TEXT NOT NULL,
    riwayat TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS kantong (
    id TEXT PRIMARY KEY, pendonoran TEXT NOT NULL, golongan TEXT NOT NULL,
    ambil TEXT NOT NULL, komponen TEXT NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pendonoran (
    id TEXT PRIMARY KEY, donor TEXT NOT NULL, tanggal TEXT NOT NULL,
    komponen TEXT NOT NULL, alasan TEXT NOT NULL, kantong TEXT
);
"""


class RepositoriSQLite(RepositoriMemori):
    def __init__(self, lokasi_file):
        super().__init__()
        lokasi = Path(lokasi_file)
        lokasi.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(lokasi), check_same_thread=False)
        self._db.executescript(_SKEMA)
        self._muat()

    def _muat(self):
        for x in self._db.execute("SELECT id, nama, lahir, kelamin, berat, golongan, riwayat FROM donor"):
            super().simpan_donor(Donor(
                x[0], x[1], date.fromisoformat(x[2]), JenisKelamin[x[3]], x[4],
                GolonganDarah[x[5]], [date.fromisoformat(t) for t in json.loads(x[6])]))
        for x in self._db.execute("SELECT id, pendonoran, golongan, ambil, komponen, status FROM kantong"):
            super().simpan_kantong(KantongDarah(
                x[0], x[1], GolonganDarah[x[2]], date.fromisoformat(x[3]),
                buat_komponen(x[4]), StatusKantong[x[5]]))
        for x in self._db.execute("SELECT id, donor, tanggal, komponen, alasan, kantong FROM pendonoran"):
            kantong = self.cari_kantong(x[5]) if x[5] else None
            super().simpan_pendonoran(HasilPendonoran(
                x[0], x[1], date.fromisoformat(x[2]), x[3], json.loads(x[4]), kantong))

    def simpan_donor(self, donor):
        super().simpan_donor(donor)
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO donor VALUES (?, ?, ?, ?, ?, ?, ?)",
                (donor.id_donor, donor.nama, donor.tanggal_lahir.isoformat(),
                 donor.jenis_kelamin.name, donor.berat_badan, donor.golongan_darah.name,
                 json.dumps([t.isoformat() for t in donor.riwayat_donor])))

    def simpan_kantong(self, kantong):
        super().simpan_kantong(kantong)
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO kantong VALUES (?, ?, ?, ?, ?, ?)",
                (kantong.id_kantong, kantong.id_pendonoran, kantong.golongan_darah.name,
                 kantong.tanggal_ambil.isoformat(), kantong.komponen.nama, kantong.status.name))

    def simpan_pendonoran(self, hasil):
        super().simpan_pendonoran(hasil)
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO pendonoran VALUES (?, ?, ?, ?, ?, ?)",
                (hasil.id_pendonoran, hasil.id_donor, hasil.tanggal.isoformat(),
                 hasil.nama_komponen, json.dumps(list(hasil.alasan_penolakan)),
                 hasil.kantong.id_kantong if hasil.kantong else None))

    def kosongkan(self):
        super().kosongkan()
        with self._db:
            for tabel in ("pendonoran", "kantong", "donor"):
                self._db.execute(f"DELETE FROM {tabel}")