
"""Halaman penelusuran kantong darah."""
from flask import Blueprint, render_template, request

from web.bantu import sistem

bp = Blueprint("penelusuran", __name__)


@bp.route("/penelusuran", methods=["GET"])
def penelusuran():
    id_kantong = request.args.get("id_kantong", "").strip()

    kantong_dicari = None
    hasil_pendonoran = None
    donor = None

    if id_kantong:
        kantong_dicari, hasil_pendonoran, donor = (
            sistem().telusuri_kantong(id_kantong)
        )

    return render_template(
        "penelusuran.html",
        daftar=sistem().semua_kantong(),
        id_kantong=id_kantong,
        kantong_dicari=kantong_dicari,
        hasil_pendonoran=hasil_pendonoran,
        donor=donor,
    )
