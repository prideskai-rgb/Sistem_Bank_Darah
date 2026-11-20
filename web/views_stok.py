"""TODO Fadhilah: halaman stok."""
from flask import Blueprint

bp = Blueprint("stok", __name__)


@bp.route("/stok")
def stok():
    return "Halaman stok belum dikerjakan (Fadhilah)."