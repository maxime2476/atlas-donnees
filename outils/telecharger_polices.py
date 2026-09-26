"""Telecharge les polices du site depuis Google Fonts et les stocke dans le depot.

Le site n'appelle jamais Google Fonts a l'execution : cela creerait une dependance
reseau et enverrait l'adresse IP des lecteurs a un tiers. Les fichiers sont donc
telecharges une fois et versionnes.

Les fichiers woff2 vont dans site/src/polices/ et la feuille @font-face dans
site/src/css/polices.css. Deux pieges ont ete rencontres et doivent le rester :
depuis site/static/, il faudrait des chemins absolus que webpack ne sait pas
resoudre ; et une regle @import dans custom.css est supprimee sans message par le
pipeline CSS de Docusaurus. La feuille est donc declaree comme second fichier
customCss dans docusaurus.config.ts.
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Seuls ces sous-ensembles nous servent : le francais n'a besoin que du latin,
# et de latin-ext pour les caracteres comme « oe ».
SOUS_ENSEMBLES_UTILES = ["latin", "latin-ext"]

# Un navigateur moderne est annonce, sinon Google Fonts renvoie du woff au lieu du woff2.
NAVIGATEUR = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

ADRESSE_CSS = (
    "https://fonts.googleapis.com/css2"
    "?family=IBM+Plex+Mono:wght@400;600"
    "&family=IBM+Plex+Sans:wght@400;600"
    "&family=Silkscreen:wght@400;700"
    "&display=swap"
)


def telecharger(adresse: str) -> bytes:
    """Telecharge une adresse et renvoie son contenu brut.

    Leve une erreur explicite en francais si le reseau ou le serveur refuse.
    """
    requete = urllib.request.Request(adresse, headers={"User-Agent": NAVIGATEUR})
    try:
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            return reponse.read()
    except urllib.error.HTTPError as erreur:
        raise SystemExit(f"Le serveur a refuse {adresse} : code {erreur.code}") from erreur
    except urllib.error.URLError as erreur:
        raise SystemExit(f"Reseau indisponible pour {adresse} : {erreur.reason}") from erreur


def decouper_en_blocs(css: str) -> list[str]:
    """Decoupe la feuille de style recue en blocs @font-face, un par fichier."""
    blocs = []
    for morceau in css.split("@font-face"):
        if "src:" in morceau:
            blocs.append(morceau)
    return blocs


def lire_valeur(bloc: str, propriete: str) -> str:
    """Lit la valeur d'une propriete CSS dans un bloc, sans guillemets ni espaces."""
    motif = propriete + r"\s*:\s*([^;]+);"
    trouve = re.search(motif, bloc)
    if trouve is None:
        return ""
    return trouve.group(1).strip().strip("'\"")


def lire_sous_ensemble(css: str, position: int) -> str:
    """Renvoie le nom du sous-ensemble annonce en commentaire avant un bloc."""
    debut = css.rfind("/*", 0, position)
    fin = css.find("*/", debut)
    if debut == -1 or fin == -1:
        return "inconnu"
    return css[debut + 2 : fin].strip()


def nom_de_fichier(famille: str, graisse: str, sous_ensemble: str) -> str:
    """Construit un nom de fichier lisible a partir des caracteristiques de la police."""
    famille_courte = famille.lower().replace(" ", "_")
    return f"{famille_courte}_{graisse}_{sous_ensemble}.woff2"


def main() -> None:
    """Telecharge les polices utiles et ecrit la feuille de style locale."""
    racine = Path(__file__).resolve().parent.parent / "site" / "src"
    dossier = racine / "polices"
    feuille = racine / "css" / "polices.css"
    dossier.mkdir(parents=True, exist_ok=True)
    css = telecharger(ADRESSE_CSS).decode("utf-8")
    blocs = decouper_en_blocs(css)
    if not blocs:
        raise SystemExit("Google Fonts n'a renvoye aucun bloc @font-face.")

    declarations = []
    position_recherche = 0
    telecharges = 0

    for bloc in blocs:
        position = css.find(bloc, position_recherche)
        position_recherche = position + 1
        sous_ensemble = lire_sous_ensemble(css, position)
        if sous_ensemble not in SOUS_ENSEMBLES_UTILES:
            continue

        famille = lire_valeur(bloc, "font-family")
        graisse = lire_valeur(bloc, "font-weight")
        plage = lire_valeur(bloc, "unicode-range")
        adresse_trouvee = re.search(r"url\((https://[^)]+\.woff2)\)", bloc)
        if adresse_trouvee is None:
            continue

        fichier = nom_de_fichier(famille, graisse, sous_ensemble)
        (dossier / fichier).write_bytes(telecharger(adresse_trouvee.group(1)))
        telecharges += 1
        print(f"  {fichier}")

        declarations.append(
            "@font-face {\n"
            f"  font-family: '{famille}';\n"
            "  font-style: normal;\n"
            f"  font-weight: {graisse};\n"
            "  font-display: swap;\n"
            f"  src: url('../polices/{fichier}') format('woff2');\n"
            f"  unicode-range: {plage};\n"
            "}\n"
        )

    entete = (
        "/* Feuille generee par outils/telecharger_polices.py. Ne pas modifier a la main. */\n"
        "/* Silkscreen, IBM Plex Sans et IBM Plex Mono : SIL Open Font License 1.1. */\n\n"
    )
    feuille.write_text(entete + "\n".join(declarations), encoding="utf-8")
    print(f"{telecharges} fichiers telecharges dans {dossier}")
    print(f"feuille @font-face ecrite dans {feuille}")


if __name__ == "__main__":
    sys.exit(main())
