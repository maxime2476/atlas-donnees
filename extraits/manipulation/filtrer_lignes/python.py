"""Filtrer des lignes : les manchots de l'ile Dream les plus lourds."""

import pandas as pd

# --- affichage:debut
manchots = pd.read_csv("donnees/manchots.csv")

# Deux conditions combinees avec &. Chaque condition doit etre entre parentheses.
sur_dream = manchots["ile"] == "Dream"
assez_lourds = manchots["masse_g"] > 4000
selection = manchots[sur_dream & assez_lourds]

colonnes = ["espece", "sexe", "longueur_nageoire_mm", "masse_g"]
resultat = selection[colonnes].sort_values(
    by=["masse_g", "longueur_nageoire_mm", "espece", "sexe"],
    ascending=[False, False, True, True],
)
# --- affichage:fin

print(resultat.to_csv(index=False), end="")
