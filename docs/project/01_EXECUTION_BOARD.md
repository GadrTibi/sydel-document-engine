# Tableau d'ex?cution

## Statuts
- READY
- IN_PROGRESS
- BLOCKED
- DONE

## Tickets actifs

| ID | Statut | Objet | Entr?es obligatoires | Sorties obligatoires |
|---|---|---|---|---|
| TRACK-B-SELARL-UX-FOLLOWUP-001 | DONE | Corriger les retours UI SELARL apres test local | retour utilisateur du 2026-05-27 + clean front SELARL V1 | dates JJ/MM/AAAA sans borne Streamlit + situation matrimoniale en liste + valeur nominale calculee + labels ordre clarifies + ruff/test/HTTP 200 |
| TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 | DONE | Corriger l'UX SELARL V1 apres reconciliation associe / NotebookLM | retours associe + NotebookLM + audit dedup + branche track-b/clean-rebuild | front_app SELARL sans doubles saisies implicites + derivations + tests cibles + lancement local |
| TRACK-B-FRONT-ARCHITECTURE-RESET-001 | DONE | Refonder le chemin front Track B propre et isoler le legacy | arbitrage produit front + fondations front_data + branche track-b/clean-rebuild | nouveau front_app clean + rapport + tests + lancement local |
| TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 | DONE | Figer le contrat metier-front SELARL V1 depuis les sources de verite | sources SELARL V2/V3 + reponse metier + NotebookLM + specs/revues + branche track-b/clean-rebuild | `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md` + conclusion GO bornee |
| TRACK-B-SELARL-VERTICAL-SLICE-IMPLEMENT-001 | DONE | Brancher la vraie vertical slice SELARL V1 dans le front_app clean | contrat `TRACK_B_SELARL_FRONT_CONTRACT_V1.md` + moteur documentaire existant + branche track-b/clean-rebuild | slice SELARL V1 bornee dans `front_app` + generation DOCX/ZIP + tests cibles |
| TRACK-B-SELARL-FIELD-DEDUP-AUDIT-001 | DONE | Auditer les doublons de champs utilisateur dans le clean front SELARL V1 | front_app SELARL V1 + contrat metier-front + branche track-b/clean-rebuild | rapport `docs/review/track_b_selarl_field_dedup_audit_001_report_v1.md` + conclusion PASS |
| PM-001 | DONE | Installer la m?moire projet dans le repo | source de v?rit? + specs Lot 1 | docs/project/* |
| PM-002 | DONE | V?rifier et compl?ter la m?moire projet op?rationnelle | AGENTS.md + docs/project/* | docs/project compl?t?s + artefact parasite trait? |
| PM-003 | DONE | Installer le kit de reprise nouveau ChatGPT / Codex | m?moire projet existante | handoff + last state + prompt nouveau chat |
| DOC-001 | DONE | Impl?menter la d?claration de non-condamnation | source doc + spec Lot 1 | g?n?rateur + tests + MAJ doc |
| DOC-003 | DONE | Impl?menter la procuration | source doc + spec Lot 1 | g?n?rateur + tests + MAJ doc |
| DOC-002 | DONE | Impl?menter l'autorisation de domiciliation | source doc + spec Lot 1 + d?cision V1 adresse libre | g?n?rateur + tests + MAJ doc |
| ORCH-001 | DONE | Brancher l'orchestrateur Lot 1 | g?n?rateurs DOC-001/002/003 | service orchestrateur + tests |
| PM-004 | DONE | Int?grer l'arbre moteur document-centr? V1 dans la m?moire projet | arbre moteur document-centr? V1 | board + dernier ?tat mis ? jour |
| PM-005 | DONE | Int?grer le dictionnaire canonique des variables V1 dans la m?moire projet | dictionnaire canonique des variables V1 | board + dernier ?tat mis ? jour |
| SMOKE-001 | DONE | Smoke test r?el Lot 1 via orchestrateur | contexte exemple Lot 1 + orchestrateur | 3 DOCX g?n?r?s + docs projet mises ? jour |
| VAR-001 | DONE | Ajouter une table de mapping document -> variables canoniques | arbre documentaire V1 + dictionnaire canonique V1 + specs | table de mapping document -> variables canoniques |
| PM-006 | DONE | Int?grer le cadrage m?tier PV nomination g?rant V1 dans la m?moire projet | cadrage Lot 2 PV nomination g?rant | board + dernier ?tat mis ? jour |
| SPEC-PV-001 | DONE | Formaliser la spec canonique du PV nomination g?rant ? partir du cadrage V1 | cadrage Lot 2 + arbre documentaire V1 + dictionnaire canonique V1 + table de mapping V1 | spec canonique ?crite, blocs conditionnels, mapping variables, r?gles `associes[]`, points ouverts |
| SPEC-TEXTE-PV-001 | DONE | Stabiliser le texte canonique et les variantes du PV nomination g?rant | spec canonique PV nomination g?rant V1 + source Lot 2 | spec textuelle d?taill?e, variantes structurelles, wording ? valider, crit?res avant code |
| CODE-PV-001 | DONE | Impl?menter le g?n?rateur canonique PV nomination g?rant | spec canonique V1 + spec texte V1 + source Lot 2 | g?n?rateur PV from-scratch + tests associes[]/genre/emprunt + MAJ doc |
| REVIEW-PV-001 | DONE | Pr?parer la revue humaine du PV nomination g?rant g?n?r? | contexte exemple Lot 2 + g?n?rateur PV existant | DOCX r?g?n?r? + aper?u texte + checklist de revue humaine |
| SPEC-RENDER-001 | DONE | Sp?cifier une couche de rendu DOCX commune | g?n?rateurs DOC-001/002/003 + PV nomination g?rant + specs existantes | spec technique render style system V1 |
| RENDER-STYLE-001 | DONE | Impl?menter la couche de rendu DOCX commune | spec render style system V1 + g?n?rateurs existants | helpers communs + g?n?rateurs migr?s + tests + smoke DOCX |
| ORCH-L2-PV-001 | DONE | Brancher le PV nomination g?rant dans l'orchestrateur | g?n?rateur PV + specs Lot 2 + d?cisions de s?lection | catalogue + registre orchestrateur + tests cibl?s |
| SMOKE-ORCH-L2-001 | DONE | Smoke test r?el orchestrateur Lot 2 positif SCI / n?gatif SAS | contextes exemples Lot 2 + orchestrateur | DOCX g?n?r?s, PV pr?sent en SCI et absent en SAS, revue smoke |
| FIX-PV-RENDER-001 | DONE | Restaurer la structure visuelle essentielle du PV nomination g?rant | source Lot 2 + specs PV + render style system V1 | listes ? tirets, titre, intertitres, italique votes, smoke DOCX |
| ANALYSE-ORDRE-001 | DONE | Cadrer Demande d'inscription ? l'ordre et batch r?gime communautaire Lot 2 | sources Lot 2 ordre + r?gime communautaire + r?f?rentiels V1 | cadrages delivery + tickets SPEC-ORDRE-001/SPEC-RC-001 READY |
| ARBITRAGE-SOURCES-001 | DONE | R?parer le manifest d'import sources et arbitrer les placements V1 | source truth + raw_drive_dump + source_documents + d?cisions m?tier | docs projet 10/11/12/13 + prochain ticket placement |
| PLACEMENT-HIGH-001 | DONE | D?placer physiquement dans source_documents uniquement les cas HIGH valid?s | plan de placement V1 + d?cisions d'arbitrage sources V1 | placement HIGH confirm? no-op + journal d'ex?cution |
| SPEC-ORDRE-001 | DONE | Formaliser la spec canonique Demande d'inscription ? l'ordre | cadrage ordre V1 + source Lot 2 + r?f?rentiels V1 + variantes raw dump | spec canonique ?crite, variantes compar?es, mapping variables, accords, points ouverts |
| SPEC-TEXTE-ORDRE-001 | DONE | Stabiliser le texte canonique et les variantes de Demande d'inscription ? l'ordre | spec canonique ordre V1 + variantes SELARL/SELAS/SPFPL/SPFPL apport/SCM | spec texte d?taill?e, tronc commun, overlays, blocs conditionnels/manuels, r?gles de blocage avant code |
| CODE-ORDRE-001 | DONE | Impl?menter le g?n?rateur canonique Demande d'inscription ? l'ordre | spec canonique ordre V1 + spec texte ordre V1 + source Lot 2 + variantes raw dump | g?n?rateur ordre from-scratch + tests overlays/d?rogation/mandataire + MAJ doc |
| SPEC-RC-001 | DONE | Formaliser la spec canonique batch r?gime communautaire | cadrage r?gime communautaire V1 + deux sources Lot 2 + r?f?rentiels V1 | spec canonique batch, spec texte batch, mapping commun, r?gles de g?n?ration, points ouverts |
| CODE-RC-001 | DONE | Impl?menter le batch r?gime communautaire v1 | specs canonique et texte r?gime communautaire V1 + sources Lot 2 + variantes raw dump | deux g?n?rateurs DOCX from-scratch + s?lection orchestrateur + tests cibl?s + MAJ doc |
| SPEC-SPFPL-001 | DONE | Formaliser le batch SPFPL sp?cifique | source v?rit? + raw dump SPFPL | spec canonique SPFPL V1 |
| SPEC-DEROG-001 | DONE | Formaliser la famille d?rogations | source v?rit? + raw dump d?rogations | spec canonique d?rogations V1 |
| SPEC-CESSION-BAIL-001 | DONE | Formaliser les blocs cession cabinets et bail/appel de fonds | source v?rit? + raw dump cession | specs canoniques cession cabinets + bail/appel de fonds V1 |
| SYNC-SPECS-001 | DONE | Synchroniser les specs parall?les dans main | branches SPEC-RC/SPFPL/DEROG/CESSION | specs int?gr?es + pilotage align? |
| SPEC-TEXTE-BAIL-APP-001 | DONE | Stabiliser le texte canonique bail / appel de fonds | spec canonique bail/appel de fonds V1 + sources raw dump | spec texte V1 bail / appel de fonds |
| SPEC-TEXTE-CESSION-CAB-001 | DONE | Stabiliser le texte canonique cession cabinets | spec canonique cession cabinets V1 + sources raw dump | spec texte V1 cession cabinets |
| SPEC-TEXTE-DEROG-001 | DONE | Stabiliser le texte canonique d?rogations | spec canonique d?rogations V1 + sources raw dump | spec texte V1 d?rogations |
| SPEC-TEXTE-SPFPL-001 | DONE | Stabiliser le texte canonique SPFPL sp?cifique | spec canonique SPFPL V1 + sources raw dump | spec texte V1 SPFPL |
| SYNC-TEXTE-SPECS-001 | DONE | Synchroniser les specs texte parall?les dans main | branches SPEC-TEXTE bail/appel, cession, d?rogations, SPFPL | specs texte int?gr?es + pilotage align? |
| SYNC-ARBITRAGES-001 | DONE | Synchroniser les arbitrages parall?les dans main | branches ARBITRAGE cession, d?rogations, SPFPL | arbitrages int?gr?s + pilotage align? |
| CODE-BAIL-APP-001 | DONE | Impl?menter le mini-batch bail / appel de fonds | specs canonique et texte bail/appel V1 + arbitrages de blocage V1 | g?n?rateurs DOCX + tests cibl?s + MAJ doc |
| ARBITRAGE-CESSION-001 | DONE | Arbitrer les points bloquants cession cabinets avant code | spec texte cession cabinets V1 + points ouverts | d?cisions m?tier trac?es pour acte/compromis, medical/dentaire et anomalies source |
| ARBITRAGE-DEROG-001 | DONE | Arbitrer les points bloquants d?rogations avant code | spec texte d?rogations V1 + sources Lot 03 | d?cisions m?tier sur formulaires pr?remplis, r?les et sources legacy |
| ARBITRAGE-SPFPL-001 | DONE | Arbitrer les points bloquants SPFPL avant code | spec texte SPFPL V1 + points ouverts | d?cisions m?tier cession/apport, commissaire, souscripteurs et sources |
| CODE-CESSION-CAB-001 | DONE | Impl?menter la famille cession cabinets | specs canonique/texte cession cabinets V1 + arbitrage V1 | g?n?rateurs DOCX + blocages explicites + tests cibl?s + MAJ doc |
| RESUME-CODE-CESSION-CAB-001 | DONE | Reprendre proprement CODE-CESSION-CAB-001 sur main synchronis? | main ? jour Lot 03/Lot 05 + specs/arbitrages cession V1 | reprise cadr?e de la famille cession cabinets |
| PREP-DEROG-001 | DONE | Pr?parer les sources d?rogations avant code | arbitrages d?rogations V1 + raw dump + plan de placement | sources Lot 03 plac?es + rapport de pr?paration |
| CODE-DEROG-CORE-001 | DONE | Impl?menter le c?ur d?rogations | specs/arbitrages d?rogations V1 + PREP-DEROG-001 | g?n?rateurs DOCX d?rogations c?ur + blocages explicites + tests |
| CODE-SPFPL-AGR-INFO-001 | DONE | Impl?menter le sous-batch SPFPL agr?ment / note d'information | specs canonique/texte SPFPL V1 + arbitrage V1 | g?n?rateurs DOCX cibl?s + tests + sources Lot 05 plac?es |
| CODE-SPFPL-CORE-001 | DONE | Impl?menter le c?ur SPFPL restant | specs canonique/texte SPFPL V1 + arbitrage V1 + sources pr?par?es | g?n?rateurs SPFPL cibl?s + blocages explicites + tests |
| PREP-STATUTS-001 | DONE | Pr?parer les sources statuts avant sp?cification/code | source v?rit? + raw dump + plan de placement/arbitrage sources | sources statuts cadr?es + ?carts document?s |
| SPEC-STATUTS-SEL-001 | DONE | Sp?cifier les statuts SEL d'exercice | pr?paration statuts V1 + sources Lot 04 SELARL/SELAS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SPFPL-001 | DONE | Sp?cifier les statuts SPFPL | pr?paration statuts V1 + sources Lot 04 SPFPL cession/apport | spec canonique + spec texte avant code |
| SPEC-STATUTS-CIVILS-001 | DONE | Sp?cifier les statuts civils | pr?paration statuts V1 + sources Lot 04 SCI/SCI IRIS/SCM/SCS | spec canonique + spec texte avant code |
| SPEC-STATUTS-SAS-001 | DONE | Sp?cifier les statuts SAS | pr?paration statuts V1 + source Lot 04 SAS | spec canonique + spec texte avant code |
| SYNC-STATUTS-SPECS-001 | DONE | Synchroniser les specs statuts parall?les dans main | branches statuts SAS/SPFPL/SEL/CIVILS | specs int?gr?es + pilotage align? |
| CODE-STATUTS-SAS-001 | DONE | Impl?menter les statuts SAS | specs statuts SAS V1 + blocages explicites | g?n?rateur DOCX + tests cibl?s + MAJ doc |
| CODE-STATUTS-SPFPL-001 | DONE | Impl?menter les statuts SPFPL cession/apport | specs statuts SPFPL V1 + blocages explicites | g?n?rateurs DOCX + tests cibl?s + MAJ doc |
| ARBITRAGE-STATUTS-SEL-001 | DONE | Arbitrer les points bloquants statuts SEL avant code | specs statuts SEL V1 + points ouverts | d?cisions pluralit? associ?s, SELAS et wording |
| ARBITRAGE-STATUTS-CIVILS-001 | DONE | Arbitrer les points bloquants statuts civils avant code | specs statuts civils V1 + points ouverts | d?cisions SCI/SCI IRIS/SCM/SCS avant code |
| SYNC-STATUTS-CODE-ARB-001 | DONE | Synchroniser code statuts SAS/SPFPL et arbitrage SEL dans main | branches code/arbitrage statuts | commits int?gr?s + pilotage r?align? |
| CODE-STATUTS-SEL-001 | DONE | Impl?menter les statuts SEL d'exercice | specs statuts SEL V1 + arbitrages SEL V1 | g?n?rateur(s) DOCX + tests cibl?s + MAJ doc |
| CODE-STATUTS-CIVILS-CORE-001 | DONE | Impl?menter le c?ur des statuts civils | specs statuts civils V1 + arbitrages civils V1 | g?n?rateurs SCS/SCI/SCI IRIS + tests cibl?s + MAJ doc |
| FIX-STYLE-LETTERS-001 | DONE | Corriger les ?carts de style prioritaires des lettres | blueprint style batch V1 + g?n?rateurs existants | rendu lettres harmonis? + tests/smoke cibl?s |
| RESUME-FIX-STYLE-LETTERS-001 | DONE | Reprendre proprement les corrections de style lettres | blueprint style batch V1 + ?tat main synchronis? | reprise cadr?e de FIX-STYLE-LETTERS-001 absorb?e |
| ARBITRAGE-STATUTS-SCM-001 | DONE | Arbitrer les points bloquants statuts SCM avant code | specs statuts civils V1 + anomalies SCM document?es | d?cisions SCM avant spec/code |
| PREP-SCM-SAT-001 | DONE | Pr?parer le p?rim?tre SCM et satellites | arbitrage SCM + sources disponibles | cadrage sources et p?rim?tre exploitable |
| SPEC-SAS-SATELLITES-001 | DONE | Sp?cifier les satellites SAS | specs statuts SAS V1 + sources satellites | spec canonique + spec texte avant code |
| CODE-OPTION-IS-001 | DONE | Impl?menter la lettre option IS | specs/arbitrages applicables + source re?ue | g?n?rateur DOCX + tests cibl?s |
| PREP-ACTE-ACTIONS-001 | DONE | Pr?parer les sources acte de cession d'actions | arbitrages SPFPL + sources disponibles | source confirm?e ou blocage document? |
| RESUME-ARBITRAGE-STATUTS-CIVILS-001 | DONE | Reprendre proprement l'arbitrage des statuts civils | specs statuts civils V1 + ?tat main synchronis? | remplac? par l'arbitrage civils V1 absorb? |
| STYLE-ANALYSE-BATCH-001 | DONE | Analyser le style documentaire en batch avant harmonisation | g?n?rateurs/statuts disponibles + besoins de rendu | cadrage style batch + points d'arbitrage |
| SYNC-STYLE-CIVILS-001 | DONE | Synchroniser style batch et arbitrage civils dans main | branches style/arbitrage civils | commits int?gr?s + pilotage r?align? |
| SYNC-STATUTS-SEL-CIVILS-001 | DONE | Synchroniser code statuts SEL et arbitrage civils dans main | branches code SEL/arbitrage civils | commits int?gr?s + pilotage r?align? |
| SYNC-WAVE-005 | DONE | Synchroniser SCM, satellites SAS, option IS et pr?paration legacy dans main | branches CODE-OPTION-IS/PREP-SCM-SAT/ARBITRAGE-STATUTS-SCM/SPEC-SAS-SATELLITES/PREP-ACTE-ACTIONS | commits int?gr?s + pilotage r?align? |
| SYNC-WAVE-006 | DONE | Synchroniser la vague tardive Lot 04 / Lot 05 dans main | branches style/civils/SAS satellites/conversions/spec SCM | commits int?gr?s + pilotage r?align? |
| SYNC-WAVE-007 | DONE | Synchroniser la vague SCM et acte actions dans main | branches statuts SCM / liste d?penses / satellites SCM / spec acte actions | commits int?gr?s + pilotage r?align? |
| SYNC-WAVE-008 | DONE | Synchroniser la vague SCM style review et acte actions dans main | branches acte actions / sources SCM cession / reviews / audits / style / spec SCM cession | commits int?gr?s + pilotage r?align? |
| CODE-STATUTS-SCM-001 | DONE | Impl?menter les statuts SCM | specs statuts civils V1 + arbitrages SCM V1 | g?n?rateur DOCX + tests cibl?s |
| CODE-SAS-SATELLITES-001 | DONE | Impl?menter les satellites SAS | specs satellites SAS V1 + sources confirm?es | g?n?rateurs DOCX + tests cibl?s |
| SPEC-SCM-SATELLITES-001 | DONE | Sp?cifier les satellites SCM | pr?paration SCM satellites V1 + sources confirm?es | spec canonique + spec texte avant code |
| CONVERT-ACTE-ACTIONS-001 | DONE | Convertir ou remplacer la source acte de cession d'actions | audit source acte actions V1 | DOCX exploitable plac? + pr?paration document?e |
| CONVERT-DEROG-SALARIEE-001 | DONE | Convertir ou remplacer la source d?rogation salari?e legacy | pr?paration d?rogations V1 + source legacy `.doc` | blocage conversion document? |
| PREP-SCM-LISTE-DEPENSES-CONVERT-001 | DONE | Convertir la source legacy liste d?penses communes SCM | source legacy Lot 05 SCM | DOCX exploitable + pr?paration document?e |
| CODE-SCM-SAT-DOCX-001 | DONE | Impl?menter les satellites SCM DOCX hors liste d?penses | specs satellites SCM V1 + sources DOCX confirm?es | g?n?rateurs DOCX + tests cibl?s |
| SPEC-ACTE-ACTIONS-001 | DONE | Sp?cifier l'acte de cession d'actions SPFPL avant code | source DOCX convertie + pr?paration V1 | spec canonique + spec texte avant code |
| CODE-ACTE-ACTIONS-001 | DONE | Impl?menter l'acte de cession d'actions SPFPL | specs acte actions V1 + source DOCX convertie | g?n?rateur DOCX + tests cibl?s |
| PREP-SCM-CESSION-SOURCES-001 | DONE | Pr?parer les sources cession SCM | raw dump SCM cession + plan de placement | sources plac?es + pr?paration document?e |
| REVIEW-BATCH-LOT03-001 | DONE | Revoir le batch Lot 03 g?n?r? | g?n?rateurs Lot 03 + smoke DOCX disponibles | revue humaine juridique/visuelle document?e |
| REVIEW-BATCH-LOT04-001 | DONE | Revoir le batch Lot 04 g?n?r? | g?n?rateurs statuts + smoke DOCX disponibles | revue humaine juridique/visuelle document?e |
| AUDIT-REMAINING-SCOPE-001 | DONE | Auditer le p?rim?tre restant | board + specs + registre moteur | audit restant document? |
| STYLE-ANALYSE-LOT03-BATCH-001 | DONE | Analyser le style du batch Lot 03 avant harmonisation | g?n?rateurs Lot 03 int?gr?s + besoins de rendu | blueprint style Lot 03 |
| STYLE-ANALYSE-STATUTS-BATCH-001 | DONE | Analyser le style du batch statuts avant harmonisation | g?n?rateurs statuts int?gr?s + besoins de rendu | blueprint style statuts |
| SPEC-SCM-CESSION-BLOCK-001 | DONE | Sp?cifier le blocage cession SCM avant code | sources SCM cession disponibles + arbitrages SCM | spec canonique + spec texte de blocage |
| CODE-SCM-CESSION-BLOCK-001 | DONE | Impl?menter le blocage cession SCM | specs SCM cession block V1 | blocage explicite historique + tests cibl?s |
| CODE-SCM-LISTE-DEPENSES-001 | DONE | Impl?menter la liste des d?penses communes SCM | source DOCX convertie + specs satellites SCM V1 | g?n?rateur DOCX + tests cibl?s |
| SPEC-DEROG-SALARIEE-MANUAL-001 | DONE | Sp?cifier le traitement manuel de la d?rogation salari?e legacy | blocage conversion d?rogation salari?e V1 | spec manuelle ou d?cision de blocage document?e |
| FIX-STYLE-LOT03-BATCH-001 | DONE | Corriger les ?carts de style prioritaires du batch Lot 03 | blueprint style Lot 03 | rendu Lot 03 harmonis? + tests cibl?s |
| FIX-STYLE-STATUTS-BATCH-001 | DONE | Corriger les ?carts de style prioritaires du batch statuts | blueprint style statuts | rendu statuts harmonis? + tests cibl?s |
| REVIEW-BATCH-LOT05-001 | DONE | Revoir le batch Lot 05 g?n?r? | g?n?rateurs Lot 05 + smoke DOCX disponibles | revue humaine juridique/visuelle document?e |
| ARBITRAGE-SCM-CESSION-RESOLVE-001 | DONE | Arbitrer la r?solution de la cession SCM | specs de blocage cession SCM + sources pr?par?es + vague style/revue absorb?e | d?cision de r?solution avant code |
| SYNC-WAVE-010 | DONE | Synchroniser la vague finale moteur SCM cession dans main | branches arbitrage/code SCM cession | commits int?gr?s + pilotage final moteur align? |
| FINAL-SCM-CESSION-WAVE-001 | DONE | Finaliser le bloc cession SCM et cl?turer la vague moteur V1 | r?solution SCM cession V1 + specs + six sources | DOC-031 ? DOC-033 + tests + smoke + audit moteur |
| SYNC-CLOSE-AUDIT-001 | DONE | Synchroniser l'audit de cl?ture moteur V1 dans main | `origin/codex/close-motor-audit-001` @ `0139202b170531fd628f25811c55855a2512acc0` | merge de synchronisation + audit pr?sent + pilotage align? |
| RECONCILE-MOTOR-CLOSE-001 | DONE | R?concilier et cl?turer le moteur DOCX V1 | audits 16/17 + fondation 18 + catalogue/orchestrateur | DOC-001 ? DOC-043 align?s + audits conclusifs + tests |
| PDF-BACKEND-001 | DONE | Impl?menter le backend d'export PDF V1 | moteur DOCX clos + fondation phase 18 | backend PDF best-effort + tests + smoke DOCX vers PDF |
| UI-FLOW-001 | DONE | Cadrer le flux UI Streamlit V1 | moteur DOCX clos + fondation phase 18 | r?f?rentiel de flux UI V1 |
| UI-OCCURRENCES-001 | DONE | Cadrer les occurrences documentaires affichables en UI | registre moteur DOC-001 ? DOC-043 | r?f?rentiel occurrences UI V1 |
| UI-FORM-SCHEMA-001 | DONE | Cadrer le sch?ma formulaire UI V1 | flux UI + occurrences UI | sch?ma formulaire UI V1 |
| RECIPE-FRAME-001 | DONE | Cadrer la recette finale V1 | moteur DOCX clos + fondations UI/PDF/ZIP | framework de recette finale V1 |
| SYNC-POST-MOTOR-UI-001 | DONE | Synchroniser la fondation UI/PDF/recette dans main | branches UI/PDF/recette list?es | commits int?gr?s + pilotage align? |
| UI-CORE-001 | DONE | Impl?menter le c?ur UI Streamlit V1 | UI flow + occurrences + form schema + backend PDF | superseded / remplac? par `UI-PDF-ZIP-INTEGRATION-001` |
| RESUME-ZIP-BACKEND-001 | DONE | Reprendre le backend ZIP V1 sur main synchronis? | moteur DOCX clos + backend PDF + fondation phase 18 | backend ZIP dossier document? et test? |
| REVIEW-FINAL-001 | DONE | Ex?cuter la revue finale V1 | moteur DOCX + UI/PDF/ZIP int?gr?s | rapport d'execution + decision GO avec reserves |
| UI-PDF-ZIP-INTEGRATION-001 | DONE | Brancher PDF et ZIP dans l'UI Streamlit | UI core + backend PDF + backend ZIP | t?l?chargements DOCX/PDF/ZIP + smoke manuel + tests |
| SYNC-FINAL-FOUNDATIONS-001 | DONE | Synchroniser les fondations finales UI/PDF/ZIP/cl?ture dans main | branches finales list?es | main r?align? + pilotage final |
| WORKTREE-CLEANUP-AND-UI-STATUS-001 | DONE | Consolider la revue finale, clarifier le statut UI et archiver les anciens worktrees locaux | `main` propre + audit branches/worktrees + `codex/review-final-001` | rapport 23 + pack de revue finale int?gr? + dossier canonique unique |
| CLOSE-PROJECT-V1-001 | READY | Clore le projet V1 apr?s revue finale | `REVIEW-FINAL-001` termin? | cl?ture V1 document?e |
| UI-BUSINESS-WIZARD-001 | DONE | Lancer le wizard metier UI dossier-centre | `REVIEW-FINAL-001` + docs UI 19/20/21 + moteur DOCX/ZIP | UI metier guidee sans logique juridique cachee |
| DEPLOY-STREAMLIT-CLOUD-FIX-001 | DONE | Corriger l'installation Poetry Streamlit Cloud | erreur cloud package `sydel-document-engine` + package source `src/sydel_doc_engine` | `pyproject.toml` package explicite + rapport de deploiement + validations locales |
| CASE-CATALOG-001 | DONE | Cr?er la couche m?tier catalogue des cas depuis la source de v?rit? | `project/source_truth/Documents_a_generer_par_cas.docx` + registre DOC-001 ? DOC-043 | service pur `get_expected_documents` + tests + rapport |
| UI-CASE-WIZARD-002 | DONE | Brancher l'assistant m?tier Streamlit sur le catalogue des cas | `CASE-CATALOG-001` + docs UI 19/20/21 + assistant existant | s?lection documentaire via `get_expected_documents` + statuts honn?tes + tests + rapport |
| SELARL-PILOT-PROTOCOL-001 | DONE | Cadrer le protocole produit SELARL pilote depuis la source V2 | `Documents_a_generer_par_cas_V2.docx` + CASE-CATALOG-001 + UI actuelle | protocole r?plicable + specs SELARL + plan d'impl?mentation + rapport |
| SELARL-PILOT-SOURCE-VERIFY-001 | DONE | R?concilier les specs SELARL avec la vraie source V2 | vraie V2 `project/source_truth/Documents_a_generer_par_cas_V2.docx` + specs SELARL + catalogue | matrice d'?carts + statuts d?rogation corrig?s + specs align?es + tests |
| SELARL-FORM-SCHEMA-IMPL-001 | DONE | Impl?menter le sch?ma de donn?es SELARL c?t? Assistant m?tier | vraie V2 + specs SELARL + catalogue corrig? | module `selarl_form_schema.py` + r?serve DOC-006 + couverture variables V2 + tests + rapport |
| SELARL-UI-WIZARD-IMPL-001 | DONE | Brancher l'UI Assistant m?tier sur le sch?ma SELARL | `selarl_form_schema.py` + spec UI SELARL | parcours SELARL visible, documents manuels visibles mais exclus de la g?n?ration + tests + rapport |
| SELARL-NOTEBOOKLM-RECONCILIATION-001 | DONE | R?concilier le pilote SELARL avec NotebookLM et la V3 | NotebookLM + V3 + V2 + code/specs SELARL | hi?rarchie source V2 + rapport d'?carts + backlog de reconstruction contr?l?e |
| SELARL-PLAN-CORRECTION-001 | DONE | Resserrer le plan SELARL selon arbitrages associ? | rapport NotebookLM + backlog V2 | hi?rarchie source corrig?e, backlog simplifi?, UI SELARL non valid?e produit |
| SELARL-WORDING-REALIGN-001 | DONE | R?aligner le vocabulaire visible SELARL | rapport NotebookLM corrig? + backlog V2 corrig? | labels Praticien/Fiche Client/r?les + tests anti-r?gression |
| SELARL-FLOW-REALIGN-001 | DONE | R?aligner l'ordre du formulaire SELARL | `SELARL-WORDING-REALIGN-001` | flow schema/projections Qualification / Fiche Client / Soci?t? / Capital / Sc?narios / Documents + tests |
| SELARL-REUSE-RULES-REALIGN-001 | DONE | Corriger les r?gles de r?utilisation SELARL | `SELARL-FLOW-REALIGN-001` | Dossier unipersonnel, Praticien source, d?rivations explicites |
| SELARL-UI-REALIGN-001 | DONE | R?aligner le parcours UI SELARL apr?s sch?ma corrig? | `SELARL-REUSE-RULES-REALIGN-001` | Streamlit SELARL r?align? sans push/red?ploiement pr?matur? |
| SELARL-SMOKE-REALISTIC-001 | DONE | Smoke tester SELARL avec donn?es r?alistes apr?s r?alignement | `SELARL-UI-REALIGN-001` | rapport de smoke r?aliste, documents manuels exclus, catalogue existant respect? |
| SELARL-CLOUD-GENERATION-BUG-001 | DONE | Corriger le blocage de g?n?ration SELARL visible | test utilisateur Cloud + parcours Streamlit SELARL | session state d?riv? corrig?, g?n?ration visible restaur?e, test AppTest |
| DOCUMENT-UNITAIRE-001 | DONE | Ajouter le mode Streamlit Document unitaire | Streamlit + catalogue cas + sch?ma SELARL | choix document, champs limit?s, DOCX unique, ZIP/PDF optionnels, rapport |
| ASSISTANT-METIER-PREFILL-001 | DONE | Ajouter des sc?narios fictifs d?terministes de pr?remplissage dans Assistant m?tier | Assistant m?tier SELARL/SCI + specs UI/SELARL | module presets + boutons Pr?remplir/R?initialiser + tests + rapport |
| GLOBAL-VARIABLE-INVENTORY-001 | DONE | Construire l'inventaire global brut des variables documentaires | r?f?rentiels V1 + source truth V1/V2/V3 + templates + specs + registre | CSV global brut + rapport ex?cutif + pilotage |
| GLOBAL-VARIABLE-IDENTITY-AUDIT-001 | DONE | Auditer l'identit? s?mantique globale des variables avant rebuild front | `GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` + r?f?rentiels V1 + templates + specs | matrice identit? V2 + registre canonique global V2 + questions humaines + rapport |
| GLOBAL-HUMAN-ANSWERS-INTEGRATION-001 | DONE | Int?grer les r?ponses humaines dans le registre canonique global | audit global V2 + r?ponse Albane + mod?le SELAS micro-holding + V3/NotebookLM | questions V2 + registre canonique V2.1 + rapport ex?cutif |
| GLOBAL-FRONT-ARCHITECTURE-001 | DONE | Concevoir l'architecture du nouveau front global sur le registre V2.1 | registre canonique global V2.1 + questions V2 | architecture front sans modification moteur/g?n?rateurs/UI existante |
| GLOBAL-FRONT-ARCHITECTURE-QA-001 | DONE | Contr?ler l'architecture front globale sur documents sentinelles | architecture front V1 + registre V2.1 + catalogue moteur + templates sentinelles | rapport QA + CSV sentinelles sans modification moteur/g?n?rateurs/UI |
| FRONT-DATA-LAYER-001 | DONE | Cr?er la couche de donn?es front globale | architecture front V1 + registre V2.1 | objets front globaux + tests/validations sans toucher aux g?n?rateurs |
| FRONT-ROLE-MODEL-001 | DONE | Mod?liser les r?les explicites du front global | `FRONT-DATA-LAYER-001` | RoleAssignment sans fusion silencieuse |
| FRONT-ADDRESS-MODEL-001 | DONE | Mod?liser les adresses typ?es par usage | `FRONT-DATA-LAYER-001` + `FRONT-ROLE-MODEL-001` | adresses pivots, r?gles de r?utilisation, overrides |
| FRONT-DOSSIER-FLOW-001 | DONE | D?finir le flow dossier complet global | data layer + r?les + adresses | flow dossier par op?ration/famille documentaire |
| FRONT-DOCUMENT-STATUS-LAYER-001 | DONE | Construire la couche de statuts documentaires front | `FRONT-DOSSIER-FLOW-001` | documents attendus, manuels, r?serv?s, non pr?ts |
| FRONT-UNIT-DOCUMENT-MODE-001 | DONE | Reconcevoir le mode document unitaire comme diagnostic s?par? | `FRONT-DOCUMENT-STATUS-LAYER-001` | test document unique sans polluer le parcours dossier |
| FRONT-TEST-PREFILL-001 | DONE | Concevoir les pr?remplissages fictifs de test du nouveau front | `FRONT-DOSSIER-FLOW-001` + status layer | sc?narios d?terministes non m?tier |
| FRONT-REVIEW-001 | DONE | Faire valider le mod?le front global avant UI visible | tickets front data/role/address/flow/status/prefill | carte de migration + backlog UI visible |
| FRONT-UI-SHELL-001 | DONE | Creer la premiere tranche visible du nouveau front global | `FRONT-REVIEW-001` + `front_data` | shell cible distinct du prototype, outils de test isoles |
| FRONT-DOSSIER-EDITOR-001 | DONE | Construire l'editeur dossier data-first | `FRONT-UI-SHELL-001` | editeur dossier V1, flow/blocs/exigences/statuts visibles |
| FRONT-DOSSIER-DATA-ENTRY-001 | DONE | Ajouter la premiere saisie reelle du nouvel editeur dossier | `FRONT-DOSSIER-EDITOR-001` + `front_data` | saisie SELARL simple vers DossierRecord + statuts recalcules |
| FRONT-DOCUMENTS-PANEL-001 | BLOCKED | Afficher les documents attendus et leurs statuts | decision post-test utilisateur minimal | ne pas ajouter de panneau visible sans besoin confirme |
| FRONT-GENERATION-ACTIONS-001 | DONE | Brancher les actions DOCX/PDF/ZIP du nouveau front | `FRONT-DOSSIER-DATA-ENTRY-001` + status layer | generation V1 DOC-001 a DOC-004 depuis le nouveau front |
| FRONT-UX-CLEANUP-001 | DONE | Simplifier le nouveau front pour test utilisateur reel | `FRONT-GENERATION-ACTIONS-001` | parcours principal type dossier / saisie / resume / generation, diagnostics replies |
| FRONT-UX-HARD-CUT-001 | DONE | Retirer tout bruit non-user du nouveau front | `FRONT-UX-CLEANUP-001` | vue principale limitee a type dossier, saisie et generation ; outils internes en sidebar |
| FRONT-STATE-AUDIT-001 | DONE | Auditer l'etat reel projet/front apres retour utilisateur | docs projet + front Streamlit + tests front | rapport d'audit + direction front immediate |
| FRONT-REALITY-CHECK-001 | DONE | Auditer l'ecart entre debriefs front et code reel | code Streamlit + debriefs front + etat Git | rapport de realite + plan surface minimale |
| FRONT-MINIMAL-SURFACE-CLEANUP-001 | DONE | Appliquer la surface utilisateur minimale | `FRONT-REALITY-CHECK-001` + `FRONT_MINIMAL_USER_SURFACE_V1.md` | type dossier / saisie / generation, debug cache |
| SELARL-COMPLETE-CASE-PLAYBOOK-001 | DONE | Cadrer la SELARL complete et la recette reproductible | specs SELARL + code front reel + catalogue moteur | playbook SELARL complet + rapport de realite |
| SELARL-COMPLETE-CONTEXT-ADAPTER-001 | DONE | Brancher l'adaptateur contexte SELARL complet cote front | `SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` + `front_data` + catalogue | selection documentaire conditionnelle + readiness + contexte moteur |
| SELARL-COMPLETE-COMPLEX-SUBFORMS-001 | READY | Completer les sous-formulaires SELARL complexes | `SELARL-COMPLETE-CONTEXT-ADAPTER-001` + catalogue + specs cession/SCM | cession medicale/dentaire et SCM generables quand les donnees sont completes |
| FRONT-GENERATION-READINESS-UX-001 | BLOCKED | Expliquer les blocages de generation dans la vue normale | a absorber dans `FRONT-MINIMAL-SURFACE-CLEANUP-001` | ne pas lancer comme ticket separe avant la coupe UX |
| FRONT-UNIT-DOCUMENT-UI-001 | BLOCKED | Consolider l'UI Document unitaire autour de `front_data` | `FRONT-UI-SHELL-001` | mode document unique separe du dossier complet |
| FRONT-TEST-TOOLS-CONSOLIDATION-001 | BLOCKED | Regrouper prefills, smoke et diagnostic | `FRONT-UI-SHELL-001` | outils de test marques et separes du produit |
| FRONT-PROTOTYPE-DEPRECATION-001 | BLOCKED | Deprecier le prototype historique sans perte de diagnostic | nouveaux parcours UI visibles | prototype marque obsolete ou archive |
| SELARL-JURIST-REVIEW-001 | READY | Faire valider le parcours SELARL r?align? par un juriste | `SELARL-SMOKE-REALISTIC-001` | revue juriste, r?serves et arbitrages document?s |
| SELARL-DOCS-GENERATION-SMOKE-001 | BLOCKED | Smoke tester la g?n?ration SELARL depuis le parcours Assistant m?tier | parcours SELARL r?align? + catalogue + schema + contextes r?alistes | bloqu? par la r?conciliation NotebookLM ; remplac? par `SELARL-SMOKE-REALISTIC-001` apr?s r?alignement |
| UI-001 | BLOCKED | Brancher Streamlit V0 Lot 1 | orchestrateur Lot 1 + spec canonique PV nomination g?rant valid?e | ?cran simple + test manuel |

## R?f?rentiels moteur disponibles
- Le moteur dispose d?sormais d'un arbre documentaire document-centr? V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`.
- Le moteur dispose d?sormais d'un dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le moteur dispose d?sormais d'une table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage m?tier de la famille `PV nomination g?rant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination g?rant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination g?rant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- La spec technique V1 de couche de rendu DOCX commune est disponible : `docs/delivery/render_style_system_v1.md`.
- Le cadrage V1 `Demande d'inscription ? l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- La spec canonique V1 `Demande d'inscription ? l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- La spec texte V1 `Demande d'inscription ? l'ordre` est disponible : `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Le cadrage V1 du batch `r?gime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- La spec canonique V1 du batch `r?gime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md`.
- La spec texte V1 du batch `r?gime communautaire` est disponible : `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- La spec canonique V1 du batch SPFPL sp?cifique est disponible : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- La spec texte V1 du batch SPFPL sp?cifique est disponible : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- La pr?paration V1 des sources statuts est disponible : `docs/delivery/lot_04_statuts_preparation_v1.md`.
- La spec canonique V1 de la famille `d?rogations` est disponible : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- La spec texte V1 de la famille `d?rogations` est disponible : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- La spec canonique V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`.
- La spec texte V1 `cession cabinets` est disponible : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Les arbitrages V1 `cession cabinets` sont disponibles : `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- La spec canonique V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- La spec texte V1 `bail / appel de fonds` est disponible : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Les arbitrages V1 `d?rogations` sont disponibles : `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Les arbitrages V1 du batch SPFPL sp?cifique sont disponibles : `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Les specs V1 des statuts SEL d'exercice sont disponibles : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Les specs V1 des statuts SPFPL sont disponibles : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Les specs V1 des statuts civils sont disponibles : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Les specs V1 des statuts SAS sont disponibles : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Les arbitrages V1 des statuts SCM sont disponibles : `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.
- La pr?paration V1 des satellites SCM est disponible : `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.
- Les specs V1 des satellites SAS sont disponibles : `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` et `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.
- La spec V1 de la lettre option IS est disponible : `docs/delivery/lot_05_lettre_option_is_spec_v1.md`.
- L'audit V1 de l'acte de cession d'actions est disponible : `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.
- Les specs V1 de l'acte de cession d'actions sont disponibles : `docs/delivery/lot_05_acte_cession_actions_spec_canonique_v1.md` et `docs/delivery/lot_05_acte_cession_actions_spec_texte_v1.md`.
- La pr?paration V1 des sources cession SCM est disponible : `docs/delivery/lot_05_scm_cession_sources_preparation_v1.md`.
- Les specs V1 du blocage cession SCM sont disponibles : `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` et `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- La r?solution V1 du bloc cession SCM est disponible : `docs/delivery/lot_05_scm_cession_block_resolution_v1.md`.
- L'audit de cl?ture moteur V1 est disponible : `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`.
- L'audit qualit? final moteur V1 est disponible : `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md`.
- Le plan de fondation post-moteur V1 est disponible : `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md`.
- Le flux UI V1 est disponible : `docs/project/19_UI_FLOW_V1.md`.
- Le r?f?rentiel des occurrences UI V1 est disponible : `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`.
- Le sch?ma formulaire UI V1 est disponible : `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Le framework de recette finale V1 est disponible : `docs/review/final_recipe_framework_v1.md`.
- Le blueprint style Lot 03 est disponible : `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.
- Le blueprint style statuts est disponible : `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- Le manifest d'import sources V1 est disponible : `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`.
- Le rapport de doublons sources V1 est disponible : `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`.
- Le plan de placement sources V1 est disponible : `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Les d?cisions d'arbitrage sources V1 sont disponibles : `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`.
- Le journal d'ex?cution du placement HIGH V1 est disponible : `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.
- L'audit du p?rim?tre restant V1 est disponible : `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.
- Le pack de revue humaine du PV nomination g?rant est disponible : `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aper?u texte extrait du DOCX g?n?r? est disponible : `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- La revue smoke orchestrateur Lot 2 est disponible : `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Les revues batch Lot 03 et Lot 04 sont disponibles : `docs/review/lot_03_batch_review_v1.md` et `docs/review/lot_04_batch_review_v1.md`.
- Ces r?f?rentiels cadrent les prochains tickets ; ils ne doivent pas ?tre r?invent?s pendant l'impl?mentation.

## Ecart temporaire connu
- Nom canonique retenu pour la domiciliation : `domiciliation.adresse_affichee`.
- Alias legacy temporaire pr?sent dans le code Lot 1 : `adresse_domiciliation_affichee`.
- Le pr?sent ticket ne refactore pas le code Python ; les prochains tickets doivent converger vers le nom canonique sans recr?er de variante locale.

## D?tail des prochains tickets

### DOC-001
- Objectif : g?n?rer la d?claration sur l'honneur de non-condamnation.
- Spec ? lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- ADR ? relire : ADR-0001, ADR-0002, ADR-0004, ADR-0005.
- Contraintes : source re?ue, spec ?crite, accords de genre, DOCX propre, tests obligatoires.
- Sortie attendue : g?n?rateur DOC-001, tests, mise ? jour documentaire.

### DOC-003
- Objectif : g?n?rer la procuration apr?s DOC-001.
- Spec ? lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contraintes : bloc mandataire SYDEL externalis? en configuration, wording source conserv?.
- Sortie attendue : g?n?rateur DOC-003, tests, mise ? jour documentaire.

### DOC-002
- Objectif : g?n?rer l'autorisation de domiciliation apr?s arbitrage V1 d?j? pos?.
- Spec ? lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contrainte sensible : le nom canonique documentaire est d?sormais `domiciliation.adresse_affichee`; le code Lot 1 existant conserve temporairement l'alias legacy `adresse_domiciliation_affichee`.
- Sortie : g?n?rateur DOC-002 termin?, tests unitaires cibl?s ajout?s, validations locales vertes.

### ORCH-001
- Objectif : brancher les trois g?n?rateurs Lot 1 dans l'orchestrateur dossier.
- Pr?requis : DOC-001, DOC-002 et DOC-003 termin?s.
- Sortie : registre minimal DOC-001/DOC-002/DOC-003 branch?, g?n?ration DOCX dossier selon `ctx.structure`, tests d'orchestration ajout?s.

### VAR-001
- Objectif : ajouter une table de mapping document -> variables canoniques sans refaire le dictionnaire.
- Pr?requis : arbre documentaire V1 et dictionnaire canonique des variables V1 int?gr?s.
- Sortie : table de mapping V1 int?gr?e ? la m?moire projet, sans r??criture ; ?cart temporaire document? entre `domiciliation.adresse_affichee` et l'alias legacy `adresse_domiciliation_affichee`.

### SPEC-PV-001
- Objectif : formaliser la spec canonique du PV nomination g?rant ? partir du cadrage V1, sans refaire le cadrage.
- Spec/cadrage ? lire : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- Pr?requis : arbre documentaire V1, dictionnaire canonique V1 et table de mapping document -> variables canoniques V1.
- Contraintes : traiter `PV nomination g?rant` comme une famille documentaire mutualisable, g?rer `associes[]` dynamiquement, distinguer `dirigeant_nomine` de `associes[]`, identifier les blocs conditionnels, ne coder aucun g?n?rateur.
- Sortie attendue : spec canonique ?crite dans `docs/delivery/`, avec structure, blocs fixes, blocs conditionnels, mapping variables, r?gles de r?p?tition, r?gles de grammaire minimales et points ouverts.
- Statut : termin? ; spec canonique V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.

### SPEC-TEXTE-PV-001
- Objectif : stabiliser le texte canonique et les variantes du PV nomination g?rant avant tout codage.
- Spec ? lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- Source ? consulter : `project/source_documents/lot_02/PV nomination ge?rant - transforme.docx`.
- Contraintes : ne pas refaire la spec canonique, ne pas coder de g?n?rateur, ne pas modifier implicitement le wording juridique ; signaler les formulations ? validation.
- Sortie attendue : spec textuelle d?taill?e du PV nomination g?rant, variantes structurelles explicites, wording ? valider, crit?res d'entr?e avant code.
- Statut : termin? ; spec texte V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.

### CODE-PV-001
- Objectif : impl?menter le g?n?rateur canonique `PV nomination g?rant` ? partir des specs V1, sans reprendre `personne_1` / `personne_2` comme v?rit? m?tier.
- Specs ? lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` et `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- Source ? consulter : `project/source_documents/lot_02/PV nomination ge?rant - transforme.docx`.
- Contraintes : g?n?rateur DOCX from-scratch, `associes[]` dynamique, `dirigeant_nomine` distinct, variantes `n?/n?e`, branche `emprunt.actif`, renum?rotation des d?cisions, aucun changement de wording juridique hors spec texte.
- Sortie attendue : g?n?rateur d?di?, tests unitaires cibl?s, validation locale, mise ? jour documentaire.
- Statut : termin? ; g?n?rateur disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`, non branch? ? l'orchestrateur.
- Smoke test r?el : contexte exemple disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, DOCX g?n?r? dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.

### REVIEW-PV-001
- Objectif : pr?parer la revue humaine du rendu DOCX et du wording du PV nomination g?rant d?j? cod?, sans modifier le code m?tier.
- Entr?es : g?n?rateur PV existant, contexte exemple `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, specs Lot 2.
- Sortie : DOCX r?g?n?r? dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`, aper?u texte et checklist de revue dans `docs/review/`.
- Statut : termin? ; le PV reste non branch? ? l'orchestrateur Lot 2 tant qu'une validation humaine explicite n'a pas ?t? donn?e.

### SPEC-RENDER-001
- Objectif : formaliser une couche de rendu DOCX commune avant refactor du code m?tier.
- Spec ? lire : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ne modifier aucun g?n?rateur, ne changer aucun wording juridique, documenter les styles communs, le titre encadr?, les signatures simples/encadr?es, le rappel l?gal et les surcharges documentaires.
- Sortie : spec technique V1 cr??e ; documents impact?s list?s : DOC-001, DOC-002, DOC-003 et PV nomination g?rant.
- Statut : termin? ; le point d'?cart explicite est que les encadr?s de signature manquent aujourd'hui dans le rendu g?n?r?.

### RENDER-STYLE-001
- Objectif : impl?menter la couche commune de rendu DOCX dans `src/sydel_doc_engine/rendering/docx_builder.py`.
- Pr?requis : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ticket technique uniquement, aucun changement de wording juridique, migration progressive, tests existants ? conserver verts.
- Sortie attendue : profil global de style, helpers de paragraphes/blocs, titre encadr?, signature simple, signature encadr?e disponible, rappel l?gal commun.
- Statut : termin? ; couche commune impl?ment?e et appliqu?e ? DOC-001, DOC-002, DOC-003 et PV nomination g?rant.

### ORCH-L2-PV-001
- Objectif : brancher le g?n?rateur PV nomination g?rant dans le catalogue et l'orchestrateur, sans UI, PDF ni ZIP.
- Pr?requis : g?n?rateur PV existant, specs Lot 2, d?cisions de s?lection SELARL/SELAS/SPFPL cession/SPFPL apport/SCS/SCI/SCM et exclusion SAS.
- Sortie : `DOC-004` ajout? au catalogue, g?n?rateur enregistr?, s?lection test?e pour SELARL/SCI/SAS, g?n?ration orchestr?e test?e avec production du DOCX PV.
- Statut : termin? ; aucune modification de wording juridique.

### SMOKE-ORCH-L2-001
- Objectif : v?rifier en g?n?ration r?elle l'orchestrateur Lot 2 avec un cas positif SCI et un cas n?gatif SAS.
- Entr?es : contextes `examples/contexts/lot_02_orchestrator_positive_example.yaml` et `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`.
- Sortie : smoke DOCX dans `artifacts/lot_02_orchestrator_positive_smoke_test/` et `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`, revue dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- Statut : termin? ; le PV est g?n?r? pour SCI et absent pour SAS.

### FIX-PV-RENDER-001
- Objectif : am?liorer le rendu from-scratch du PV nomination g?rant sans chercher une copie parfaite du Word source.
- Entr?es : source Lot 2 `PV nomination g?rant - transforme.docx`, specs PV V1 et spec `render_style_system_v1.md`.
- Contraintes : ne pas modifier le wording juridique, ne pas toucher ? l'UI, ne pas g?n?rer PDF/ZIP, ne pas versionner `artifacts/`.
- Sortie : bloc soci?t? centr? avec d?nomination en gras, titre principal encadr?, listes ? tirets pour associ?s et d?cisions, intertitres de d?cision gras/soulign?s, formules de vote en italique, signatures centr?es, smoke DOCX.
- Statut : termin? ; aucun changement de wording juridique volontaire.

### ANALYSE-ORDRE-001
- Objectif : pr?parer le prochain batch mutualisable Lot 2 sans coder, en analysant la demande d'inscription ? l'ordre et les deux lettres de r?gime communautaire.
- Entr?es : r?f?rentiels projet V1 + trois sources Lot 2 pr?sentes dans `project/source_documents/lot_02/`.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Statut : termin? ; aucun code Python modifi?.

### ARBITRAGE-SOURCES-001
- Objectif : r?parer les pr?requis documentaires d'import sources puis arbitrer les placements possibles sans d?placer de fichier.
- Entr?es : `project/source_truth/Documents_a_generer_par_cas.docx`, `project/source_import/raw_drive_dump/`, `project/source_documents/`, d?cisions m?tier chef de projet.
- Sortie : manifest import sources V1, rapport doublons V1, plan placement V1, d?cisions arbitrage V1.
- Statut : termin? ; aucun code Python, aucun fichier source, aucun artefact modifi?.

### PLACEMENT-HIGH-001
- Objectif : d?placer physiquement dans `source_documents` uniquement les cas HIGH valid?s par `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.
- Entr?es : plan de placement V1 + d?cisions d'arbitrage sources V1.
- Contraintes : ne pas toucher aux cas MEDIUM/LOW, ne pas versionner `project/source_import/raw_drive_dump/`, documenter les no-op si les fichiers HIGH sont d?j? pr?sents.
- Statut : termin? ; les 4 cas HIGH sont d?j? pr?sents aux emplacements cibles et ont ?t? confirm?s en no-op document?. Aucun fichier MEDIUM/LOW ou hors p?rim?tre n'a ?t? modifi?.

### SPEC-ORDRE-001
- Objectif : formaliser la spec canonique `Demande d'inscription ? l'ordre` ? partir du cadrage V1.
- Cadrage ? lire : `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`.
- Contraintes : ne pas coder, comparer les variantes SELARL / SELAS / SPFPL, identifier le traitement de `D?rogation ?`, les accords de genre, le titre `Dr`, le destinataire ordinal et le mapping des donn?es ordinales.
- Sortie : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`, avec p?rim?tre structures, comparaison des variantes, noyau texte, variables canoniques, r?gles de blocage et points ouverts.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-TEXTE-ORDRE-001
- Objectif : stabiliser le texte canonique et les variantes de `Demande d'inscription ? l'ordre` avant tout codage.
- Spec ? lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`.
- Sources ? consulter : source Lot 2 + variantes raw dump SELARL, SELAS et SPFPL compar?es dans la spec canonique.
- Contraintes : ne pas coder, trancher le wording de `D?rogation ?`, la granularit? des donn?es ordinales, le mandataire, les accords et le destinataire ordinal.
- Sortie attendue : spec texte d?taill?e, wording stabilis? ou points de blocage explicites, crit?res avant code.
- Statut : termin? ; spec texte V1 disponible dans `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.

### CODE-ORDRE-001
- Objectif : impl?menter le g?n?rateur canonique `Demande d'inscription ? l'ordre`.
- Specs ? lire : `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md` et `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`.
- Sources ? consulter : source Lot 2 + variantes raw dump SELARL, SELAS, SPFPL cession, SPFPL apport et absence de variante SCM d?di?e document?e.
- Contraintes : g?n?rateur DOCX from-scratch, overlays SELARL/SELAS, SPFPL cession/apport et SCM, bloc `D?rogation ?` manuel/conditionnel, mandataire configurable, aucune constante SYDEL en dur, aucun changement de wording juridique hors spec texte.
- Sortie attendue : g?n?rateur d?di?, tests unitaires cibl?s, validation locale, mise ? jour documentaire.
- Statut : termin? ; g?n?rateur disponible dans `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`, tests cibl?s ajout?s, smoke DOCX r?el g?n?r? hors versionnement.

### SPEC-RC-001
- Objectif : formaliser la spec canonique du batch `r?gime communautaire` pour la lettre de renonciation et la lettre d'avertissement.
- Cadrage ? lire : `docs/delivery/lot_02_regime_communautaire_batch_cadrage_v1.md`.
- Contraintes : garder deux documents canoniques distincts, mutualiser le pack de variables, arbitrer les r?les `apporteur` / `conjoint`, les montants, les dates crois?es, les formes sociales et la mention manuscrite.
- Sortie : specs canonique et texte cr??es dans `docs/delivery/`, variantes SELARL / SELAS / SPFPL compar?es, mapping commun ?crit, overlays de mention manuscrite document?s, r?gles de blocage avant code pr?cis?es.
- Statut : termin? ; `CODE-RC-001` est ajout? en READY.

### CODE-RC-001
- Objectif : impl?menter le batch `r?gime communautaire` V1 pour la lettre d'avertissement au conjoint et la lettre de renonciation.
- Specs ? lire : `docs/delivery/lot_02_regime_communautaire_batch_spec_canonique_v1.md` et `docs/delivery/lot_02_regime_communautaire_batch_spec_texte_v1.md`.
- Sources ? consulter : sources Lot 2 plac?es + variantes raw dump SELARL, SELAS et SPFPL compar?es dans SPEC-RC-001.
- Contraintes : deux documents canoniques distincts, g?n?ration DOCX from-scratch, s?lection uniquement si `dossier.options.regime_communautaire == true`, structures SELARL / SELAS / SPFPL cession / SPFPL apport, aucun changement de wording juridique hors variables et overlays document?s.
- Sortie attendue : g?n?rateurs d?di?s, branchement orchestrateur/catalogue si n?cessaire, tests cibl?s des quatre structures, de la mention manuscrite SELARL vs SELAS/SPFPL, des dates crois?es et des blocages.
- Statut : termin? ; g?n?rateurs `lettre_renonciation_associe` et `lettre_avertissement_conjoint` disponibles, catalogue/orchestrateur branch?s, contexte exemple et smoke DOCX g?n?r?s.

### SPEC-SPFPL-001
- Objectif : formaliser le batch documentaire SPFPL sp?cifique sans coder.
- Spec ? lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`.
- Contraintes : garder les documents universels et le r?gime communautaire hors de cette spec, ne pas coder depuis une source absente, ne pas corriger les ambigu?t?s cession/apport sans arbitrage.
- Sortie : spec canonique V1 SPFPL, sous-familles, variables propos?es, blocages et points ouverts.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-DEROG-001
- Objectif : formaliser la famille documentaire `d?rogations` sans automatiser les formulaires manuels.
- Spec ? lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`.
- Contraintes : distinguer site distinct, multi-sites SEL, cumul SEL/BNC, cumul salari?e et pi?ces manuelles ; ne pas g?n?rer de contenu narratif sensible.
- Sortie : spec canonique V1 d?rogations, p?rim?tre automatisable/manuel, variables et blocages.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-CESSION-BAIL-001
- Objectif : formaliser les blocs `cession cabinets` et `bail / appel de fonds` avant tout code.
- Specs ? lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`.
- Contraintes : ne pas fusionner acte/compromis ou m?dical/dentaire sans arbitrage, traiter les anomalies de bail et de placeholders comme points ouverts.
- Sortie : deux specs canoniques V1, variables, conditions, r?gles de blocage et points ouverts.
- Statut : termin? ; aucun code Python modifi?.

### SYNC-SPECS-001
- Objectif : absorber dans `main` les specs parall?les RC, SPFPL, d?rogations et cession/bail.
- Entr?es : branches et commits de specs d?j? produits en parall?le.
- Sortie : commits de specs int?gr?s dans `main`, pilotage align?, `CODE-RC-001` confirm? READY.
- Statut : termin? ; aucun fichier Python stag? pour le commit de synchronisation.

### SPEC-TEXTE-BAIL-APP-001
- Objectif : stabiliser le texte canonique du mini-batch `bail / appel de fonds` avant code.
- Spec ? lire : `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : conserver le wording source, bloquer l'appel de fonds m?dical et les cas SELAS non arbitr?s, ne pas coder.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-TEXTE-CESSION-CAB-001
- Objectif : stabiliser le texte canonique de la famille `cession cabinets`.
- Spec ? lire : `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Contraintes : ne pas harmoniser m?dical/dentaire, acte/compromis ou SELARL/SELAS sans arbitrage.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-TEXTE-DEROG-001
- Objectif : stabiliser le texte canonique des d?rogations.
- Spec ? lire : `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, ne pas inventer les zones narratives sensibles.
- Statut : termin? ; aucun code Python modifi?.

### SPEC-TEXTE-SPFPL-001
- Objectif : stabiliser le texte canonique du batch SPFPL sp?cifique.
- Spec ? lire : `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Contraintes : ne pas corriger les conflits cession/apport, commissaire aux apports ou souscripteurs sans arbitrage.
- Statut : termin? ; aucun code Python modifi?.

### SYNC-TEXTE-SPECS-001
- Objectif : absorber dans `main` les quatre specs texte parall?les bail/appel, cession cabinets, d?rogations et SPFPL.
- Entr?es : branches `codex/spec-texte-bail-app-001`, `codex/spec-texte-cession-cab-001`, `codex/spec-texte-derog-001`, `codex/spec-texte-spfpl-001`.
- Sortie : quatre specs texte int?gr?es dans `main`, pilotage align?, prochains tickets READY confirm?s.
- Statut : termin? ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifi?.

### SYNC-ARBITRAGES-001
- Objectif : absorber dans `main` les trois arbitrages parall?les cession cabinets, d?rogations et SPFPL.
- Entr?es : branches `codex/arbitrage-cession-001`, `codex/arbitrage-derog-001`, `codex/arbitrage-spfpl-001`.
- Sortie : arbitrages int?gr?s dans `main`, pilotage align?, prochains tickets READY confirm?s.
- Statut : termin? ; aucun fichier Python, aucun `project/source_import/raw_drive_dump/` et aucun `artifacts/` modifi?.

### CODE-BAIL-APP-001
- Objectif : impl?menter le mini-batch `bail / appel de fonds`.
- Specs ? lire : `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md` et `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`.
- Contraintes : g?n?ration DOCX from-scratch, activation cession SELARL/SELAS pour l'avenant, appel de fonds limit? SELARL dentaire, blocages explicites sur les points ouverts.
- Statut : DONE ; commit `557a013274aa9f7122c81d5e6e0b52c4043a540c` absorb? dans `main`, g?n?rateurs `avenant_contrat_bail` et `appel_fond_sel` disponibles, catalogue/orchestrateur branch?s et tests cibl?s int?gr?s.

### ARBITRAGE-CESSION-001
- Objectif : arbitrer les points bloquants de la famille `cession cabinets` avant tout code.
- Entr?es : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md` et `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`.
- Sortie attendue : d?cisions sur acte/compromis, SELAS, anomalies m?dical/dentaire, placeholders acqu?reur/vendeur, cr?dit-vendeur, SCM et salari?s.
- Statut : termin? ; arbitrages V1 disponibles dans `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.

### ARBITRAGE-DEROG-001
- Objectif : arbitrer les points bloquants de la famille `d?rogations` avant code.
- Entr?es : `docs/delivery/lot_03_derogations_spec_canonique_v1.md` et `docs/delivery/lot_03_derogations_spec_texte_v1.md`.
- Sortie attendue : d?cisions sur formulaires pr?remplis, placement sources Lot 03, conversion `.doc`, r?les et champs narratifs obligatoires.
- Statut : termin? ; arbitrages V1 disponibles dans `docs/delivery/lot_03_derogations_arbitrages_v1.md`.

### ARBITRAGE-SPFPL-001
- Objectif : arbitrer les points bloquants du batch SPFPL sp?cifique avant code.
- Entr?es : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_05_spfpl_spec_texte_v1.md`.
- Sortie attendue : d?cisions sur note d'information cession/apport, PV agr?ment, commissaire aux apports, liste des souscripteurs et sources manquantes.
- Statut : termin? ; arbitrages V1 disponibles dans `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.

### CODE-CESSION-CAB-001
- Objectif : impl?menter la famille `cession cabinets` en respectant les arbitrages V1.
- Specs ? lire : `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`, `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md` et `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`.
- Contraintes : quatre documents canoniques distincts, s?lection par ?tape explicite, s?paration m?dical/dentaire, blocages explicites sur les anomalies restantes, aucun wording corrig? silencieusement.
- Statut : DONE ; quatre g?n?rateurs cession cabinets disponibles sous `DOC-009` ? `DOC-012`, branch?s au catalogue et ? l'orchestrateur.

### RESUME-CODE-CESSION-CAB-001
- Objectif : reprendre proprement `CODE-CESSION-CAB-001` depuis `main` apr?s absorption de la pr?paration d?rogations et du sous-batch SPFPL.
- Entr?es : `main` synchronis?, specs/arbitrages cession cabinets V1, ?tat local CODE-CESSION non fusionn?.
- Contraintes : repartir d'un ?tat Git propre, ne pas reprendre de fichiers non suivis sans revue, conserver les blocages explicites d?j? arbitr?s.
- Statut : DONE ; branche reprise depuis `main`, travail cession restaur?, validations locales et smoke DOCX verts.

### PREP-DEROG-001
- Objectif : pr?parer les sources de la famille `d?rogations` avant code.
- Specs ? lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md` et `docs/delivery/lot_03_derogations_arbitrages_v1.md`.
- Contraintes : placer uniquement les sources Lot 03 explicitement d?cid?es, convertir ou remplacer le `.doc` legacy si `cumul_salariee` est cibl?, ne pas automatiser les formulaires manuels.
- Statut : DONE ; commit source `36828fbc45d6b8a37c2e76eb8227460df441ebde` absorb? dans `main`, sources Lot 03 plac?es et rapports de pr?paration disponibles.

### CODE-DEROG-CORE-001
- Objectif : impl?menter le c?ur de la famille `d?rogations` apr?s pr?paration des sources.
- Specs ? lire : `docs/delivery/lot_03_derogations_spec_canonique_v1.md`, `docs/delivery/lot_03_derogations_spec_texte_v1.md`, `docs/delivery/lot_03_derogations_arbitrages_v1.md` et `docs/delivery/lot_03_derogations_preparation_v1.md`.
- Contraintes : ne pas automatiser les formulaires manuels, distinguer document finalis? et formulaire ? compl?ter, bloquer les narratifs sensibles manquants.
- Statut : DONE ; g?n?rateurs partiels `multi_sites_sel` et `cumul_sel_bnc` cod?s en formulaires ? compl?ter, sources DOCX propres utilis?es, `cumul_salariee` legacy non trait?.

### CODE-SPFPL-AGR-INFO-001
- Objectif : impl?menter le sous-batch SPFPL `agr?ment / note d'information` limit? par les arbitrages V1.
- Specs ? lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : piloter le wording cession/apport par `operation_spfpl.type`, bloquer l'acte de cession d'actions et les multi-souscripteurs, ne jamais rendre `OU` ou une double option non tranch?e.
- Statut : DONE ; commit source `958fce5d2a9d5d30df4d918cb098fec483f5140e` absorb? dans `main`, g?n?rateurs cibl?s SPFPL et tests int?gr?s.

### CODE-SPFPL-CORE-001
- Objectif : impl?menter le c?ur SPFPL restant dans le respect des specs et arbitrages V1.
- Specs ? lire : `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`, `docs/delivery/lot_05_spfpl_spec_texte_v1.md` et `docs/delivery/lot_05_spfpl_arbitrages_v1.md`.
- Contraintes : rester limit? aux documents SPFPL sourc?s/arbitr?s, bloquer l'acte de cession d'actions sans source DOCX confirm?e, bloquer les multi-souscripteurs hors V1 et ne pas corriger le wording juridique sans validation explicite.
- Statut : DONE ; commit source `09cbad120d22910f05ba5e645971ade56fedb76d` absorb? dans `main`, g?n?rateurs SPFPL c?ur et tests cibl?s int?gr?s.

### PREP-STATUTS-001
- Objectif : pr?parer les sources statuts avant toute sp?cification ou impl?mentation.
- Entr?es : source de v?rit?, raw dump, r?f?rentiels projet et d?cisions de placement/arbitrage sources.
- Contraintes : ne pas d?dupliquer ni harmoniser les statuts sans comparaison document?e, ne pas coder de g?n?rateur, ne pas modifier le wording juridique source.
- Statut : DONE ; commit source `b854821061b85ac66fe785c11cb3c6b0bac5a85b` absorb? dans `main`, sources Lot 04 cadr?es et ?carts document?s.

### SPEC-STATUTS-SEL-001
- Objectif : sp?cifier les statuts SEL d'exercice avant tout codage.
- Specs/sources ? lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SELARL chirurgien-dentiste, SELARL m?decin, SELAS m?decin.
- Contraintes : comparer les variantes, extraire les variables, documenter les clauses sensibles, ne pas coder de g?n?rateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.

### SPEC-STATUTS-SPFPL-001
- Objectif : sp?cifier les statuts SPFPL cession/apport avant tout codage.
- Specs/sources ? lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 SPFPL.
- Contraintes : traiter cession et apport en comparaison, conserver les sorties distinctes tant que la fusion n'est pas prouv?e, ne pas coder de g?n?rateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.

### SPEC-STATUTS-CIVILS-001
- Objectif : sp?cifier les statuts civils SCI, SCI IRIS, SCM et SCS avant tout codage.
- Specs/sources ? lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et sources Lot 04 civiles.
- Contraintes : ne pas d?dupliquer SCI/SCI IRIS/SCM/SCS sans analyse document?e, identifier les variables capital, associ?s, si?ge, objet et options fiscales, ne pas coder de g?n?rateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.

### SPEC-STATUTS-SAS-001
- Objectif : sp?cifier les statuts SAS avant tout codage.
- Specs/sources ? lire : `docs/delivery/lot_04_statuts_preparation_v1.md` et source Lot 04 SAS.
- Contraintes : v?rifier le fichier source dont le nom contient aussi SPFPL, traiter s?par?ment la liste des souscripteurs et l'attestation sur le capital si n?cessaire, ne pas coder de g?n?rateur.
- Statut : DONE ; specs disponibles dans `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.

### SYNC-STATUTS-SPECS-001
- Objectif : absorber dans `main` les specs statuts parall?les SAS, SPFPL, SEL et civils.
- Entr?es : branches `codex/spec-statuts-sas-001`, `codex/spec-statuts-spfpl-001`, `codex/spec-statuts-sel-001` et `codex/spec-statuts-civils-001`.
- Sortie : commits de specs int?gr?s dans `main`, pilotage align? et prochains tickets confirm?s READY.
- Statut : DONE ; specs int?gr?es sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SAS-001
- Objectif : impl?menter les statuts SAS ? partir des specs V1.
- Specs ? lire : `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`.
- Contraintes : limiter le p?rim?tre au mod?le SAS/SPFPL m?decins source, bloquer les cas non arbitr?s, ne pas corriger le wording juridique sans validation.
- Statut : DONE ; g?n?rateur SAS V1 int?gr? dans `main` avec tests cibl?s.

### CODE-STATUTS-SPFPL-001
- Objectif : impl?menter les statuts SPFPL cession/apport ? partir des specs V1.
- Specs ? lire : `docs/delivery/lot_04_statuts_spfpl_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`.
- Contraintes : conserver deux overlays cession/apport, bloquer le multi-associ?s non arbitr? et les anomalies de wording non valid?es.
- Statut : DONE ; g?n?rateurs SPFPL cession/apport V1 int?gr?s dans `main` avec tests cibl?s.

### ARBITRAGE-STATUTS-SEL-001
- Objectif : arbitrer les points bloquants des statuts SEL avant code.
- Specs ? lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`.
- Contraintes : trancher pluralit? des associ?s, ligne `personne_2`, second lieu SELAS, f?minisation dirigeant et signatures.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.

### ARBITRAGE-STATUTS-CIVILS-001
- Objectif : arbitrer les points bloquants des statuts civils avant code.
- Specs ? lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : trancher SCI/SCI IRIS, SCM, SCS, associ?s personnes morales, signatures dynamiques et lettre option IS hors statuts.
- Statut : DONE ; arbitrages disponibles dans `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.

### SYNC-STATUTS-CODE-ARB-001
- Objectif : absorber dans `main` les branches code statuts SAS/SPFPL et arbitrage statuts SEL.
- Entr?es : `codex/code-statuts-sas-001`, `codex/code-statuts-spfpl-001`, `codex/arbitrage-statuts-sel-001`.
- Sortie : commits int?gr?s, tests relanc?s, pilotage align? sur les tickets suivants.
- Statut : DONE ; int?gration effectu?e sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.

### CODE-STATUTS-SEL-001
- Objectif : impl?menter les statuts SEL d'exercice apr?s arbitrages V1.
- Specs ? lire : `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`.
- Contraintes : appliquer strictement les arbitrages SEL, conserver les blocages explicites et ne pas corriger le wording juridique sans validation.
- Statut : DONE ; g?n?rateurs SEL d'exercice V1 int?gr?s dans `main` avec tests cibl?s.

### CODE-STATUTS-CIVILS-CORE-001
- Objectif : impl?menter le c?ur des statuts civils apr?s arbitrages V1.
- Specs ? lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Contraintes : couvrir uniquement SCS, SCI et SCI IRIS dans ce ticket, utiliser `associes[]`, bloquer les donn?es legacy insuffisantes et garder l'option IS hors g?n?rateur statuts.
- Statut : DONE ; SCM reste hors ticket ? cause des ambigu?t?s source document?es.

### RESUME-ARBITRAGE-STATUTS-CIVILS-001
- Objectif : reprendre proprement l'arbitrage des statuts civils depuis `main` synchronis?.
- Specs ? lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md` et `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`.
- Contraintes : arbitrer SCI/SCI IRIS, SCM, SCS, associ?s personnes morales, signatures dynamiques et lettre option IS hors statuts avant tout code.
- Statut : DONE ; remplac? par l'absorption de `ARBITRAGE-STATUTS-CIVILS-001`.

### STYLE-ANALYSE-BATCH-001
- Objectif : cadrer l'analyse de style documentaire en batch avant harmonisation de rendu.
- Entr?es : g?n?rateurs existants, specs disponibles et rendus DOCX d?j? produits hors versionnement.
- Contraintes : analyse/cadrage uniquement, sans modification de wording juridique ni d?placement de sources.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_batch_v1.md`.

### FIX-STYLE-LETTERS-001
- Objectif : corriger les ?carts de style prioritaires des lettres ? partir du blueprint batch V1.
- Specs ? lire : `docs/delivery/render_style_blueprint_batch_v1.md` et specs texte des lettres concern?es.
- Contraintes : ne pas modifier le wording juridique, limiter les changements au rendu DOCX, conserver les artefacts hors versionnement.
- Statut : DONE ; rendu lettres harmonis? et absorb? dans `main` via `RESUME-FIX-STYLE-LETTERS-001`.

### RESUME-FIX-STYLE-LETTERS-001
- Objectif : reprendre proprement la correction des ?carts de style prioritaires des lettres depuis `main` synchronis?.
- Specs ? lire : `docs/delivery/render_style_blueprint_batch_v1.md` et specs texte des lettres concern?es.
- Contraintes : ne pas modifier le wording juridique, limiter les changements au rendu DOCX, conserver les artefacts hors versionnement.
- Statut : DONE ; commit source `557fc1920361a8c7831e6b023d70471c9c29e5ff` absorb? dans `main`.

### ARBITRAGE-STATUTS-SCM-001
- Objectif : arbitrer les points bloquants statuts SCM avant toute impl?mentation.
- Specs ? lire : `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`, `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md` et `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`.
- Contraintes : traiter l'anomalie source de parts et la ligne fixe `510 euros` avant code.
- Statut : DONE ; arbitrages V1 disponibles dans `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`.

### PREP-SCM-SAT-001
- Objectif : pr?parer le p?rim?tre SCM et satellites avant sp?cification/code.
- Specs ? lire : specs statuts civils V1 et arbitrages SCM ? venir.
- Contraintes : ne pas d?placer de sources sans d?cision explicite et documenter tout blocage de source.
- Statut : DONE ; pr?paration V1 disponible dans `docs/delivery/lot_05_scm_satellites_preparation_v1.md`.

### SPEC-SAS-SATELLITES-001
- Objectif : sp?cifier les satellites SAS avant code.
- Specs ? lire : specs statuts SAS V1 et sources satellites ? confirmer.
- Contraintes : conserver le wording source et isoler les satellites du g?n?rateur statuts SAS existant.
- Statut : DONE ; specs V1 disponibles dans `docs/delivery/lot_05_sas_satellites_spec_canonique_v1.md` et `docs/delivery/lot_05_sas_satellites_spec_texte_v1.md`.

### CODE-OPTION-IS-001
- Objectif : impl?menter la lettre option IS hors g?n?rateurs statuts.
- Specs ? lire : spec/arbitrage applicable avant code.
- Contraintes : ne pas int?grer l'option IS dans les statuts civils ; g?n?rer un document d?di? avec tests.
- Statut : DONE ; g?n?rateur et tests int?gr?s dans `main`.

### PREP-ACTE-ACTIONS-001
- Objectif : pr?parer les sources de l'acte de cession d'actions.
- Specs ? lire : specs/arbitrages SPFPL V1 et source documentaire ? confirmer.
- Contraintes : ne pas coder sans source DOCX confirm?e.
- Statut : DONE ; audit V1 disponible dans `docs/delivery/lot_05_acte_cession_actions_audit_v1.md`.

### CODE-STATUTS-SCM-001
- Objectif : impl?menter les statuts SCM.
- Specs ? lire : specs statuts civils V1 et arbitrages SCM V1.
- Contraintes : respecter les arbitrages SCM, bloquer toute ambigu?t? de wording, ajouter tests et branchement orchestrateur cibl?s.
- Statut : DONE ; g?n?rateur statuts SCM int?gr? sous `DOC-025` avec tests cibl?s.

### CODE-SAS-SATELLITES-001
- Objectif : impl?menter les satellites SAS.
- Specs ? lire : specs satellites SAS V1.
- Contraintes : isoler les satellites du g?n?rateur statuts SAS existant et conserver le wording source.
- Statut : DONE ; g?n?rateurs satellites SAS int?gr?s et test?s.

### SPEC-SCM-SATELLITES-001
- Objectif : sp?cifier les satellites SCM avant code.
- Specs ? lire : pr?paration SCM satellites V1 et sources Lot 05 confirm?es.
- Contraintes : ne pas coder les satellites SCM sans spec canonique et texte.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### CONVERT-ACTE-ACTIONS-001
- Objectif : convertir ou remplacer la source de l'acte de cession d'actions.
- Specs ? lire : audit acte de cession d'actions V1.
- Contraintes : ne pas automatiser l'acte tant qu'une source DOCX propre n'est pas confirm?e.
- Statut : DONE ; DOCX converti dans `project/source_documents/lot_05/` et pr?paration disponible dans `docs/delivery/lot_05_acte_cession_actions_preparation_v1.md`.

### CONVERT-DEROG-SALARIEE-001
- Objectif : convertir ou remplacer la source legacy de d?rogation salari?e.
- Specs ? lire : pr?paration d?rogations V1 et arbitrages d?rogations V1.
- Contraintes : ne pas coder `cumul_salariee` sans source DOCX exploitable.
- Statut : DONE ; tentative Word COM retent?e, aucun DOCX produit, blocage document? dans `docs/delivery/lot_03_derogation_salariee_conversion_blocker_v1.md`.

### SPEC-ACTE-ACTIONS-001
- Objectif : sp?cifier l'acte de cession d'actions SPFPL avant tout code.
- Specs ? lire : audit et pr?paration acte de cession d'actions V1.
- Contraintes : ne pas coder sans spec canonique et texte.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### SPEC-DEROG-SALARIEE-MANUAL-001
- Objectif : sp?cifier le traitement manuel ou le blocage V1 de la d?rogation salari?e legacy.
- Specs ? lire : pr?paration d?rogations V1 et blocage conversion salari?e V1.
- Contraintes : ne pas automatiser sans source DOCX exploitable.
- Statut : DONE ; strat?gie V1 document?e dans `docs/delivery/lot_03_derogation_salariee_v1_strategy.md`.

### PREP-SCM-LISTE-DEPENSES-CONVERT-001
- Objectif : pr?parer une source exploitable pour la liste de d?penses SCM.
- Specs ? lire : pr?paration SCM satellites V1.
- Contraintes : ne pas toucher au raw dump ; documenter tout blocage de conversion.
- Statut : DONE ; DOCX exploitable plac? dans `project/source_documents/lot_05/` et pr?paration document?e.

### CODE-SCM-SAT-DOCX-001
- Objectif : impl?menter les satellites SCM DOCX hors liste d?penses.
- Specs ? lire : specs satellites SCM V1.
- Contraintes : ne pas coder la liste d?penses dans ce ticket ; conserver le wording source des trois DOCX.
- Statut : DONE ; g?n?rateurs `DOC-026`, `DOC-027` et `DOC-028` int?gr?s et test?s.

### CODE-SCM-LISTE-DEPENSES-001
- Objectif : impl?menter la liste des d?penses communes SCM.
- Specs ? lire : specs satellites SCM V1 et pr?paration conversion liste d?penses.
- Contraintes : limiter le ticket ? la liste d?penses communes SCM, avec tests cibl?s.
- Statut : DONE ; g?n?rateur liste d?penses communes SCM int?gr? et test?.

### CODE-ACTE-ACTIONS-001
- Objectif : impl?menter l'acte de cession d'actions SPFPL.
- Specs ? lire : specs acte actions V1 et pr?paration source.
- Contraintes : ne pas modifier le wording juridique hors spec.
- Statut : DONE ; g?n?rateur acte de cession d'actions SPFPL int?gr? et test?.

### SPEC-SCM-CESSION-BLOCK-001
- Objectif : sp?cifier le blocage ou le p?rim?tre de la cession SCM.
- Specs ? lire : arbitrages SCM et sources SCM cession disponibles.
- Contraintes : pas de code avant d?cision document?e.
- Statut : DONE ; specs canonique et texte disponibles dans `docs/delivery/`.

### CODE-SCM-CESSION-BLOCK-001
- Objectif : impl?menter le blocage explicite de la cession SCM.
- Specs ? lire : `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md` et `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`.
- Contraintes : ne pas g?n?rer de document cession SCM tant que le blocage V1 s'applique ; tests cibl?s obligatoires.
- Statut : DONE ; blocage explicite cession SCM historique, lev? par `FINAL-SCM-CESSION-WAVE-001` selon r?solution V1.

### REVIEW-BATCH-LOT03-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 03.
- Specs ? lire : specs et arbitrages Lot 03, smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_03_batch_review_v1.md`.

### REVIEW-BATCH-LOT04-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 04.
- Specs ? lire : specs et arbitrages statuts Lot 04, smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_04_batch_review_v1.md`.

### AUDIT-REMAINING-SCOPE-001
- Objectif : auditer le p?rim?tre restant apr?s les vagues SCM, statuts et acte actions.
- Specs ? lire : board, dernier ?tat, registre moteur et specs disponibles.
- Contraintes : audit documentaire, sans code ni d?placement de sources.
- Statut : DONE ; audit disponible dans `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`.

### STYLE-ANALYSE-LOT03-BATCH-001
- Objectif : analyser le style du batch Lot 03 avant harmonisation.
- Specs ? lire : g?n?rateurs Lot 03, specs texte et rendus disponibles.
- Contraintes : analyse de rendu uniquement, sans modification de wording juridique.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.

### STYLE-ANALYSE-STATUTS-BATCH-001
- Objectif : analyser le style du batch statuts avant harmonisation.
- Specs ? lire : specs et g?n?rateurs statuts int?gr?s.
- Contraintes : analyse et cadrage avant modification de rendu.
- Statut : DONE ; blueprint disponible dans `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.

### PREP-SCM-CESSION-SOURCES-001
- Objectif : pr?parer les sources cession SCM.
- Specs ? lire : plan de placement sources et raw dump SCM cession.
- Contraintes : ne pas toucher au raw dump ; documenter tout placement ou blocage.
- Statut : DONE ; sources cession SCM plac?es dans `project/source_documents/lot_05/` et pr?paration document?e.

### FIX-STYLE-LOT03-BATCH-001
- Objectif : corriger les ?carts de style prioritaires du batch Lot 03.
- Specs ? lire : `docs/delivery/render_style_blueprint_lot03_batch_v1.md`.
- Contraintes : limiter les changements au rendu DOCX, sans d?rive de wording juridique.
- Statut : DONE ; rendu Lot 03 harmonis? avec tests cibl?s.

### FIX-STYLE-STATUTS-BATCH-001
- Objectif : corriger les ?carts de style prioritaires du batch statuts.
- Specs ? lire : `docs/delivery/render_style_blueprint_statuts_batch_v1.md`.
- Contraintes : limiter les changements au rendu DOCX, sans d?rive de wording juridique.
- Statut : DONE ; rendu statuts harmonis? avec tests cibl?s.

### REVIEW-BATCH-LOT05-001
- Objectif : documenter la revue juridique/visuelle du batch Lot 05.
- Specs ? lire : specs Lot 05, g?n?rateurs int?gr?s et smoke DOCX disponibles.
- Contraintes : revue uniquement, sans modification de wording juridique.
- Statut : DONE ; revue disponible dans `docs/review/lot_05_batch_review_v1.md`.

### ARBITRAGE-SCM-CESSION-RESOLVE-001
- Objectif : arbitrer la r?solution de la cession SCM apr?s blocage V1 et vague style/revue.
- Specs ? lire : specs cession SCM, sources pr?par?es et revues Lot 05.
- Contraintes : d?cision m?tier avant tout code documentaire de cession SCM.
- Statut : DONE ; arbitrage absorb? dans `main`.

### FINAL-SCM-CESSION-WAVE-001
- Objectif : finaliser le bloc cession SCM V1 et cl?turer la vague moteur documentaire.
- Specs ? lire : r?solution V1 cession SCM, specs canonique/texte, six sources SCM cession et audit moteur.
- Contraintes : DOCX uniquement, sans UI, PDF, ZIP, ni versionnement de `artifacts/`.
- Statut : DONE ; `DOC-031`, `DOC-032` et `DOC-033` sont branch?s, test?s et couverts par smoke DOCX r?el.

### SYNC-CLOSE-AUDIT-001
- Objectif : absorber proprement le commit d'audit moteur `0139202b170531fd628f25811c55855a2512acc0` dans `main`.
- Contraintes : conserver l'audit de cl?ture plus r?cent d?j? pr?sent dans `main`, sans modification de code Python.
- Statut : DONE ; merge de synchronisation effectu?, `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` confirm? pr?sent.

### RECONCILE-MOTOR-CLOSE-001
- Objectif : lever les incoh?rences finales signal?es par `FINAL-MOTOR-AUDIT-002` et cl?turer le moteur DOCX V1.
- Contraintes : correction minimale, aucun wording juridique modifi?, aucun toucher ? `project/source_import/raw_drive_dump/` ni `artifacts/`.
- Statut : DONE ; runtime align? sur 43 documents, audits `16/17/18` et r?f?rentiels `08/09` consolid?s.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 176 tests pass?s.

### PDF-BACKEND-001
- Objectif : ajouter une capacit? locale d'export PDF depuis les DOCX g?n?r?s, sans toucher ? l'UI ni modifier le contenu juridique.
- Contraintes : backend best-effort explicite, erreurs bloquantes si aucun convertisseur fiable n'est disponible, `artifacts/` hors versionnement.
- Statut : DONE ; `src/sydel_doc_engine/rendering/pdf_export.py` expose l'export DOCX vers PDF avec priorit? LibreOffice headless puis fallback Word COM Windows.
- Validation : tests cibl?s OK, smoke r?el DOCX vers PDF OK via Word COM ; validations globales ruff/pytest ? jour.

### UI-FLOW-001
- Objectif : cadrer le flux Streamlit V1 post-moteur sans impl?menter l'UI.
- Sortie : `docs/project/19_UI_FLOW_V1.md`.
- Statut : DONE ; commit source `d62670efe10481926437c0e1a5dabbe349fd5938` absorb? dans `main`.

### UI-OCCURRENCES-001
- Objectif : cadrer les occurrences documentaires n?cessaires ? l'UI V1.
- Sortie : `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`.
- Statut : DONE ; commit source `24a881b999371811d39a2403c0b51d9ae8ce0556` absorb? dans `main`.

### UI-FORM-SCHEMA-001
- Objectif : cadrer le sch?ma formulaire UI V1.
- Sortie : `docs/project/21_UI_FORM_SCHEMA_V1.md`.
- Statut : DONE ; commit source `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1` absorb? dans `main`.

### RECIPE-FRAME-001
- Objectif : cadrer la recette finale V1.
- Sortie : `docs/review/final_recipe_framework_v1.md`.
- Statut : DONE ; commit source `c2fc0db4d51485c7c5e721c5184028ae17c68cb3` absorb? dans `main`.

### SYNC-POST-MOTOR-UI-001
- Objectif : int?grer proprement les fondations UI/PDF/recette dans `main`.
- Entr?es : branches `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001`, `codex/recipe-frame-001`.
- Contraintes : ne pas toucher ? `project/source_import/raw_drive_dump/` ni ? `artifacts/`.
- Statut : DONE ; les cinq commits sources sont absorb?s dans `main` et le pilotage confirme `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` en READY.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 182 tests pass?s.

### UI-CORE-001
- Objectif : impl?menter le c?ur Streamlit V1 ? partir des r?f?rentiels UI absorb?s.
- Pr?requis : `docs/project/19_UI_FLOW_V1.md`, `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`, `docs/project/21_UI_FORM_SCHEMA_V1.md`, orchestrateur moteur clos et backend PDF disponible.
- Statut : DONE par remplacement ; le p?rim?tre est superseded / remplac? par `UI-PDF-ZIP-INTEGRATION-001`, qui livre directement le flux Streamlit dossier avec DOCX, PDF local optionnel et ZIP.

### RESUME-ZIP-BACKEND-001
- Objectif : reprendre le backend ZIP V1 sur `main` synchronis?.
- Pr?requis : moteur DOCX clos, backend PDF int?gr? et fondation phase 18.
- Statut : DONE ; le backend ZIP d?terministe `src/sydel_doc_engine/rendering/zip_bundle.py` est pr?sent, test? et utilis? par le runtime UI.

### REVIEW-FINAL-001
- Objectif : ex?cuter la revue finale V1 apr?s int?gration UI/PDF/ZIP.
- Pr?requis : moteur DOCX clos, UI c?ur, PDF et ZIP int?gr?s.
- Statut : DONE ; rapport d'execution disponible dans `docs/review/review_final_001_execution_report_v1.md`.
- Decision : GO avec reserves pour lancer `UI-BUSINESS-WIZARD-001`.
- Reserves : `git fetch --prune` bloque sur `.git/FETCH_HEAD`, backend PDF local indisponible pendant la revue, la detection Word COM peut accrocher un processus Word, et la majorite des contextes exemples sont des contextes de famille/generateur incomplets pour le flux dossier global.

### UI-PDF-ZIP-INTEGRATION-001
- Objectif : brancher les sorties DOCX, PDF local optionnel et ZIP dossier dans l'UI Streamlit.
- Pr?requis : moteur DOCX clos, backend PDF `rendering/pdf_export.py`, backend ZIP disponible sous `rendering/zip_bundle.py`.
- Statut : DONE ; l'UI charge un contexte YAML/JSON, affiche la s?lection orchestrateur, g?n?re les DOCX, propose les t?l?chargements DOCX, tente les PDF si un backend local est disponible et produit un ZIP d?terministe avec manifeste.
- Limitation : le PDF d?pend de l'environnement local LibreOffice ou Word COM ; un ?chec PDF est affich? sans modifier les DOCX.
- Smoke manuel : `docs/review/ui_pdf_zip_integration_001_smoke.md`.

### SYNC-FINAL-FOUNDATIONS-001
- Objectif : r?aligner `main` avant revue/cl?ture avec les fondations UI, audits, PDF, ZIP et recette finale.
- Entr?es : `codex/ui-flow-001`, `codex/ui-occurrences-001`, `codex/ui-form-schema-001`, `codex/pdf-backend-001`, `codex/recipe-frame-001`, `codex/ui-pdf-zip-integration-001`, `codex/zip-backend-001`, `codex/close-motor-audit-001`, `codex/final-motor-audit-002`, `codex/next-phase-foundation-001`.
- Contraintes : ne pas toucher ? `project/source_import/raw_drive_dump/` ni ? `artifacts/`.
- Statut : DONE ; les fichiers critiques de cadrage/cl?ture sont pr?sents sur `main`, l'UI int?gr?e et les backends PDF/ZIP sont pr?sents, et le pilotage confirme uniquement `REVIEW-FINAL-001` et `CLOSE-PROJECT-V1-001` en READY.
- Validation : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 191 tests pass?s.

### WORKTREE-CLEANUP-AND-UI-STATUS-001
- Objectif : rendre le poste local lisible avec un seul dossier canonique, consolider le contenu restant de `codex/review-final-001` dans `main` et clarifier le statut reel de l'UI.
- Entr?es : worktree `main`, branches locales/distantes, dossier parent `C:\Users\Gad\Desktop\Sydel\`, branche `codex/review-final-001`.
- Contraintes : archiver sans suppression definitive, ne pas toucher a `project/source_import/raw_drive_dump/`, ne pas inventer d'UI wizard non implementee.
- Statut : DONE ; `docs/review/final_review_pack_v1.md` est integre dans `main`, `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md` documente l'etat local et l'UI actuelle est qualifiee comme UI technique de pilotage par contexte, pas UI produit finale.

### CLOSE-PROJECT-V1-001
- Objectif : clore le projet V1 apr?s revue finale.
- Pr?requis : `REVIEW-FINAL-001` termin?.
- Statut : READY.

### UI-BUSINESS-WIZARD-001
- Objectif : lancer le wizard metier dossier-centre a partir des specs UI `19_UI_FLOW_V1.md`, `20_UI_DOCUMENT_OCCURRENCES_V1.md` et `21_UI_FORM_SCHEMA_V1.md`.
- Pr?requis : `REVIEW-FINAL-001` termine, moteur DOCX/ZIP vert, reserves PDF et contextes exemples documentees.
- Statut : DONE.
- Livraison : mode `Assistant metier` ajoute dans Streamlit avec formulaire structure, validation, liste de documents, generation DOCX, ZIP et PDF optionnel ; mode `Technique / diagnostic` YAML/JSON conserve.
- Perimetre V1 : generation assistant limitee au scenario SCI simple pour `DOC-001`, `DOC-002`, `DOC-003` et `DOC-004`.
- Rapport : `docs/review/ui_business_wizard_001_report_v1.md`.
- Garde-fous : ne pas relancer l'ancien `UI-WIZARD-001`, ne pas dupliquer la selection documentaire hors orchestrateur, ne pas presenter la generation comme validation juridique.

### CASE-CATALOG-001
- Objectif : creer la couche metier `catalogue des cas` depuis la source de verite produit, sans modifier l'UI, le moteur DOCX/PDF/ZIP ni les generateurs.
- Source analysee : `project/source_truth/Documents_a_generer_par_cas.docx` ; les chemins `docs/source_truth/*` demandes par le ticket ne sont pas presents dans ce workspace.
- Statut : DONE.
- Livraison : `src/sydel_doc_engine/domain/case_catalog.py` expose `CaseType`, `CaseCondition`, `DocumentOccurrence`, `DocumentAvailability`, `ExpectedDocument` et `get_expected_documents(...)`.
- Couverture courante apr?s `SELARL-PILOT-SOURCE-VERIFY-001` : 8 familles, 46 documents attendus uniques, 104 occurrences source, 43 documents mappes a `DOC-XXX`, 41 documents `GENERATABLE`, 4 documents `MANUAL_ONLY`, 1 document `NOT_IMPLEMENTED`, 0 `NEEDS_MAPPING`.
- Rapport : `docs/review/case_catalog_001_report_v1.md`.
- Prochaine etape realisee : `UI-CASE-WIZARD-002`.

### UI-CASE-WIZARD-002
- Objectif : brancher le mode `Assistant metier` Streamlit sur `get_expected_documents(...)` pour piloter l'affichage documentaire depuis CASE-CATALOG-001.
- Prerequis : `CASE-CATALOG-001`, docs UI 19/20/21, assistant metier existant et mode technique YAML/JSON conserve.
- Statut : DONE.
- Livraison : conditions UI par famille, tableau des documents attendus avec statuts `Generable`, `A remplir manuellement`, `Non implemente`, `Mapping a confirmer`, blocages de champs et contexte incomplet V2.
- Generation : filtree sur les documents attendus, `GENERATABLE`, avec `document_code`, et prets dans le contexte formulaire ; documents manuels/non implementes exclus.
- Rapport : `docs/review/ui_case_wizard_002_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- Prochaine etape recommandee : `UI-CASE-WIZARD-003`, enrichir les blocs formulaire pour rendre generables les documents aujourd'hui marques contexte incomplet V2, par famille ou lot limite.

### SELARL-PILOT-PROTOCOL-001
- Objectif : reprendre le cadrage produit de l'Assistant metier a partir du processus pilote SELARL et de la source V2 fournie par l'associe.
- Source V2 : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, copie du fichier non suivi initial `docs/docssource_truth/Documents ? g?n?rer par cas.docx`.
- Statut : DONE.
- Livraison : `docs/project/PROCESS_BUILD_PROTOCOL_V1.md`, `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md`, `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`, `docs/project/SELARL_IMPLEMENTATION_PLAN_V1.md`.
- Rapport : `docs/review/selarl_pilot_protocol_001_report_v1.md`.
- Decisions historiques : pas de modification UI/moteur/generateurs ; `PV d'autorisation d'emprunt` traite comme branche conditionnelle du `DOC-004` ; wording SELARL ensuite corrig? par `SELARL-PLAN-CORRECTION-001` vers `Fiche Client` / `Praticien`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests passes.
- Prochaine etape recommandee : `SELARL-FORM-SCHEMA-IMPL-001`.

### SELARL-PILOT-SOURCE-VERIFY-001
- Objectif : v?rifier les livrables SELARL contre la vraie source V2 fournie par l'associ?, puis corriger uniquement les ?carts.
- Source V2 v?rifi?e : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Statut : DONE.
- Livraison : `docs/review/selarl_source_verify_001_report_v1.md`, source V2 canonique remplac?e, specs SELARL r?concili?es, `case_catalog.py` align? sur les statuts d?rogation V2.
- D?cisions : `DOC-013` et `DOC-014` restent connus c?t? moteur mais sont `MANUAL_ONLY` dans le catalogue produit ; `DOC-006` garde une r?serve source V2.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 217 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-FORM-SCHEMA-IMPL-001`.

### SELARL-FORM-SCHEMA-IMPL-001
- Objectif : impl?menter le sch?ma de donn?es SELARL c?t? Assistant m?tier, sans refaire l'UI visible et sans modifier les g?n?rateurs ni le moteur DOCX/PDF/ZIP.
- Source V2 utilis?e : `project/source_truth/Documents_a_generer_par_cas_V2.docx`, hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Statut : DONE.
- Livraison : `src/sydel_doc_engine/app/selarl_form_schema.py` expose blocs m?tier, champs qualifi?s, r?gles de r?utilisation, documents attendus SELARL, codes g?n?rables et couverture des variables V2.
- Corrections QA : `DOC-006` porte une r?serve source V2 exploitable dans le catalogue ; le rapport source V2 clarifie que `DOC-013` et `DOC-014` sont finaux `MANUAL_ONLY`.
- Garde-fous : `DOC-013` et `DOC-014` restent visibles mais exclus des codes g?n?rables SELARL ; aucun changement Streamlit, moteur DOCX/PDF/ZIP ou g?n?rateur.
- Rapport : `docs/review/selarl_form_schema_impl_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 231 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-UI-WIZARD-IMPL-001`.

### SELARL-UI-WIZARD-IMPL-001
- Objectif : brancher l'Assistant m?tier visible sur le sch?ma SELARL, sans modifier les g?n?rateurs ni le moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : parcours Streamlit SELARL en ?crans qualification, soci?t?, professionnel/g?rant, associ?s, conditions sp?cifiques, documents attendus et g?n?ration.
- Sch?ma consomm? : conditions, labels, blocs, r?gles de r?utilisation, champs par bloc et documents depuis `selarl_form_schema.py` via `business_wizard.py`.
- Garde-fous : mode SCI existant et mode Technique / diagnostic conserv?s ; `DOC-006` affich? avec r?serve ; `DOC-013` et `DOC-014` visibles mais `MANUAL_ONLY` et exclus de la g?n?ration automatique.
- Rapport : `docs/review/selarl_ui_wizard_impl_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 239 tests pass?s.
- Prochaine ?tape recommand?e corrig?e : `SELARL-WORDING-REALIGN-001`, puis `SELARL-FLOW-REALIGN-001` avant tout smoke r?aliste.

### SELARL-NOTEBOOKLM-RECONCILIATION-001
- Objectif : reprendre le cadrage SELARL avec la hi?rarchie NotebookLM / V3 / templates / code, sans coder ni modifier l'UI ou les g?n?rateurs.
- Statut : DONE.
- Sources ajout?es : `project/source_truth/notebooklm_selarl_10_prompts_v1.md` et `project/source_truth/Documents_a_generer_par_cas_V3.docx`, commit source `f1da08b`.
- Livraison : `docs/project/SELARL_SOURCE_HIERARCHY_V2.md`, `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md`, `docs/project/SELARL_REBUILD_BACKLOG_V2.md`.
- Diagnostic initial : le cadrage documentaire V2/V3 est conservable, mais le wording, l'ordre du formulaire et les r?utilisations doivent ?tre corrig?s avant smoke.
- Garde-fous : aucun fichier Python, g?n?rateur, moteur DOCX/PDF/ZIP ou UI modifi?.
- Tests : non lanc?s ; ticket documentaire Markdown uniquement.
- Prochaine ?tape recommand?e : `SELARL-WORDING-REALIGN-001`.

### SELARL-PLAN-CORRECTION-001
- Objectif : corriger la planification SELARL selon les arbitrages explicites de l'associ?, sans modifier le code applicatif.
- Statut : DONE.
- Arbitrages int?gr?s : `Fiche Client`, `Praticien`, logique `Dossier unipersonnel`, abandon du mode Projet / filigrane V1, pas de couche produit documentaire lourde, mandataire hors priorit?s UX si aucune variable ne l'impose.
- Livraison : hi?rarchie de sources, rapport de r?conciliation et backlog V2 corrig?s.
- Garde-fous : aucun fichier Python, g?n?rateur, moteur DOCX/PDF/ZIP ou UI modifi? ; ne pas pousser ni red?ployer l'UI SELARL existante avant r?alignement produit.
- Tests : non lanc?s ; modifications documentaires uniquement.
- Prochaine ?tape recommand?e : `SELARL-WORDING-REALIGN-001`.

### SELARL-WORDING-REALIGN-001
- Objectif : r?aligner uniquement le vocabulaire visible SELARL sur `Fiche Client`, `Praticien` et les r?les juridiques exacts.
- Statut : DONE.
- Livraison : labels visibles corrig?s dans le sch?ma, Streamlit et specs actives ; rapport `docs/review/selarl_wording_realign_001_report_v1.md`.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, `case_catalog.py`, ordre d'?cran ou r?gle de r?utilisation fonctionnelle modifi?.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 241 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-FLOW-REALIGN-001`.

### SELARL-FLOW-REALIGN-001
- Objectif : r?aligner l'ordre conceptuel SELARL dans le sch?ma et les projections m?tier, sans g?n?rateurs ni moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : `FormStep`, `SELARL_FLOW_STEPS`, projections par ?tape dans `business_wizard.py`, specs actives mises ? jour et rapport `docs/review/selarl_flow_realign_001_report_v1.md`.
- Ordre cible : Qualification, Fiche Client / Praticien, Fiche Soci?t?, Capital & Associ?s, Contexte & sc?narios m?tier, Documents & g?n?ration.
- Garde-fous : `streamlit_app.py` non modifi? ; r?ordonnancement visible complet repouss? ? `SELARL-UI-REALIGN-001` apr?s les r?gles de r?utilisation.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` OK, 41 tests pass?s ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 245 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-REUSE-RULES-REALIGN-001`.

### SELARL-REUSE-RULES-REALIGN-001
- Objectif : r?aligner les r?gles de r?utilisation SELARL, sans g?n?rateurs ni moteur DOCX/PDF/ZIP.
- Statut : DONE.
- Livraison : `Dossier unipersonnel` ajout? comme r?gle pivot dans `selarl_form_schema.py` et projet? dans `business_wizard.py`.
- R?gles : Praticien = associ? unique = g?rant = signataire seulement si `Dossier unipersonnel` est actif ; SELARL acqu?reur, SELARL cessionnaire SCM et domiciliation = si?ge restent des options explicites ; mandataire / signataire n'est pas un d?faut.
- Relations non automatiques : vendeur / locataire, si?ge / lieu d'exercice / cabinet, vendeur / Praticien et c?dant SCM / Praticien.
- Garde-fous : `streamlit_app.py` non modifi? ; documents attendus SELARL inchang?s ; `DOC-013` et `DOC-014` restent exclus de la g?n?ration ; `DOC-006` conserve sa r?serve.
- Rapport : `docs/review/selarl_reuse_rules_realign_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_selarl_form_schema.py tests/unit/test_business_wizard.py` OK, 48 tests pass?s ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 252 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-UI-REALIGN-001`.

### SELARL-UI-REALIGN-001
- Objectif : r?aligner le parcours Streamlit visible SELARL sur le wording, le flow et les r?gles de r?utilisation corrig?s.
- Statut : DONE.
- Livraison : titres d'?crans d?riv?s du flow m?tier, Fiche Client avant Fiche Soci?t?, `Dossier unipersonnel` en qualification, ?cran 6 unique Documents & g?n?ration.
- Consommation sch?ma/projections : `selarl_ui_visible_screen_title(...)`, `selarl_ui_visible_fields_by_step(...)`, `selarl_ui_reuse_projection(...)`, `selarl_ui_reuse_rules()` et `selarl_ui_document_specs()`.
- Mandataire : d?plac? dans un expander secondaire repli? ; aucune assimilation au signataire par d?faut.
- Garde-fous : g?n?rateurs, moteur DOCX/PDF/ZIP, `case_catalog.py`, parcours SCI et mode `Technique / diagnostic` non modifi?s ; aucun mode Projet ni filigrane ajout?.
- Rapport : `docs/review/selarl_ui_realign_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py` OK, 34 tests pass?s ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-SMOKE-REALISTIC-001`.

### SELARL-SMOKE-REALISTIC-001
- Objectif : smoke tester le parcours SELARL r?align? avec trois dossiers r?alistes, sans g?n?rateurs ni moteur DOCX/PDF/ZIP modifi?s.
- Statut : DONE.
- Sc?narios ex?cut?s : m?decin unipersonnelle simple ; chirurgien-dentiste avec r?gime communautaire, site distinct et d?rogation ; m?decin avec cession de cabinet m?dical, bail et financement.
- R?sultat g?n?ration : chaque sc?nario g?n?re uniquement `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004` et un ZIP avec manifeste.
- Documents visibles non g?n?r?s : `DOC-034`, statuts SELARL `DOC-016` / `DOC-017`, r?gime communautaire `DOC-005` / `DOC-006`, bail/cession `DOC-007` ? `DOC-010` restent en contexte incomplet V2 selon sc?nario.
- Documents manuels : `DOC-013`, `DOC-014` et les formulaires sans code li?s ? la d?rogation/site distinct restent visibles et exclus de g?n?ration.
- Contr?les : `DOC-006` conserve sa r?serve, aucun document manuel n'entre dans les ZIP, le PV d'autorisation d'emprunt reste une option de `DOC-004`, `Dossier unipersonnel` produit les verrouillages attendus.
- Artefacts : `artifacts/selarl_smoke_realistic_001/20260519_185045/`.
- Rapport : `docs/review/selarl_smoke_realistic_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 257 tests pass?s.
- Prochaine ?tape recommand?e : `SELARL-JURIST-REVIEW-001`.

### SELARL-CLOUD-GENERATION-BUG-001
- Objectif : diagnostiquer le blocage utilisateur o? le parcours SELARL visible ne permettait pas de g?n?rer, malgr? le smoke local.
- Statut : DONE.
- Cause racine : ?tat Streamlit de widgets d?riv?s d?sactiv?s conserv? ? vide lorsque `Dossier unipersonnel` ou la domiciliation par si?ge ?tait coch? avant la saisie des champs source.
- Correction : synchronisation explicite du `session_state` pour l'associ? unique d?riv? et l'adresse de domiciliation d?riv?e dans `streamlit_app.py`.
- Garde-fous : g?n?rateurs, moteur DOCX/PDF/ZIP, `case_catalog.py`, SCI et `Technique / diagnostic` non modifi?s.
- Rapport : `docs/review/selarl_cloud_generation_bug_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py -q` OK, 35 tests pass?s ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 266 tests pass?s.
- Prochaine ?tape recommand?e : r?tablir les permissions Git locales, cr?er le commit de correction, push manuel puis red?ploiement Streamlit Cloud et retest utilisateur SELARL.

### DOCUMENT-UNITAIRE-001
- Objectif : ajouter un mode Streamlit `Document unitaire` pour tester un seul document sans saisir tout un dossier.
- Statut : DONE.
- Impl?mentation : nouveau module UI pur `single_document_mode.py`, branchement dans `streamlit_app.py`, s?lection par code/libell? et g?n?ration d'un DOCX unique via les services existants.
- P?rim?tre V1 : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`; documents manuels affich?s mais non g?n?r?s ; documents hors p?rim?tre marqu?s comme pas encore support?s dans ce mode.
- Garde-fous : g?n?rateurs, moteur DOCX/PDF/ZIP, catalogue m?tier, Assistant m?tier et mode `Technique / diagnostic` conserv?s.
- Rapport : `docs/review/document_unitaire_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 266 tests pass?s.
- Prochaine ?tape recommand?e : revue utilisateur sur les quatre documents support?s, puis extension incr?mentale document par document si les champs sont couverts.

### ASSISTANT-METIER-PREFILL-001
- Objectif : ajouter un pr?remplissage de test d?terministe dans le seul mode `Assistant metier`.
- Statut : DONE.
- Impl?mentation : module d?di? `src/sydel_doc_engine/app/test_prefill_presets.py`, s?lecteur `Sc?nario de test`, boutons `Pr?remplir` et `R?initialiser`, indication visible des donn?es fictives charg?es.
- Sc?narios : `SELARL m?decin unipersonnelle simple`, `SELARL chirurgien-dentiste + r?gime communautaire + site distinct`, `SELARL m?decin + cession cabinet m?dical + bail + financement`, `SCI simple`.
- Garde-fous : g?n?rateurs, moteur DOCX/PDF/ZIP, wording juridique, mode `Technique / diagnostic` et mode `Document unitaire` non modifi?s.
- Rapport : `docs/review/assistant_metier_prefill_001_report_v1.md`.
- Tests : `.\.venv\Scripts\python.exe -m pytest tests\unit\test_business_wizard.py -q` OK, 41 tests pass?s ; `.\.venv\Scripts\python.exe -m pytest tests\unit\test_single_document_mode.py tests\unit\test_ui_runtime.py -q` OK, 12 tests pass?s ; `.\.venv\Scripts\python.exe -m ruff check .` OK ; `.\.venv\Scripts\python.exe -m pytest` OK, 272 tests pass?s.
- Prochaine ?tape recommand?e : revue manuelle Streamlit des quatre sc?narios de test, puis `SELARL-JURIST-REVIEW-001`.

### GLOBAL-VARIABLE-INVENTORY-001
- Objectif : construire un inventaire global brut des variables documentaires sur tout le p?rim?tre moteur, sans d?cider les fusions.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` et `docs/review/global_variable_inventory_001_report_v1.md`.
- Couverture : 12 443 lignes de variables brutes, 1 334 slugs normalis?s distincts sur documents `DOC-XXX`, 43 documents `DOC-001` ? `DOC-043` couverts, 15 familles couvertes.
- Sources : dictionnaire canonique V1, mapping documents/variables V1, arbre moteur, registre `catalog.py`, source truth V1/V2/V3, templates `project/source_documents/`, specs `docs/delivery/`, `case_catalog.py` en aide uniquement.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifi? ; les groupes suspects sont signal?s sans fusion canonique d?finitive.
- Validations : contr?le CSV/report, absence de lignes `UNMAPPED`, couverture compl?te `DOC-001` ? `DOC-043`; aucun test Python requis car aucun fichier Python modifi?.
- Prochaine ?tape r?alis?e : `GLOBAL-VARIABLE-IDENTITY-AUDIT-001`, audit d'identit? s?mantique et registre canonique global V2.

### GLOBAL-VARIABLE-IDENTITY-AUDIT-001
- Objectif : auditer l'identit? s?mantique globale des variables de tous les documents afin de minimiser le futur front sans fusionner des informations distinctes.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2.md`, `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md` et `docs/review/global_variable_identity_audit_001_report_v1.md`.
- Couverture : 1 334 slugs normalis?s distincts audit?s, 43 documents `DOC-001` ? `DOC-043`, 15 familles, 49 champs canoniques V2 propos?s, 142 rapprochements repr?sentatifs, 10 questions humaines group?es.
- D?cision : pas de fusion silencieuse ; les relations sont class?es en `SAME_FIELD`, `SAME_DATA_DIFFERENT_SHAPE`, `EXPLICIT_REUSE_ONLY`, `DISTINCT_FIELDS` ou `UNCERTAIN_REQUIRES_HUMAN_DECISION`.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifi? ; aucun test Python requis car aucun fichier Python modifi?.
- Prochaine ?tape r?alis?e : `GLOBAL-HUMAN-ANSWERS-INTEGRATION-001`, int?grer les r?ponses humaines disponibles puis geler un registre V2.1 avant architecture front.

### GLOBAL-HUMAN-ANSWERS-INTEGRATION-001
- Objectif : int?grer les r?ponses humaines d?j? obtenues dans l'audit global des variables et figer une version V2.1 du registre canonique global.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`, `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` et `docs/review/global_human_answers_integration_001_report_v1.md`.
- D?cisions : 4 questions V1 ferm?es, 5 questions restant arbitrables en interne, 1 question bascul?e en backlog documentaire ; r?gles V2.1 sur r?les, adresses, parties de cession, SCM, bail et cas futur SELAS micro-holding.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, UI ou wording juridique modifi? ; contradiction filigrane PROJET document?e mais non impl?ment?e.
- Validation : relecture documentaire et contr?le du diff ; aucun test Python requis car aucun fichier Python modifi?.
- Prochaine ?tape recommand?e : `GLOBAL-FRONT-ARCHITECTURE-001`, concevoir l'architecture du nouveau front global sur le registre V2.1.

### GLOBAL-FRONT-ARCHITECTURE-001
- Objectif : concevoir l'architecture produit et donn?es du nouveau front global sur le registre canonique global V2.1.
- Statut : DONE.
- Livrables : `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`, `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`, `docs/project/GLOBAL_FRONT_RULES_V1.md`, `docs/project/GLOBAL_FRONT_SCREEN_STRATEGY_V1.md`, `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md` et `docs/review/global_front_architecture_001_report_v1.md`.
- D?cisions : mod?le front par objets m?tier role-based, adresses typ?es par usage, reutilisation uniquement via r?gles explicites, distinction dossier / document / lot, mode document unitaire s?par? du parcours dossier complet.
- Prototype : conserver les concepts utiles et le diagnostic technique ; ne pas g?n?raliser les ?crans, le `session_state` ou les listes de champs du prototype actuel.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, Streamlit ou wording juridique modifi? ; `docs/docssource_truth/` non suivi laiss? hors p?rim?tre.
- Validation : relecture documentaire et contr?le du diff ; aucun test Python requis car aucun fichier Python modifi?.
- Prochaine ?tape recommand?e : `FRONT-DATA-LAYER-001`, cr?er la couche de donn?es front globale sans toucher au moteur ni au prototype.

### GLOBAL-FRONT-ARCHITECTURE-QA-001
- Objectif : v?rifier l'architecture front globale V1 sur des documents sentinelles repr?sentatifs du moteur.
- Statut : DONE.
- Sentinelles contr?l?es : `DOC-002`, `DOC-034`, `DOC-017`, `DOC-033`, `DOC-009`, `DOC-041` et `DOC-025`.
- Livrables : `docs/review/global_front_architecture_qa_001_report_v1.md` et `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`.
- Verdict : architecture globalement ORANGE ma?trisable ; `DOC-002` et `DOC-033` verts, cinq sentinelles orange, aucun rouge.
- Garde-fous : aucun g?n?rateur, moteur DOCX/PDF/ZIP, Streamlit, UI ou wording juridique modifi? ; `docs/docssource_truth/` non suivi laiss? hors p?rim?tre.
- Validation : relecture documentaire et contr?le du diff ; aucun test Python requis car aucun fichier Python modifi?.
- Prochaine ?tape recommand?e : `FRONT-DATA-LAYER-001`, en int?grant les sentinelles orange comme crit?res de couverture data.

### FRONT-STATE-AUDIT-001
- Objectif : auditer l'etat reel du projet et du nouveau front apres retour utilisateur sur la limitation a quatre documents et le blocage de generation.
- Statut : DONE.
- Livrable : `docs/review/front_state_audit_001_report_v1.md`.
- Constat : le moteur reste disponible sur 43 documents moteurs, mais la surface normale du nouveau front est volontairement limitee au pilote `SELARL creation simple` et a `DOC-001` a `DOC-004`.
- Cause UX identifiee : la readiness data-layer peut annoncer quatre documents generables tandis que l'adaptateur moteur bloque ensuite sur un format de date, une adresse ou une ville RCS, sans exposer le detail dans la vue normale.
- Validation : tests cibles `test_front_generation_actions.py` et `test_front_dossier_data_entry.py` OK ; diagnostic lecture seule des blocages runtime OK.
- Prochaine ?tape recommandee : `FRONT-GENERATION-READINESS-UX-001`, avant toute extension du perimetre SELARL.

### FRONT-REALITY-CHECK-001
- Objectif : auditer l'ecart entre les debriefs recents du nouveau front et le code reel visible / branche.
- Statut : DONE.
- Livrables : `docs/review/front_reality_check_001_report_v1.md` et `docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`.
- Constat : le hard cut est reel sur la vue normale (3 titres, 0 table, 0 radio), mais la surface reste chargee par les expanders ouverts, 22 champs, la sidebar `Outils internes`, le bouton PDF visible quand le backend est indisponible et les blocages runtime non expliques.
- Generation reelle : DOCX et ZIP branches pour `DOC-001` a `DOC-004`; PDF branche en code mais indisponible localement (`is_pdf_export_available() == False`).
- Decision de pilotage : ne pas ajouter de panneau documents visible avant une coupe UX minimale ; absorber les explications de readiness dans un ticket unique de surface minimale.
- Validation : audit code + inventaire AppTest de la vue normale + controle PDF local ; aucun fichier Python modifie, donc pas de ruff/pytest requis.
- Prochaine ?tape recommandee : `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

### FRONT-MINIMAL-SURFACE-CLEANUP-001
- Objectif : appliquer la surface utilisateur minimale avant tout push, redeploiement ou test utilisateur.
- Statut : DONE.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique ; ne pas etendre le perimetre documentaire.
- Livrables : coupe UI dans `src/sydel_doc_engine/app/streamlit_app.py`, tests AppTest adaptes, rapport `docs/review/front_minimal_surface_cleanup_001_report_v1.md`.
- Sortie realisee : page normale limitee a `Type de dossier`, `Donnees a saisir`, `Generation`; 0 radio, 0 table, 0 expander ; debug interne cache hors session utilisateur ; PDF cache si backend indisponible ; blocages data-layer/runtime visibles dans `Generation`.
- Validation : tests cibles front OK, 79 tests passes ; `ruff check .` OK ; `pytest` OK, 382 tests passes.
- Prochaine ?tape ensuite : test utilisateur local du pilote `SELARL creation simple`.

### SELARL-COMPLETE-CASE-PLAYBOOK-001
- Objectif : transformer le retour utilisateur "SELARL seulement quatre documents / encore test" en cadrage executable pour une SELARL complete.
- Statut : DONE.
- Contraintes : aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie ; pas de push ni redeploiement.
- Livrables : `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` et `docs/review/selarl_complete_case_playbook_001_report_v1.md`.
- Constat : le moteur sait deja generer les familles SELARL principales, mais le nouveau front global reste explicitement limite a `DOC-001` a `DOC-004` via `FRONT_GENERATION_SUPPORTED_DOC_CODES`, `UNIT_DOCUMENT_V1_SUPPORTED_CODES` et `BUSINESS_WIZARD_CONTEXT_READY_DOCUMENT_IDS`.
- Decision : la cible SELARL complete passe par un adaptateur contexte/readiness front, pas par une modification immediate des generateurs.
- Validation : documentation et pilotage uniquement ; aucun test Python requis.
- Prochaine ?tape recommandee : `SELARL-COMPLETE-CONTEXT-ADAPTER-001`.

### SELARL-COMPLETE-CONTEXT-ADAPTER-001
- Objectif : brancher cote nouveau front une selection documentaire SELARL conditionnelle et un `DocumentGenerationContext` complet pour les documents deja autorises par la source et disponibles cote moteur.
- Statut : DONE.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP ou le wording juridique ; conserver `DOC-013`, `DOC-014` et les documents sans code en manuel ; garder `DOC-006` en reserve explicite.
- Livrables : `src/sydel_doc_engine/app/front_selarl_complete.py`, extension de `front_dossier_entry.py`, `front_generation_actions.py`, `streamlit_app.py`, tests unitaires front et rapport `docs/review/selarl_complete_context_adapter_001_report_v1.md`.
- Sortie realisee : la SELARL medecin simple genere maintenant `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034` et `DOC-017` depuis le nouveau front ; la profession chirurgien-dentiste bascule vers `DOC-016` ; le regime communautaire ajoute `DOC-005` en cible et conserve `DOC-006` en reserve exclue.
- Limite volontaire : cession medicale/dentaire et cession SCM sont selectionnees depuis le catalogue, mais restent `context_incomplete` tant que les sous-formulaires metier detailles ne sont pas branches.
- Validation : `ruff check .` OK ; tests cibles `test_front_generation_actions.py` + `test_front_dossier_data_entry.py` OK, 23 tests passes ; smoke DOCX dentiste et regime communautaire OK ; `pytest` complet tente mais non conclusif a cause de `PermissionError` Windows sur les dossiers temporaires `tmp_path`/`basetemp`.
- Prochaine etape recommandee : `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`.

### SELARL-COMPLETE-COMPLEX-SUBFORMS-001
- Objectif : brancher les sous-formulaires et l'adaptateur contexte pour les scenarios cession medicale/dentaire, bail/appel de fonds et cession SCM.
- Statut : READY.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique ; ne pas exposer de nouveau panneau de diagnostic en surface principale.
- Sorties attendues : champs metier detailles, contexte moteur complet pour `DOC-007` a `DOC-012` et `DOC-031` a `DOC-033`, readiness actionnable, tests par scenario et smoke DOCX/ZIP.
- Prochaine etape ensuite : `SELARL-COMPLETE-SMOKE-001`.

### FRONT-GENERATION-READINESS-UX-001
- Objectif : rendre les blocages de generation visibles et actionnables dans la vue normale du nouveau front.
- Statut : BLOCKED.
- Contraintes : ne pas modifier les generateurs, le moteur DOCX/PDF/ZIP, la source de verite ou le wording juridique.
- Sortie attendue : a absorber dans `FRONT-MINIMAL-SURFACE-CLEANUP-001` pour eviter un ticket qui ajoute de la surface avant la coupe UX.
- Prochaine ?tape ensuite : reassessment apres le test utilisateur local minimal.

### UI-001
- Objectif : exposer une Streamlit simple pour g?n?rer le Lot 1.
- Statut : en attente explicite ; ne pas lancer sans ticket explicite d?di?.
- Pr?requis : orchestrateur Lot 1 fonctionnel et spec canonique `PV nomination g?rant` valid?e.
- Sortie attendue : ?cran simple, g?n?ration testable manuellement, aucun m?tier cach? dans l'UI.

## R?gle de mise ? jour
Chaque ticket termin? doit mettre ? jour ce fichier :
- passer son statut ? DONE
- d?placer le ticket actif en IN_PROGRESS pendant l'ex?cution si la t?che dure plus qu'une modification courte
- indiquer le prochain ticket ? lancer
- indiquer les ?ventuels points ouverts
- mettre ? jour `docs/project/04_LAST_STATE.md`

## Prochaine ?tape pr?vue
- `SELARL-COMPLETE-CONTEXT-ADAPTER-001` est DONE ; le nouveau front n'est plus limite a quatre documents : medecin simple cible et genere `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017`, dentiste bascule vers `DOC-016`, regime communautaire ajoute `DOC-005` et conserve `DOC-006` en reserve.
- Prochaine etape recommandee : `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`, pour transformer les scenarios cession medicale/dentaire et SCM encore `context_incomplete` en generation utilisable quand les donnees sont completes.
- `SELARL-COMPLETE-CASE-PLAYBOOK-001` est DONE ; la SELARL complete est cadree comme une extension front/adaptateur/readiness, avec matrice documentaire et mode d'emploi reproductible pour les autres cas.
- `FRONT-MINIMAL-SURFACE-CLEANUP-001` est DONE ; la surface normale est maintenant limitee a `Type de dossier`, `Donnees a saisir`, `Generation`, sans outil interne visible, sans radio, sans table et sans expander.
- Prochaine etape recommandee : test utilisateur local du pilote `SELARL creation simple`, avant tout ajout de panneau ou extension documentaire.
- `FRONT-REALITY-CHECK-001` est DONE ; l'audit confirme que la vue normale etait reduite techniquement a trois zones, mais encore trop chargee dans la saisie et trop muette sur les blocages runtime.
- `FRONT-STATE-AUDIT-001` est DONE ; l'audit confirme que le moteur est plus avance que le front visible, que le nouveau front est volontairement limite a `SELARL creation simple` / `DOC-001` a `DOC-004`, et que les blocages runtime de date/adresse/ville RCS ne sont pas assez visibles dans la vue normale.
- `FRONT-GENERATION-READINESS-UX-001` reste a reassesser apres test utilisateur ; `FRONT-DOCUMENTS-PANEL-001` reste suspendu comme panneau visible tant que le besoin n'est pas confirme.
- `FRONT-REVIEW-001` est DONE ; le prototype actuel est confirme comme bac a sable / outil de diagnostic, la carte de migration V1 est creee et le backlog pointe maintenant vers les tickets UI visibles.
- Jalon front revise apres `FRONT-MINIMAL-SURFACE-CLEANUP-001` : ne pas ajouter `FRONT-DOCUMENTS-PANEL-001` en surface visible avant test utilisateur local.
- `GLOBAL-FRONT-ARCHITECTURE-QA-001` est DONE ; l'architecture front globale a ete controlee sur 7 documents sentinelles, avec 2 verts, 5 oranges et aucun rouge.
- `GLOBAL-FRONT-ARCHITECTURE-001` est DONE ; l'architecture produit et donn?es du nouveau front global est cadr?e sans toucher au moteur, aux g?n?rateurs, ? Streamlit ni au wording juridique.
- `GLOBAL-HUMAN-ANSWERS-INTEGRATION-001` est DONE ; les r?ponses humaines disponibles sont int?gr?es dans les questions V2, le registre canonique global V2.1 et le rapport ex?cutif, sans toucher au moteur ni ? l'UI.
- `WORKTREE-CLEANUP-AND-UI-STATUS-001` est DONE ; le pack `REVIEW-FINAL-001` est consolide dans `main`, le rapport 23 clarifie le dossier canonique et le statut UI, et les anciens worktrees locaux sont a considerer comme archives.
- `SYNC-FINAL-FOUNDATIONS-001` est DONE ; `main` contient les audits 16/17/18, les cadrages UI 19/20/21, le framework de recette finale, l'UI int?gr?e, le backend PDF et le backend ZIP d?terministe.
- `UI-PDF-ZIP-INTEGRATION-001` est DONE ; l'UI sait produire et telecharger DOCX, PDF local optionnel et ZIP dossier.
- `UI-CORE-001` est superseded / remplac? par `UI-PDF-ZIP-INTEGRATION-001`.
- `RESUME-ZIP-BACKEND-001` est DONE ; `rendering/zip_bundle.py` est int?gr? et test?.
- `SYNC-POST-MOTOR-UI-001` est DONE ; les fondations UI/PDF/recette sont absorb?es dans `main`.
- `REVIEW-FINAL-001` est DONE ; rapport d'execution disponible dans `docs/review/review_final_001_execution_report_v1.md`.
- `UI-BUSINESS-WIZARD-001` est DONE ; l'UI Streamlit dispose maintenant d'un mode assistant metier SCI V1 et conserve le mode technique YAML/JSON.
- `CASE-CATALOG-001` est DONE ; le catalogue metier par cas couvre 46 documents attendus, dont 43 mappes au registre moteur et 3 non generables.
- `UI-CASE-WIZARD-002` est DONE ; l'assistant metier utilise maintenant `get_expected_documents(...)` pour afficher les documents attendus et exclut les documents manuels/non implementes de la generation.
- `SELARL-PILOT-PROTOCOL-001` est DONE ; le pilote SELARL dispose d'un protocole r?plicable, d'une spec processus, d'une spec formulaire, d'une spec wizard et d'un plan d'impl?mentation.
- `SELARL-PILOT-SOURCE-VERIFY-001` est DONE ; la vraie V2 est au chemin canonique, les d?rogations SELARL sont r?concili?es en manuel et les variables V2 brutes sont reprises dans les specs.
- `SELARL-FORM-SCHEMA-IMPL-001` est DONE ; le sch?ma machine-readable SELARL existe, `DOC-006` porte une r?serve V2 exploitable, `DOC-013` / `DOC-014` restent manuels et la couverture des variables V2 est test?e.
- `SELARL-UI-WIZARD-IMPL-001` est DONE techniquement ; l'Assistant m?tier expose le parcours SELARL pilote depuis le sch?ma, conserve SCI et Technique / diagnostic, et garde `DOC-013` / `DOC-014` hors g?n?ration, mais il n'est pas encore valid? produit.
- `SELARL-PLAN-CORRECTION-001` est DONE ; les arbitrages associ? priment d?sormais sur NotebookLM pour `Fiche Client`, `Praticien`, `Dossier unipersonnel`, l'absence de mode Projet / filigrane V1 et l'absence de couche statut produit lourde.
- `SELARL-FLOW-REALIGN-001` est DONE ; le sch?ma et les projections m?tier expriment Qualification, Fiche Client / Praticien, Fiche Soci?t?, Capital & Associ?s, Contexte & sc?narios m?tier, Documents & g?n?ration.
- `SELARL-REUSE-RULES-REALIGN-001` est DONE ; `Dossier unipersonnel` pilote les liens Praticien / associ? unique / g?rant / signataire, les autres r?utilisations restent opt-in et les relations sensibles sont non automatiques.
- `SELARL-UI-REALIGN-001` est DONE ; le parcours Streamlit visible SELARL suit les six ?crans m?tier et consomme le sch?ma/projections corrig?s.
- tickets READY confirm?s : `CLOSE-PROJECT-V1-001`, `SELARL-JURIST-REVIEW-001`.
- ticket SELARL smoke pr?c?dent bloqu? : `SELARL-DOCS-GENERATION-SMOKE-001`, remplac? par la s?quence `WORDING -> FLOW -> REUSE -> UI -> SMOKE -> JURIST`.
- prochain ticket recommand? : `SELARL-JURIST-REVIEW-001`, revue associ? / juriste du parcours SELARL avant extension ou g?n?ralisation.
- ne pas pousser ni red?ployer l'UI SELARL actuelle sans d?cision explicite apr?s smoke et revue.
- moteur documentaire DOCX V1 feature complete et clos apr?s `RECONCILE-MOTOR-CLOSE-001`.
- tickets absorb?s par `SYNC-POST-MOTOR-UI-001` : `UI-FLOW-001`, `UI-OCCURRENCES-001`, `UI-FORM-SCHEMA-001`, `PDF-BACKEND-001` et `RECIPE-FRAME-001`.
- `RECONCILE-MOTOR-CLOSE-001` est DONE ; les g?n?rateurs ordre/SPFPL orphelins sont expos?s sous `DOC-034` ? `DOC-043`, `08/09/16/17/18` sont align?s et les r?f?rences delivery Lot 2 manquantes sont pr?sentes sur `main`.
- `PDF-BACKEND-001` est DONE ; le backend PDF est int?gr? ? la fondation absorb?e, sans ticket PDF suppl?mentaire confirm? dans cette synchronisation.
- `FINAL-SCM-CESSION-WAVE-001` est DONE ; `DOC-031`, `DOC-032` et `DOC-033` cession SCM sont branch?s au catalogue/orchestrateur et couverts par tests/smoke.
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` conclut la cl?ture moteur V1 et liste les exclusions restantes.
- `SYNC-CLOSE-AUDIT-001` est DONE ; le commit source `0139202b170531fd628f25811c55855a2512acc0` a ?t? absorb? via merge de synchronisation en conservant la version finale plus r?cente de l'audit.
- tickets absorb?s par SYNC-WAVE-010 : `ARBITRAGE-SCM-CESSION-RESOLVE-001` et `CODE-SCM-CESSION-BLOCK-001`.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE.
- `CODE-SCM-CESSION-BLOCK-001` est DONE.
- tickets absorb?s par SYNC-WAVE-009 : `CODE-SCM-LISTE-DEPENSES-001`, `SPEC-DEROG-SALARIEE-MANUAL-001`, `REVIEW-BATCH-LOT05-001`, `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001`.
- tickets absorb?s par SYNC-WAVE-008 : `CODE-ACTE-ACTIONS-001`, `PREP-SCM-CESSION-SOURCES-001`, `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001`, `AUDIT-REMAINING-SCOPE-001`, `STYLE-ANALYSE-LOT03-BATCH-001`, `STYLE-ANALYSE-STATUTS-BATCH-001` et `SPEC-SCM-CESSION-BLOCK-001`.
- tickets absorb?s par SYNC-WAVE-007 : `CODE-STATUTS-SCM-001`, `PREP-SCM-LISTE-DEPENSES-CONVERT-001`, `CODE-SCM-SAT-DOCX-001` et `SPEC-ACTE-ACTIONS-001`.
- tickets absorb?s par SYNC-WAVE-006 : `RESUME-FIX-STYLE-LETTERS-001`, `CODE-STATUTS-CIVILS-CORE-001`, `CODE-SAS-SATELLITES-001`, `CONVERT-DEROG-SALARIEE-001`, `CONVERT-ACTE-ACTIONS-001` et `SPEC-SCM-SATELLITES-001`.
- `CODE-SCM-LISTE-DEPENSES-001` est DONE ; `DOC-030` liste des d?penses communes SCM est branch? au catalogue/orchestrateur.
- `SPEC-DEROG-SALARIEE-MANUAL-001` est DONE ; la strat?gie V1 reste manuelle/faute de source DOCX exploitable.
- `REVIEW-BATCH-LOT05-001` est DONE ; la revue Lot 05 est document?e.
- `FIX-STYLE-STATUTS-BATCH-001` et `FIX-STYLE-LOT03-BATCH-001` sont DONE ; les corrections portent sur le rendu DOCX sans d?rive volontaire de wording juridique.
- `CODE-ACTE-ACTIONS-001` est DONE ; l'acte de cession d'actions SPFPL est int?gr? au catalogue/orchestrateur.
- `PREP-SCM-CESSION-SOURCES-001` est DONE ; les sources cession SCM exploitables sont plac?es dans `project/source_documents/lot_05/`.
- `SPEC-SCM-CESSION-BLOCK-001` est DONE ; les specs de blocage cession SCM V1 sont disponibles dans `docs/delivery/`.
- `ARBITRAGE-SCM-CESSION-RESOLVE-001` est DONE ; la r?solution V1 cession SCM est disponible dans `docs/delivery/`.
- `STYLE-ANALYSE-LOT03-BATCH-001` et `STYLE-ANALYSE-STATUTS-BATCH-001` sont DONE ; les blueprints style d?di?s sont disponibles dans `docs/delivery/`.
- `REVIEW-BATCH-LOT03-001`, `REVIEW-BATCH-LOT04-001` et `AUDIT-REMAINING-SCOPE-001` sont DONE.
- `CODE-STATUTS-SCM-001` est DONE ; les statuts SCM sont branch?s sous `DOC-025`.
- `CODE-SCM-SAT-DOCX-001` est DONE ; les satellites SCM DOCX sont branch?s sous `DOC-026`, `DOC-027` et `DOC-028`.
- `PREP-SCM-LISTE-DEPENSES-CONVERT-001` est DONE ; le DOCX exploitable est plac? dans `project/source_documents/lot_05/`.
- `SPEC-ACTE-ACTIONS-001` est DONE ; les specs acte actions V1 sont disponibles dans `docs/delivery/`.
- `CONVERT-ACTE-ACTIONS-001` est DONE ; le DOCX exploitable est plac? dans `project/source_documents/lot_05/`.
- `CONVERT-DEROG-SALARIEE-001` est DONE ; la source salariee reste non convertie et `cumul_salariee` demeure bloque faute de DOCX propre.
- `CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` sont DONE et absorb?s dans `main`.
- `RESUME-FIX-STYLE-LETTERS-001` est DONE et absorb? dans `main`.
- `FIX-STYLE-LETTERS-001` est DONE et absorb? dans `main`.
- `CODE-STATUTS-SEL-001` est DONE et absorb? dans `main`.
- `CODE-STATUTS-CIVILS-CORE-001` est DONE pour SCS, SCI et SCI IRIS.
- `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` sont DONE et absorb?s dans `main`.
- `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` sont DONE et absorb?s dans `main`.
- `CODE-BAIL-APP-001` est DONE et absorb? dans `main`.
- `PREP-DEROG-001` est DONE et absorb? dans `main`.
- `CODE-SPFPL-AGR-INFO-001` est DONE et absorb? dans `main`.
- `CODE-CESSION-CAB-001` est DONE et absorb? dans `main`.
- `CODE-DEROG-CORE-001` est DONE et absorb? dans `main`.
- `PREP-STATUTS-001` est DONE et absorb? dans `main`.
- `CODE-SPFPL-CORE-001` est DONE et absorb? dans `main`.
- `SPEC-STATUTS-SAS-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-SEL-001` et `SPEC-STATUTS-CIVILS-001` sont DONE et absorb?s dans `main`.
- revue humaine toujours recommand?e : smoke DOCX `r?gime communautaire`, notamment le rendu SELARL de la renonciation canonique.
- les autres cas MEDIUM/LOW restent bloqu?s tant que leurs variantes sources n'ont pas ?t? compar?es.
- UI-001 reste explicitement en attente.

## Points ouverts
- Aucun point bloquant moteur DOCX identifi? apr?s `RECONCILE-MOTOR-CLOSE-001`.
- Restent hors p?rim?tre moteur : UI, ZIP, recette finale, revue humaine juridique/visuelle, documents explicitement manuels et sources legacy non converties.
- PDF-BACKEND-001 est termin? : le backend local `rendering/pdf_export.py` produit un PDF depuis un DOCX g?n?r? via Word COM, avec LibreOffice headless prioritaire si disponible.
- Points ouverts PDF apr?s PDF-BACKEND-001 : LibreOffice n'est pas install? localement, l'int?gration batch/orchestrateur reste hors ticket, et le succ?s technique PDF ne vaut pas validation visuelle ou juridique.
- Aucun point bloquant identifi? apr?s le smoke test r?el Lot 1.
- Les trois DOCX sont bien produits par l'orchestrateur dans `artifacts/lot_01_smoke_test/`, mais le rendu visuel et le wording juridique restent ? relire humainement dans les fichiers g?n?r?s.
- PDF et ZIP restent hors ORCH-001 et devront ?tre trait?s dans un ticket d?di?.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'? refactor d?di?.
- ORCH-L2-PV-001 est termin? ; le PV nomination g?rant est branch? dans l'orchestrateur pour les structures concern?es et exclu pour SAS.
- SMOKE-ORCH-L2-001 est termin? ; le smoke r?el confirme la g?n?ration du PV pour SCI et son absence pour SAS.
- FIX-PV-RENDER-001 est termin? ; le PV from-scratch restaure les structures visuelles essentielles du document source sans UI, PDF ni ZIP.
- ANALYSE-ORDRE-001 est termin? ; les cadrages V1 ordre et r?gime communautaire sont disponibles dans `docs/delivery/`.
- ARBITRAGE-SOURCES-001 est termin? ; le scan a identifi? 147 fichiers dans `raw_drive_dump`, 11 fichiers dans `source_documents`, 18 groupes de doublons probables, 6 documents sans source claire et 16 documents hors p?rim?tre.
- PLACEMENT-HIGH-001 est termin? ; les 4 cas HIGH document?s dans le plan de placement V1 ont ?t? confirm?s comme d?j? pr?sents, sans nouvelle copie.
- SPEC-ORDRE-001, SPEC-TEXTE-ORDRE-001, CODE-ORDRE-001, SPEC-RC-001, CODE-RC-001, SPEC-SPFPL-001, SPEC-DEROG-001, SPEC-CESSION-BAIL-001, SPEC-TEXTE-BAIL-APP-001, SPEC-TEXTE-CESSION-CAB-001, SPEC-TEXTE-DEROG-001, SPEC-TEXTE-SPFPL-001, ARBITRAGE-CESSION-001, ARBITRAGE-DEROG-001, ARBITRAGE-SPFPL-001 et CODE-BAIL-APP-001 sont DONE.
- REVIEW-PV-001 est termin?, mais la validation humaine du rendu DOCX et du wording reste ? obtenir pour la revue juridique fine.
- RENDER-STYLE-001 est termin? ; les signatures encadr?es sont disponibles dans la couche commune et appliqu?es aux signatures Lot 1.
- Le PV nomination g?rant conserve des signatures r?p?tables simples ; toute signature encadr?e dirigeant/associ?s s?par?e reste soumise ? validation m?tier.
- UI-001 reste en attente explicite : ne pas lancer le branchement Streamlit sans nouveau ticket.
- Points ouverts PV document?s dans la spec texte : p?rim?tre SELAS, capital non variable, soci?t? d?j? immatricul?e, dirigeant non associ?, ponctuation finale des associ?s, f?minisation ?ventuelle de la fonction, r?gle `euro/euros`.
- Points ouverts ordre post-CODE-ORDRE-001 : revue humaine du premier rendu SCM, mention de d?rogation limit?e au bloc manuel fourni, valeurs ordinales et mandataire toujours fournis par contexte/r?f?rentiel.
- Points ouverts r?gime communautaire apr?s SPEC-RC-001 : revue humaine SELARL de la renonciation canonique, f?minisation ?ventuelle de `futur`, absence de variante `ma conjointe`, apport limit? ? une somme en num?raire, valeurs par d?faut de r?gime matrimonial / qualit? renonc?e / formes sociales ? fournir par contexte ou r?f?rentiel.
- CODE-RC-001 est termin? ; le smoke DOCX r?el confirme la production des deux lettres, mais ne vaut pas validation juridique fine.
- Points ouverts SPFPL apr?s ARBITRAGE-SPFPL-001 : acte de cession d'actions hors automatisation faute de source DOCX confirm?e, multi-souscripteurs hors V1, commissaire et ?valuateur fournis par contexte ou r?f?rentiel valid?.
- Points ouverts d?rogations apr?s PREP-DEROG-001 : les deux sources Lot 03 pr?par?es sont plac?es, le `.doc` legacy reste ? convertir ou remplacer si `cumul_salariee` entre dans le p?rim?tre, et le mode de rendu `document finalis?` ou `formulaire ? compl?ter` doit ?tre port? explicitement dans le registre ou le nom de sortie.
- CODE-DEROG-CORE-001 est termin? ; `DOC-013` formulaire multi-sites SEL et `DOC-014` demande cumul SELARL/BNC sont branch?s dans le catalogue/orchestrateur comme formulaires ? compl?ter.
- Points ouverts d?rogations apr?s CONVERT-DEROG-SALARIEE-001 : revue humaine juridique/visuelle du premier rendu `DOC-013` et `DOC-014`, `cumul_salariee` toujours bloqu? faute de DOCX propre apres erreur Word COM `0x800706BE`, zones narratives sensibles laiss?es ? compl?ter.
- CODE-BAIL-APP-001 est termin? ; `DOC-007` avenant au contrat de bail et `DOC-008` appel de fonds SEL sont branch?s dans le catalogue/orchestrateur.
- Points ouverts bail/appel apr?s CODE-BAIL-APP-001 : appel de fonds limit? ? SELARL dentaire, avenant limit? SELARL/SELAS avec `dossier_options.cession=true`, revue humaine juridique/visuelle du premier rendu toujours n?cessaire.
- Points ouverts cession apr?s CODE-CESSION-CAB-001 : revue humaine juridique/visuelle du premier rendu DOCX, sources SELAS non stabilis?es au-del? du param?trage V1, PDF/ZIP hors ticket.
- Points ouverts statuts apr?s SYNC-WAVE-007 : SAS limit? au mod?le SAS/SPFPL m?decins source ; SPFPL doit conserver cession/apport sans harmonisation ; SCM est cod? en V1 mais reste soumis ? revue humaine juridique/visuelle du premier rendu.

## Journal court
- 2026-05-27 : TRACK-B-SELARL-UX-FOLLOWUP-001 remplace les dates Streamlit par des champs `JJ/MM/AAAA`, ajoute la liste `Situation matrimoniale`, retire le doublon visible `Regime matrimonial`, calcule la valeur nominale depuis capital / parts et clarifie les champs d'ordre ; `ruff check .` OK, test clean front OK, HTTP 200 sur `http://localhost:8510` avec PID `3480` arrete.
- 2026-05-27 : TRACK-B-SELARL-UX-DEDUP-RECONCILIATION-001 nettoie l'UX du clean front SELARL V1 : genre/titre, montants et dates en lettres, mandataire, prestataire de signature, seuils de gerance, lieu d'exercice et conjoint sont derives, pre-remplis ou conditionnels ; tests clean front et ruff valides, aucun push/merge.
- 2026-05-12 : m?moire projet install?e dans `docs/project/`.
- 2026-05-12 : m?moire projet compl?t?e pour servir de contexte op?rationnel autonome ; artefact `tall -U pip` identifi? comme fichier parasite ? supprimer.
- 2026-05-12 : kit de reprise ajout? pour nouveau ChatGPT / Codex avec handoff, dernier ?tat et prompt de reprise.
- 2026-05-12 : DOC-001 impl?ment? en g?n?ration DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-001 corrig? pour rendre l'adresse personnelle dans l'ordre source `num voie + voie, ville cp`.
- 2026-05-12 : DOC-003 impl?ment? en g?n?ration DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-002 impl?ment? en g?n?ration DOCX from-scratch avec champ libre `adresse_domiciliation_affichee` ; validations locales vertes.
- 2026-05-12 : ORCH-001 branche les g?n?rateurs DOC-001, DOC-002 et DOC-003 dans l'orchestrateur dossier ; g?n?ration DOCX uniquement.
- 2026-05-13 : logique documentaire du moteur formalis?e par l'arbre document-centr? V1 ; m?moire projet align?e sans r??criture de l'arbre.
- 2026-05-13 : SMOKE-001 g?n?re r?ellement les trois DOCX du Lot 1 via l'orchestrateur avec `examples/contexts/lot_01_example.yaml` corrig? au strict minimum.
- 2026-05-13 : dictionnaire canonique des variables V1 int?gr? dans la m?moire projet ; le moteur dispose d?sormais d'un arbre documentaire et d'un dictionnaire canonique de variables.
- 2026-05-13 : table de mapping document -> variables canoniques V1 int?gr?e dans la m?moire projet sans r??criture ; ?cart temporaire `domiciliation.adresse_affichee` / `adresse_domiciliation_affichee` document?.
- 2026-05-13 : cadrage m?tier V1 de la famille `PV nomination g?rant` int?gr? dans la m?moire projet ; SPEC-PV-001 ajout? en READY et UI-001 plac? en attente tant que cette famille n'est pas sp?cifi?e.
- 2026-05-13 : spec canonique V1 de la famille `PV nomination g?rant` int?gr?e dans la m?moire projet ; SPEC-PV-001 pass? DONE, SPEC-TEXTE-PV-001 ajout? READY, UI-001 maintenu en attente explicite.
- 2026-05-13 : spec texte V1 de la famille `PV nomination g?rant` cr??e ; SPEC-TEXTE-PV-001 pass? DONE, CODE-PV-001 ajout? READY, aucun code Python modifi?.
- 2026-05-13 : CODE-PV-001 impl?mente le g?n?rateur DOCX from-scratch du PV nomination g?rant avec `associes[]`, `dirigeant_nomine`, branche `emprunt.actif`, variantes de genre/singulier-pluriel et tests cibl?s ; ruff et pytest verts.
- 2026-05-13 : smoke test r?el CODE-PV-001 ajout? via `examples/contexts/lot_02_pv_nomination_gerant_example.yaml` ; DOCX g?n?r? dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/` hors versionnement.
- 2026-05-13 : REVIEW-PV-001 r?g?n?re le DOCX PV depuis le contexte exemple, extrait un aper?u texte et cr?e une checklist de revue humaine dans `docs/review/`, sans modification du code Python.
- 2026-05-13 : SPEC-RENDER-001 cr?e la spec technique `docs/delivery/render_style_system_v1.md` pour une couche de rendu DOCX commune, sans modification de code Python.
- 2026-05-13 : RENDER-STYLE-001 impl?mente la couche commune de rendu DOCX, migre DOC-001/DOC-002/DOC-003/PV nomination g?rant, ajoute les tests de rendu et g?n?re les smoke DOCX dans `artifacts/render_style_001_*`.
- 2026-05-13 : ORCH-L2-PV-001 branche le PV nomination g?rant dans le catalogue et l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; SAS reste exclue ; ruff et pytest verts.
- 2026-05-13 : SMOKE-ORCH-L2-001 ajoute deux contextes orchestrateur Lot 2, g?n?re r?ellement le dossier SCI positif et le dossier SAS n?gatif, puis documente la pr?sence/absence du PV dans `docs/review/lot_02_orchestrator_smoke_review_v1.md`.
- 2026-05-13 : ANALYSE-ORDRE-001 cr?e les cadrages V1 pour `Demande d'inscription ? l'ordre` et le batch `r?gime communautaire`, puis ajoute SPEC-ORDRE-001 et SPEC-RC-001 en READY, sans modification de code Python.
- 2026-05-13 : ARBITRAGE-SOURCES-001 r?pare les docs projet 10/11/12, cr?e les d?cisions d'arbitrage sources V1, classe les cas HIGH/MEDIUM/LOW et ajoute PLACEMENT-HIGH-001 en READY, sans d?placer de fichier source.
- 2026-05-14 : PLACEMENT-HIGH-001 confirme en no-op les 4 cas HIGH d?j? pr?sents dans `source_documents`, cr?e le journal d'ex?cution V1 et ne touche pas aux cas MEDIUM/LOW ni au raw dump.
- 2026-05-14 : SPEC-ORDRE-001 compare les variantes `Demande d'inscription ? l'ordre` SELARL, SELAS et SPFPL, cr?e la spec canonique V1 et ajoute SPEC-TEXTE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : SPEC-TEXTE-ORDRE-001 cr?e la spec texte V1 `Demande d'inscription ? l'ordre`, retient un tronc commun avec overlays SELARL/SELAS, SPFPL cession/apport et SCM, classe `D?rogation ?` en bloc manuel conditionnel, puis ajoute CODE-ORDRE-001 en READY, sans modification de code Python.
- 2026-05-14 : FIX-PV-RENDER-001 am?liore la structure visuelle du PV nomination g?rant from-scratch : listes ? tirets, titre encadr?, intertitres visibles, formules de vote en italique et smoke DOCX d?di?.
- 2026-05-14 : CODE-ORDRE-001 impl?mente le g?n?rateur DOCX from-scratch `Demande d'inscription ? l'ordre`, couvre SELARL, SELAS, SPFPL cession, SPFPL apport et SCM, teste la d?rogation manuelle et le mandataire configurable, puis g?n?re un smoke DOCX d?di?.
- 2026-05-14 : SPEC-RC-001 cr?e les specs canonique et texte V1 du batch r?gime communautaire, compare les variantes SELARL / SELAS / SPFPL, retient deux documents canoniques distincts et ajoute CODE-RC-001 en READY, sans modification de code Python.
- 2026-05-14 : SYNC-SPECS-001 absorbe dans `main` les specs parall?les RC, SPFPL, d?rogations et cession/bail, puis aligne le pilotage sur `CODE-RC-001` READY, sans stage de code Python.
- 2026-05-14 : CODE-RC-001 impl?mente le batch r?gime communautaire V1 avec deux g?n?rateurs DOCX from-scratch, champs mod?le d?di?s, catalogue/orchestrateur conditionn?s par `dossier_options.regime_communautaire`, tests cibl?s et smoke DOCX r?el.
- 2026-05-14 : SYNC-TEXTE-SPECS-001 absorbe dans `main` les specs texte parall?les bail/appel, cession cabinets, d?rogations et SPFPL, puis confirme `CODE-BAIL-APP-001`, `ARBITRAGE-CESSION-001`, `ARBITRAGE-DEROG-001` et `ARBITRAGE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-ARBITRAGES-001 absorbe dans `main` les arbitrages cession cabinets, d?rogations et SPFPL, passe les trois tickets d'arbitrage en DONE et confirme `CODE-BAIL-APP-001`, `CODE-CESSION-CAB-001` et `CODE-SPFPL-001` en READY, sans modification de code Python.
- 2026-05-14 : SYNC-CODE-BAIL-APP-001 absorbe dans `main` le commit `557a013274aa9f7122c81d5e6e0b52c4043a540c`, passe `CODE-BAIL-APP-001` en DONE et confirme `CODE-CESSION-CAB-001`, `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en READY/parall?lisables, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-LOT03-05-001 absorbe dans `main` les commits `36828fbc45d6b8a37c2e76eb8227460df441ebde` et `958fce5d2a9d5d30df4d918cb098fec483f5140e`, passe `PREP-DEROG-001` et `CODE-SPFPL-AGR-INFO-001` en DONE, puis confirme `RESUME-CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : RESUME-CODE-CESSION-CAB-001 reprend `CODE-CESSION-CAB-001` depuis `main`, restaure les g?n?rateurs cession cabinets, branche `DOC-009` ? `DOC-012`, g?n?re quatre DOCX de smoke test et valide `ruff` / `pytest`.
- 2026-05-14 : CODE-DEROG-CORE-001 impl?mente les g?n?rateurs DOCX partiels `multi_sites_sel` et `cumul_sel_bnc`, les branche au catalogue/orchestrateur sous `DOC-013` et `DOC-014`, ajoute le contexte exemple et les tests cibl?s, puis g?n?re le smoke DOCX r?el dans `artifacts/lot_03_derogations_core_smoke_test/`.
- 2026-05-14 : SYNC-CODE-WAVE-002 absorbe dans `main` les commits sources `ea35d2af353ac5b8567e82091ab978cf24a27445` et `bee4c8bec27397198a170c4f9888b2470b24c67f`, confirme `CODE-CESSION-CAB-001` et `CODE-DEROG-CORE-001` en DONE, puis confirme `CODE-SPFPL-CORE-001` et `PREP-STATUTS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-WAVE-003 absorbe dans `main` les commits sources `b854821061b85ac66fe785c11cb3c6b0bac5a85b` et `09cbad120d22910f05ba5e645971ade56fedb76d`, passe `PREP-STATUTS-001` et `CODE-SPFPL-CORE-001` en DONE, puis confirme `SPEC-STATUTS-SEL-001`, `SPEC-STATUTS-SPFPL-001`, `SPEC-STATUTS-CIVILS-001` et `SPEC-STATUTS-SAS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-SPECS-001 absorbe dans `main` les commits sources `00b7886ac431c8a47d9cdcca8bfed026a756cb69`, `b34c66e5e67f3261317035943e974536be27d6d3`, `9b25e09d08ec2161d757d1581c34073dcbbc594f` et `704eeb7301cf69460c16b2ed9fbc0ea22ca83c8c`, passe les quatre specs statuts en DONE, puis confirme `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001`, `ARBITRAGE-STATUTS-SEL-001` et `ARBITRAGE-STATUTS-CIVILS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-14 : SYNC-STATUTS-CODE-ARB-001 absorbe dans `main` les commits sources `82e67120ed714b791d5483108336a570ea520e59`, `a98939c649e4124e40f2cd69c9ed125d342acc31` et `1caafd7`, passe `CODE-STATUTS-SAS-001`, `CODE-STATUTS-SPFPL-001` et `ARBITRAGE-STATUTS-SEL-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `RESUME-ARBITRAGE-STATUTS-CIVILS-001` et `STYLE-ANALYSE-BATCH-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-STYLE-CIVILS-001 absorbe dans `main` les commits sources `76dd139da65c233f0c6aecc76bc2ea5e929381ca` et `b21f1b0cc5b975049e4acc279b8303f1d739b60f`, passe `STYLE-ANALYSE-BATCH-001` et `ARBITRAGE-STATUTS-CIVILS-001` en DONE, puis confirme `CODE-STATUTS-SEL-001`, `CODE-STATUTS-CIVILS-CORE-001` et `FIX-STYLE-LETTERS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-STATUTS-SEL-CIVILS-001 absorbe dans `main` le commit source `9a79560c4bae1ae3a98ec5305b4187f9f4ebd6a8`, confirme l'arbitrage civils V1 d?j? pr?sent avec un contenu identique au commit source `b21f1b0cc5b975049e4acc279b8303f1d739b60f`, passe `CODE-STATUTS-SEL-001` en DONE, puis confirme `RESUME-FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : CODE-STATUTS-CIVILS-CORE-001 impl?mente les g?n?rateurs statuts SCS, SCI et SCI IRIS, ajoute le mod?le `statuts_civils`, branche DOC-019 ? DOC-021 au catalogue/orchestrateur, ajoute le contexte exemple et g?n?re le smoke DOCX r?el ; SCM reste hors ticket.
- 2026-05-15 : SYNC-WAVE-004 absorbe dans `main` les commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8`, passe `RESUME-FIX-STYLE-LETTERS-001`, `FIX-STYLE-LETTERS-001` et `CODE-STATUTS-CIVILS-CORE-001` en DONE, puis confirme `ARBITRAGE-STATUTS-SCM-001`, `PREP-SCM-SAT-001`, `SPEC-SAS-SATELLITES-001`, `CODE-OPTION-IS-001` et `PREP-ACTE-ACTIONS-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-005 absorbe dans `main` les commits sources `91436f0916fdecbcc98450b72ba6e602cb8f1a3b`, `1b3ba14d0bcc31fc7dcbf1752d6d3263645ae8b3`, `32059155c618b4e985893f42ef2817187599c281`, `74d41db53543b790e197082e8b9c713f7de92dc2` et `d1d649e11fdc638e6d7da0640c154d1f213739ee`, passe `CODE-OPTION-IS-001`, `PREP-SCM-SAT-001`, `ARBITRAGE-STATUTS-SCM-001`, `SPEC-SAS-SATELLITES-001` et `PREP-ACTE-ACTIONS-001` en DONE, puis confirme `CODE-STATUTS-SCM-001`, `CODE-SAS-SATELLITES-001`, `SPEC-SCM-SATELLITES-001`, `CONVERT-ACTE-ACTIONS-001` et `CONVERT-DEROG-SALARIEE-001` en READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : CONVERT-DEROG-SALARIEE-001 retente la conversion Word COM du `.doc` legacy salariee ; aucun DOCX exploitable n'est produit, le blocage est documente dans `docs/delivery/lot_03_derogation_salariee_conversion_blocker_v1.md`, sans modification de code Python.
- 2026-05-15 : CONVERT-ACTE-ACTIONS-001 convertit `Acte_cession_SPFPL_tiers_modele.doc` en DOCX via `Wordconv.exe`, place le r?sultat dans `project/source_documents/lot_05/` et documente l'origine/confiance dans `docs/delivery/lot_05_acte_cession_actions_preparation_v1.md`, sans modification de code Python.
- 2026-05-15 : SYNC-WAVE-006 absorbe dans `main` les commits sources `557fc1920361a8c7831e6b023d70471c9c29e5ff` et `291da7b6db68b3de413fba50cf652dde98a8f6a8` par ?quivalence, puis cherry-picke `2c55a7ab5f8a44de5c29305cfbc280f930ee32ec`, `568336bed7ccb0a5901abe5d921fd9056573e32d`, `8f0c8ab13d6e8f1a9e50747f8a9d5b607bcb90d6` et `11dc0d8dda23f841d650586e0977e0202270a3b5`, passe la vague en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-007 absorbe dans `main` les commits sources `3c040774cdfe57c203b78776a9ea412ec3d14d94`, `6453b6f64665feda898a076f730cba9a6684825b`, `075af377f7c9d7475429f1e738b46483127d757f` et `c221681570782a1b1efc5afc72087cb903cd8a65`, passe les quatre tickets correspondants en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : SYNC-WAVE-008 absorbe dans `main` les commits sources `61a1c49353724bbf5b8f1bb8f039d5e96b877ecc`, `d3188c0b4a4a61d889a2ce9ccc37e84e1284adaa`, `939e1c2088892abcf4a8fdcbaa35911f4f8a2f9f`, `19468886f5e885f79b2b35e17e2ff2a097ea9c3a`, `d8747ef20aba478c575c5a491cdf0f634a9c26d3`, `00b4c955b372399bb8701f47a5686748539f061b`, `a181e069f756a1ea846fdcd1824b3f8c57cc11f5` et `518e46fbb8d8bee03a23ea203654b4199103fb7e`, passe les huit tickets correspondants en DONE, puis confirme les prochains tickets READY, sans modification de `project/source_import/raw_drive_dump/` ni de `artifacts/`.
- 2026-05-15 : FINAL-SCM-CESSION-WAVE-001 restaure la r?solution V1 cession SCM, impl?mente `DOC-031` ? `DOC-033`, g?n?re le smoke DOCX r?el, valide ruff/pytest et cr?e l'audit de cl?ture moteur V1.
- 2026-05-15 : SYNC-CLOSE-AUDIT-001 absorbe le commit source `0139202b170531fd628f25811c55855a2512acc0` depuis `origin/codex/close-motor-audit-001`, confirme `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` sur `main` et conserve la version finale plus r?cente, sans modification de code Python.
- 2026-05-17 : RECONCILE-MOTOR-CLOSE-001 expose les g?n?rateurs ordre/SPFPL sous `DOC-034` ? `DOC-043`, consolide `08/09`, int?gre `17/18`, corrige l'audit `16` et cl?t le moteur DOCX V1 hors UI/PDF/ZIP/recette finale.
- 2026-05-17 : PDF-BACKEND-001 ajoute un backend d'export PDF best-effort avec priorit? LibreOffice headless puis fallback Word COM Windows, tests cibl?s et smoke r?el DOCX vers PDF.
- 2026-05-17 : SYNC-POST-MOTOR-UI-001 absorbe dans `main` les commits sources `d62670efe10481926437c0e1a5dabbe349fd5938`, `24a881b999371811d39a2403c0b51d9ae8ce0556`, `ef6252b3c15dc3fc39f1efdc05687c0f448f8fe1`, `2f76f61848469ddf2f7b29c3169e8893e83fd3a5` et `c2fc0db4d51485c7c5e721c5184028ae17c68cb3`, passe les fondations UI/PDF/recette en DONE et confirme `UI-CORE-001`, `RESUME-ZIP-BACKEND-001` et `REVIEW-FINAL-001` en READY.
- 2026-05-17 : UI-PDF-ZIP-INTEGRATION-001 branche l'UI Streamlit sur la g?n?ration dossier DOCX, l'export PDF local optionnel et le ZIP de sortie, ajoute un smoke manuel document? et conserve `artifacts/` hors versionnement.
- 2026-05-17 : SYNC-FINAL-FOUNDATIONS-001 absorbe les compl?ments manquants `UI-PDF-ZIP-INTEGRATION-001` et `ZIP-BACKEND-001`, confirme les fondations/audits d?j? pr?sents sur `main`, remplace `UI-CORE-001` par `UI-PDF-ZIP-INTEGRATION-001`, valide ruff/pytest 191 tests et confirme uniquement `REVIEW-FINAL-001` puis `CLOSE-PROJECT-V1-001` en READY.
- 2026-05-18 : WORKTREE-CLEANUP-AND-UI-STATUS-001 integre le pack `docs/review/final_review_pack_v1.md` depuis `codex/review-final-001`, cree `docs/project/23_WORKTREE_CLEANUP_AND_UI_STATUS_V1.md`, documente l'archivage local des worktrees et confirme que l'UI actuelle est une UI technique de pilotage par contexte, pas une UI produit finale.
- 2026-05-18 : UI-BUSINESS-WIZARD-001 ajoute le mode Assistant metier Streamlit en deux modes, construit un contexte SCI simple pour `DOC-001` a `DOC-004`, conserve le mode technique YAML/JSON, separe les actions DOCX/ZIP/PDF et valide ruff + pytest 196 tests.
- 2026-05-18 : DEPLOY-STREAMLIT-CLOUD-FIX-001 ajoute la declaration Poetry explicite du package `src/sydel_doc_engine`, documente la cause racine Streamlit Cloud et valide installation editable, ruff et pytest 196 tests ; Poetry local reste indisponible.
- 2026-05-18 : CASE-CATALOG-001 cree le service pur `get_expected_documents(...)` et le catalogue metier par cas depuis la source Word canonique, couvre 46 documents attendus uniques dont 43 mappes a `DOC-XXX`, documente 2 manuels et 1 non implemente, ajoute les tests unitaires de selection et valide ruff + pytest 208 tests.
- 2026-05-19 : SELARL-PILOT-PROTOCOL-001 ajoute la source V2 cible, cree le protocole de construction de processus, les specs produit/formulaire/wizard SELARL et le plan d'implementation, puis valide ruff + pytest 217 tests sans modifier l'UI, le moteur ni les generateurs.
- 2026-05-19 : SELARL-PILOT-SOURCE-VERIFY-001 lit la vraie source V2, remplace le fichier canonique provisoire, corrige les statuts SELARL `DOC-013` / `DOC-014` en manuel, compl?te les variables V2 dans les specs et cr?e la matrice d'?carts source.
- 2026-05-19 : SELARL-FORM-SCHEMA-IMPL-001 ajoute le module `selarl_form_schema.py`, verrouille la r?serve source V2 sur `DOC-006`, confirme `DOC-013` / `DOC-014` hors g?n?ration pilote et teste la couverture des variables V2 ; ruff OK et pytest 231 tests pass?s.
- 2026-05-19 : SELARL-UI-WIZARD-IMPL-001 branche l'Assistant m?tier Streamlit sur le sch?ma SELARL, ajoute le parcours pilote visible, conserve SCI et Technique / diagnostic, affiche les documents manuels/r?serv?s et valide ruff + pytest 239 tests.
- 2026-05-19 : SELARL-NOTEBOOKLM-RECONCILIATION-001 ajoute les sources NotebookLM/V3, cr?e la hi?rarchie source SELARL V2, le rapport d'?carts et le backlog de reconstruction ; aucun code Python modifi?, smoke SELARL bloqu? jusqu'au r?alignement wording / flow / r?utilisations / UI.
- 2026-05-19 : SELARL-PLAN-CORRECTION-001 corrige la planification selon les arbitrages associ? (`Fiche Client`, `Praticien`, `Dossier unipersonnel`), retire le ticket statut documentaire lourd, exclut mode Projet / filigrane V1 et confirme que l'UI SELARL ne doit pas ?tre pouss?e/red?ploy?e avant r?alignement produit.
- 2026-05-19 : SELARL-WORDING-REALIGN-001 remplace le vocabulaire visible SELARL par `Fiche Client` / `Praticien` / r?les juridiques exacts, conserve l'ordre et la logique, ajoute les tests anti-r?gression wording et valide ruff + pytest 241 tests.
- 2026-05-19 : SELARL-FLOW-REALIGN-001 ajoute le flow conceptuel SELARL en six ?tapes dans le sch?ma et les projections m?tier, met ? jour les specs actives, laisse `streamlit_app.py` intact pour le ticket UI d?di? et valide les tests cibl?s schema/wizard.
- 2026-05-19 : SELARL-REUSE-RULES-REALIGN-001 ajoute `Dossier unipersonnel` comme r?gle pivot, conserve les r?utilisations utiles en opt-in, sort le mandataire du d?faut UX, documente les relations non automatiques et valide ruff + pytest 252 tests.
- 2026-05-19 : SELARL-UI-REALIGN-001 r?aligne le parcours Streamlit visible SELARL en six ?crans, expose `Dossier unipersonnel`, rend le mandataire secondaire, conserve SCI et Technique / diagnostic, puis valide ruff + pytest 257 tests.
- 2026-05-19 : SELARL-SMOKE-REALISTIC-001 ex?cute trois sc?narios SELARL r?alistes, g?n?re `DOC-001` ? `DOC-004` et un ZIP par sc?nario, confirme l'exclusion des documents manuels `DOC-013` / `DOC-014`, la r?serve `DOC-006`, le blocage contexte incomplet V2 des documents non pr?ts et pr?pare la revue associ? / juriste.
- 2026-05-20 : SELARL-CLOUD-GENERATION-BUG-001 reproduit le blocage de g?n?ration visible quand les r?utilisations SELARL sont coch?es avant saisie, corrige le `session_state` des champs d?riv?s associ?/domiciliation, ajoute un test AppTest de g?n?ration r?elle et valide ruff + pytest 266 tests ; commit local bloqu? par refus d'?criture dans `.git`.
- 2026-05-20 : DOCUMENT-UNITAIRE-001 ajoute le mode Streamlit `Document unitaire`, limite la V1 ? `DOC-001` ? `DOC-004`, affiche honn?tement les documents manuels ou non encore support?s et valide ruff + pytest 266 tests.
- 2026-05-20 : ASSISTANT-METIER-PREFILL-001 ajoute des sc?narios de test d?terministes dans l'Assistant m?tier, avec s?lecteur, pr?remplissage, r?initialisation, indication visible, synchronisation `session_state` des champs d?riv?s SELARL/domiciliation et non-r?gression SCI/Document unitaire/Technique ; aucun g?n?rateur, moteur DOCX/PDF/ZIP ni wording juridique modifi?.
- 2026-05-20 : GLOBAL-VARIABLE-INVENTORY-001 cr?e l'inventaire global brut `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` et le rapport `docs/review/global_variable_inventory_001_report_v1.md` : 12 443 lignes, 43 documents `DOC-001` ? `DOC-043`, 15 familles, aucun g?n?rateur/moteur/UI/wording juridique modifi?.
- 2026-05-20 : GLOBAL-VARIABLE-IDENTITY-AUDIT-001 cr?e la matrice d'identit? V2, le registre canonique global V2, la liste de 10 questions humaines et le rapport ex?cutif : 1 334 slugs distincts audit?s, 49 champs propos?s, 142 rapprochements class?s, aucun g?n?rateur/moteur/UI/wording juridique modifi?.
- 2026-05-24 : GLOBAL-FRONT-ARCHITECTURE-001 cr?e l'architecture front globale V1, le mod?le d'objets, les r?gles structurelles, la strat?gie d'?crans, le backlog de rebuild et le rapport ex?cutif ; aucun g?n?rateur, moteur DOCX/PDF/ZIP, Streamlit ou wording juridique modifi?.
- 2026-05-24 : GLOBAL-FRONT-ARCHITECTURE-QA-001 contr?le l'architecture front sur 7 documents sentinelles, cr?e le rapport QA et le CSV de couverture ; verdict global ORANGE ma?trisable, aucun rouge, aucun g?n?rateur/moteur/UI/Python modifi?.
- 2026-05-24 : FRONT-DATA-LAYER-001 cr?e le package `front_data` avec objets front globaux, mapping canonique V2.1, checks sentinelles, diagnostics de validation et tests unitaires ; ruff OK et pytest 288 tests pass?s ; aucun g?n?rateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifi?.
- 2026-05-24 : FRONT-ROLE-MODEL-001 raffine les roles front globaux avec familles, portees, modele ordre, representation de personne morale, tiers commissaire/evaluateur, garde-fous de placeholders et tests dedies ; ruff OK et pytest 298 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- 2026-05-24 : FRONT-ADDRESS-MODEL-001 raffine les adresses typees avec usages explicites, politiques de reutilisation tracees, formes affichees/composants, overrides legacy, mapping canonique et validations dediees ; ruff OK et pytest 313 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, Streamlit ou UI visible modifie.
- 2026-05-24 : FRONT-TEST-PREFILL-001 realigne les prefills fictifs de l'Assistant metier sur `front_data`, conserve les quatre scenarios existants, ajoute les profils front_data, la conversion en `BusinessWizardInput`, le `DossierRecord` de test, la synthese de statuts documentaires et les tests dedies ; ruff OK et pytest OK, 352 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, wording juridique, mode Technique ou mode Document unitaire modifie.
- 2026-05-24 : FRONT-REVIEW-001 audite le prototype Streamlit face aux fondations `front_data`, classe les briques en prototype / migration / test / deprecation, cree `FRONT_MIGRATION_MAP_V1.md`, met a jour le backlog vers `FRONT-UI-SHELL-001` puis les tickets UI visibles ; aucun code Python, generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-DOSSIER-EDITOR-001 ajoute un editeur dossier V1 dans le nouveau shell, avec profils prudents, `DossierRecord` minimal, etapes/blocs `dossier_flow`, exigences, documents attendus et statuts/lots `document_status` ; ruff OK et pytest OK, 364 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou prototype historique modifie.
- 2026-05-24 : FRONT-DOSSIER-DATA-ENTRY-001 ajoute la premiere saisie reelle du nouvel editeur dossier sur le profil `SELARL creation simple` : personne principale, societe principale, adresses typees, role assignments explicites, `domiciliation = siege` via `ReuseRuleState`, valeurs canoniques et statuts DOC-001 a DOC-004 recalcules ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-GENERATION-ACTIONS-001 branche les actions de generation du nouveau front sur le profil `SELARL creation simple`, cree l'adaptateur `DossierRecord` vers contexte moteur, limite la generation a `DOC-001` a `DOC-004`, exclut `DOC-006`, `DOC-013` et `DOC-014`, expose DOCX/ZIP/PDF optionnel dans le shell, valide ruff et pytest 380 tests, et conserve le prototype comme zone secondaire ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-UX-CLEANUP-001 simplifie la vue principale du nouveau front : suppression de la navigation interne visible, tables de flow/blocs/exigences/statuts repliees en diagnostics, parcours principal limite a type de dossier, saisie, resume documents et generation ; ruff OK et pytest OK 380 tests ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-24 : FRONT-UX-HARD-CUT-001 retire les diagnostics et outils de la surface utilisateur normale : aucun radio, aucun tableau par defaut, seulement Type de dossier / Donnees a saisir / Generation ; les outils internes sont accessibles via sidebar `Outils internes`, ruff OK et pytest OK 380 tests ; aucun generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-25 : FRONT-REALITY-CHECK-001 audite le front reel contre les debriefs recents, confirme DOCX/ZIP branches sur `DOC-001` a `DOC-004`, PDF conditionnel indisponible localement, identifie les pollutions restantes de surface et cree le plan `FRONT_MINIMAL_USER_SURFACE_V1.md`; aucun Python, generateur, moteur DOCX/PDF/ZIP ou wording juridique modifie.
- 2026-05-25 : FRONT-MINIMAL-SURFACE-CLEANUP-001 applique la surface minimale du nouveau front : 3 zones principales, 0 radio, 0 table, 0 expander, outils internes caches par mode equipe, PDF cache si backend indisponible et blocages visibles dans `Generation`; ruff OK et pytest OK, 382 tests passes ; aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-25 : SELARL-COMPLETE-CASE-PLAYBOOK-001 cadre la SELARL complete : le moteur est plus avance que le front, la generation visible reste limitee a `DOC-001` a `DOC-004`, les documents manuels restent hors generation, et le prochain ticket unique devient `SELARL-COMPLETE-CONTEXT-ADAPTER-001`; aucun Python, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-25 : SELARL-COMPLETE-CONTEXT-ADAPTER-001 branche la selection/readiness/contexte SELARL complet cote nouveau front : medecin simple genere 6 DOCX (`DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-017`), dentiste bascule vers `DOC-016`, regime communautaire ajoute `DOC-005`, `DOC-006` reste reserve, `DOC-013`/`DOC-014` restent manuels, et cession/SCM restent `context_incomplete` jusqu'aux sous-formulaires ; ruff OK et tests cibles OK, 23 passes ; pytest complet non conclusif par `PermissionError` Windows temp ; aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-26 : TRACK-B-FRONT-ARCHITECTURE-RESET-001 cree le nouveau point d'entree clean `src/sydel_doc_engine/front_app/app.py`, separe shell/routing/selection/saisie/generation du legacy, conserve `app/streamlit_app.py` comme reference historique non importee, documente la frontiere legacy et le lancement local ; generation SELARL volontairement non implementee dans ce ticket ; aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
- 2026-05-26 : TRACK-B-SELARL-SOURCE-OF-TRUTH-CONTRACT-001 cree le contrat `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`, consolide les sources metier SELARL et conclut GO pour une vertical slice V1 strictement bornee ; aucun code, generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique modifie.
