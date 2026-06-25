"""Garde-fou CENTRALISÉ anti-texte-français-non-accentué (Akainu B1/M1, 2026-06-26).

Tout générateur *from-scratch* (qui ÉMET des littéraux français, par opposition aux
générateurs token-replacement qui recopient verbatim un modèle source validé) doit
sortir un texte intégralement accentué. Ce helper centralise la liste noire et
l'assertion, en remplacement des copies locales qui divergeaient.

Discipline de la liste noire (vérifiée par scan runtime, cf.
``artifacts/_aksweep_scan.py``) : on ne retient QUE les suites de lettres dont la forme
NON accentuée est *sans ambiguïté* fautive — noms / adjectifs / participes employés
comme tels (« Société », « siège », « numéro », « prévoit », « immatriculée »…). On
EXCLUT volontairement :

* les mots accent-NEUTRES, corrects sans accent (« exercice », « fonctions »,
  « extraordinaires », « adresse ») ;
* les formes verbales 3ᵉ personne homographes d'un participe accentué — « il certifie »,
  « se situe », « il nomme », « constitue », « compose », « décide » : sans accent ce
  sont des verbes LÉGITIMES, les blacklister corromprait du texte correct.

Ces cas ambigus restent couverts par des assertions de littéral CIBLÉES dans le test du
générateur concerné (ex. note_information : ``"prévoit d'acquérir"``, ``"Après ladite
cession"``).

Usage dans un test::

    from _accents import assert_no_unaccented_french
    ...
    assert_no_unaccented_french(text)

⚠️ NE PAS appliquer aux générateurs token-replacement (scm_satellites_templates,
contrat_apport_spfpl, courrier_sde_cession_scm, acte_cession_parts_spfpl, …) : ceux-là
préservent la casse/orthographe VERBATIM du modèle source validé (y compris les
intitulés légaux en CAPITALES non accentuées « SOCIETE », « CONSEQUENCE », etc.).
"""
from __future__ import annotations

import re

# Liste noire des mots dont la forme NON accentuée est sans ambiguïté fautive
# (variantes minuscule + majuscule de début de phrase / intitulé).
MOTS_NON_ACCENTUES_INTERDITS: tuple[str, ...] = (
    # société & dérivés (jamais un verbe)
    "Societe", "societe", "Societes", "societes",
    "Simplifiee", "simplifiee", "simplifiees",
    "Financieres", "financieres", "Financiere", "financiere",
    "Liberale", "liberale", "Liberales", "liberales",
    # associé (nom/adj)
    "Associe", "associe", "Associes", "associes", "associee", "associees",
    # siège (nom)
    "Siege", "siege", "sieges",
    # prévoir conjugué + participe (jamais homographe sans accent)
    "prevoit", "prevoient", "prevu", "prevus", "prevue", "prevues",
    # acquérir / acquise
    "acquerir", "acquise", "acquises",
    # décomposé (participe ; « décompose » verbe exclu)
    "decompose", "decomposee", "decomposes",
    # immatriculé / numéro / numéroté
    "immatricule", "immatriculee", "immatricules", "immatriculees",
    "numero", "numeros", "numerotee", "numerotees",
    # après (jamais sans accent)
    "Apres", "apres",
    # qualité / quantité-nom
    "qualite", "qualites", "totalite", "totalites",
    "correlative", "correlativement",
    # libéré / attribué (participes)
    "liberees", "liberee", "liberes",
    "attribuees", "attribuee", "attribues",
    # manière / entièrement / inchangé
    "maniere", "manieres", "entierement", "inchange", "inchangee",
    # réuni / régulier / gérance
    "reunis", "reunie", "reunies", "reguliere", "regulier", "regulieres",
    "gerance",
    # assemblée (nom)
    "Assemblee", "assemblee", "Assemblees", "assemblees",
    "presidence", "seance", "seances",
    # résolution (nom) / proposé (participe)
    "resolutions", "resolution", "proposees", "proposee", "proposes",
    # réglementation / délai / précédé / composé(participe)
    "reglementation", "reglemente", "reglementee",
    "delai", "delais",
    "composee", "composees",  # participe accordé (verbe « compose » exclu)
    # formalités (nom) / déposé(participe)
    "formalites", "formalite",
    "deposee", "deposes",
    # décision (nom)
    "decisions", "decision",
    # répartition / dénommé / numéraire
    "Repartition", "repartition", "denommee", "denomme", "denommes", "denommees",
    "numeraire",
    # certifié(participe accordé)/sincère/véritable/président/réalisation
    "certifiee", "certifies", "sincere", "sinceres",
    "veritable", "veritables", "President", "Presidente",
    "realisation", "realisations",
    # délibération / durée
    "deliberation", "deliberations", "duree", "durees",
    # générale (adj) / nommé(participe accordé) / désigné(participe accordé)
    "Generale", "generale", "Generales", "generales",
    "nommee", "nommes", "nommees",
    "designee", "designes", "designees",
    # nomination / rémunération / arrêté(participe accordé)
    "nominations", "nomination", "remuneration", "remunerations",
    "arretee", "arretes",
    # opération / période / échéance / bénéficiaire / médecin
    "operation", "operations", "periode", "periodes",
    "echeance", "echeances", "beneficiaire", "beneficiaires",
    "medecin", "medecins",
)


def assert_no_unaccented_french(text: str) -> None:
    """Échoue si la sortie générée contient un mot français non accentué de la liste noire.

    L'heure « a 10 heures » (préposition « à ») est aussi vérifiée car récurrente dans
    les PV ; un « a » verbe avoir (« il a pris ») reste légitime et n'est pas matché.
    """
    residus = sorted(
        {m for m in MOTS_NON_ACCENTUES_INTERDITS if re.search(rf"\b{re.escape(m)}\b", text)}
    )
    if re.search(r"\ba \d+\s*heure", text):
        residus.append("a {heure}")
    assert not residus, f"Mots français non accentués dans la sortie générée : {sorted(residus)}"
