# 004. Direction artistique

Décidée le 25 septembre 2026.

## Contexte

Le site doit se reconnaître immédiatement et rester lisible pour un débutant complet qui
va y passer des heures à lire du code. Ces deux exigences tirent dans des directions
opposées : une identité forte pousse vers des choix marqués, la lisibilité pousse vers
la neutralité.

La référence retenue est la collection d'icônes Pixel de Streamline, d'esthétique
années 80.

## Parti pris

**Registre terminal rétro plutôt qu'arcade.** L'univers pixel est décliné en écran de
terminal, pas en borne de jeu. Ce registre a un avantage concret au-delà de
l'esthétique : l'analyste travaille dans un terminal, donc le décor correspond au métier
enseigné au lieu de lui être étranger.

**Immersif sur l'habillage, lisible sur le contenu.** Les titres, la navigation et les
bordures assument le pixel. Le corps de texte et les blocs de code utilisent des
caractères dessinés pour être lus. Une police pixel appliquée à un paragraphe devient
illisible au bout de deux lignes, et sur un bloc de code elle rend le travail impossible.

## Les deux modes

Le site suit la préférence de l'appareil. Les deux modes changent de référence au lieu
de s'inverser l'un l'autre.

**Sombre, l'écran.** Noir profond, texte gris chaud, accent vert phosphore. C'est le
mode natif de la direction artistique.

**Clair, le manuel.** Papier crème, encre presque noire, vert d'imprimerie. Le mode clair
n'imite pas un terminal éclairé, il évoque le manuel papier qui accompagnait la console.
Un terminal à fond blanc serait une contradiction visuelle, et le rendu en pâtirait.

## Palette

Tous les rapports de contraste ci-dessous ont été calculés selon WCAG 2.1, à partir des
valeurs hexadécimales exactes des tableaux.

### Mode sombre

| Rôle | Valeur | Contraste sur le fond | Niveau |
|---|---|---|---|
| Fond | `#0D0D0D` | référence | |
| Surface (panneaux, blocs de code) | `#161614` | | |
| Texte | `#D8D8D0` | 13,56:1 | AAA |
| Texte atténué | `#A5A59C` | 7,83:1 | AAA |
| Accent, vert phosphore | `#00E05A` | 10,93:1 | AAA |
| Alerte, ambre | `#FFB000` | 10,61:1 | AAA |
| Bordure décorative | `#2E2E2A` | 1,43:1 | décorative uniquement |
| Bordure d'élément interactif | `#6B6B62` | 3,61:1 | conforme 1.4.11 |

### Mode clair

| Rôle | Valeur | Contraste sur le fond | Niveau |
|---|---|---|---|
| Fond, papier | `#F4F0E4` | référence | |
| Surface | `#FBF9F2` | | |
| Texte, encre | `#1A1A16` | 15,32:1 | AAA |
| Texte atténué | `#514F46` | 7,21:1 | AAA |
| Accent, vert d'imprimerie | `#0A5629` | 7,76:1 | AAA |
| Alerte, brun ambré | `#7A4200` | 7,07:1 | AAA |
| Bordure décorative | `#CFC9B6` | 1,45:1 | décorative uniquement |
| Bordure d'élément interactif | `#7A7260` | 4,19:1 | conforme 1.4.11 |

Les deux bordures décoratives sont sous le seuil de 3:1. C'est admis parce qu'elles ne
portent aucune information : elles habillent des surfaces. Dès qu'une bordure délimite
un élément cliquable, un onglet de langage par exemple, c'est la bordure d'élément
interactif qui s'applique.

L'accent ne sert jamais à distinguer deux informations à lui seul. Une couleur seule
exclut les lecteurs daltoniens, donc toute distinction portée par la couleur est
doublée par une forme, un mot ou une icône.

## Typographie

Trois familles, toutes sous licence SIL Open Font License, toutes hébergées dans le
dépôt. Aucun appel à un service de polices externe, ce qui évite une dépendance réseau
et une fuite de données vers un tiers.

| Usage | Police | Licence |
|---|---|---|
| Titres, navigation, étiquettes | Silkscreen, de Jason Kottke | OFL 1.1 |
| Corps de texte | IBM Plex Sans | OFL 1.1 |
| Code et sorties | IBM Plex Mono | OFL 1.1 |

IBM Plex a été retenue pour des raisons précises. Cette famille est née de
l'informatique d'entreprise,
elle tient le registre rétro-informatique sans verser dans le pastiche, et ses variantes
sans-serif et monospace ont été dessinées ensemble, donc elles s'accordent.

### Contrainte de taille propre à Silkscreen

Les glyphes de Silkscreen sont dessinés sur une grille de 4 pixels sur 5. À toute taille
qui n'est pas un multiple entier de la grille, le rendu devient flou et l'effet
recherché se retourne contre le site.

Tailles autorisées pour Silkscreen, et aucune autre : **8, 16, 24, 32, 48 pixels**.

Échelle du reste du texte :

| Élément | Taille | Interligne |
|---|---|---|
| Titre de page | 32 px Silkscreen | 40 px |
| Titre de section | 24 px Silkscreen | 32 px |
| Navigation, onglets | 16 px Silkscreen | 24 px |
| Corps | 16 px IBM Plex Sans | 24 px |
| Code | 16 px IBM Plex Mono | 24 px |
| Légende, note | 14 px IBM Plex Sans | 24 px |

Le code reste à 16 pixels. Le réduire ferait gagner de la place au détriment du seul
contenu que le lecteur vient vraiment lire.

## Grille et espacements

Base de 8 pixels, cohérente avec la grille des glyphes et avec celle des icônes.

Valeurs autorisées : 8, 16, 24, 32, 48, 64 pixels. Toute autre valeur est une erreur, y
compris les ajustements d'un ou deux pixels destinés à rattraper un alignement. Sur une
grille pixel, ces rattrapages se voient.

## Bordures et surfaces

- Bordures de 2 pixels, toujours nettes, jamais arrondies. Aucun `border-radius` sur
  l'ensemble du site.
- Aucune ombre portée floue. Les reliefs se traitent par un décalage plein de 4 pixels
  dans la couleur de bordure, à la manière des interfaces d'époque.
- Les blocs de code, les encadrés d'avertissement et les exercices se distinguent par
  leur bordure et leur couleur de surface, jamais par un dégradé.

## Icônes

Collection Pixel de Streamline, 662 icônes sous licence CC BY 4.0, dessinées sur une
grille de **32 par 32 pixels**. Le site de Streamline annonce du 64 par 64 ; le paquet
Iconify, qui est notre source réelle, fournit du 32 par 32. C'est cette valeur qui
compte pour les tailles d'affichage.

Le jeu complet est disponible par le paquet `@iconify-json/streamline-pixel`, en
dépendance de développement. Les icônes réellement utilisées sont extraites en SVG
autonomes vers `site/static/icones/` par `outils/extraire_icones.py`. Ajouter une icône
revient à ajouter une ligne au dictionnaire du script. Le paquet pourrait être retiré
sans casser le site, puisque les SVG sont versionnés.

Douze icônes sont extraites à ce jour : avertissement, information, exercice, indice,
code, base de données, filtre, lien, niveau, durée, objectif, fichier.

L'attribution CC BY 4.0 figure dans `LICENCE_CONTENU.md`.

Les icônes sont affichées à 16, 32 ou 64 pixels, seules tailles qui tombent juste sur
une grille de 32. Toute autre taille produit un rééchantillonnage visible.

## Effet cathodique

Traitement marqué, comme décidé : lignes de balayage visibles, halo prononcé sur la
couleur d'accent, léger scintillement animé.

### Garde-fous obligatoires

L'animation permanente déclenche des troubles chez certaines personnes, et WCAG 2.1
impose de pouvoir l'arrêter. Deux mécanismes sont donc exigés, sans quoi l'effet ne doit
pas être mis en ligne.

1. **Respect de `prefers-reduced-motion`.** Si le système du lecteur signale une
   préférence pour un mouvement réduit, le scintillement est désactivé sans intervention
   de sa part. Les lignes de balayage statiques peuvent rester.
2. **Commande visible.** Un bouton accessible depuis la barre de navigation coupe
   l'effet, et le choix est mémorisé localement d'une visite à l'autre.

L'effet ne s'applique jamais à l'intérieur d'un bloc de code, d'un tableau ou d'un champ
de formulaire, c'est-à-dire partout où le lecteur doit déchiffrer des caractères exacts.

## Conséquences

- Les polices sont versionnées dans le dépôt. Silkscreen pèse peu, les deux variantes
  d'IBM Plex seront limitées aux graisses réellement utilisées.
- La contrainte de grille interdit la plupart des réglages par défaut de Docusaurus. Une
  feuille de variables CSS devra les remplacer entièrement.
- Deux modes complets à maintenir. Toute page nouvelle se contrôle dans les deux, et
  cette vérification entre dans le protocole de l'étape 8.
- L'effet cathodique ajoute du JavaScript et un état persistant. C'est la seule part
  d'état de l'interface prévue à ce jour.

## Reste à décider

- Le logo. Un traitement pixel du nom en Silkscreen suffit peut-être, sans marque dessinée.
- La page d'accueil, traitée à l'étape 3.
- La représentation des trois jeux de données, qui gagneraient à être identifiables d'un
  coup d'œil par une icône dédiée. La collection Streamline Pixel ne contient ni manchot
  ni oiseau, il faudra donc détourner une icône existante ou en dessiner une.
