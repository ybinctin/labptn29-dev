from PIL import Image
import os

nom_fichier = input("Saisissez le nom du fichier de l'image : ")
image = Image.open(nom_fichier).convert("RGB")

def redimensionner_image(img, sortie="image_redimensionnee.jpg"):
    image_redim = img.resize((283, 378))
    image_redim.save(sortie, format="JPEG")
    print("Image redimensionnée avec succès.")
    return image_redim

def compresser_image(img, sortie="image_compressee.jpg"):
    taille_max_kb = 35

    for qualite in range(90, 0, -5):
        img.save(sortie, format="JPEG", quality=qualite, optimize=True)

        taille_kb = os.path.getsize(sortie) / 1024

        if taille_kb <= taille_max_kb:
            print("Image compressée avec succès")
            return img

# redimensionner_image(image)
compresser_image(image)