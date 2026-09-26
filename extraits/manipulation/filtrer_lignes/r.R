# Filtrer des lignes : les manchots de l'ile Dream les plus lourds.

# --- affichage:debut
library(readr)
library(dplyr)

# show_col_types desactive le recapitulatif des types, qui encombrerait la console.
manchots <- read_csv("donnees/manchots.csv", show_col_types = FALSE)

resultat <- manchots |>
  filter(ile == "Dream", masse_g > 4000) |>
  select(espece, sexe, longueur_nageoire_mm, masse_g) |>
  arrange(desc(masse_g), desc(longueur_nageoire_mm), espece, sexe)
# --- affichage:fin

write_csv(resultat, stdout())
