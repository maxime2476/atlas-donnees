"""Execute tous les extraits de code du site et compare leurs sorties a une reference.

Principe, decide en fiche 003 : chaque extrait ecrit son resultat final en CSV sur la
sortie standard. Pour un concept donne, les sorties de tous les langages sont comparees
a un seul fichier attendu.csv. L'egalite des sorties est donc la condition de passage
des tests, et non une intention.

Usage :
    python outils/verifier_extraits.py
    python outils/verifier_extraits.py --langages python sql
    python outils/verifier_extraits.py --concept filtrer_lignes
"""

import argparse
import csv
import io
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_EXTRAITS = RACINE / "extraits"
NOM_REFERENCE = "attendu.csv"

# Nombre de decimales conservees dans les sorties. Les representations flottantes
# different d'un langage a l'autre : sans arrondi commun, des extraits corrects
# seraient declares faux.
DECIMALES = 3

# Delai maximum accorde a un extrait. Large pour les volumes du site, assez court
# pour qu'une boucle infinie ne bloque pas l'integration continue.
DELAI_MAXIMUM = 60

# Extension de fichier vers nom de langage.
LANGAGES = {
    ".py": "python",
    ".sql": "sql",
    ".R": "r",
    ".jl": "julia",
    ".sc": "scala",
}


class Resultat(NamedTuple):
    """Issue de la verification d'un extrait."""

    concept: str
    langage: str
    reussi: bool
    message: str


def construire_commande(fichier: Path) -> list[str]:
    """Renvoie la commande systeme qui execute un extrait, selon son extension."""
    extension = fichier.suffix
    if extension == ".py":
        return [sys.executable, str(fichier)]
    if extension == ".sql":
        # Le SQL passe par notre executeur DuckDB, qui produit le CSV.
        return [sys.executable, str(RACINE / "outils" / "executer_sql.py"), str(fichier)]
    if extension == ".R":
        return ["Rscript", str(fichier)]
    if extension == ".jl":
        return ["julia", str(fichier)]
    if extension == ".sc":
        return ["scala-cli", "run", str(fichier)]
    raise SystemExit(f"Extension inconnue : {extension}")


def executer_extrait(fichier: Path) -> tuple[bool, str]:
    """Execute un extrait et renvoie sa sortie standard.

    Renvoie un couple (reussi, contenu). Si l'execution echoue, contenu est un
    message d'erreur en francais.
    """
    commande = construire_commande(fichier)
    try:
        termine = subprocess.run(
            commande,
            capture_output=True,
            text=True,
            timeout=DELAI_MAXIMUM,
            cwd=RACINE,
            check=False,
        )
    except FileNotFoundError:
        return False, (
            f"Le programme « {commande[0]} » n'est pas installe. "
            "Installez-le ou excluez ce langage avec --langages."
        )
    except subprocess.TimeoutExpired:
        return False, f"L'extrait ne s'est pas termine en {DELAI_MAXIMUM} secondes."

    if termine.returncode != 0:
        erreur = termine.stderr.strip() or "aucun message d'erreur"
        return False, f"L'extrait a echoue (code {termine.returncode}) : {erreur}"

    return True, termine.stdout


def normaliser_nombre(valeur: str) -> str:
    """Renvoie un nombre ecrit de facon identique quel que soit le langage d'origine.

    Une valeur qui n'est pas un nombre est renvoyee telle quelle.
    """
    try:
        nombre = float(valeur)
    except ValueError:
        return valeur

    arrondi = round(nombre, DECIMALES)
    if arrondi == 0:
        # Evite que -0.0 et 0.0 soient consideres comme differents.
        return "0"

    texte = f"{arrondi:.{DECIMALES}f}"
    # 5550.000 devient 5550, et 39.100 devient 39.1.
    return texte.rstrip("0").rstrip(".")


def normaliser_cellule(valeur: str) -> str:
    """Nettoie une cellule : espaces de bord supprimes, nombres arrondis."""
    return normaliser_nombre(valeur.strip())


def normaliser_sortie(texte: str) -> list[list[str]]:
    """Transforme une sortie CSV en tableau normalise, pret a etre compare.

    Les fins de ligne, les espaces de bord et l'ecriture des nombres sont uniformises.
    Les lignes entierement vides sont ignorees.
    """
    tableau = []
    lecteur = csv.reader(io.StringIO(texte))
    for ligne in lecteur:
        if not any(cellule.strip() for cellule in ligne):
            continue
        tableau.append([normaliser_cellule(cellule) for cellule in ligne])
    return tableau


def comparer(obtenu: list[list[str]], attendu: list[list[str]]) -> str:
    """Compare deux tableaux normalises.

    Renvoie une chaine vide s'ils sont identiques, sinon la description du premier
    ecart trouve.
    """
    if not obtenu:
        return "L'extrait n'a rien ecrit sur la sortie standard."

    if obtenu[0] != attendu[0]:
        return f"En-tete different.\n      attendu : {attendu[0]}\n      obtenu  : {obtenu[0]}"

    if len(obtenu) != len(attendu):
        return (
            f"Nombre de lignes different : {len(attendu) - 1} attendue(s), "
            f"{len(obtenu) - 1} obtenue(s)."
        )

    for numero in range(1, len(attendu)):
        if obtenu[numero] != attendu[numero]:
            return (
                f"Ligne {numero} differente.\n"
                f"      attendu : {attendu[numero]}\n"
                f"      obtenu  : {obtenu[numero]}"
            )

    return ""


def lire_reference(dossier: Path) -> list[list[str]]:
    """Lit et normalise le fichier attendu.csv d'un concept."""
    chemin = dossier / NOM_REFERENCE
    if not chemin.exists():
        raise SystemExit(f"Fichier de reference manquant : {chemin}")
    return normaliser_sortie(chemin.read_text(encoding="utf-8"))


def trouver_extraits(dossier: Path, langages_demandes: list[str]) -> list[Path]:
    """Renvoie les fichiers d'extrait d'un concept, filtres par langage."""
    fichiers = []
    for fichier in sorted(dossier.iterdir()):
        langage = LANGAGES.get(fichier.suffix)
        if langage is None:
            continue
        if langages_demandes and langage not in langages_demandes:
            continue
        fichiers.append(fichier)
    return fichiers


def verifier_concept(dossier: Path, langages_demandes: list[str]) -> list[Resultat]:
    """Verifie tous les extraits d'un concept et renvoie un resultat par extrait."""
    reference = lire_reference(dossier)
    resultats = []

    for fichier in trouver_extraits(dossier, langages_demandes):
        langage = LANGAGES[fichier.suffix]
        reussi, contenu = executer_extrait(fichier)
        if not reussi:
            resultats.append(Resultat(dossier.name, langage, False, contenu))
            continue

        ecart = comparer(normaliser_sortie(contenu), reference)
        if ecart:
            resultats.append(Resultat(dossier.name, langage, False, ecart))
        else:
            resultats.append(Resultat(dossier.name, langage, True, ""))

    return resultats


def trouver_concepts(concept_demande: str) -> list[Path]:
    """Renvoie les dossiers de concept a verifier, tries par chemin."""
    if not DOSSIER_EXTRAITS.exists():
        raise SystemExit(f"Dossier des extraits introuvable : {DOSSIER_EXTRAITS}")

    dossiers = []
    for chemin in sorted(DOSSIER_EXTRAITS.rglob(NOM_REFERENCE)):
        dossier = chemin.parent
        if concept_demande and dossier.name != concept_demande:
            continue
        dossiers.append(dossier)
    return dossiers


def afficher_resultats(resultats: list[Resultat]) -> None:
    """Affiche le detail de chaque extrait verifie, puis le resume."""
    for resultat in resultats:
        etat = "OK   " if resultat.reussi else "ECHEC"
        print(f"  {etat} {resultat.concept} / {resultat.langage}")
        if not resultat.reussi:
            print(f"      {resultat.message}")

    reussis = sum(1 for resultat in resultats if resultat.reussi)
    print(f"\n{reussis}/{len(resultats)} extraits OK")


def main() -> int:
    """Point d'entree. Renvoie 0 si tout passe, 1 au moindre ecart."""
    analyseur = argparse.ArgumentParser(
        description="Execute les extraits du site et compare leurs sorties a attendu.csv."
    )
    analyseur.add_argument(
        "--langages",
        nargs="+",
        default=[],
        choices=sorted(set(LANGAGES.values())),
        help="ne verifier que ces langages (tous par defaut)",
    )
    analyseur.add_argument(
        "--concept",
        default="",
        help="ne verifier qu'un concept, designe par le nom de son dossier",
    )
    arguments = analyseur.parse_args()

    concepts = trouver_concepts(arguments.concept)
    if not concepts:
        raise SystemExit("Aucun concept a verifier.")

    resultats = []
    for dossier in concepts:
        resultats.extend(verifier_concept(dossier, arguments.langages))

    if not resultats:
        raise SystemExit("Aucun extrait a verifier pour ces langages.")

    afficher_resultats(resultats)
    return 0 if all(resultat.reussi for resultat in resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
