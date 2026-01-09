import configparser

def charger_config(path="config.ini"):
    config = configparser.ConfigParser()

    if not config.read(path):
        raise FileNotFoundError("config.ini introuvable")

    return {
        "largeur_cible": config.getint("IMAGE", "largeur_cible"),
        "hauteur_cible": config.getint("IMAGE", "hauteur_cible"),
        "tolerance_px": config.getint("IMAGE", "tolerance_px"),
        "format_sortie": config.get("IMAGE", "format_sortie"),
        "taille_max_kb": config.getint("COMPRESSION", "taille_max_kb"),
        "qualite_max": config.getint("COMPRESSION", "qualite_max"),
        "qualite_min": config.getint("COMPRESSION", "qualite_min"),
        "pas_qualite": config.getint("COMPRESSION", "pas_qualite"),
    }