# Retours Rafael 2026-07-09 (soir) — focus SPFPL cession + statuts/PV/actes

Verbatim = spec. Base HEAD `f327d1c` (batches 1-3 + Akainu poussés).

## ✅ Validés (juste vigilance)
- **DNC / Autorisation domiciliation / Procuration** : « Niquel », juste attention **ponctuation** (majuscule début de phrase, point final). → vérif R12 + point final.

## PV (nomination gérant)
| # | Retour | Fichier |
|---|---|---|
| P1 | Ne pas mettre d'espaces pour la **dénomination du client** ni pour les **décisions** | pv_nomination_gerant |
| P2 | En-tête SPFPLAS : « Société de Participations Financières de Profession Libérale **de Chirurgiens-Dentistes par actions simplifiée** » au lieu de « société de participations financières de professions libérales » (profession + forme + casse) | pv_nomination_gerant |

## DEMANDE INSCRIPTION CDO
| # | Retour | Fichier |
|---|---|---|
| D1 | En-tête (haut à gauche) : mettre l'**adresse du SIÈGE**, pas l'adresse perso du client | demande_inscription_ordre |

## STATUTS
| # | Retour | Fichier |
|---|---|---|
| S1 | En-tête : **retirer « Statuts »** du titre (juste la dénomination) ; **pas d'espace entre les lignes** (comme le modèle) | statuts (lot_04) |
| S2 | Mettre **« STATUTS » dans un encadré/tableau** (lisibilité), un peu plus bas que l'en-tête, puis **saut de page** pour commencer l'acte | statuts |
| S3 | **Pas d'espace pour le soussigné** | statuts |
| S4 | **Article 26 : titre pas en gras** comme le reste → mettre en gras | statuts |
| S5 | Dernière page : « Fait à et Le » à **gauche**, signature client à **droite** + **saut de page** avant l'annexe | statuts |

## NOTE D'INFORMATION
| # | Retour | Fichier |
|---|---|---|
| N1 | Actions ou parts : peut-être une **case à cocher en plus** (distinguer actions/parts) | front + note |
| N2 | Signature : **aligner le trait noir sous le nom** du client | note_information |

## CESSION — PV (agrément)
| # | Retour | Fichier |
|---|---|---|
| C1 | Uniformiser l'**en-tête** avec le titre de la société **en gras** | pv_agrement |
| C2 | La **date en lettres apparaît 2 fois** → dédupliquer | pv_agrement |
| C3 | Décisions : **ajouter des tirets** | pv_agrement |
| C4 | 2e résolution : **case front pour le n° d'article du capital social de la SEL** (« 7 bis » ressort à chaque fois, à rendre saisissable) | front + pv_agrement |

## ACTE DE CESSION
| # | Retour | Fichier |
|---|---|---|
| A1 | **Saut de page** entre la 1ʳᵉ page de présentation et le début de l'acte | acte_cession_parts_spfpl |
| A2 | Début de la désignation du client **en gras ?** → juste **nom + prénom** suffisent (simplifier/pas gras) | acte_cession |
| A3 | (rédaction exposé↔origine de propriété a changé mais **OK** = pas d'action) | — |
| A4 | Chiffres écrits en lettres → **en MAJUSCULE partout** | acte + convention transverse |
| A5 | « DÉCLARATION DES PARTIES » : **tirets** à chaque énonciation | acte_cession |

## ATTESTATION CAPITAL
| # | Retour | Fichier |
|---|---|---|
| AT1 | Signature : la **profession du client indiquée 2 fois** à côté du nom → en retirer une | attestation_capital_*_cession |

## ⚠️ DOCUMENTS MANQUANTS (SPFPL cession)
| # | Retour | Statut |
|---|---|---|
| M1 | Il **manque la procuration pour la SEL** | à investiguer (existe ? wiring bundle ?) |
| M2 | Il **manque l'attestation de dépôt de cession de parts** | à investiguer (existe ? à bâtir ?) |

## ⚠️ Flag N1 — support « cible en ACTIONS » = feature à cadrer (pas deviné)
La case front actions/parts est posée (défaut `parts sociales` = flux SELARL validé, zéro régression). MAIS choisir « actions » ne produit PAS encore un bundle cohérent : le front hardcode DOC-040 (acte PARTS) ; DOC-029 (acte ACTIONS) existe mais n'est pas câblé au bundle front ; `note_information`/`pv_agrement`/`capital_after_lines` écrivent « parts sociales » en dur ; données `CessionActions` non collectées. → **Le support cible-actions complet est une feature à cadrer avec Albane/PM**, pas un simple branchement. Aujourd'hui : case présente, vocabulaire piloté quand le générateur échoit `operation_spfpl.nature_titres`, mais « actions » reste incomplet côté bundle.

## Défauts logiques tranchés seul
- A4 « chiffres en lettres en MAJUSCULE » : convention transverse → règle de conformité (R16) après confirmation du périmètre exact (partout dans les actes ? ou tout doc ?).
- N1/C4 : nouvelles cases front → dérivées si possible, saisie sinon.
