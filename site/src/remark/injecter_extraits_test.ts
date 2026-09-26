/**
 * Tests du plugin d'injection des extraits.
 *
 * Ce plugin decide quel code s'affiche sur le site. S'il se trompe en silence, une page
 * peut montrer un code qui n'a jamais ete teste, ce qui est exactement ce que le projet
 * cherche a rendre impossible.
 */

import assert from 'node:assert/strict';
import path from 'node:path';
import { test } from 'node:test';

import injecterExtraits, {
  extraireZone,
  lireAttributs,
  retirerAttributs,
  retirerIndentationCommune,
} from './injecter_extraits.ts';

const RACINE = path.resolve(import.meta.dirname, '..', '..', '..');

function blocDeCode(meta: string) {
  return { type: 'code', lang: 'python', meta, value: '' } as Record<string, unknown>;
}

function arbreAvec(noeuds: Record<string, unknown>[]) {
  return { type: 'root', children: noeuds };
}

// --- lireAttributs ---------------------------------------------------------

test('un bloc sans metadonnees ne demande aucune injection', () => {
  assert.equal(lireAttributs(null), null);
  assert.equal(lireAttributs(''), null);
});

test('un bloc avec un titre seul ne demande aucune injection', () => {
  assert.equal(lireAttributs('title="exemple.py"'), null);
});

test('l attribut fichier est reconnu', () => {
  assert.deepEqual(lireAttributs('fichier="extraits/a/python.py"'), {
    fichier: 'extraits/a/python.py',
    entier: false,
  });
});

test('l attribut entier est reconnu', () => {
  const attributs = lireAttributs('fichier="extraits/a/attendu.csv" entier');
  assert.equal(attributs?.entier, true);
});

test('un nom de fichier contenant le mot entier ne declenche pas le mode entier', () => {
  const attributs = lireAttributs('fichier="extraits/entierement/python.py"');
  assert.equal(attributs?.entier, false);
});

// --- retirerAttributs ------------------------------------------------------

test('les attributs consommes disparaissent de la ligne de metadonnees', () => {
  assert.equal(retirerAttributs('fichier="a/b.py"'), '');
  assert.equal(retirerAttributs('fichier="a/b.csv" entier'), '');
});

test('un attribut etranger survit', () => {
  assert.equal(retirerAttributs('fichier="a/b.py" title="b.py"'), 'title="b.py"');
});

// --- retirerIndentationCommune ---------------------------------------------

test('l indentation commune est retiree', () => {
  const resultat = retirerIndentationCommune(['    a = 1', '    b = 2']);
  assert.deepEqual(resultat, ['a = 1', 'b = 2']);
});

test('l indentation relative est conservee', () => {
  const resultat = retirerIndentationCommune(['  if vrai:', '      a = 1']);
  assert.deepEqual(resultat, ['if vrai:', '    a = 1']);
});

test('un bloc sans indentation n est pas modifie', () => {
  assert.deepEqual(retirerIndentationCommune(['a = 1']), ['a = 1']);
});

// --- extraireZone ----------------------------------------------------------

const EXTRAIT = [
  'import pandas as pd',
  '',
  '# --- affichage:debut',
  'donnees = pd.read_csv("x.csv")',
  '# --- affichage:fin',
  '',
  'print(donnees)',
].join('\n');

test('seule la zone entre les marqueurs est extraite', () => {
  assert.equal(extraireZone(EXTRAIT, 'x.py'), 'donnees = pd.read_csv("x.csv")');
});

test('les lignes vides de bord de zone sont rognees', () => {
  const contenu = '# --- affichage:debut\n\na = 1\n\n# --- affichage:fin\n';
  assert.equal(extraireZone(contenu, 'x.py'), 'a = 1');
});

test('un marqueur de debut absent leve une erreur explicite', () => {
  assert.throws(() => extraireZone('a = 1\n', 'x.py'), /affichage:debut.*absent/s);
});

test('un marqueur de fin absent leve une erreur explicite', () => {
  assert.throws(
    () => extraireZone('# --- affichage:debut\na = 1\n', 'x.py'),
    /affichage:fin.*absent/s,
  );
});

test('une zone vide leve une erreur', () => {
  const contenu = '# --- affichage:debut\n# --- affichage:fin\n';
  assert.throws(() => extraireZone(contenu, 'x.py'), /vide/);
});

test('le message d erreur nomme le fichier fautif', () => {
  assert.throws(() => extraireZone('a = 1\n', 'extraits/truc/python.py'), /extraits\/truc/);
});

// --- le plugin sur un vrai extrait du depot --------------------------------

test('le plugin injecte le code du vrai extrait filtrer_lignes', () => {
  const noeud = blocDeCode('fichier="extraits/manipulation/filtrer_lignes/python.py"');
  injecterExtraits({ racine: RACINE })(arbreAvec([noeud]));
  assert.match(noeud.value as string, /read_csv\("donnees\/manchots\.csv"\)/);
  // Ce qui est hors marqueurs ne doit pas apparaitre sur le site.
  assert.doesNotMatch(noeud.value as string, /import pandas/);
  assert.doesNotMatch(noeud.value as string, /print\(/);
});

test('le mode entier injecte tout le fichier de reference', () => {
  const noeud = blocDeCode('fichier="extraits/manipulation/filtrer_lignes/attendu.csv" entier');
  injecterExtraits({ racine: RACINE })(arbreAvec([noeud]));
  assert.match(noeud.value as string, /^espece,sexe,longueur_nageoire_mm,masse_g/);
});

test('un fichier absent fait echouer la construction', () => {
  const noeud = blocDeCode('fichier="extraits/nexiste/pas.py"');
  assert.throws(
    () => injecterExtraits({ racine: RACINE })(arbreAvec([noeud]), { path: 'page.mdx' }),
    /Extrait introuvable.*page\.mdx/s,
  );
});

test('un bloc de code ordinaire est laisse intact', () => {
  const noeud = { type: 'code', lang: 'bash', meta: null, value: 'ls -la' } as Record<
    string,
    unknown
  >;
  injecterExtraits({ racine: RACINE })(arbreAvec([noeud]));
  assert.equal(noeud.value, 'ls -la');
});

test('un bloc imbrique profondement est bien trouve', () => {
  const noeud = blocDeCode('fichier="extraits/manipulation/filtrer_lignes/python.py"');
  const arbre = arbreAvec([{ type: 'blockquote', children: [arbreAvec([noeud])] }]);
  injecterExtraits({ racine: RACINE })(arbre);
  assert.match(noeud.value as string, /read_csv/);
});
