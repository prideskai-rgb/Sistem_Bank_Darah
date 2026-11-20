"""AturanKelayakan: kontrak penilaian kelayakan donor (abstrak)."""
from abc import ABC, abstractmethod


class AturanKelayakan(ABC):
    @abstractmethod
    def periksa(self, donor, hasil_pemeriksaan, tanggal):
        """Kembalikan daftar alasan penolakan. Daftar kosong berarti donor layak.

        LSP: semua aturan turunan harus mengikuti kontrak ini.
        """