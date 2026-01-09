from PIL import Image
import os


class ImageProcessor:
    def __init__(
        self,
        largeur_cible,
        hauteur_cible,
        tolerance_px,
        format_sortie,
        taille_max_kb,
        qualite_max,
        qualite_min,
        pas_qualite,
    ):
        self.largeur_cible = largeur_cible
        self.hauteur_cible = hauteur_cible
        self.tolerance_px = tolerance_px
        self.format_sortie = format_sortie
        self.taille_max_kb = taille_max_kb
        self.qualite_max = qualite_max
        self.qualite_min = qualite_min
        self.pas_qualite = pas_qualite

    def redimensionner(self, img: Image.Image) -> Image.Image:
        largeur_orig, hauteur_orig = img.size

        facteur = min(
            self.largeur_cible / largeur_orig,
            self.hauteur_cible / hauteur_orig,
        )

        nouvelle_largeur = int(largeur_orig * facteur)
        nouvelle_hauteur = int(hauteur_orig * facteur)

        if abs(nouvelle_largeur - self.largeur_cible) <= self.tolerance_px:
            nouvelle_largeur = self.largeur_cible

        if abs(nouvelle_hauteur - self.hauteur_cible) <= self.tolerance_px:
            nouvelle_hauteur = self.hauteur_cible

        return img.resize(
            (nouvelle_largeur, nouvelle_hauteur),
            Image.LANCZOS
        )

    def compresser(self, img: Image.Image, sortie: str) -> bool:
        for qualite in range(
            self.qualite_max,
            self.qualite_min - 1,
            -self.pas_qualite
        ):
            img.save(
                sortie,
                format=self.format_sortie,
                quality=qualite,
                optimize=True
            )

            taille_kb = os.path.getsize(sortie) / 1024
            if taille_kb <= self.taille_max_kb:
                return True

        return False