"""Halaman permintaan darah: pencocokan golongan, FEFO, status permintaan."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.komponen_darah import KOMPONEN_TERSEDIA
from models.status import StatusPermintaan
from web.bantu import ambil_angka, ambil_golongan, ambil_tanggal, hari_ini, sistem

bp = Blueprint("permintaan", __name__)

KATEGORI = {StatusPermintaan.DIPENUHI: "sukses", StatusPermintaan.SEBAGIAN: "info",
            StatusPermintaan.TIDAK_TERPENUHI: "galat"}


@bp.route("/permintaan", methods=["GET", "POST"])
def permintaan():
    if request.method == "POST":
        try:
            hasil = sistem().ajukan_permintaan(
                ambil_golongan(request.form.get("golongan_penerima", "")),
                request.form.get("komponen", ""),
                ambil_angka(request.form.get("jumlah"), "Jumlah", int),
                ambil_tanggal(request.form.get("tanggal")))
            id_kantong = ", ".join(k.id_kantong for k in hasil.kantong_terkumpul) or "-"
            flash(f"Permintaan {hasil.id_permintaan}: {hasil.status.value} "
                  f"({len(hasil.kantong_terkumpul)} dari {hasil.jumlah} kantong). "
                  f"Kantong: {id_kantong}.", KATEGORI[hasil.status])
        except ValueError as galat:
            flash(str(galat), "galat")
        return redirect(url_for("permintaan.permintaan"))
    tanggal = hari_ini()
    tersedia = {nama: len(sistem().stok.daftar_tersedia(tanggal, nama))
                for nama in KOMPONEN_TERSEDIA}
    return render_template("permintaan.html", komponen=list(KOMPONEN_TERSEDIA), tersedia=tersedia)