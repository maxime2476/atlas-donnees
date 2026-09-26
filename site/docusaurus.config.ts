import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import { themes as prismThemes } from 'prism-react-renderer';

const config: Config = {
  title: 'Atlas des données',
  tagline: 'Le même concept, dans plusieurs langages, exécuté et vérifié',
  favicon: 'img/favicon.svg',

  // baseUrl doit correspondre au nom du dépôt, sinon tous les liens cassent
  // une fois le site publié sur GitHub Pages.
  url: 'https://maxime2476.github.io',
  baseUrl: '/atlas-donnees/',
  organizationName: 'maxime2476',
  projectName: 'atlas-donnees',
  trailingSlash: false,

  // Un lien mort doit faire échouer la construction, pas passer inaperçu.
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'throw',

  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  i18n: {
    defaultLocale: 'fr',
    locales: ['fr'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/maxime2476/atlas-donnees/tree/main/site/',
        },
        // Le blog ne sert pas ce projet : le contenu est organisé par concept.
        blog: false,
        theme: {
          // Deux feuilles distinctes : une regle @import placee dans custom.css est
          // supprimee sans message par le pipeline CSS, les polices ne se chargent
          // alors jamais.
          customCss: ['./src/css/polices.css', './src/css/custom.css'],
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Atlas des données',
      logo: {
        alt: 'Atlas des données',
        src: 'img/logo.svg',
        srcDark: 'img/logo_sombre.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'chapitreManipulation',
          position: 'left',
          label: 'Manipulation',
        },
        {
          href: 'https://github.com/maxime2476/atlas-donnees',
          label: 'Code source',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Le site',
          items: [
            { label: 'Manipulation', to: '/docs/manipulation' },
          ],
        },
        {
          title: 'Licences',
          items: [
            { label: 'Code sous MIT', href: 'https://github.com/maxime2476/atlas-donnees/blob/main/LICENSE' },
            { label: 'Contenus sous CC BY 4.0', href: 'https://github.com/maxime2476/atlas-donnees/blob/main/LICENCE_CONTENU.md' },
          ],
        },
      ],
      copyright: `Maxime Gourguechon, ${new Date().getFullYear()}. Code sous licence MIT, contenus sous licence CC BY 4.0.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.vsDark,
      // java doit preceder scala : la definition Prism de Scala etend celle de
      // Java, et la construction echoue si Java n'est pas charge avant.
      additionalLanguages: ['r', 'julia', 'java', 'scala', 'sql', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
