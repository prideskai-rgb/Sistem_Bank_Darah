"""TODO Kezia: halaman penelusuran."""
from flask import Blueprint

bp = Blueprint("penelusuran", __name__)


@bp.route("/penelusuran")
def penelusuran():
    return "Halaman penelusuran belum dikerjakan (Kezia)."