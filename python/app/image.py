from PIL import Image
import os
import configparser
import sys

config = configparser.ConfigParser()

if not config.read("config.ini"):
    print("Fichier config.ini introuvable.")
    sys.exit(1)

try:
    largeur_cible = config.getint("IMAGE", "largeur_cible")
    hauteur_cible = config.getint("IMAGE", "hauteur_cible")
    tolerance_px = config.getint("IMAGE", "tolerance_px")
    format_sortie = config.get("IMAGE", "format_sortie")

    taille_max_kb = config.getint("COMPRESSION", "taille_max_kb")
    qualite_max = config.getint("COMPRESSION", "qualite_max")
    qualite_min = config.getint("COMPRESSION", "qualite_min")
    pas_qualite = config.getint("COMPRESSION", "pas_qualite")

    sortie_redimensionnee = config.get("FICHIERS", "sortie_redimensionnee")
    sortie_compressee = config.get("FICHIERS", "sortie_compressee")

except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
    print("Erreur dans le fichier config.ini : " + e)
    sys.exit(1)

nom_fichier = input("Saisissez le nom du fichier de l'image : ")

try:
    image = Image.open(nom_fichier).convert("RGB")
except FileNotFoundError:
    print("Fichier image introuvable.")
    sys.exit(1)
except OSError:
    print("Format d'image non reconnu ou fichier corrompu.")
    sys.exit(1)

def redimensionner_image(img, sortie=sortie_redimensionnee):
    try:
        largeur_orig, hauteur_orig = img.size

        facteur = min(
            largeur_cible / largeur_orig,
            hauteur_cible / hauteur_orig
        )

        nouvelle_largeur = int(largeur_orig * facteur)
        nouvelle_hauteur = int(hauteur_orig * facteur)

        if abs(nouvelle_largeur - largeur_cible) <= tolerance_px:
            nouvelle_largeur = largeur_cible

        if abs(nouvelle_hauteur - hauteur_cible) <= tolerance_px:
            nouvelle_hauteur = hauteur_cible

        image_redim = img.resize((nouvelle_largeur, nouvelle_hauteur), Image.LANCZOS)

        image_redim.save(sortie, format=format_sortie)

        print("Image redimensionnée avec succès.")

        return image_redim

    except Exception as e:
        print("Erreur lors du redimensionnement : " + e)
        sys.exit(1)

def compresser_image(img, sortie=sortie_compressee):
    for qualite in range(qualite_max, qualite_min - 1, -pas_qualite):
        try:
            img.save(sortie, format=format_sortie, quality=qualite, optimize=True)

            taille_kb = os.path.getsize(sortie) / 1024

            if taille_kb <= taille_max_kb:
                print("Image compressée avec succès.")
                return True

        except Exception as e:
            print("Erreur lors de la compression : " + e)
            sys.exit(1)

    print("Impossible d'atteindre la taille maximale avec les paramètres de compression.")
    return False

image_redimensionnee = redimensionner_image(image)

compression_ok = compresser_image(image_redimensionnee)

if compression_ok:
    print("Traitement terminé avec succès.")
else:
    print("Traitement terminé avec échec de la compression.")