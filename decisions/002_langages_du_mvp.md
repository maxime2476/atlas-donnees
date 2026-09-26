# 002. Langages du MVP

Décidé le 25 septembre 2026.

## Contexte

Le site vise cinq langages : Python, SQL, R, Julia et Scala. Chaque concept ajouté doit
être écrit, testé et maintenu dans chacun des langages actifs. Le coût de l'ajout d'un
concept croît donc linéairement avec le nombre de langages, et le coût d'installation
de la chaîne d'intégration continue aussi.

## Options examinées

**Python et SQL seulement.** Démarrage immédiat, rien à installer au-delà de ce qui est
présent. Mais deux langages ne démontrent pas la thèse du site, qui est la comparaison.
Avec deux colonnes, le tableau de correspondance n'a pas d'intérêt.

**Python, SQL et R.** Les trois cultures d'analyse réellement rencontrées. Python et
pandas côté ingénierie et production, SQL côté entrepôt de données, R et le tidyverse
côté statistique et recherche. Coût : installer `r-base`.

**Les cinq d'emblée.** Couverture maximale, mais Julia et Scala exigent chacun leur
runtime, leur gestion de dépendances et leur job d'intégration continue. Le risque est
de passer des semaines sur l'outillage avant d'avoir publié un seul concept.

## Décision

**Python, SQL et R pour le MVP.** Julia puis Scala après la publication des douze
premiers concepts.

## Conséquences

- `r-base` 4.5.2 à installer sur le poste de travail, et un job R dans l'intégration
  continue.
- Le style de chaque extrait suit l'idiome de son langage : pandas pour Python, dplyr
  pour R, SQL standard exécuté par DuckDB. On ne cherche pas à écrire du R qui
  ressemble à du Python.
- L'outil de vérification prend une option `--langages`, pour que l'ajout de Julia et
  Scala n'oblige pas à réécrire la chaîne.
- Quand un concept n'a pas d'équivalent idiomatique dans un langage, le manque sera
  documenté plutôt que masqué. La forme exacte est à décider à l'étape 4.
