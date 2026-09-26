# 001. Choix du framework

Décidé le 25 septembre 2026.

## Contexte

Le site doit afficher un même concept dans plusieurs langages, avec des onglets dont la
sélection se propage d'une page à l'autre : un lecteur qui choisit R doit rester en R
en changeant de page. Le code affiché doit provenir de fichiers versionnés et testés,
jamais être recopié dans la page. Le site est statique, hébergé sur GitHub Pages, et
recevra des contributions d'étudiants par pull requests.

## Options examinées

**Docusaurus.** Générateur statique React, maintenu par Meta, conçu pour la
documentation technique. Les onglets synchronisés existent nativement via `groupId`, y
compris la persistance dans l'URL. L'écriture se fait en MDX, donc le Markdown accepte
des composants React. TypeScript pris en charge. Contrepartie : c'est un écosystème
Node, avec les mises à jour que cela suppose.

**Quarto.** Très adapté au contenu scientifique, exécute nativement des blocs Python, R
et Julia, produit des onglets. Mais Quarto exécute le code au moment du rendu du
document. Or le projet veut l'inverse : le code est testé séparément, dans une chaîne
d'intégration continue, et la page ne fait qu'afficher un résultat déjà validé.
Quarto imposerait aussi une chaîne R ou Python complète à chaque construction du site.

**Astro.** Excellent en performance, agnostique côté framework. Mais rien n'est fourni
pour les onglets synchronisés ni pour la structure documentaire : sommaire, versions,
recherche, fil d'Ariane seraient à construire.

**Application React écrite à la main.** Contrôle total, et tout à écrire : routage,
rendu Markdown, coloration syntaxique, recherche, accessibilité. Ce travail devrait
être maintenu indéfiniment, pour des besoins que les autres options couvrent déjà.

## Décision

**Docusaurus, en TypeScript.**

Le point décisif est la synchronisation des onglets, qui est le mécanisme central du
site et que Docusaurus fournit sans code supplémentaire. Le second point est la
séparation nette entre l'exécution du code et son affichage, que Quarto ne permet pas
dans le sens voulu.

## Conséquences

- Node est nécessaire pour construire le site. Version 22 fixée par nvm.
- Les pages sont en MDX. L'injection du code depuis `extraits/` passera par un plugin
  remark, choisi à l'étape 5.
- Le paramètre `baseUrl` doit correspondre au nom du dépôt, faute de quoi les liens
  cassent sur GitHub Pages.
- `onBrokenLinks` sera réglé sur `throw` : un lien mort fait échouer la construction
  plutôt que de passer inaperçu.
- Migrer vers un autre générateur plus tard resterait possible : le contenu est du
  Markdown et le code source de vérité vit hors du site, dans `extraits/`.
