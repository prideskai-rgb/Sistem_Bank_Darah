"""StokDarah: kumpulan kantong, urutan FEFO, dan peringatan kedaluwarsa."""
from models.status import StatusKantong


class StokDarah:
    def __init__(self, repositori_kantong, batas_peringatan_hari):
        # DIP: bergantung pada kontrak RepositoriKantong, bukan pada penyimpanan tertentu.
        self._repositori = repositori_kantong
        self._batas_peringatan = batas_peringatan_hari

    def tambah_kantong(self, kantong):
        self._repositori.simpan_kantong(kantong)

    def daftar_tersedia(self, tanggal, nama_komponen=None):
        """Kantong layak pakai, urut FEFO: yang paling cepat kedaluwarsa di depan."""
        layak = [k for k in self._repositori.semua_kantong()
                 if k.layak_diberikan(tanggal)
                 and (nama_komponen is None or k.komponen.nama == nama_komponen)]
        return sorted(layak, key=lambda k: (k.tanggal_kedaluwarsa(), k.id_kantong))

    def ambil_fefo(self, golongan_penerima, komponen, tanggal):
        """Kantong cocok dengan kedaluwarsa terdekat, atau None bila tidak ada."""
        for kantong in self.daftar_tersedia(tanggal, komponen.nama):
            if kantong.bisa_diberikan_ke(golongan_penerima):
                return kantong
        return None

    def keluarkan(self, kantong):
        """Tandai terpakai dan simpan perubahannya."""
        kantong.tandai_digunakan()
        self._repositori.simpan_kantong(kantong)

    def kantong_hampir_kedaluwarsa(self, tanggal):
        return [k for k in self.daftar_tersedia(tanggal)
                if k.sisa_hari(tanggal) <= self._batas_peringatan]

    def kantong_sudah_kedaluwarsa(self, tanggal):
        return [k for k in self._repositori.semua_kantong()
                if k.status == StatusKantong.TERSEDIA and k.sudah_kedaluwarsa(tanggal)]

    def jumlah_per_golongan(self, tanggal, nama_komponen=None):
        """Dict {GolonganDarah: jumlah kantong layak pakai}."""
        jumlah = {}
        for kantong in self.daftar_tersedia(tanggal, nama_komponen):
            jumlah[kantong.golongan_darah] = jumlah.get(kantong.golongan_darah, 0) + 1
        return jumlah