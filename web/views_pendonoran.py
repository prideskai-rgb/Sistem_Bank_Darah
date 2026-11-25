
"""Halaman pendonoran: memproses pemeriksaan dan kelayakan donor."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.hasil_pemeriksaan import HasilPemeriksaan
from models.komponen_darah import KOMPONEN_TERSEDIA
from web.bantu import ambil_angka, ambil_tanggal, hari_ini, sistem

bp = Blueprint("pendonoran", __name__)


@bp.route("/pendonoran", methods=["GET", "POST"])
def pendonoran():
    if request.method == "POST":
        try:
            hasil_pemeriksaan = HasilPemeriksaan(
                ambil_angka(request.form.get("hemoglobin"), "Hemoglobin"),
                ambil_angka(request.form.get("sistolik"), "Tekanan sistolik"),
                ambil_angka(request.form.get("diastolik"), "Tekanan diastolik")
            )

            hasil = sistem().catat_pendonoran(
                request.form.get("id_donor", ""),
                request.form.get("nama_komponen", ""),
                hasil_pemeriksaan,
                ambil_tanggal(request.form.get("tanggal"))
            )

            if hasil.layak:
                flash(
                    f"Pendonoran berhasil! ID pendonoran: {hasil.id_pendonoran}, "
                    f"ID kantong: {hasil.kantong.id_kantong}.",
                    "sukses"
                )
            else:
                flash(
                    "Pendonoran ditolak: " + "; ".join(hasil.alasan_penolakan),
                    "galat"
                )

        except ValueError as galat:
            flash(str(galat), "galat")

        return redirect(url_for("pendonoran.pendonoran"))

    return render_template(
        "pendonoran.html",
        daftar=sistem().daftar_donor(),
        komponen=list(KOMPONEN_TERSEDIA),
        tanggal=hari_ini()
    )
