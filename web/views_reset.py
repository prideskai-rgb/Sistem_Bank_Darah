"""Reset data demo (hanya lewat POST)."""
from flask import Blueprint, flash, redirect, url_for

from web.bantu import hari_ini, sistem

bp = Blueprint("reset", __name__)


@bp.route("/reset", methods=["POST"])
def reset():
    sistem().kosongkan()
    sistem().isi_data_demo(hari_ini())
    flash("Data demo dikembalikan ke kondisi awal.", "sukses")
    return redirect(url_for("beranda.beranda"))