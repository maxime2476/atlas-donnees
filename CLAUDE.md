# CLAUDE.md

Règles permanentes pour toutes les sessions de travail sur ce projet.

## Contexte du projet

Site de référence pour data analysts et data scientists, construit par un enseignant
pour lui et ses élèves. Tu m'accompagnes étape par étape : tu travailles AVEC moi,
pas à ma place, et tu ne prends aucune décision structurante sans me la soumettre.

- Site statique en React basé sur **Docusaurus (TypeScript)**, hébergé sur **GitHub Pages**,
  déployé par **GitHub Actions**.
- Contenu organisé **par concept** (filtrer des lignes, jointure, groupby…). Chaque concept
  est montré dans plusieurs langages côte à côte (onglets synchronisés) :
  Python, SQL, R en priorité (MVP), puis Julia et Scala.
- **Principe central :** le code n'est jamais écrit directement dans les pages MDX.
  Il vit dans le dossier `extraits/`, où il est **exécuté et testé automatiquement**, puis
  il est injecté dans les pages. Tous les langages d'un même concept doivent produire
  **exactement la même sortie**, comparée à un fichier `attendu.csv`.
- Le SQL est exécuté avec **DuckDB** (pas de serveur, rapide en CI).
- Jeu de données : à arrêter à l'étape 2. Palmer Penguins (CC0, `donnees/manchots.csv`)
  convient aux concepts les plus simples, mais il est trop propre pour illustrer des
  problèmes professionnels réels. Il faut au moins un second jeu de données crédible
  et imparfait (valeurs manquantes, doublons, types ambigus), sous licence ouverte.
- À terme, mes élèves contribueront au site par pull requests.

---

# RÈGLES DE CODE

Écris du code comme un étudiant expérimenté et soigneux, pas comme un expert qui
cherche l'élégance maximale. Le code doit être lisible par un élève de niveau moyen.

- Fonctions courtes (idéalement moins de 30 lignes), qui font une seule chose.
- Pas de formules ni de constructions complexes :
  - pas de compréhensions imbriquées ;
  - pas de lambdas enchaînées ;
  - pas de métaprogrammation ;
  - pas d'expressions régulières compliquées ;
  - pas de one-liners « malins ».
- Préfère une boucle `for` claire à une construction compacte difficile à lire.
- Variables intermédiaires nommées plutôt que de longues chaînes d'appels.
- Typage simple en Python (`str`, `int`, `list[str]`, `Path`). Pas de génériques avancés.
- Docstring courte en français pour chaque fonction : ce qu'elle fait, ce qu'elle renvoie.
- Commentaires en français, qui expliquent le POURQUOI, pas le quoi.
- Gestion d'erreurs explicite, avec des messages d'erreur compréhensibles en français
  (fichier absent, runtime non installé, délai dépassé…).
- En TypeScript/React : composants fonctionnels simples, props typées avec une
  `interface`, pas de gestion d'état complexe, pas de bibliothèque ajoutée sans mon accord.
- Les extraits pédagogiques (dans `extraits/`) suivent le style idiomatique de chaque
  langage : pandas pour Python, dplyr (tidyverse) pour R, DataFrames.jl pour Julia.
  Ils doivent rester courts et lisibles par un débutant.

# NOMMAGE

Noms en français, sans accents, sans espaces, en `snake_case` pour les fichiers et
dossiers, en `PascalCase` pour les composants React. Noms clairs et professionnels.

Exceptions imposées par les outils (ne pas traduire) :
- fichiers GitHub : `README.md`, `CONTRIBUTING.md`, `LICENSE`, `CODEOWNERS`, `.github/` ;
- dossiers imposés par Docusaurus : `docs/`, `src/`, `static/` ;
- mots-clés des langages et noms des bibliothèques.

Arborescence cible :

```
racine/
├── CLAUDE.md
├── README.md
├── CONTRIBUTING.md
├── LICENSE                        # MIT pour le code
├── LICENCE_CONTENU.md             # CC BY 4.0 pour les textes
├── decisions/                     # une fiche par décision d'architecture
│   └── 001_choix_du_framework.md
├── site/                          # Docusaurus
│   ├── docs/
│   └── src/components/
│       ├── EnTeteConcept/
│       ├── TableauCorrespondance/
│       └── Exercice/
├── extraits/                      # code source de vérité, testé
│   └── manipulation/
│       └── filtrer_lignes/
│           ├── python.py
│           ├── r.R
│           ├── sql.sql
│           ├── julia.jl
│           ├── scala.sc
│           └── attendu.csv
├── donnees/
│   └── manchots.csv
├── outils/
│   ├── verifier_extraits.py       # exécute les extraits, compare à attendu.csv
│   ├── executer_sql.py            # exécute un fichier .sql avec DuckDB
│   └── generer_index.py           # produit l'index JSON des extraits pour le site
├── environnements/                # verrouillage des versions (renv, Julia…)
└── .github/workflows/
    ├── deploiement.yml
    └── verification_extraits.yml
```

Marqueurs dans les extraits pour délimiter la partie affichée sur le site :
- `# --- affichage:debut` et `# --- affichage:fin` (Python, R, Julia) ;
- `-- --- affichage:debut` et `-- --- affichage:fin` (SQL) ;
- `// --- affichage:debut` et `// --- affichage:fin` (Scala).

Ce qui est hors marqueurs (écriture du CSV de sortie pour les tests) n'est pas affiché.

Messages de commit en français, au format `type: description`
(types : feat, fix, docs, test, ci, refactor, chore).
Exemple : `feat: ajout du concept filtrer_lignes en Python, SQL et R`.

**Peu de commits** : environ 3 ou 4 pour l'ensemble du projet, aux jalons réels
(socle du dépôt, MVP technique fonctionnel, contenu complet, ouverture aux élèves).
On ne commite pas à chaque étape. Jamais de ligne de co-auteur dans un message.

# TON ET CONTENU

Le site est le travail d'un enseignant et de ses élèves. Rien d'autre ne doit
transparaître.

- **Aucune mention de l'IA**, nulle part dans ce qui est publié : pages MDX, README,
  CONTRIBUTING, fiches de décision, titres, exemples, messages de commit, descriptions
  de pull request, modèles d'issues. Pas de mention d'assistant, de modèle, de
  génération automatique, ni de signature ou de co-auteur automatique.
- **Aucune formulation qui sent le texte généré.** En particulier : pas de triades
  rhétoriques à répétition, pas de « il est important de noter que », pas de
  conclusions grandiloquentes qui résument ce qu'on vient de lire, pas de tirets
  cadratins en rafale, pas de vocabulaire promotionnel employé à vide
  (« puissant », « révolutionnaire », « élégant », « robuste »), pas de parallélismes
  négatifs du type « ce n'est pas X, c'est Y ».
- **Passage obligatoire par le skill `humanizer`** sur tout texte rédigé pour le site,
  avant de me le montrer : pages de concept, README, CONTRIBUTING, fiches de décision,
  énoncés d'exercices. Signale-moi dans le compte-rendu que le passage a été fait.
- **Ton** : professionnel, sobre, direct. On écrit comme une documentation technique
  d'entreprise sérieuse, pas comme un article de blog. Phrases courtes. Pas de
  familiarité, pas d'enthousiasme affiché, pas d'emoji dans le contenu publié.

# RÉALISME DES EXEMPLES

Le site doit être crédible pour quelqu'un qui travaille vraiment avec des données.

- Chaque concept est illustré par une situation qu'on rencontre réellement : en
  entreprise, en recherche expérimentale, en administration, en laboratoire. Pas
  d'exemple jouet gratuit.
- Chaque page de concept dit explicitement **quel problème concret on résout** et
  **pourquoi cette opération intervient à cet endroit** de la chaîne de traitement.
- Les pièges documentés sont des pièges réels, pas des curiosités de syntaxe :
  valeurs manquantes, types mal inférés à la lecture, doublons créés par une jointure,
  clé de jointure incomplète, fuseaux horaires, encodage, séparateur décimal,
  agrégation qui masque un déséquilibre d'effectifs.
- Quand une opération a un coût ou un risque en production (mémoire, lignes dupliquées,
  ordre de lignes non garanti, conversion implicite de type), la page le dit.
- Les exercices posent une question à laquelle un professionnel devrait savoir répondre,
  pas une manipulation de syntaxe hors contexte.

# OUTILS ET SKILLS

- **`humanizer`** (installé localement) : obligatoire sur tout texte destiné au site.
  Voir la section TON ET CONTENU.
- **`scientific-agent-skills`** (K-Dense-AI, dépôt sous licence MIT, chaque skill ayant
  sa propre licence à vérifier avant toute reprise de code) : référence méthodologique
  pour tout ce qui touche à l'analyse statistique, au plan d'expérience, à la
  visualisation et à la rédaction scientifique.
  Douze skills de cette collection sont installés dans `~/.claude/skills/`, donc **hors
  du dépôt** :
  - méthode et statistiques : `statistical-analysis`, `statistical-power`,
    `experimental-design`, `statsmodels`, `exploratory-data-analysis` ;
  - visualisation : `scientific-visualization`, `matplotlib`, `seaborn` ;
  - modélisation : `scikit-learn` ;
  - rédaction : `scientific-writing`, `peer-review`, `markdown-mermaid-writing`.

  Les 154 autres (bio-informatique, chimie, découverte de médicaments) ne sont pas
  installés et sont hors sujet ici.
- Avant d'utiliser un skill sur une page, dis-moi lequel et pourquoi. Aucune
  installation de skill sans mon accord explicite.

# DIRECTION ARTISTIQUE

La direction artistique est arrêtée. Elle fait foi et se trouve dans
`decisions/004_direction_artistique.md`. Toute question visuelle se tranche en s'y
reportant, pas au jugé.

Règles non négociables qui en découlent :

- **Registre** : terminal rétro, univers pixel. Deux modes complets, sombre « l'écran »
  et clair « le manuel », suivant la préférence du système.
- **Polices** : Silkscreen pour les titres et la navigation, IBM Plex Sans pour le corps,
  IBM Plex Mono pour le code. Toutes hébergées dans le dépôt, jamais appelées à distance.
- **Silkscreen uniquement en 8, 16, 24, 32 ou 48 pixels.** Toute autre taille rend les
  glyphes flous.
- **Grille de 8 pixels** pour tous les espacements : 8, 16, 24, 32, 48, 64. Aucun
  ajustement d'un ou deux pixels.
- **Aucun `border-radius`, aucune ombre floue.** Bordures de 2 pixels, reliefs par
  décalage plein.
- **Contrastes** : chaque couleur du site a un rapport calculé et consigné dans la fiche.
  Une nouvelle couleur ne s'ajoute qu'après calcul de son contraste.
- **Effet cathodique** : jamais mis en ligne sans le respect de `prefers-reduced-motion`
  et sans commande visible de désactivation. Jamais appliqué à un bloc de code, un
  tableau ou un champ de formulaire.
- Le niveau d'exigence attendu est celui d'un site produit : précision des espacements,
  cohérence des composants, lisibilité dans les deux modes, rendu correct sur mobile.
  Pas d'à-peu-près visuel.

# PROTOCOLE DE TRAVAIL

Pour CHAQUE étape de la feuille de route, suis exactement cette boucle :

1. **Annonce** : résume en 3 à 5 lignes ce que l'étape va produire.
2. **Questions** : pose-moi les questions listées pour l'étape, plus celles que tu juges
   utiles. Utilise l'outil de questions à choix multiples s'il est disponible
   (4 questions maximum par salve), sinon pose-les en texte numéroté.
   - Pour chaque question, propose 2 à 4 options, indique ta recommandation en premier
     et explique en une phrase le compromis de chaque option.
   - Si une question dépend de la réponse d'une autre, pose-les en deux salves.
3. **Plan** : présente la liste des fichiers que tu vas créer ou modifier.
   Attends mon « ok » avant d'écrire.
4. **Réalisation** : écris le code par petits morceaux cohérents.
5. **Vérification** : applique le protocole de vérification (section suivante).
   Si quelque chose échoue, corrige puis relance TOUTES les vérifications, pas seulement
   celle qui a échoué.
6. **Compte-rendu**, au format :
   - ✅ Ce qui est fait
   - 🧪 Résultat de chaque vérification (commande lancée + résultat)
   - ⚠️ Points d'attention ou dettes techniques notées
   - ❓ Questions ouvertes pour l'étape suivante
7. **Commit** : uniquement si l'étape termine un jalon. Sinon, ne propose rien et passe
   au point 8. À un jalon, propose le message et ne commite qu'après mon accord.
8. Ne passe JAMAIS à l'étape suivante sans mon feu vert explicite.

Si je te demande quelque chose qui contredit ces règles ou qui te semble une mauvaise
idée techniquement, dis-le clairement, explique pourquoi, propose une alternative,
puis laisse-moi trancher.

# PROTOCOLE DE VÉRIFICATION

Après chaque modification, lance toutes les vérifications pertinentes parmi celles-ci :

| Quoi | Commande |
|---|---|
| Build du site | `npm run build` (dans `site/`), doit finir sans erreur ni lien cassé |
| Types TypeScript | `npm run typecheck` (dans `site/`) |
| Extraits | `python outils/verifier_extraits.py --langages <langages actifs>` |
| Lint Python | `ruff check extraits outils` et `ruff format --check extraits outils` |
| Lint R | `Rscript -e "lintr::lint_dir('extraits')"` |
| Lint SQL | `sqlfluff lint extraits --dialect duckdb` |
| Tests des outils | `pytest outils` (tests unitaires des scripts d'outillage) |
| CI distante | après un push autorisé : `gh run list` puis `gh run watch` |

**Sous WSL, toute commande `node` ou `npm` doit être précédée de**
`export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh"`. Sans ça, un shell non
interactif retombe sur le npm de Windows (`/mnt/c/Program Files/nodejs`), ce qui
produit une installation inutilisable.

Règles :
- Montre-moi la commande et un extrait du résultat, jamais seulement « tout est vert ».
- Si un outil n'est pas installé, ne l'installe pas globalement sans me demander :
  signale-le et propose la commande d'installation.
- Si une vérification est impossible (outil absent, pas de réseau), dis-le explicitement
  au lieu de la sauter en silence.
- Après chaque nouvel extrait, vérifie aussi à la main dans le build que la partie
  affichée correspond bien à la zone entre les marqueurs.

# INTERDITS

- Pas de `git push`, de création de dépôt distant ni de modification des réglages GitHub
  sans mon accord explicite.
- Pas d'installation globale de paquets sans accord. Préfère les environnements locaux
  (uv pour Python, renv pour R, environnement de projet pour Julia).
- Pas de nouvelle dépendance npm, pip, CRAN, etc. sans m'expliquer pourquoi et sans
  mon accord.
- Pas de fichier de données de plus de 5 Mo dans le dépôt.
- Pas de code écrit directement dans une page MDX : il passe toujours par `extraits/`.
- Pas de modification de plusieurs étapes à la fois.
- Ne jamais désactiver un test ou une règle de lint pour « faire passer » la CI
  sans me le signaler.
- Aucune mention de l'IA dans quoi que ce soit de publié : site, dépôt, messages de
  commit, pull requests, issues. Pas de co-auteur automatique dans les commits.
- Pas de texte publié sans passage préalable par le skill `humanizer`.
- Pas d'exemple jouet sans ancrage dans une situation professionnelle ou de recherche
  réelle.
- Pas de choix visuel définitif avant réception de la direction artistique.
- Pas de commit en dehors des jalons, et jamais plus de 4 commits sur le projet.
