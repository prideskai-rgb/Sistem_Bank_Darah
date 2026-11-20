"""GolonganDarah: Enum ABO + Rhesus (delapan golongan)."""
from enum import Enum


class GolonganDarah(Enum):
    A_POSITIF = ("A", True)
    A_NEGATIF = ("A", False)
    B_POSITIF = ("B", True)
    B_NEGATIF = ("B", False)
    AB_POSITIF = ("AB", True)
    AB_NEGATIF = ("AB", False)
    O_POSITIF = ("O", True)
    O_NEGATIF = ("O", False)

    @property
    def punya_antigen_a(self):
        return self.value[0] in ("A", "AB")

    @property
    def punya_antigen_b(self):
        return self.value[0] in ("B", "AB")

    @property
    def rhesus_positif(self):
        return self.value[1]

    @property
    def label(self):
        """Contoh: 'A+' atau 'O-'."""
        return self.value[0] + ("+" if self.rhesus_positif else "-")