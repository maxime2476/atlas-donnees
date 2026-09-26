# Contribuer

Ce document explique comment ajouter ou corriger un concept. Les modalités d'accès au
dépôt, fork ou branche, seront précisées plus tard.

## Le principe à comprendre avant tout le reste

**Le code ne s'écrit jamais dans une page.** Il vit dans `extraits/`, où il est exécuté
et comparé à une sortie de référence à chaque modification. Les pages vont le chercher
là au moment de la construction du site.

Conséquence directe : les versions Python, SQL et R d'un même concept doivent produire
une sortie **identique au caractère près**. C'est la condition pour que la vérification
passe, pas une préférence de style.

## Installer le projet

Prérequis : Node 22 ou plus récent, Python 3.12 ou plus récent, `uv`, et R 4.5 avec
`dplyr` et `readr`.

```bash
git clone https://github.com/maxime2476/atlas-donnees.git
cd atlas-donnees
uv sync
cd site && npm install
```

Sous WSL, chargez nvm avant toute commande npm :

```bash
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"
```

Sans ce chargement, c'est le npm de Windows qui est utilisé et l'installation devient
inutilisable.

## Le contrat d'un extrait

Tout fichier placé dans `extraits/` doit respecter ces règles. Une seule qui manque et
la vérification échoue.

- Être exécutable seul depuis la racine du dépôt.
- Écrire son résultat final **en CSV sur la sortie standard**, et rien d'autre. Aucun
  message, aucun avertissement, aucune ligne de diagnostic.
- Nommer ses colonnes.
- **Trier sur toutes les colonnes affichées.** C'est ce qui garantit un ordre unique :
  si deux lignes restent à égalité sur tout ce qui est affiché, elles sont identiques, et
  leur ordre relatif n'a donc aucun effet sur le fichier produit. Sans cette règle, deux
  exécutions peuvent renvoyer les mêmes lignes dans un ordre différent.
- Suivre l'idiome de son langage : pandas en Python, dplyr en R, SQL standard exécuté
  par DuckDB. On n'écrit pas du R qui ressemble à du Python.
- Rester court et lisible par un débutant.

Les nombres sont arrondis à trois décimales au moment de la comparaison, ce qui absorbe
les écarts de représentation flottante entre les langages. Vous n'avez donc rien à
arrondir vous-même.

## Les marqueurs d'affichage

Seule la zone comprise entre deux marqueurs est montrée sur le site. Ce qui est en
dehors, typiquement l'écriture du CSV, sert aux tests et reste invisible.

| Langage | Marqueurs |
|---|---|
| Python, R, Julia | `# --- affichage:debut` et `# --- affichage:fin` |
| SQL | `-- --- affichage:debut` et `-- --- affichage:fin` |
| Scala | `// --- affichage:debut` et `// --- affichage:fin` |

Un marqueur manquant fait échouer la construction du site, avec un message qui nomme le
fichier fautif.

## Ajouter un concept, pas à pas

Prenons un concept appelé `trier_lignes`, dans le chapitre `manipulation`.

**1. Créer le dossier de l'extrait.**

```bash
mkdir -p extraits/manipulation/trier_lignes
```

**2. Écrire une première version**, par exemple en Python, dans
`extraits/manipulation/trier_lignes/python.py`. Placez les marqueurs, et faites écrire
le CSV en dehors.

**3. Produire le fichier de référence** depuis cette première version.

```bash
uv run python extraits/manipulation/trier_lignes/python.py \
  > extraits/manipulation/trier_lignes/attendu.csv
```

**4. Écrire les autres langages** et vérifier qu'ils produisent la même chose.

```bash
uv run python outils/verifier_extraits.py --concept trier_lignes
```

Tant que la commande n'affiche pas `3/3 extraits OK`, le concept n'est pas prêt. Lisez
le message : il indique la ligne qui diffère, avec la valeur attendue et celle obtenue.

**5. Écrire la page** dans `site/docs/manipulation/trier_lignes.mdx`, en partant du
modèle ci-dessous.

**6. Vérifier l'ensemble.**

```bash
uv run python outils/verifier_extraits.py
uv run ruff check outils extraits
uv run pytest outils
cd site && npm run typecheck && npm run test && npm run build
```

## Lancer les vérifications en local

| Commande | Ce qu'elle vérifie |
|---|---|
| `uv run python outils/verifier_extraits.py` | Tous les extraits produisent la sortie attendue |
| `uv run python outils/verifier_extraits.py --langages python sql` | Seulement certains langages |
| `uv run python outils/verifier_extraits.py --concept filtrer_lignes` | Seulement un concept |
| `uv run ruff check outils extraits` | Style du code Python |
| `uv run pytest outils` | Les outils de vérification eux-mêmes |
| `npm run typecheck` dans `site/` | Types TypeScript |
| `npm run test` dans `site/` | Le plugin d'injection du code |
| `npm run build` dans `site/` | Le site se construit, aucun lien mort |

Après toute modification d'une feuille de style, lancez `npm run clear` avant de
reconstruire, sinon l'ancienne version vous est servie sans avertissement.

## Le modèle d'une page de concept

Les sept sections sont obligatoires, dans cet ordre. Un plan imposé est ce qui rend les
pages comparables entre elles.

````markdown
---
id: nom_du_concept
title: Titre lisible
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Titre lisible

Une phrase qui dit ce que fait l'opération.

## À quoi ça sert

La situation concrète que l'opération résout, et pourquoi elle intervient à cet endroit
de la chaîne de traitement. Deux à quatre phrases. Pas d'exemple inventé.

## Ce qu'il faut savoir

Les prérequis. Une à deux phrases.

## Le code

<Tabs groupId="langage" queryString>
<TabItem value="python" label="Python" default>

```python fichier="extraits/manipulation/nom_du_concept/python.py"
```

Un commentaire sur ce qui est propre à ce langage.

</TabItem>
<TabItem value="sql" label="SQL">

```sql fichier="extraits/manipulation/nom_du_concept/sql.sql"
```

</TabItem>
<TabItem value="r" label="R">

```r fichier="extraits/manipulation/nom_du_concept/r.R"
```

</TabItem>
</Tabs>

## Ce que ça produit

```csv fichier="extraits/manipulation/nom_du_concept/attendu.csv" entier
```

## Les pièges

Les erreurs réellement commises : valeurs manquantes, types mal inférés, doublons,
casse des chaînes, ordre non garanti. Pas de curiosités de syntaxe.

## Ce que ça coûte

Mémoire, copies, lignes dupliquées, ordre non garanti. Ce que l'opération implique sur
un volume réel.

## Exercice

Un énoncé auquel un professionnel devrait savoir répondre, avec un indice et le résultat
à obtenir, tous deux repliables.
````

L'ordre des onglets est toujours Python, SQL, R, et Python porte l'attribut `default`.
L'attribut `groupId="langage"` est indispensable : c'est lui qui fait que le choix du
lecteur le suit de page en page.

## Style attendu

- Noms de fichiers et de dossiers en français, sans accents, sans espaces, en
  `snake_case`.
- Commentaires et docstrings en français. Ils expliquent le pourquoi, pas le quoi.
- Ton sobre. Pas d'emoji dans le contenu publié, pas de vocabulaire promotionnel.
- Messages de commit en français, au format `type: description`, avec `type` parmi
  `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`.

## Ce qui fait refuser une contribution

- Du code écrit directement dans une page au lieu de passer par `extraits/`.
- Un `attendu.csv` modifié pour faire passer un test. C'est le code qu'il faut corriger.
- Une dépendance ajoutée sans discussion préalable.
- Un exemple sans ancrage dans une situation réelle.
- Un test ou une règle de style désactivé pour faire passer l'intégration continue.
