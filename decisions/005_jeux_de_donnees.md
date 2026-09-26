# 005. Jeux de données

Décidé le 25 septembre 2026.

## Contexte

Le site doit être crédible pour quelqu'un qui travaille vraiment avec des données. Les
exemples doivent donc porter sur des situations qu'on rencontre en entreprise, en
administration ou en laboratoire, et sur des données qui présentent les défauts réels
de ces situations.

Palmer Penguins, envisagé au départ comme jeu unique, ne suffit pas. Le jeu est propre :
pas de doublons, pas de codes sentinelles, pas d'ambiguïté de type, pas de problème
d'encodage. Il permet d'enseigner l'opération, pas le métier.

Contrainte supplémentaire : le public visé découvre la programmation. Ouvrir le premier
chapitre sur un fichier de plusieurs centaines de colonnes à moitié vides découragerait
avant d'avoir enseigné quoi que ce soit.

## Options examinées

**Demandes de valeurs foncières (DVF).** Transactions immobilières, très réaliste, sous
Licence Ouverte. **Écarté pour raison juridique** : la DGFiP impose que la réutilisation
n'autorise ni l'indexation par les moteurs de recherche externes ni la réidentification
indirecte des personnes. Un site public indexé ne peut pas respecter cette clause.

**Open Food Facts.** Produits alimentaires renseignés par une communauté. Champs libres,
unités incohérentes, valeurs aberrantes, colonnes presque vides. Sujet neutre et
immédiatement compréhensible. Une seule grande table, donc les jointures y seraient
artificielles. Licence ODbL, avec partage à l'identique.

**Accidents corporels de la circulation routière (ONISR).** Quatre fichiers annuels
(`caracteristiques`, `lieux`, `vehicules`, `usagers`) liés par la clé `Num_Acc`. Les
jointures y sont la façon normale de travailler, alors qu'elles seraient un exercice
inventé sur une table unique. Variables
codées en entiers avec un dictionnaire séparé, valeurs manquantes notées `-1`, date
éclatée en plusieurs colonnes. Licence Ouverte 2.0, sans partage à l'identique.

## Décision

**Trois jeux, chacun avec un rôle distinct.**

| Concepts | Jeu | Rôle |
|---|---|---|
| 1 à 5 | Palmer Penguins | Apprendre l'opération sur des données propres et peu nombreuses |
| 6 à 9 | Open Food Facts | Affronter des données sales |
| 10 à 12 | Accidents ONISR | Travailler sur un modèle à plusieurs tables |

Cet ordre correspond à celui dans lequel un analyste débutant rencontre réellement ces
difficultés : il apprend l'opération, puis il découvre que les données résistent, puis
qu'elles sont réparties sur plusieurs tables.

## Conséquences

- Trois contextes métier à poser au lieu d'un. Chaque page doit rappeler en deux
  phrases de quoi parlent les données, sans supposer que la page précédente a été lue.
- Les extraits sont versionnés dans `donnees/`, sous forme d'échantillons réduits.
  Aucun fichier de plus de 5 Mo, conformément aux règles du projet. La méthode de
  constitution de ces échantillons doit être scriptée et reproductible, sans quoi
  personne ne pourra les régénérer.
- **Contrainte ODbL à respecter.** Tout extrait dérivé d'Open Food Facts, y compris les
  fichiers `attendu.csv` correspondants, est une base dérivée : il doit être repartagé
  sous ODbL et citer la source. Les fichiers concernés seront signalés explicitement.
- Les attributions des trois jeux figurent dans `LICENCE_CONTENU.md`.
- Le dictionnaire des variables ONISR devra être fourni ou résumé, faute de quoi les
  codes numériques resteront illisibles.
