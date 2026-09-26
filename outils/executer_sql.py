"""Execute un fichier .sql avec DuckDB et ecrit le resultat en CSV sur la sortie standard.

DuckDB est utilise parce qu'il ne demande aucun serveur : le fichier SQL lit
directement les CSV du dossier donnees/. Le script doit etre lance depuis la racine
du depot, comme tous les extraits.

Usage :
    python outils/executer_sql.py extraits/manipulation/filtrer_lignes/sql.sql
"""

import argparse
import csv
import sys
from pathlib import Path

import duckdb


def lire_requete(chemin: Path) -> str:
    """Lit un fichier SQL et renvoie son contenu.

    Leve une erreur explicite si le fichier est absent ou vide.
    """
    if not chemin.exists():
        raise SystemExit(f"Fichier SQL introuvable : {chemin}")
    requete = chemin.read_text(encoding="utf-8").strip()
    if not requete:
        raise SystemExit(f"Le fichier SQL est vide : {chemin}")
    return requete


def executer(requete: str) -> tuple[list[str], list[tuple]]:
    """Execute une requete avec DuckDB.

    Renvoie les noms de colonnes et les lignes du resultat.
    """
    connexion = duckdb.connect(database=":memory:")
    try:
        resultat = connexion.execute(requete)
        if resultat.description is None:
            raise SystemExit(
                "La requete n'a renvoye aucun resultat. Un extrait SQL doit se terminer "
                "par un SELECT."
            )
        colonnes = [colonne[0] for colonne in resultat.description]
        return colonnes, resultat.fetchall()
    except duckdb.Error as erreur:
        raise SystemExit(f"DuckDB a refuse la requete : {erreur}") from erreur
    finally:
        connexion.close()


def ecrire_csv(colonnes: list[str], lignes: list[tuple]) -> None:
    """Ecrit un resultat en CSV sur la sortie standard, sans ligne vide finale."""
    redacteur = csv.writer(sys.stdout, lineterminator="\n")
    redacteur.writerow(colonnes)
    for ligne in lignes:
        # Une valeur nulle devient un champ vide, comme dans les CSV du projet.
        valeurs = ["" if valeur is None else valeur for valeur in ligne]
        redacteur.writerow(valeurs)


def main() -> None:
    """Point d'entree : execute le fichier SQL passe en argument."""
    analyseur = argparse.ArgumentParser(description="Execute un fichier SQL avec DuckDB.")
    analyseur.add_argument("fichier", type=Path, help="chemin du fichier .sql a executer")
    arguments = analyseur.parse_args()

    requete = lire_requete(arguments.fichier)
    colonnes, lignes = executer(requete)
    ecrire_csv(colonnes, lignes)


if __name__ == "__main__":
    sys.exit(main())
