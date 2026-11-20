"""Halaman beranda: ringkasan stok dan peringatan kedaluwarsa."""
from flask import Blueprint, render_template

from models.komponen_darah import KOMPONEN_TERSEDIA
from web.bantu import hari_ini, sistem

bp = Blueprint("beranda", __name__)


@bp.route("/")
def beranda():
    tanggal = hari_ini()
    nama_komponen = list(KOMPONEN_TERSEDIA)
    matriks = {nama: sistem().stok.jumlah_per_golongan(tanggal, nama) for nama in nama_komponen}
    return render_template("beranda.html", ringkasan=sistem().ringkasan(tanggal),
                           komponen=nama_komponen, matriks=matriks)