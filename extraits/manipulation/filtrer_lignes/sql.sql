-- Filtrer des lignes : les manchots de l'ile Dream les plus lourds.

-- --- affichage:debut
SELECT
    espece,
    sexe,
    longueur_nageoire_mm,
    masse_g
FROM 'donnees/manchots.csv'
WHERE ile = 'Dream'
  AND masse_g > 4000
ORDER BY
    masse_g DESC,
    longueur_nageoire_mm DESC,
    espece,
    sexe
-- --- affichage:fin
;
