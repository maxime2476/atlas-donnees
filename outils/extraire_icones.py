"""Extrait les icones utiles du jeu Streamline Pixel vers des fichiers SVG autonomes.

Le paquet npm @iconify-json/streamline-pixel n'est qu'une source : les SVG produits
sont versionnes dans site/static/icones/, donc le paquet pourrait etre retire sans
casser le site. Aucun code d'Iconify ne tourne chez les lecteurs.

Licence des icones : CC BY 4.0, attribution obligatoire. Voir LICENCE_CONTENU.md.

Usage :
    python outils/extraire_icones.py
"""

import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "site" / "node_modules" / "@iconify-json" / "streamline-pixel" / "icons.json"
DESTINATION = RACINE / "site" / "static" / "icones"

# Nom du fichier produit vers nom de l'icone dans le jeu Streamline. Les noms de
# fichiers sont en francais, comme le reste du depot.
ICONES = {
    "avertissement": "interface-essential-alert-triangle-1",
    "information": "interface-essential-information-circle-1",
    "exercice": "interface-essential-question-help-circle-1",
    "indice": "interface-essential-light-bulb",
    "code": "coding-apps-websites-programming-hold-code",
    "base_de_donnees": "coding-apps-websites-database",
    "filtre": "interface-essential-filter",
    "lien": "interface-essential-link",
    "niveau": "school-science-graduation-cap",
    "duree": "interface-essential-clock",
    "objectif": "business-product-target",
    "fichier": "content-files-book",
}


def charger_jeu() -> dict:
    """Charge le jeu d'icones Iconify depuis node_modules.

    Leve une erreur explicite si le paquet n'est pas installe.
    """
    if not SOURCE.exists():
        raise SystemExit(
            f"Jeu d'icones introuvable : {SOURCE}\nInstallez-le avec : cd site && npm install"
        )
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def construire_svg(corps: str, largeur: int, hauteur: int) -> str:
    """Enveloppe le corps d'une icone Iconify dans un SVG autonome.

    shape-rendering garde les bords nets, ce qui est indispensable pour du pixel art.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
        f'width="{largeur}" height="{hauteur}" shape-rendering="crispEdges" '
        f'fill="currentColor" aria-hidden="true">'
        f"{corps}"
        "</svg>\n"
    )


def extraire(jeu: dict, nom_fichier: str, nom_icone: str) -> None:
    """Ecrit une icone du jeu dans un fichier SVG autonome."""
    icones = jeu.get("icons", {})
    if nom_icone not in icones:
        raise SystemExit(
            f"Icone absente du jeu : « {nom_icone} ». Le jeu a peut-etre change de version."
        )
    icone = icones[nom_icone]
    largeur = icone.get("width", jeu.get("width", 32))
    hauteur = icone.get("height", jeu.get("height", 32))
    destination = DESTINATION / f"{nom_fichier}.svg"
    destination.write_text(construire_svg(icone["body"], largeur, hauteur), encoding="utf-8")
    print(f"  {nom_fichier}.svg  ({largeur}x{hauteur})  depuis {nom_icone}")


def main() -> None:
    """Extrait toutes les icones declarees dans ICONES."""
    jeu = charger_jeu()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for nom_fichier, nom_icone in sorted(ICONES.items()):
        extraire(jeu, nom_fichier, nom_icone)
    print(f"{len(ICONES)} icones extraites dans {DESTINATION}")


if __name__ == "__main__":
    sys.exit(main())
