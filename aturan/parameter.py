"""Semua angka aturan ada di sini. Ubah di file ini, bukan di class lain.

PENTING: seluruh nilai medis di bawah adalah NILAI DEMO (terverifikasi=False)
sampai dicocokkan dengan Permenkes No. 91 Tahun 2015 (tugas Rizki, R-2).
"""

SUMBER_DEMO = "Nilai demo, belum dicocokkan dengan Permenkes No. 91 Tahun 2015."
SUMBER_APLIKASI = "Pengaturan aplikasi (bukan aturan medis)."


def _medis(nilai, satuan, keterangan, sumber=SUMBER_DEMO, terverifikasi=False):
    """Parameter medis. Setelah dicocokkan dengan sumber resmi: isi sumber dan terverifikasi=True."""
    return {"nilai": nilai, "satuan": satuan, "keterangan": keterangan,
            "medis": True, "sumber": sumber, "terverifikasi": terverifikasi}


def _aplikasi(nilai, satuan, keterangan):
    return {"nilai": nilai, "satuan": satuan, "keterangan": keterangan,
            "medis": False, "sumber": SUMBER_APLIKASI, "terverifikasi": True}


PARAMETER = {
    "usia_minimal": _medis(17, "tahun", "Usia minimal donor", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 56", terverifikasi=True),
    "usia_maksimal": _medis(60, "tahun", "Usia maksimal donor"),
    "berat_minimal": _medis(45, "kg", "Berat badan minimal donor"),
    "hb_minimal": _medis(12.5, "g/dL", "Hemoglobin minimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "hb_maksimal": _medis(17.0, "g/dL", "Hemoglobin maksimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "sistolik_minimal": _medis(90, "mmHg", "Tekanan sistolik minimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "sistolik_maksimal": _medis(160, "mmHg", "Tekanan sistolik maksimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "diastolik_minimal": _medis(60, "mmHg", "Tekanan diastolik minimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "diastolik_maksimal": _medis(100, "mmHg", "Tekanan diastolik maksimal", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.1, hal. 57", terverifikasi=True),
    "interval_donor_hari": _medis(60, "hari", "Jeda minimal antar donasi", sumber="Permenkes 91/2015, Lampiran Bab III 3.2.2 C.6, hal. 64 (2 bulan, dikonversi 60 hari)", terverifikasi=True),
    "masa_simpan_sel_darah_merah": _medis(35, "hari", "Masa simpan sel darah merah"),
    "masa_simpan_plasma": _medis(365, "hari", "Masa simpan plasma"),
    "batas_peringatan_hari": _aplikasi(7, "hari", "Peringatan kantong hampir kedaluwarsa"),
}


def nilai(kunci):
    """Ambil nilai parameter berdasarkan kunci."""
    if kunci not in PARAMETER:
        raise KeyError(f"Parameter '{kunci}' tidak ada di aturan/parameter.py")
    return PARAMETER[kunci]["nilai"]


def ada_yang_belum_terverifikasi():
    """True bila masih ada parameter medis yang belum dicocokkan dengan sumber."""
    return any(p["medis"] and not p["terverifikasi"] for p in PARAMETER.values())