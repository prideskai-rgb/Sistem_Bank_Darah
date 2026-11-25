"""Halaman stok: kantong layak pakai, urut FEFO (kedaluwarsa terdekat di atas)."""
from flask import Blueprint, render_template, request
from models.komponen_darah import KOMPONEN_TERSEDIA
from web.bantu import hari_ini, sistem

bp = Blueprint("stok", __name__)


@bp.route("/stok")
def stok():
    nama_komponen = request.args.get("komponen", "")
    if nama_komponen not in KOMPONEN_TERSEDIA:
        nama_komponen = None
    tanggal = hari_ini()
    kantong = sistem().stok.daftar_tersedia(tanggal, nama_komponen)
    return render_template("stok.html", kantong=kantong, komponen=list(KOMPONEN_TERSEDIA),
                           dipilih=nama_komponen,
                           batas=sistem().stok.kantong_hampir_kedaluwarsa(tanggal))