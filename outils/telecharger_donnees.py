"""Telecharge et prepare les jeux de donnees du site.

Les fichiers prepares sont versionnes dans donnees/. Ce script existe pour que
n'importe qui puisse les regenerer a l'identique, et pour que les transformations
appliquees soient visibles au lieu d'etre perdues.

Usage :
    python outils/telecharger_donnees.py --jeu manchots
"""

import argparse
import csv
import io
import sys
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Palmer Penguins, licence CC0. Mesures relevees a la station Palmer, Antarctique.
ADRESSE_MANCHOTS = (
    "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/"
    "inst/extdata/penguins.csv"
)

# Les noms de colonnes sont traduits parce que le site est en francais et s'adresse
# a des debutants. Les valeurs, elles, ne sont jamais modifiees : un jeu de donnees
# reel comporte des valeurs en anglais, autant l'apprendre tout de suite.
COLONNES_MANCHOTS = {
    "species": "espece",
    "island": "ile",
    "bill_length_mm": "longueur_bec_mm",
    "bill_depth_mm": "profondeur_bec_mm",
    "flipper_length_mm": "longueur_nageoire_mm",
    "body_mass_g": "masse_g",
    "sex": "sexe",
    "year": "annee",
}

# La source note les valeurs manquantes « NA ». On ecrit un champ vide, que Python,
# DuckDB et R interpretent tous les trois comme une valeur manquante.
MARQUEURS_MANQUANTS = ["NA", "na", "N/A", ""]


def telecharger(adresse: str) -> str:
    """Telecharge un fichier texte et renvoie son contenu decode en UTF-8.

    Leve une erreur explicite en francais si le reseau ou le serveur refuse.
    """
    try:
        with urllib.request.urlopen(adresse, timeout=60) as reponse:
            return reponse.read().decode("utf-8")
    except urllib.error.HTTPError as erreur:
        raise SystemExit(f"Le serveur a refuse {adresse} : code {erreur.code}") from erreur
    except urllib.error.URLError as erreur:
        raise SystemExit(f"Reseau indisponible pour {adresse} : {erreur.reason}") from erreur


def renommer_colonnes(anciennes: list[str], correspondance: dict[str, str]) -> list[str]:
    """Traduit une liste de noms de colonnes, et refuse toute colonne inconnue.

    Une colonne inattendue signifie que la source a change : mieux vaut echouer
    bruyamment que produire un fichier silencieusement different.
    """
    nouvelles = []
    for ancienne in anciennes:
        if ancienne not in correspondance:
            raise SystemExit(
                f"Colonne inconnue dans la source : « {ancienne} ». "
                "La source a probablement change, verifiez la correspondance."
            )
        nouvelles.append(correspondance[ancienne])
    return nouvelles


def nettoyer_valeur(valeur: str) -> str:
    """Renvoie une valeur nettoyee, avec un champ vide pour toute valeur manquante."""
    valeur = valeur.strip()
    if valeur in MARQUEURS_MANQUANTS:
        return ""
    return valeur


def preparer_manchots() -> Path:
    """Telecharge Palmer Penguins, traduit les colonnes, ecrit donnees/manchots.csv.

    Renvoie le chemin du fichier ecrit.
    """
    texte = telecharger(ADRESSE_MANCHOTS)
    lecteur = csv.reader(io.StringIO(texte))
    lignes = list(lecteur)
    if not lignes:
        raise SystemExit("La source des manchots est vide.")

    entete = renommer_colonnes(lignes[0], COLONNES_MANCHOTS)
    corps = []
    for ligne in lignes[1:]:
        if not ligne:
            continue
        corps.append([nettoyer_valeur(valeur) for valeur in ligne])

    destination = RACINE / "donnees" / "manchots.csv"
    with destination.open("w", newline="", encoding="utf-8") as fichier:
        redacteur = csv.writer(fichier, lineterminator="\n")
        redacteur.writerow(entete)
        redacteur.writerows(corps)

    print(f"{len(corps)} lignes ecrites dans {destination}")
    return destination


def main() -> None:
    """Point d'entree : prepare le jeu de donnees demande."""
    analyseur = argparse.ArgumentParser(description="Prepare les jeux de donnees du site.")
    analyseur.add_argument(
        "--jeu",
        required=True,
        choices=["manchots"],
        help="jeu de donnees a preparer",
    )
    arguments = analyseur.parse_args()

    if arguments.jeu == "manchots":
        preparer_manchots()


if __name__ == "__main__":
    sys.exit(main())
