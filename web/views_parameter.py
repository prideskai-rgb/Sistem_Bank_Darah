"""TODO Rizki: halaman parameter."""
from flask import Blueprint

bp = Blueprint("parameter", __name__)


@bp.route("/parameter")
def parameter():
    return "Halaman parameter belum dikerjakan (Rizki)."