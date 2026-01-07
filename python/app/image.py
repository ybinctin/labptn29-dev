from PIL import Image
import os
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

largeur_cible = config.getint("IMAGE", "largeur_cible")
hauteur_cible = config.getint("IMAGE", "hauteur_cible")
format_sortie = config.get("IMAGE", "format_sortie")

taille_max_kb = config.getint("COMPRESSION", "taille_max_kb")
qualite_max = config.getint("COMPRESSION", "qualite_max")
qualite_min = config.getint("COMPRESSION", "qualite_min")
pas_qualite = config.getint("COMPRESSION", "pas_qualite")

sortie_redimensionnee = config.get("FICHIERS", "sortie_redimensionnee")
sortie_compressee = config.get("FICHIERS", "sortie_compressee")


nom_fichier = input("Saisissez le nom du fichier de l'image : ")
image = Image.open(nom_fichier).convert("RGB")

def redimensionner_image(img, sortie=sortie_redimensionnee):
    image_redim = img.resize((largeur_cible, hauteur_cible))
    image_redim.save(sortie, format=format_sortie)
    print("Image redimensionnée avec succès.")
    return image_redim

def compresser_image(img, sortie=sortie_compressee):
    taille_max = taille_max_kb

    for qualite in range(qualite_max, qualite_min, -pas_qualite):
        img.save(sortie, format=format_sortie, quality=qualite, optimize=True)

        taille_kb = os.path.getsize(sortie) / 1024

        if taille_kb <= taille_max_kb:
            print("Image compressée avec succès")
            return img

redimensionner_image(image)
compresser_image(image)