# Atlas des données

**https://maxime2476.github.io/atlas-donnees/**

Ouvrage de référence sur les opérations d'analyse de données, présentées côte à côte
dans plusieurs langages.

## Ce que contient le site

Chaque page traite une opération : filtrer des lignes, joindre deux tables, agréger par
groupe. La même opération est montrée en Python, SQL et R, sur les mêmes données, avec
la même sortie. Qui connaît déjà un langage trouve l'équivalent dans les autres. Qui
n'en connaît aucun voit ce qui relève du raisonnement et ce qui relève de la syntaxe.

Julia et Scala seront ajoutés une fois les trois premiers langages en place.

## Pour qui

Étudiants en BTS, BUT, licence et master qui abordent l'analyse de données. Le site
part du principe qu'on découvre la programmation : la syntaxe est expliquée, pas
supposée acquise.

## Le principe de fonctionnement

Aucun code n'est écrit dans les pages du site. Le code vit dans `extraits/`, où il est
exécuté à chaque modification et comparé à une sortie de référence stockée en
`attendu.csv`. Les pages vont chercher le code à cet endroit au moment de la
construction du site.

Un exemple faux ne peut donc pas rester publié : l'intégration continue refuse la
modification. Cette contrainte en impose une seconde, qui est recherchée. Les
langages d'un même concept doivent produire une sortie identique au caractère près,
ce qui écarte les équivalences approximatives.

Le SQL est exécuté avec DuckDB, sans serveur à installer.

## Les jeux de données

| Jeu | Usage | Licence |
|---|---|---|
| Palmer Penguins | Les cinq premières opérations, sur des données propres | CC0 |
| Open Food Facts | Le nettoyage : champs libres, unités incohérentes, valeurs aberrantes | ODbL |
| Accidents corporels de la circulation routière (ONISR) | Les jointures et l'agrégation, sur un modèle à quatre tables | Licence Ouverte 2.0 |

La progression suit la difficulté réelle du travail : des données propres, puis des
données sales, puis plusieurs tables à relier.

## Installation

Prérequis : Node 22 ou plus récent, Python 3.13 ou plus récent, et R 4.5 pour les
extraits en R.

```bash
git clone https://github.com/maxime2476/atlas-donnees.git
cd atlas-donnees/site
npm install
npm start
```

Le site est alors accessible sur `http://localhost:3000/atlas-donnees/`.

Sous WSL, chargez nvm avant toute commande npm, faute de quoi le npm de Windows est
utilisé et l'installation devient inutilisable :

```bash
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"
```

Autres commandes utiles, depuis `site/` :

| Commande | Effet |
|---|---|
| `npm run build` | Construit le site pour la production |
| `npm run typecheck` | Vérifie les types TypeScript |
| `npm run serve` | Sert le site construit, pour contrôler le résultat réel |
| `npm run clear` | Vide les caches, nécessaire après un changement de feuille de style |

Les polices sont versionnées dans le dépôt. Pour les régénérer :

```bash
python3 outils/telecharger_polices.py
```

## Intégration continue

Deux workflows tournent sur GitHub Actions.

`verification_extraits.yml` exécute les extraits et compare leurs sorties, avec un job
par langage. Il se déclenche sur les pull requests qui touchent `extraits/`, `donnees/`
ou `outils/`.

`deploiement.yml` construit le site et le met en ligne à chaque envoi sur `main`. Il
appelle d'abord le workflow de vérification : **le site n'est jamais publié si un extrait
ne produit pas la sortie attendue.**

## Contribuer

Voir `CONTRIBUTING.md` : le contrat d'un extrait, l'ajout d'un concept pas à pas, et les
commandes de vérification à lancer en local.

## Licences

Le code est sous licence MIT, voir `LICENSE`. Les contenus rédactionnels sont sous
licence Creative Commons Attribution 4.0, voir `LICENCE_CONTENU.md`.
