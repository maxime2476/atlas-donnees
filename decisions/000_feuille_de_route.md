# Feuille de route

Document de travail. Il fixe l'ordre des étapes de construction du site et les
questions à trancher à chacune. Les règles permanentes sont dans `CLAUDE.md`.

État d'avancement : **étape 6 écrite, en attente du premier envoi. Prochaine étape : 7.**

---

## Étape 1 : Diagnostic de l'environnement

Tâches :
- Vérifier les outils présents et leurs versions : `git`, `gh`, `node`, `npm`, `python`,
  `uv`, `Rscript`, `julia`, `scala-cli`, `duckdb` (paquet Python).
- Présenter un tableau : outil, version trouvée, requis pour le MVP (oui/non), action proposée.

Questions à trancher :
- Système d'exploitation (Windows, macOS, Linux, WSL), qui impacte les scripts et les chemins.
- Un devcontainer / GitHub Codespaces pour les élèves dès maintenant, ou plus tard ?
- Quels langages pour le MVP (proposition : Python, SQL, R) ?
- Nom d'utilisateur GitHub, et compte personnel ou organisation ?

Vérification : tableau complet, aucune installation faite sans accord.

## Étape 2 : Cadrage et fiches de décision

Tâches :
- Rédiger `README.md` (vision, public, principes).
- Rédiger les fiches de décision :
  - `decisions/001_choix_du_framework.md` (Docusaurus vs Quarto vs Astro vs SPA maison) ;
  - `decisions/002_langages_du_mvp.md` ;
  - `decisions/003_strategie_de_test.md`.

  Format de chaque fiche : contexte, options, décision, conséquences.
- Proposer la liste des 12 concepts du chapitre « manipulation » pour le MVP.
- Arrêter le ou les jeux de données (voir la note en fin de document).

Questions à trancher :
- Nom du site et nom du dépôt.
- Public exact : lycée, BTS/BUT, licence, master, bootcamp, formation continue ?
- Niveau de départ supposé des élèves en programmation.
- Validation ou modification de la liste des 12 concepts.
- Licences : MIT + CC BY 4.0 proposées, ou autre (CC BY-SA, CC BY-NC) ?

Vérification : relecture des fiches, cohérence avec les réponses, liens internes valides.

## Étape 3 : Initialisation du dépôt et du site

Tâches :
- `git init`, `.gitignore` adapté (Node, Python, R, Julia, Scala, fichiers de l'OS).
- `npx create-docusaurus@latest site classic --typescript`.
- Configurer `docusaurus.config.ts` :
  - `url`, `baseUrl`, `organizationName`, `projectName`, `trailingSlash: false` ;
  - `onBrokenLinks: 'throw'` ;
  - locale `fr` ;
  - blog désactivé ;
  - langages Prism supplémentaires : r, julia, scala, sql, bash.
- Nettoyer le contenu d'exemple de Docusaurus.
- Page d'accueil minimale et arborescence de la sidebar selon la taxonomie.

Questions à trancher :
- Couleurs et identité visuelle : dépend de la direction artistique, à fournir avant
  cette étape (voir `CLAUDE.md`, section DIRECTION ARTISTIQUE).
- Page d'accueil : simple, ou avec présentation des parcours ?
- Mode sombre par défaut, clair par défaut, ou selon le système ?

Vérification : `npm run build`, `npm run typecheck`, `npm run serve` et test de la
navigation. Vérifier que `baseUrl` est correct : c'est le piège numéro un sur GitHub Pages.

## Étape 4 : Premier extrait et outil de vérification

Tâches :
- Ajouter le jeu de données retenu à l'étape 2. La méthode de récupération est à
  décider ensemble : le téléchargement réseau peut être bloqué.
- Créer le concept `extraits/manipulation/filtrer_lignes/` en Python, SQL, R, avec
  marqueurs d'affichage et `attendu.csv`.
- Contrat de chaque extrait :
  - exécutable seul depuis la racine du dépôt ;
  - écrit son résultat final en CSV sur la sortie standard ;
  - colonnes et tri explicites ;
  - nombres arrondis de façon explicite si nécessaire.
- Écrire `outils/executer_sql.py` : lit un `.sql`, l'exécute avec DuckDB, écrit le
  résultat en CSV sur la sortie standard.
- Écrire `outils/verifier_extraits.py` :
  - parcourt `extraits/`, exécute chaque fichier avec la bonne commande selon le langage ;
  - normalise les sorties (fins de ligne, espaces de fin) et compare à `attendu.csv` ;
  - gère un délai maximum par extrait et un runtime absent (message clair) ;
  - affiche un résumé « X/Y extraits OK » et renvoie un code de sortie non nul en cas d'échec ;
  - option `--langages` pour filtrer.
- Écrire des tests `pytest` pour les fonctions de normalisation et de comparaison.

Questions à trancher :
- Normalisation des nombres : arrondi à combien de décimales dans les sorties ?
- Que faire quand un langage n'a pas d'équivalent idiomatique pour un concept :
  fichier absent, ou fichier `non_applicable.md` qui explique pourquoi (proposition) ?
- Délai maximum par extrait.

Vérification : lancer le vérificateur. Puis **casser volontairement** un extrait
(modifier une valeur) pour prouver que le test détecte l'erreur, et le restaurer.
Lancer `pytest outils` et les linters.

## Étape 5 : Injection des extraits dans les pages

Tâches :
- Mettre en place l'injection du code depuis `extraits/` dans le MDX. Les deux options
  et leurs compromis sont à présenter avant de coder :
  - A) plugin `remark-code-import` avec plages de lignes ;
  - B) petit plugin remark maison qui extrait la zone entre les marqueurs d'affichage
    (plus robuste, car les numéros de ligne ne cassent pas).
- Créer la page du concept avec `<Tabs groupId="langage" queryString>`.
- Créer un modèle de page de concept dans `CONTRIBUTING.md` : objectif, prérequis,
  code, pièges fréquents, performance, exercice.

Questions à trancher :
- Option A ou B ?
- Ordre des onglets et langage affiché par défaut.
- Sections obligatoires de chaque page de concept.

Vérification : build, puis contrôle visuel que le code affiché correspond exactement à
la zone entre les marqueurs, dans chaque langage. Modifier un extrait, rebuild et
vérifier que la page change.

## Étape 6 : Intégration continue et déploiement

Tâches :
- `.github/workflows/verification_extraits.yml` : un job par langage, déclenché
  seulement quand les fichiers concernés changent, avec cache des dépendances et
  versions verrouillées.
- `.github/workflows/deploiement.yml` : build Docusaurus puis déploiement GitHub Pages
  via les actions officielles `upload-pages-artifact` et `deploy-pages`.
  Vérifier les dernières versions majeures des actions.
- Lister les réglages GitHub à faire à la main : Pages en source « GitHub Actions »
  et protection de la branche `main`.

Questions à trancher :
- Le déploiement doit-il attendre que la vérification des extraits soit verte ?
- Dépôt public dès maintenant, ou privé pendant la construction ? GitHub Pages sur
  dépôt privé dépend de l'offre GitHub : l'offre souscrite est à préciser.

Vérification : validation de la syntaxe YAML (avec `actionlint` si disponible), puis,
après accord pour le push, suivi de la CI avec `gh run watch` et test de l'URL publique.

## Étape 7 : Qualité automatique du code

Tâches :
- Configurer `pre-commit` : ruff, lintr, sqlfluff (dialecte duckdb), prettier pour
  TS et MDX.
- Verrouiller les environnements (`uv.lock`, `renv.lock`).
- Si validé à l'étape 1 : devcontainer avec Node, Python, R, DuckDB.

Questions à trancher :
- Niveau de sévérité des linters (strict dès le départ, ou progressif) ?
- Devcontainer léger (MVP seulement) ou complet (tous les langages, plus lent à démarrer) ?

Vérification : `pre-commit run --all-files`, puis un commit test qui doit être
bloqué par une erreur volontaire.

## Étape 8 : Composants React pédagogiques

Tâches, un composant à la fois :
- `EnTeteConcept` : niveau, prérequis, temps estimé.
- `Exercice` : énoncé, indice, solution repliable.
- `TableauCorrespondance` : matrice concept × langage, alimentée par un fichier JSON
  produit par `outils/generer_index.py` lancé avant le build (script `prebuild`).

Questions à trancher, pour chaque composant :
- Informations à afficher et apparence souhaitée.
- Pour l'exercice : solution visible directement, repliable, ou sur une page séparée ?

Vérification : typecheck, build, contrôle visuel en mode clair ET sombre, et sur
largeur mobile.

## Étape 9 : Production du contenu du MVP

Tâches :
- Produire les 11 concepts restants, **un concept à la fois**. Pour chacun : extraits,
  `attendu.csv`, page MDX, exercice.
- Après chaque concept : protocole de vérification complet.

Questions à trancher, pour chaque concept :
- Validation de l'exemple choisi et de sa difficulté.
- Pièges fréquents observés chez les élèves, à ajouter dans la page.

Vérification : tous les extraits verts, build vert, relecture de la page.

## Étape 10 : Ouverture aux élèves

Tâches :
- Finaliser `CONTRIBUTING.md` : ajouter un concept pas à pas, contrat d'un extrait,
  lancer les vérifications en local.
- Modèles d'issues (nouveau concept, erreur dans un extrait, proposition) et de pull request.
- Fichier `CODEOWNERS` pour relecture obligatoire de tout ce qui touche à `extraits/`.
- Étiquettes : « bon premier ticket », « langage manquant »…

Questions à trancher :
- Les élèves travaillent-ils par fork ou comme collaborateurs du dépôt ?
- Pseudonymes autorisés ? Y a-t-il des mineurs (implications sur la visibilité publique) ?

Vérification : simuler le parcours d'un élève de bout en bout (fork fictif ou branche,
ajout d'un concept, vérifications, PR) et lister tout ce qui a bloqué.

---

## Jalons de commit

Environ 3 à 4 commits sur l'ensemble du projet, pas un par étape :

1. Socle du dépôt et site qui compile (fin d'étape 3).
2. Chaîne technique complète : extraits testés, injection, CI, déploiement (fin d'étape 6).
3. Contenu du MVP et composants (fin d'étape 9).
4. Ouverture aux contributions (fin d'étape 10).

## Points ouverts

- **Échantillonnage d'Open Food Facts et des fichiers ONISR.** Doit être scripté et
  reproductible, chaque fichier sous 5 Mo. L'étape 4 n'a traité que les manchots, donc
  ce travail arrive à l'étape 9, quand les concepts 6 à 12 seront écrits. L'export
  complet d'Open Food Facts pesant plusieurs gigaoctets, il faudra passer par son API
  plutôt que par un téléchargement intégral.
- **Version de Python du projet.** `pyproject.toml` exige 3.12 ou plus, et `uv` a retenu
  3.12.13, plus proche de ce qu'auront les élèves que le 3.14.4 du poste. À confirmer à
  l'étape 7.
- **Cache des paquets R en CI.** Sans `renv`, `readr` et `dplyr` se réinstallent à chaque
  exécution du job R. Les binaires RSPM limitent le coût à environ une minute. Le cache
  correct viendra avec `renv`, à l'étape 7.
- **21 vulnérabilités npm**, dont une de niveau élevé, toutes héritées de l'arbre de
  dépendances de Docusaurus 3.10.2. Aucune ne vient du paquet d'icônes. `npm audit fix
  --force` casserait l'installation. À examiner à l'étape 7.
- **Rechargement à chaud.** En mode `npm start`, modifier un extrait ne rafraîchit pas
  la page, puisque le fichier MDX n'a pas changé. Un `npm run build` complet reflète
  bien la modification, ce qui a été vérifié. À améliorer si la gêne se confirme.

---

## Décisions prises à l'étape 1

| Sujet | Décision |
|---|---|
| Node | Fourni par nvm, version 22.22.3 fixée par défaut. Pas d'installation système. |
| Langages du MVP | Python, SQL, R. Julia et Scala après le MVP. |
| Devcontainer | Reporté à l'étape 7, une fois l'outillage réel connu. |
| Dépôt GitHub | Compte personnel `maxime2476`. Transfert vers une organisation possible plus tard. |

## Environnement de référence

Relevé le 25 septembre 2026, sur WSL2 / Ubuntu 26.04 LTS, noyau 6.6.114.1.
Le dépôt vit dans `/home/maxime/projets`, sur le système de fichiers Linux.

| Outil | Version | Statut |
|---|---|---|
| git | 2.53.0 (`/usr/bin/git`) | installé |
| gh | 2.93.0, connecté au compte `maxime2476` | installé |
| node | 22.22.3 via nvm | installé |
| npm | 10.9.8 via nvm | installé |
| python3 | 3.14.4 | installé |
| uv | 0.12.1 | installé |
| duckdb (paquet Python) | — | à ajouter au projet avec uv, étape 4 |
| pandas | — | à ajouter au projet avec uv, étape 4 |
| ruff, pre-commit | — | à ajouter au projet avec uv, étape 7 |
| Rscript | — | `sudo apt install r-base` (4.5.2), requis à l'étape 4 |
| julia, scala-cli | — | après le MVP |

**Piège WSL à connaître.** Le PATH de WSL expose les exécutables de Windows. Sans
chargement explicite de nvm, `npm` se résout vers `/mnt/c/Program Files/nodejs/npm`,
c'est-à-dire le npm de Windows, et une installation lancée depuis là est inutilisable.
Le chargement de nvm a été ajouté à `~/.bashrc`, ce qui couvre les shells interactifs.
Les shells non interactifs, eux, ne lisent pas cette partie du fichier : toute commande
automatisée doit charger nvm elle-même.

---

## Décisions prises à l'étape 2

| Sujet | Décision |
|---|---|
| Nom | Atlas des données. Dépôt `atlas-donnees`, URL `maxime2476.github.io/atlas-donnees`. |
| Public | BTS, BUT, licence et master. Niveau de départ supposé : débutant complet en programmation. |
| Licences | Code sous MIT, contenus sous CC BY 4.0. Titulaire : Maxime Gourguechon. |
| Jeux de données | Trois : Palmer Penguins, Open Food Facts, accidents ONISR. Voir `005_jeux_de_donnees.md`. |
| Liste des 12 concepts | Provisoire à ce stade. **Arrêtée le 26 septembre 2026**, après examen de la page de `filtrer_lignes`. |
| Direction artistique | Terminal rétro, univers pixel, deux modes. Voir `004_direction_artistique.md`. |

Fiches produites : `001_choix_du_framework.md`, `002_langages_du_mvp.md`,
`003_strategie_de_test.md`, `004_direction_artistique.md`, `005_jeux_de_donnees.md`.

## Les 12 concepts du chapitre « manipulation »

**Liste arrêtée le 26 septembre 2026**, après examen de la page de `filtrer_lignes`. Le
plan en sept sections a été validé en même temps. Ce tableau fait foi : c'est lui qui
fixe le programme de l'étape 9.

L'ordre suit le déroulement d'un traitement réel, du fichier brut au résultat agrégé.

| # | Dossier | Opération | Piège réel associé | Jeu de données |
|---|---|---|---|---|
| 1 | `lire_un_fichier` | Lire un CSV en maîtrisant séparateur, encodage et types | Types mal inférés, virgule décimale, UTF-8 contre Latin-1 | Manchots |
| 2 | `inspecter_un_tableau` | Dimensions, types, aperçu, taux de valeurs manquantes | Conclure sans avoir regardé les données | Manchots |
| 3 | `selectionner_colonnes` | Ne garder que les colonnes utiles | Colonnes homonymes après import | Manchots |
| 4 | `filtrer_lignes` | Restreindre selon une condition | Une valeur manquante ne satisfait aucun test | Manchots |
| 5 | `trier_lignes` | Ordonner, gérer les ex aequo | L'ordre n'est jamais garanti sans tri explicite | Manchots |
| 6 | `creer_colonne` | Colonne calculée, recodage | Division par zéro, propagation des manquants | Open Food Facts |
| 7 | `renommer_colonnes` | Normaliser les noms de colonnes | Accents et espaces dans les en-têtes | Open Food Facts |
| 8 | `valeurs_manquantes` | Détecter, compter, décider quoi en faire | Codes sentinelles pris pour de vraies valeurs | Open Food Facts |
| 9 | `supprimer_doublons` | Identifier un doublon, choisir la clé | Doublon partiel : même entité, lignes différentes | Open Food Facts |
| 10 | `grouper_agreger` | Compter, moyenner, agréger par groupe | Une moyenne qui masque un effectif de deux | Accidents ONISR |
| 11 | `joindre_tables` | Types de jointures, choix de la clé | Jointure qui multiplie les lignes, clés non uniques | Accidents ONISR |
| 12 | `pivoter_tableau` | Passer du format large au format long | Perte d'information sur les colonnes non pivotées | Accidents ONISR |

## Décisions prises à l'étape 3

| Sujet | Décision |
|---|---|
| Page d'accueil | Tableau des 12 concepts par langage. Statique pour l'instant, remplacé par un composant à l'étape 8. |
| Logo | Glyphe pixel 16x16 représentant un tableau, en deux versions selon le mode, plus le nom en Silkscreen. |
| Navigation | Un seul chapitre, Manipulation. Les autres seront ajoutés quand ils existeront. |
| Docusaurus | Version 3.10.2, React 19, TypeScript 6. |

## Pièges rencontrés à l'étape 3

Trois défauts réels ont été trouvés et corrigés. Ils sont consignés parce qu'ils se
reproduiront à la moindre réinstallation.

1. **Prism refuse de construire si `scala` précède `java`.** La définition Scala étend
   celle de Java, et la construction échoue sur une erreur illisible si Java n'est pas
   déclaré avant dans `additionalLanguages`.
2. **Une règle `@import` dans `custom.css` est supprimée sans message.** Les polices ne
   se chargeaient jamais et le site tournait en police de secours. La feuille des
   polices est donc déclarée comme second fichier `customCss`.
3. **Le minifieur supprime les `@font-face` dont la famille n'apparaît que dans une
   variable CSS.** `cssnano`, en préréglage `advanced`, applique `discardUnused` et ne
   sait pas lire une variable. Les familles sont donc déclarées littéralement dans les
   règles qui les utilisent, en plus des variables.

## Décisions prises à l'étape 4

| Sujet | Décision |
|---|---|
| Arrondi des sorties | 3 décimales, appliqué par le vérificateur et non par les extraits. |
| Langage sans équivalent idiomatique | Un fichier `non_applicable.md` qui explique pourquoi, plutôt qu'un fichier absent. |
| Délai maximum par extrait | 60 secondes. |
| Colonnes des données | Noms traduits en français, valeurs jamais modifiées. |
| Valeurs manquantes dans les données | Champ vide, lu comme manquant par Python, DuckDB et R. |
| Icônes | Paquet `@iconify-json/streamline-pixel` en dépendance de développement, 12 icônes extraites en SVG versionnés. |

## Contrat d'un extrait

Rappel opérationnel, pour ne pas avoir à relire la fiche 003 à chaque ajout.

- Exécutable seul depuis la racine du dépôt.
- Écrit son résultat final en CSV sur la sortie standard, et rien d'autre.
- Colonnes nommées, ordre de tri explicite.
- **Le tri porte sur toutes les colonnes de sortie.** C'est ce qui garantit un ordre
  total : si deux lignes restent à égalité sur toutes les colonnes affichées, elles sont
  identiques, et leur ordre relatif n'a donc aucun effet sur le CSV produit.
- Les marqueurs `affichage:debut` et `affichage:fin` délimitent la partie montrée sur le
  site. L'écriture du CSV reste en dehors.

## Décisions prises à l'étape 5

| Sujet | Décision |
|---|---|
| Injection du code | Plugin remark maison sur les marqueurs d'affichage, aucune dépendance ajoutée. `remark-code-import` écarté : non maintenu depuis juin 2023 et en désaccord de version avec `unified@11`. |
| Onglets | Python, SQL, R. Python par défaut. `groupId="langage"` et `queryString`. |
| Plan des pages | Sept sections obligatoires. Voir le modèle dans `CONTRIBUTING.md`. |
| Coloration syntaxique | Thèmes dérivés de la palette, définis en TypeScript. Voir la fiche 004. |

## Pièges rencontrés à l'étape 5

1. **`prism-react-renderer` applique son thème en styles inline**, qui l'emportent sur
   toute règle CSS. Une coloration syntaxique ne peut donc pas se faire par surcharge
   CSS : il faut définir de vrais objets de thème.
2. **`tsc` refuse un import se terminant par `.ts`**, alors que `node --test` l'exige.
   Résolu par `allowImportingTsExtensions` dans `tsconfig.json`.
3. **`node --test` ne prend pas un dossier en argument** ici : il tente de le charger
   comme un module. Le fichier de test est donc désigné explicitement dans le script npm.

## Décision reportée à l'étape 8

**Où vit le code des solutions d'exercice.** Les règles du projet interdisent d'écrire du
code dans une page, mais une solution d'exercice n'est pas un extrait de concept et n'a
pas sa place dans `extraits/manipulation/<concept>/` à côté de `attendu.csv`. En
attendant, la page de `filtrer_lignes` donne le résultat à obtenir, 9 lignes et une masse
moyenne de 3622,2 grammes, et non le code. L'élève doit écrire la solution lui-même, ce
qui est défendable pédagogiquement, mais la question devra être tranchée avec le
composant `Exercice`.

## Décisions prises à l'étape 6

| Sujet | Décision |
|---|---|
| Dépôt distant | `maxime2476/atlas-donnees`, **public**. Créé le 26 septembre 2026. |
| Conditionnement | `verification_extraits.yml` est appelable (`workflow_call`) et `deploiement.yml` l'invoque avec `needs`. Un `workflow_run` séparé aurait perdu le contexte des pull requests. |
| Contenu déployé | L'état courant, avec l'effet cathodique statique. L'effet animé et son bouton arrivent à l'étape 8. |
| Version de R en CI | 4.5.2, épinglée pour correspondre au poste de travail, alors que R 4.6.1 est publié. |

## Versions des actions, relevées le 26 septembre 2026

| Action | Version |
|---|---|
| `actions/checkout` | v7.0.1 |
| `actions/setup-node` | v7.0.0 |
| `actions/configure-pages` | v6.0.0 |
| `actions/upload-pages-artifact` | v5.0.0 |
| `actions/deploy-pages` | v5.0.1 |
| `astral-sh/setup-uv` | v10.2.0 |
| `r-lib/actions/setup-r` | v2 |

## Réglages GitHub à faire à la main

Ces deux réglages ne se font pas en ligne de commande.

1. **Settings → Pages → Source** : choisir « GitHub Actions ». Sans cela, l'étape
   `configure-pages` échoue et rien n'est publié.
2. **Settings → Rules** : protéger `main`, en exigeant une pull request et la réussite des
   vérifications avant fusion. À faire avant l'ouverture aux élèves, à l'étape 10.

## Reste à faire avant l'étape 7

- **À ne pas perdre de vue** : l'effet cathodique n'est que statique. Le scintillement
  animé et son bouton de désactivation relèvent de l'étape 8, et la direction
  artistique interdit de mettre l'effet animé en ligne sans ce bouton. La mise en
  ligne a lieu à l'étape 6, donc avant l'étape 8.
