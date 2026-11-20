"""TODO Fadhilah: halaman permintaan."""
from flask import Blueprint

bp = Blueprint("permintaan", __name__)


@bp.route("/permintaan")
def permintaan():
    return "Halaman permintaan belum dikerjakan (Fadhilah)."