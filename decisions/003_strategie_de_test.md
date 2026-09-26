# 003. Stratégie de test

Décidé le 25 septembre 2026.

## Contexte

Un site pédagogique qui publie du code faux est pire qu'inutile : l'élève perd du temps
et sa confiance dans la source. Le risque est permanent : les bibliothèques évoluent et un
exemple recopié finit par diverger de son original. Il augmentera encore quand des
contributions extérieures arriveront, à l'étape 10.

Le projet ajoute une contrainte propre : pour qu'une comparaison entre langages ait un
sens, les trois versions d'un même concept doivent produire le même résultat. Une
comparaison où Python renvoie 152 lignes et R 153 n'enseigne rien, elle induit en
erreur.

## Options examinées

**Relecture humaine.** Ne passe pas à l'échelle et ne détecte pas les régressions dues
aux mises à jour de bibliothèques.

**Tests unitaires par langage.** Chaque extrait aurait son test dans son écosystème :
pytest, testthat, un harnais SQL. Trois harnais à maintenir, et surtout rien ne
garantirait que les trois produisent la même chose, puisque chaque test vérifierait sa
propre attente.

**Sortie normalisée comparée à une référence commune.** Chaque extrait écrit son
résultat final en CSV sur la sortie standard. Un outil unique exécute tous les extraits
d'un concept et compare chaque sortie à un seul fichier `attendu.csv`.

## Décision

**Sortie normalisée comparée à un `attendu.csv` unique par concept.**

Un seul fichier de référence par concept, partagé par tous les langages. L'égalité des
sorties devient ainsi la condition de passage des tests, au lieu de rester une
intention affichée.

## Conséquences

Contrat que chaque extrait doit respecter :

- être exécutable seul depuis la racine du dépôt ;
- écrire son résultat final en CSV sur la sortie standard, et rien d'autre ;
- produire des colonnes nommées et un ordre de lignes explicite, puisque ni SQL ni
  pandas ne garantissent un ordre par défaut ;
- arrondir explicitement les nombres, les représentations flottantes différant d'un
  langage à l'autre.

Outillage à écrire à l'étape 4 :

- `outils/executer_sql.py`, qui exécute un fichier `.sql` avec DuckDB et écrit le
  résultat en CSV ;
- `outils/verifier_extraits.py`, qui parcourt `extraits/`, exécute chaque fichier avec
  la commande de son langage, normalise la sortie, la compare à `attendu.csv`, et
  renvoie un code de sortie non nul au moindre écart.

Le vérificateur doit gérer un runtime absent et un extrait qui ne se termine pas, avec
des messages compréhensibles. Ses fonctions de normalisation et de comparaison seront
elles-mêmes couvertes par des tests pytest : un comparateur trop permissif validerait
des extraits faux.

La chaîne sera vérifiée en cassant volontairement un extrait, pour prouver que l'échec
est bien détecté. Tant qu'un test n'a jamais échoué, rien ne garantit qu'il détecte
quoi que ce soit.
