"""Tests des fonctions de normalisation et de comparaison du verificateur.

Ces fonctions decident si un extrait est juste ou faux. Un comparateur trop
permissif validerait des extraits errones sans que personne ne s'en apercoive,
d'ou ces tests.
"""

from verifier_extraits import (
    comparer,
    normaliser_cellule,
    normaliser_nombre,
    normaliser_sortie,
)

# --- normaliser_nombre -------------------------------------------------------


def test_un_entier_reste_un_entier():
    assert normaliser_nombre("4800") == "4800"


def test_un_flottant_entier_perd_son_zero_final():
    """C'est le cas central : pandas ecrit 4800.0 la ou DuckDB ecrit 4800."""
    assert normaliser_nombre("4800.0") == "4800"


def test_les_zeros_inutiles_sont_retires():
    assert normaliser_nombre("39.100") == "39.1"


def test_l_arrondi_se_fait_a_trois_decimales():
    assert normaliser_nombre("3.14159") == "3.142"


def test_deux_ecritures_du_meme_nombre_se_rejoignent():
    assert normaliser_nombre("0.1000001") == normaliser_nombre("0.1")


def test_le_zero_negatif_devient_zero():
    """Sans cela, -0.0 et 0.0 seraient consideres comme differents."""
    assert normaliser_nombre("-0.0") == "0"
    assert normaliser_nombre("-0.0001") == "0"


def test_un_nombre_negatif_garde_son_signe():
    assert normaliser_nombre("-12.5") == "-12.5"


def test_la_notation_scientifique_est_developpee():
    assert normaliser_nombre("1e3") == "1000"


def test_un_texte_n_est_pas_modifie():
    assert normaliser_nombre("Chinstrap") == "Chinstrap"


def test_un_champ_vide_reste_vide():
    """Un champ vide represente une valeur manquante, il ne doit pas devenir zero."""
    assert normaliser_nombre("") == ""


def test_une_date_n_est_pas_traitee_comme_un_nombre():
    assert normaliser_nombre("2007-01-15") == "2007-01-15"


# --- normaliser_cellule -----------------------------------------------------


def test_les_espaces_de_bord_sont_supprimes():
    assert normaliser_cellule("  Adelie  ") == "Adelie"


def test_un_nombre_entoure_d_espaces_est_bien_normalise():
    assert normaliser_cellule(" 4800.0 ") == "4800"


# --- normaliser_sortie ------------------------------------------------------


def test_une_sortie_simple_est_decoupee_en_tableau():
    tableau = normaliser_sortie("espece,masse_g\nAdelie,3750\n")
    assert tableau == [["espece", "masse_g"], ["Adelie", "3750"]]


def test_les_fins_de_ligne_windows_sont_acceptees():
    """R sous Windows peut ecrire des fins de ligne CRLF."""
    unix = normaliser_sortie("a,b\n1,2\n")
    windows = normaliser_sortie("a,b\r\n1,2\r\n")
    assert unix == windows


def test_les_lignes_vides_sont_ignorees():
    tableau = normaliser_sortie("a,b\n1,2\n\n\n")
    assert len(tableau) == 2


def test_une_sortie_vide_donne_un_tableau_vide():
    assert normaliser_sortie("") == []


def test_les_nombres_sont_normalises_dans_tout_le_tableau():
    tableau = normaliser_sortie("a,b\n1.0,2.500\n")
    assert tableau == [["a", "b"], ["1", "2.5"]]


# --- comparer ---------------------------------------------------------------

REFERENCE = [["espece", "masse_g"], ["Adelie", "3750"], ["Gentoo", "5000"]]


def test_deux_tableaux_identiques_ne_produisent_aucun_ecart():
    assert comparer(REFERENCE, REFERENCE) == ""


def test_une_sortie_vide_est_signalee():
    message = comparer([], REFERENCE)
    assert "rien ecrit" in message


def test_un_en_tete_different_est_signale():
    obtenu = [["espece", "poids"], ["Adelie", "3750"], ["Gentoo", "5000"]]
    assert "En-tete different" in comparer(obtenu, REFERENCE)


def test_un_nombre_de_lignes_different_est_signale():
    obtenu = [["espece", "masse_g"], ["Adelie", "3750"]]
    message = comparer(obtenu, REFERENCE)
    assert "Nombre de lignes different" in message
    assert "2 attendue(s)" in message
    assert "1 obtenue(s)" in message


def test_une_valeur_differente_est_signalee_avec_son_numero_de_ligne():
    obtenu = [["espece", "masse_g"], ["Adelie", "3750"], ["Gentoo", "5001"]]
    message = comparer(obtenu, REFERENCE)
    assert "Ligne 2 differente" in message
    assert "5001" in message


def test_un_ordre_different_est_signale():
    """Deux tableaux aux memes lignes mais dans un autre ordre doivent differer."""
    obtenu = [["espece", "masse_g"], ["Gentoo", "5000"], ["Adelie", "3750"]]
    assert comparer(obtenu, REFERENCE) != ""


def test_l_ecriture_du_nombre_ne_cree_pas_de_faux_ecart():
    """4800 et 4800.0 doivent etre acceptes comme egaux apres normalisation."""
    attendu = normaliser_sortie("espece,masse_g\nAdelie,4800\n")
    obtenu = normaliser_sortie("espece,masse_g\nAdelie,4800.0\n")
    assert comparer(obtenu, attendu) == ""
