"""TODO Kezia: halaman pendonoran."""
from flask import Blueprint

bp = Blueprint("pendonoran", __name__)


@bp.route("/pendonoran")
def pendonoran():
    return "Halaman pendonoran belum dikerjakan (Kezia)."