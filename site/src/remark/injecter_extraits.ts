/**
 * Plugin remark qui injecte le code des extraits dans les pages.
 *
 * Le code du site n'est jamais recopie dans le MDX : il vit dans extraits/, ou il est
 * execute et compare a une sortie de reference. Une page declare le fichier a montrer,
 * et ce plugin va chercher la zone delimitee par les marqueurs d'affichage.
 *
 * Dans une page :
 *
 *     ```python fichier="extraits/manipulation/filtrer_lignes/python.py"
 *     ```
 *
 * L'attribut « entier » prend le fichier complet, sans chercher de marqueurs. Il sert
 * pour attendu.csv, qui n'en contient pas.
 *
 * Un fichier absent ou des marqueurs manquants font echouer la construction. Afficher
 * un bloc vide serait pire : personne ne le remarquerait.
 */

import fs from 'node:fs';
import path from 'node:path';

const MARQUEUR_DEBUT = 'affichage:debut';
const MARQUEUR_FIN = 'affichage:fin';

export interface AttributsBloc {
  fichier: string;
  entier: boolean;
}

export interface OptionsPlugin {
  /** Racine du depot. Par defaut le dossier parent de site/. */
  racine?: string;
}

/**
 * Lit les attributs d'un bloc de code.
 * Renvoie null si le bloc ne demande aucune injection.
 */
export function lireAttributs(meta: string | null | undefined): AttributsBloc | null {
  if (!meta) {
    return null;
  }
  const trouve = meta.match(/fichier="([^"]+)"/);
  if (trouve === null) {
    return null;
  }
  return { fichier: trouve[1], entier: /(^|\s)entier(\s|$)/.test(meta) };
}

/**
 * Retire de la ligne de metadonnees les attributs que ce plugin consomme.
 * Les autres attributs, comme title, doivent survivre.
 */
export function retirerAttributs(meta: string): string {
  const restant = meta.replace(/fichier="[^"]+"/, '').replace(/(^|\s)entier(?=\s|$)/, ' ');
  return restant.trim();
}

/**
 * Supprime les lignes vides en tete et en queue d'un bloc de lignes.
 */
function rognerLignesVides(lignes: string[]): string[] {
  let debut = 0;
  let fin = lignes.length;
  while (debut < fin && lignes[debut].trim() === '') {
    debut += 1;
  }
  while (fin > debut && lignes[fin - 1].trim() === '') {
    fin -= 1;
  }
  return lignes.slice(debut, fin);
}

/**
 * Retire l'indentation commune a toutes les lignes non vides.
 * Sans cela, un extrait ecrit dans une fonction s'afficherait decale.
 */
export function retirerIndentationCommune(lignes: string[]): string[] {
  let minimum = Number.POSITIVE_INFINITY;
  for (const ligne of lignes) {
    if (ligne.trim() === '') {
      continue;
    }
    const espaces = ligne.length - ligne.trimStart().length;
    if (espaces < minimum) {
      minimum = espaces;
    }
  }
  if (minimum === Number.POSITIVE_INFINITY || minimum === 0) {
    return lignes;
  }
  return lignes.map((ligne) => (ligne.trim() === '' ? ligne : ligne.slice(minimum)));
}

/**
 * Extrait la zone situee entre les deux marqueurs d'affichage.
 * Leve une erreur explicite si un marqueur manque.
 */
export function extraireZone(contenu: string, chemin: string): string {
  const lignes = contenu.split('\n');
  let debut = -1;
  let fin = -1;

  for (let numero = 0; numero < lignes.length; numero += 1) {
    if (debut === -1 && lignes[numero].includes(MARQUEUR_DEBUT)) {
      debut = numero;
    } else if (debut !== -1 && lignes[numero].includes(MARQUEUR_FIN)) {
      fin = numero;
      break;
    }
  }

  if (debut === -1) {
    throw new Error(
      `Marqueur « ${MARQUEUR_DEBUT} » absent de ${chemin}. ` +
        'Ajoutez-le, ou utilisez l\'attribut « entier » pour injecter tout le fichier.',
    );
  }
  if (fin === -1) {
    throw new Error(
      `Marqueur « ${MARQUEUR_FIN} » absent de ${chemin}, alors que « ${MARQUEUR_DEBUT} » ` +
        'est present. La zone a afficher n\'est pas fermee.',
    );
  }

  const zone = rognerLignesVides(lignes.slice(debut + 1, fin));
  if (zone.length === 0) {
    throw new Error(`La zone d'affichage de ${chemin} est vide.`);
  }
  return retirerIndentationCommune(zone).join('\n');
}

/**
 * Parcourt recursivement un arbre mdast en appliquant une action a chaque noeud.
 * Ecrit a la main pour eviter d'ajouter une dependance au projet.
 */
function parcourir(noeud: unknown, action: (noeud: Record<string, unknown>) => void): void {
  if (noeud === null || typeof noeud !== 'object') {
    return;
  }
  const courant = noeud as Record<string, unknown>;
  action(courant);
  const enfants = courant.children;
  if (Array.isArray(enfants)) {
    for (const enfant of enfants) {
      parcourir(enfant, action);
    }
  }
}

/**
 * Construit le plugin remark. Renvoie la fonction de transformation attendue par unified.
 */
export default function injecterExtraits(options: OptionsPlugin = {}) {
  const racine = options.racine ?? path.resolve(process.cwd(), '..');

  return (arbre: unknown, fichierMdx?: { path?: string }) => {
    parcourir(arbre, (noeud) => {
      if (noeud.type !== 'code') {
        return;
      }
      const attributs = lireAttributs(noeud.meta as string | null);
      if (attributs === null) {
        return;
      }

      const chemin = path.resolve(racine, attributs.fichier);
      const page = fichierMdx?.path ?? 'page inconnue';
      if (!fs.existsSync(chemin)) {
        throw new Error(
          `Extrait introuvable : ${attributs.fichier}\n` +
            `  demande par : ${page}\n` +
            `  cherche ici : ${chemin}`,
        );
      }

      const contenu = fs.readFileSync(chemin, 'utf8');
      try {
        noeud.value = attributs.entier
          ? contenu.replace(/\s+$/, '')
          : extraireZone(contenu, attributs.fichier);
      } catch (erreur) {
        const message = erreur instanceof Error ? erreur.message : String(erreur);
        throw new Error(`${message}\n  demande par : ${page}`);
      }

      noeud.meta = retirerAttributs(noeud.meta as string) || null;
    });
  };
}
