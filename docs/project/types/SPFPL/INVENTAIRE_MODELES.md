# SPFPL — Inventaire des modèles tokenisés

> Source Drive : `Documents avec variables/Création SPFPL/` (lecture seule).
> Copie dédupliquée (par contenu, md5) dans : `project/source_documents/spfpl/`.
> 44 `.docx` bruts dans le dossier Drive → **33 modèles distincts par contenu** copiés.
> Tokens = variables au format `[token]` réellement présentes dans le DOCX (extraction `python-docx`).
> Date d'extraction : 2026-06-05. **Non confirmé juridiquement** — ce qui suit décrit ce que le fichier
> *paraît* être, pas une vérité ratifiée.

## Avertissement de scope
- 3 fichiers **legacy `.doc`** présents dans le dossier Drive ne sont **PAS** lisibles par `python-docx`
  donc **NON inventoriés ni copiés** ici (voir `STATUT.md` → "Modèles non récupérés") :
  `Acte_cession_parts_Dr_SPFPL_modele.doc`, `Acte_cession_SPFPL_tiers_modele.doc`,
  `PV SPFPL autorisation empruntt - transforme.doc`. Ce sont de **vrais modèles SPFPL** (acte de cession
  de parts / d'actions, PV autorisation d'emprunt) → à convertir en `.docx` ou à re-fournir tokenisés.
- Aucun **PV de nomination du gérant** spécifique SPFPL n'a été trouvé tokenisé dans le dossier Drive,
  alors que le canon V1 le réclame (`PV nomination gérant.docx`) → voir `CARTOGRAPHIE_TENTATIVE.md`.

## Modèles distincts (33)

| Modèle (`project/source_documents/spfpl/`) | # tokens | Ce que le document paraît être (1 phrase) |
|---|---|---|
| `STATUTS SAS SPFPL médecins - transforme.docx` | 26 | Statuts d'une SPFPL sous forme SAS, profession **médecins**. |
| `Statuts SAS SPFPL pharmaciens - transforme.docx` | 24 | Statuts d'une SPFPL sous forme SAS, profession **pharmaciens**. |
| `Statuts_SPFPLAS_dentistes_apport_modele.docx` | 37 | Statuts SPFPL-AS **dentistes**, variante **apport** (mentionne société apportée). |
| `Statuts SPFPLAS dentistes - apport.docx` | 31 | Statuts SPFPL-AS **dentistes** apport (variante de contenu : mentionne société cédée + exercice). |
| `Statuts_SPFPLAS_dentistes_cession.docx` | 33 | Statuts SPFPL-AS **dentistes**, variante **cession** (mentionne banque / montant d'apport). |
| `Acte_cession_SPFPL_tiers_part_modele.docx` | 53 | Acte de **cession de parts** SPFPL à un tiers (cédant / cessionnaire / prix). |
| `Compromis de cession d_un cabinet médical - transforme.docx` | 66 | Compromis de cession d'un **cabinet médical** (fonds libéral, bail, prix). |
| `Compromis de cession d_un cabinet dentaire - transforme.docx` | 59 | Compromis de cession d'un **cabinet dentaire** (avec activité bail / local décrit). |
| `Compromis de cession d_un cabinet dentaire - transforme (2).docx` | 53 | Compromis cabinet **dentaire** — variante de contenu (jeu de tokens réduit). |
| `appel des fonds spfpl - transforme.docx` | 15 | Lettre d'**appel de fonds** SPFPL adressée à la banque (cédant / parts cédées). |
| `Contrat d_apport SEL SPFPL.docx` | 48 | **Contrat d'apport** d'une SEL à la SPFPL (apport de titres). |
| `Contrat d_apport SEL SPFPL - transforme.docx` | 72 | Contrat d'apport SEL→SPFPL — variante enrichie (commissaires aux apports, évaluateur). |
| `attestation nomination commissaire aux apports - transforme.docx` | 30 | Attestation de **nomination du commissaire aux apports** (apport). |
| `attestation nomination commissaire aux apports - transforme (2).docx` | 46 | Idem — variante avec 2 commissaires nommés. |
| `Attestation sur le capital - apport - liste des souscripteurs.docx` | 20 | Attestation sur le capital + liste des souscripteurs, branche **apport**. |
| `Attestation sur le capital - apport - liste des souscripteurs - transforme.docx` | 19 | Idem apport — variante (sans `forme_sociale`). |
| `Attestation sur le capital - apport - liste des souscripteurs (2).docx` | 19 | Idem apport — 2e variante de contenu. |
| `Attestation sur le capital - cession - liste des souscripteurs.docx` | 13 | Attestation sur le capital + souscripteurs, branche **cession**. |
| `Attestation sur le capital - cession - liste des souscripteurs - transforme.docx` | 13 | Idem cession — variante de contenu. |
| `Liste des souscripteurs - transforme.docx` | 14 | **Liste des souscripteurs** au capital (création / souscription). |
| `Note d_information.docx` | 17 | **Note d'information** sur l'opération (société cédée, parts). |
| `Note d_information (2).docx` | 17 | Note d'information — variante de contenu. |
| `NOTE D_INFORMATION (3).docx` | 17 | Note d'information — 3e variante de contenu. |
| `Autorisation de domiciliation.docx` | 11 | **Autorisation de domiciliation** du siège (variante détaillée : num voie / ville). |
| `Autorisation de domiciliation - transforme.docx` | 8 | Autorisation de domiciliation — variante courte. |
| `Déclaration sur l_honneur de non condamnation - transforme.docx` | 11 | **Déclaration sur l'honneur de non-condamnation** (parents, nationalité). |
| `Demande d_inscription à l_ordre - transforme.docx` | 9 | **Demande d'inscription à l'ordre** professionnel. |
| `Procuration.docx` | 15 | **Procuration** donnée à un mandataire (personne_2). |
| `Lettre de renonciation a revendiquer la qualite d_associe.docx` | 15 | **Lettre de renonciation** du conjoint à la qualité d'associé (régime communautaire). |
| `Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx` | 21 | **Lettre d'avertissement au conjoint** (apport d'un bien commun, régime communautaire). |
| `PV SELARL agrément cession SPFPL - SELARL 1 associé.docx` | 31 | **PV d'agrément** de la cession côté SELARL, **associé unique**. |
| `PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx` | 33 | PV d'agrément côté SELARL, **plusieurs associés**. |
| `RM Sydel SPFPL - transforme.docx` | 15 | **Rapport de mission / fiche patrimoniale** Sydel (revenus, IFI, objectifs client) — paraît hors chaîne d'actes. |

## Notes sur les quasi-doublons (contenu distinct, à arbitrer)
Plusieurs documents existent en **plusieurs variantes de contenu** (md5 différents → conservés tous,
suffixés `(2)` / `(3)` / `- transforme`). Ils ne diffèrent souvent que de **quelques tokens**. Lesquels
sont **canoniques** doit être confirmé (NotebookLM / Rafael) :
- `Note d'information` × 3 variantes (jeux de tokens identiques mais contenus binaires distincts).
- `Attestation sur le capital - apport` × 3 variantes.
- `Attestation sur le capital - cession` × 2 variantes.
- `Contrat d'apport SEL SPFPL` : version simple (48 tokens) vs enrichie commissaires (72 tokens).
- `attestation nomination commissaire aux apports` : 1 vs 2 commissaires.
- `Autorisation de domiciliation` : version courte (8) vs détaillée (11).
- `Compromis de cession cabinet dentaire` × 2 variantes.
