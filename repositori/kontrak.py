"""Kontrak penyimpanan. Dibuat kecil-kecil dan terpisah (ISP).

Service bergantung pada kontrak ini, bukan pada cara penyimpanannya (DIP).
"""
from abc import ABC, abstractmethod


class RepositoriDonor(ABC):
    @abstractmethod
    def simpan_donor(self, donor): ...

    @abstractmethod
    def cari_donor(self, id_donor): ...

    @abstractmethod
    def semua_donor(self): ...


class RepositoriPendonoran(ABC):
    @abstractmethod
    def simpan_pendonoran(self, hasil): ...

    @abstractmethod
    def cari_pendonoran(self, id_pendonoran): ...

    @abstractmethod
    def semua_pendonoran(self): ...


class RepositoriKantong(ABC):
    @abstractmethod
    def simpan_kantong(self, kantong): ...

    @abstractmethod
    def cari_kantong(self, id_kantong): ...

    @abstractmethod
    def semua_kantong(self): ...