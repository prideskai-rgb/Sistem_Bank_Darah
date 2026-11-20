"""Pabrik aplikasi Flask: merakit sistem, halaman (blueprint), dan pengaturan."""
import os
from pathlib import Path

from flask import Flask, render_template

from aturan import parameter
from models.golongan_darah import GolonganDarah
from repositori.json_file import RepositoriJSON
from repositori.memori import RepositoriMemori
from services.sistem_utd import SistemUTD
from web import (views_beranda, views_donor, views_parameter, views_pendonoran,
                 views_penelusuran, views_permintaan, views_reset, views_stok)
from web.bantu import hari_ini

AKAR = Path(__file__).resolve().parent.parent
HALAMAN = (views_beranda, views_donor, views_pendonoran, views_stok,
           views_permintaan, views_penelusuran, views_parameter, views_reset)


def rakit_sistem():
    """Pilih penyimpanan dari environment. Tanpa pengaturan: memori (cocok untuk Vercel)."""
    lokasi_json = os.environ.get("DATA_JSON")
    repositori = RepositoriJSON(lokasi_json) if lokasi_json else RepositoriMemori()
    sistem = SistemUTD(repositori)
    if os.environ.get("ISI_DATA_DEMO") == "1" and not sistem.daftar_donor():
        sistem.isi_data_demo(hari_ini())
    return sistem


def buat_app(sistem=None):
    app = Flask(__name__, static_folder=str(AKAR / "public"), static_url_path="")
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "kunci-pengembangan-bukan-untuk-produksi")
    app.extensions["sistem"] = sistem or rakit_sistem()
    for halaman in HALAMAN:
        app.register_blueprint(halaman.bp)

    app.jinja_env.filters["tgl"] = lambda tanggal: tanggal.strftime("%d/%m/%Y")

    @app.context_processor
    def data_bersama():
        return {"hari_ini": hari_ini(),
                "semua_golongan": list(GolonganDarah),
                "parameter_belum_terverifikasi": parameter.ada_yang_belum_terverifikasi()}

    @app.errorhandler(404)
    def tidak_ketemu(galat):
        return render_template("galat.html"), 404

    return app