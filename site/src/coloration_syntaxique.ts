/**
 * Themes de coloration syntaxique derives de la palette du site.
 *
 * Ces themes sont definis en TypeScript et non en CSS parce que prism-react-renderer
 * applique ses couleurs en styles inline, qui l'emportent sur toute regle CSS.
 *
 * Les rapports de contraste sont calcules contre le fond des blocs de code, et non
 * contre le fond de page : c'est la que ces couleurs apparaissent. Voir la section
 * « Coloration syntaxique » de decisions/004_direction_artistique.md.
 *
 * Le fond est laisse transparent pour que la surface definie dans custom.css reste
 * la seule source de verite.
 */

import type { PrismTheme } from 'prism-react-renderer';

/** Mode clair, dit « le manuel ». Fond de bloc #FBF9F2. */
export const colorationClaire: PrismTheme = {
  plain: {
    color: '#1A1A16',
    backgroundColor: 'transparent',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: { color: '#6B6959', fontStyle: 'italic' },
    },
    {
      types: ['keyword', 'selector', 'important', 'atrule', 'rule'],
      style: { color: '#0A5629' },
    },
    {
      types: ['string', 'char', 'attr-value', 'regex', 'inserted'],
      style: { color: '#7A4200' },
    },
    {
      types: ['number', 'boolean', 'constant', 'symbol'],
      style: { color: '#0B5A60' },
    },
    {
      types: ['function', 'class-name', 'builtin'],
      style: { color: '#1A1A16', fontWeight: 'bold' },
    },
    {
      types: ['operator', 'punctuation', 'entity', 'url'],
      style: { color: '#514F46' },
    },
    {
      types: ['variable', 'property', 'attr-name', 'tag'],
      style: { color: '#1A1A16' },
    },
    {
      types: ['deleted'],
      style: { color: '#7A4200', fontStyle: 'italic' },
    },
  ],
};

/** Mode sombre, dit « l'ecran ». Fond de bloc #161614. */
export const colorationSombre: PrismTheme = {
  plain: {
    color: '#D8D8D0',
    backgroundColor: 'transparent',
  },
  styles: [
    {
      types: ['comment', 'prolog', 'doctype', 'cdata'],
      style: { color: '#8A8A82', fontStyle: 'italic' },
    },
    {
      types: ['keyword', 'selector', 'important', 'atrule', 'rule'],
      style: { color: '#00E05A' },
    },
    {
      types: ['string', 'char', 'attr-value', 'regex', 'inserted'],
      style: { color: '#FFB000' },
    },
    {
      types: ['number', 'boolean', 'constant', 'symbol'],
      style: { color: '#5FD7D7' },
    },
    {
      types: ['function', 'class-name', 'builtin'],
      style: { color: '#F0F0E8', fontWeight: 'bold' },
    },
    {
      types: ['operator', 'punctuation', 'entity', 'url'],
      style: { color: '#A5A59C' },
    },
    {
      types: ['variable', 'property', 'attr-name', 'tag'],
      style: { color: '#D8D8D0' },
    },
    {
      types: ['deleted'],
      style: { color: '#FFB000', fontStyle: 'italic' },
    },
  ],
};
