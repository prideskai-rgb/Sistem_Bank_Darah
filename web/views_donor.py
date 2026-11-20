"""Halaman donor: registrasi dan daftar donor."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.status import JenisKelamin
from web.bantu import ambil_angka, ambil_golongan, ambil_tanggal, sistem

bp = Blueprint("donor", __name__)


@bp.route("/donor", methods=["GET", "POST"])
def donor():
    if request.method == "POST":
        try:
            baru = sistem().daftarkan_donor(
                request.form.get("nama", ""),
                ambil_tanggal(request.form.get("tanggal_lahir")),
                JenisKelamin[request.form.get("jenis_kelamin", "")],
                ambil_angka(request.form.get("berat_badan"), "Berat badan"),
                ambil_golongan(request.form.get("golongan_darah", "")))
            flash(f"Donor {baru.nama} terdaftar dengan ID {baru.id_donor}.", "sukses")
        except KeyError:
            flash("Jenis kelamin tidak dikenal.", "galat")
        except ValueError as galat:
            flash(str(galat), "galat")
        return redirect(url_for("donor.donor"))
    return render_template("donor.html", daftar=sistem().daftar_donor(),
                           jenis_kelamin=list(JenisKelamin))