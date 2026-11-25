"""Halaman parameter: semua angka aturan beserta status verifikasinya."""
from flask import Blueprint, render_template

from aturan.parameter import PARAMETER

bp = Blueprint("parameter", __name__)


@bp.route("/parameter")
def parameter():
    return render_template("parameter.html", daftar=PARAMETER.items())