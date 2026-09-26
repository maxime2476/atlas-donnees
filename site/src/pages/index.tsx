import type { ReactNode } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

// Les langages du MVP, dans l'ordre d'affichage des onglets.
const LANGAGES = ['Python', 'SQL', 'R'];

interface Concept {
  dossier: string;
  titre: string;
  jeu: string;
  // Langages pour lesquels un extrait teste existe deja.
  disponibles: string[];
}

// Liste provisoire, arretee apres l'etape 5. Voir decisions/000_feuille_de_route.md.
const CONCEPTS: Concept[] = [
  { dossier: 'lire_un_fichier', titre: 'Lire un fichier', jeu: 'Manchots', disponibles: [] },
  { dossier: 'inspecter_un_tableau', titre: 'Inspecter un tableau', jeu: 'Manchots', disponibles: [] },
  { dossier: 'selectionner_colonnes', titre: 'Sélectionner des colonnes', jeu: 'Manchots', disponibles: [] },
  {
    dossier: 'filtrer_lignes',
    titre: 'Filtrer des lignes',
    jeu: 'Manchots',
    disponibles: ['Python', 'SQL', 'R'],
  },
  { dossier: 'trier_lignes', titre: 'Trier des lignes', jeu: 'Manchots', disponibles: [] },
  { dossier: 'creer_colonne', titre: 'Créer une colonne', jeu: 'Open Food Facts', disponibles: [] },
  { dossier: 'renommer_colonnes', titre: 'Renommer des colonnes', jeu: 'Open Food Facts', disponibles: [] },
  { dossier: 'valeurs_manquantes', titre: 'Valeurs manquantes', jeu: 'Open Food Facts', disponibles: [] },
  { dossier: 'supprimer_doublons', titre: 'Supprimer les doublons', jeu: 'Open Food Facts', disponibles: [] },
  { dossier: 'grouper_agreger', titre: 'Grouper et agréger', jeu: 'Accidents', disponibles: [] },
  { dossier: 'joindre_tables', titre: 'Joindre deux tables', jeu: 'Accidents', disponibles: [] },
  { dossier: 'pivoter_tableau', titre: 'Pivoter un tableau', jeu: 'Accidents', disponibles: [] },
];

interface CaseProps {
  present: boolean;
  langage: string;
  concept: string;
}

function CaseDisponibilite({ present, langage, concept }: CaseProps): ReactNode {
  // Le marqueur visuel est double d'un texte lu par les lecteurs d'ecran :
  // une information portee par le seul symbole serait inaccessible.
  const description = present
    ? `${langage} disponible pour ${concept}`
    : `${langage} pas encore écrit pour ${concept}`;
  return (
    <td className={styles.case}>
      <span aria-hidden="true">{present ? '[x]' : '[ ]'}</span>
      <span className={styles.lectureEcran}>{description}</span>
    </td>
  );
}

function TableauConcepts(): ReactNode {
  return (
    <table className={styles.tableau}>
      <caption className={styles.legende}>
        Chapitre manipulation. Une case cochée signifie qu'un extrait existe et qu'il
        passe les vérifications.
      </caption>
      <thead>
        <tr>
          <th scope="col">Concept</th>
          <th scope="col">Données</th>
          {LANGAGES.map((langage) => (
            <th scope="col" key={langage}>{langage}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {CONCEPTS.map((concept) => (
          <tr key={concept.dossier}>
            <th scope="row" className={styles.nomConcept}>
              {/* Un concept sans aucun extrait n'a pas encore de page a lier. */}
              {concept.disponibles.length > 0 ? (
                <Link to={`/docs/manipulation/${concept.dossier}`}>{concept.titre}</Link>
              ) : (
                concept.titre
              )}
            </th>
            <td className={styles.jeu}>{concept.jeu}</td>
            {LANGAGES.map((langage) => (
              <CaseDisponibilite
                key={langage}
                present={concept.disponibles.includes(langage)}
                langage={langage}
                concept={concept.titre}
              />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function Accueil(): ReactNode {
  return (
    <Layout
      title="Atlas des données"
      description="Le même concept d'analyse de données, montré dans plusieurs langages, exécuté et vérifié à chaque modification."
    >
      <main className={styles.page}>
        <h1>Atlas des données</h1>
        <p className={styles.accroche}>
          Le même concept d'analyse, montré côte à côte en Python, SQL et R. Le code
          n'est pas recopié dans les pages : il vit dans des fichiers exécutés et
          comparés à une sortie de référence à chaque modification.
        </p>
        <TableauConcepts />
        <p>
          <Link to="/docs/manipulation">Entrer dans le chapitre manipulation</Link>
        </p>
      </main>
    </Layout>
  );
}
