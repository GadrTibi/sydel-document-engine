# Pack de revue finale V1

Ticket : `REVIEW-FINAL-001`

Date : 2026-05-17

## Objet

Ce pack consolide la revue finale exploitable du flux V1 complet :

`contexte dossier -> selection documentaire -> DOCX -> PDF -> ZIP -> revue humaine`

Il sert de support d'execution et de decision finale. Il ne modifie aucun code
Python, aucun fichier de pilotage projet et aucun wording juridique.

Ce pack ne vaut pas validation juridique. Il separe :

- la revue moteur ;
- la revue visuelle ;
- la revue UI ;
- la revue PDF ;
- la revue ZIP ;
- les criteres de go/no-go final.

## References de cadrage

- `AGENTS.md`
- `docs/review/final_recipe_framework_v1.md`
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`
- `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md`
- `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md`
- `docs/project/19_UI_FLOW_V1.md`
- `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md`
- `docs/project/21_UI_FORM_SCHEMA_V1.md`
- `docs/review/lot_02_orchestrator_smoke_review_v1.md`
- `docs/review/lot_03_batch_review_v1.md`
- `docs/review/lot_04_batch_review_v1.md`
- `docs/review/lot_05_batch_review_v1.md`
- `docs/review/ui_pdf_zip_integration_001_smoke.md`

## Perimetre de revue

### Inclus

- moteur DOCX V1 clos sur `DOC-001` a `DOC-043` ;
- selection documentaire par `select_documents_for_context` ;
- generation DOCX par `generate_documents` ;
- UI Streamlit de generation dossier ;
- export PDF local depuis les DOCX produits ;
- ZIP dossier contenant les sorties disponibles ;
- revue humaine des rendus DOCX/PDF et des exclusions V1.

### Exclus

- correction ou reecriture de wording juridique ;
- nouvelle implementation documentaire ;
- changement de catalogue, orchestrateur, UI, PDF ou ZIP ;
- validation juridique finale par ce seul document ;
- automatisation de documents manuels ou legacy non arbitres.

## Statuts a utiliser

| Statut | Sens |
|---|---|
| `OK` | Controle execute, conforme, preuve disponible. |
| `KO` | Controle execute, non conforme, correction requise. |
| `NA` | Non applicable au cas teste, justification obligatoire. |
| `BLOCKED` | Controle impossible, cause precise obligatoire. |

## Preuves minimales attendues

Chaque execution de revue finale doit conserver :

- date d'execution ;
- branche et commit testes ;
- contexte dossier utilise ;
- liste des `doc_id` selectionnes ;
- dossier de sortie DOCX ;
- correspondance DOCX -> PDF quand le PDF est active ;
- chemin du ZIP et liste de contenu ;
- captures UI ou notes de revue ;
- decision finale et reserves.

## Matrice minimale de cas

| Cas | Objectif | Contexte candidat | Sorties attendues |
|---|---|---|---|
| Lot 1 / socle simple | Verifier le socle universel et un dossier court. | `examples/contexts/lot_01_example.yaml` | DOCX socle, PDF si backend disponible, ZIP. |
| Lot 2 / PV positif | Verifier selection PV hors SAS. | `examples/contexts/lot_02_orchestrator_positive_example.yaml` | `DOC-001` a `DOC-004`, PDF, ZIP. |
| Lot 2 / PV negatif SAS | Verifier exclusion PV pour SAS. | `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml` | Socle attendu, absence du PV. |
| Lot 03 | Verifier cession, bail/appel ou derogations selon contexte disponible. | Contexte Lot 03 existant. | DOCX du batch attendu, PDF, ZIP. |
| Lot 04 | Verifier statuts longs et numerotation. | Contexte Lot 04 existant. | Statuts attendus, PDF, ZIP. |
| Lot 05 | Verifier satellites et SPFPL/SCM selon contexte disponible. | Contexte Lot 05 existant. | Documents attendus, PDF, ZIP. |
| Cas negatif | Verifier les erreurs moteur/UI. | Contexte volontairement incomplet. | Generation bloquee, message explicite. |

Si un contexte candidat n'est pas disponible ou n'est pas complet, le controle
correspondant passe `BLOCKED` et la cause exacte doit etre notee.

## 1. Revue moteur

Objectif : confirmer que le moteur DOCX et l'orchestrateur restent alignes avec
la cloture V1 avant toute decision finale.

| Controle | Preuve attendue | Statut | Notes |
|---|---|---|---|
| Catalogue et registre couvrent `DOC-001` a `DOC-043`. | Sortie de test ou rapport d'alignement. | A renseigner | |
| Les 43 generateurs documentaires attendus sont atteignables. | Test de registre ou audit runtime. | A renseigner | |
| `select_documents_for_context` retourne les `doc_id` attendus pour chaque cas de revue. | Liste par contexte. | A renseigner | |
| Le cas SAS negatif exclut le PV nomination gerant. | Liste selectionnee sans `DOC-004`. | A renseigner | |
| Les documents manuels, legacy bloques ou non arbitres ne sont pas generes automatiquement. | Liste d'exclusions controlee. | A renseigner | |
| `generate_documents` produit les DOCX attendus dans un dossier propre. | Chemin de sortie + liste fichiers. | A renseigner | |
| Aucun placeholder source visible de type `[` / `]` ne subsiste dans les DOCX finaux. | Inspection texte/OpenXML. | A renseigner | |
| Les erreurs de donnees obligatoires sont explicites et bloquantes. | Cas negatif + message. | A renseigner | |
| Les validations automatises de reference passent ou sont justifiees. | Sortie `ruff` / `pytest` ou justification. | A renseigner | |

Points d'attention issus des audits :

- la cloture moteur porte uniquement sur DOCX, catalogue, orchestrateur,
  generateurs et tests ;
- la revue humaine juridique et visuelle reste hors cloture moteur ;
- le PDF, le ZIP et l'UI sont des couches consommatrices du moteur.

## 2. Revue visuelle

Objectif : relire les DOCX et PDF comme rendus humains exploitables, sans
changer le contenu juridique.

| Controle | Preuve attendue | Statut | Notes |
|---|---|---|---|
| Les titres principaux sont lisibles et separes du corps du texte. | Note ou capture par famille. | A renseigner | |
| Les intertitres, articles, resolutions et listes restent reperables. | Note de revue. | A renseigner | |
| Les tableaux de chiffres, parts, apports ou souscripteurs sont lisibles. | Capture ou note. | A renseigner | |
| Les zones de signature sont presentes, non compactees et attribuables. | Capture ou note. | A renseigner | |
| Les statuts et documents longs conservent une numerotation exploitable. | Revue Word/PDF. | A renseigner | |
| Les documents generes plus courts que les sources gardent les grandes sections attendues. | Checklist sections. | A renseigner | |
| Les formulaires a completer restent clairement identifies comme incomplets. | Revue des libelles et noms de fichiers. | A renseigner | |
| Les anomalies signalees dans les revues Lot 03, Lot 04 et Lot 05 sont reprises. | Tableau de suivi. | A renseigner | |

Points d'attention par batch :

| Batch | Points a reprendre |
|---|---|
| Lot 02 | Selection PV positive/negative deja fumee ; revue juridique fine du rendu PV toujours distincte. |
| Lot 03 | Documents parfois plus courts que les sources ; verifier sections, tableaux, signatures, formulaires a completer. |
| Lot 04 | Statuts longs sensibles : numerotation, annexes, clauses professionnelles, sources non fumees localement selon familles. |
| Lot 05 | Verifier distinction parts/actions, satellites SAS/SCM, documents sans artefact disponible et limites multi-associes. |

## 3. Revue UI

Objectif : verifier que l'UI pilote le dossier via le moteur, sans logique
juridique cachee et sans presenter la generation comme une validation finale.

| Controle | Preuve attendue | Statut | Notes |
|---|---|---|---|
| L'UI Streamlit se lance localement. | URL locale + capture ou log. | A renseigner | |
| Un contexte YAML ou JSON de revue est charge. | Chemin contexte + capture. | A renseigner | |
| L'UI affiche structure, options et donnees principales du dossier. | Capture. | A renseigner | |
| La selection documentaire affichee correspond a l'orchestrateur. | Capture liste `doc_id` + controle moteur. | A renseigner | |
| La generation DOCX depuis l'UI produit les fichiers attendus. | Dossier de sortie + capture succes. | A renseigner | |
| Un contexte incomplet affiche une erreur lisible et bloque la generation. | Capture erreur + contexte negatif. | A renseigner | |
| L'option PDF est presente seulement comme export local dependant du backend. | Capture ou note. | A renseigner | |
| Le ZIP telechargeable contient uniquement les sorties disponibles. | Capture + inspection ZIP. | A renseigner | |
| Aucun libelle UI ne laisse croire a une validation juridique automatique. | Revue des textes UI. | A renseigner | |

Regles UI a verifier :

- l'UI est dossier-centree, pas document-centree ;
- la selection vient de l'orchestrateur ;
- les champs caches ne bloquent pas ;
- les options sensibles sont explicites ;
- les documents manuels ou legacy restent exclus ou signales comme tels.

## 4. Revue PDF

Objectif : confirmer que les PDF sont des conversions des DOCX produits, avec
tracabilite et erreurs explicites.

| Controle | Preuve attendue | Statut | Notes |
|---|---|---|---|
| Le backend PDF disponible est identifie. | `LibreOffice`, `Word COM` ou indisponible. | A renseigner | |
| Un PDF est produit pour chaque DOCX inclus dans la recette PDF. | Table DOCX -> PDF. | A renseigner | |
| Les echecs de conversion indiquent une cause precise. | Log ou message UI. | A renseigner | |
| Aucun echec PDF ne modifie les DOCX sources. | Comparaison chemins/timestamps ou note. | A renseigner | |
| Les PDF produits s'ouvrent localement. | Note d'ouverture ou capture. | A renseigner | |
| Titres, tableaux, signatures et sauts de page restent lisibles. | Revue visuelle PDF. | A renseigner | |
| Le nom PDF conserve le nom fonctionnel du DOCX source. | Liste comparee. | A renseigner | |
| Aucun PDF partiel ou manquant n'est declare valide sans reserve. | Rapport PDF. | A renseigner | |

Decision PDF locale :

- `OK` si tous les PDF attendus sont produits, ouvrables et lisibles ;
- `GO avec reserves` possible si le PDF est indisponible pour cause
  d'environnement local documentee, mais le flux DOCX/ZIP reste exploitable ;
- `NO-GO` si un PDF attendu est produit mais illisible, tronque ou rattache au
  mauvais DOCX.

## 5. Revue ZIP

Objectif : verifier que l'archive finale est propre, exploitable et trace ce qui
a ete inclus.

| Controle | Preuve attendue | Statut | Notes |
|---|---|---|---|
| Le ZIP est cree depuis un dossier de sortie identifie. | Chemin source + chemin ZIP. | A renseigner | |
| Les DOCX attendus sont inclus. | Liste du contenu ZIP. | A renseigner | |
| Les PDF attendus sont inclus quand la conversion PDF est validee. | Liste du contenu ZIP. | A renseigner | |
| Les fichiers temporaires, caches et artefacts hors dossier sont exclus. | Inspection ZIP. | A renseigner | |
| Le manifeste technique est present si produit par le backend ZIP. | `manifest.json` ou justification. | A renseigner | |
| Le manifeste liste les formats, chemins et documents inclus. | Extrait manifeste. | A renseigner | |
| Le ZIP s'ouvre et s'extrait dans un dossier propre. | Note d'extraction. | A renseigner | |
| Les noms de fichiers sont lisibles et reproductibles. | Liste comparee. | A renseigner | |

Contenu attendu par defaut :

- DOCX generes par le moteur ;
- PDF generes et valides si le backend PDF a fonctionne ;
- manifeste technique si disponible ;
- aucun fichier de travail, cache, lock Word, sortie temporaire ou artefact hors
  dossier.

## 6. Criteres de go/no-go final

La decision finale doit etre l'une des trois suivantes.

| Decision | Conditions minimales |
|---|---|
| `GO` | Tous les controles bloquants sont `OK`, toutes les preuves minimales sont disponibles, les reserves restantes sont non bloquantes et documentees. |
| `GO avec reserves` | Le flux complet est exploitable, mais des limites non bloquantes restent documentees : dependance PDF locale, corrections visuelles mineures, revue juridique fine non encore signee. |
| `NO-GO` | Au moins un controle bloquant est `KO` ou `BLOCKED`, ou une incertitude juridique/wording empeche la validation. |

Sont bloquants par defaut :

- selection documentaire incorrecte ;
- document attendu non genere ;
- document manuel ou legacy genere automatiquement sans decision explicite ;
- placeholder source residuel dans une sortie finale ;
- erreur de validation moteur masquee par l'UI ;
- derive de wording juridique non validee ;
- PDF illisible, tronque ou rattache au mauvais DOCX pour un document inclus
  dans la recette PDF ;
- ZIP incomplet, inexploitable ou contenant des fichiers hors perimetre ;
- absence de preuve de revue humaine pour un document sensible ;
- impossibilite de reconstituer les chemins des sorties produites.

## Rapport final a produire apres execution

Le rapport de revue finale doit indiquer :

- branche testee ;
- commit teste ;
- contextes utilises ;
- documents selectionnes par contexte ;
- chemins DOCX, PDF et ZIP ;
- statuts moteur, visuel, UI, PDF et ZIP ;
- reserves ouvertes ;
- decision finale `GO`, `GO avec reserves` ou `NO-GO` ;
- prochain ticket recommande.

## Synthese d'execution

| Axe | Statut final | Preuve principale | Reserve |
|---|---|---|---|
| Moteur | A renseigner | A renseigner | A renseigner |
| Visuel | A renseigner | A renseigner | A renseigner |
| UI | A renseigner | A renseigner | A renseigner |
| PDF | A renseigner | A renseigner | A renseigner |
| ZIP | A renseigner | A renseigner | A renseigner |
| Decision finale | A renseigner | A renseigner | A renseigner |

## Prochaine etape recommandee

Executer la recette finale sur la branche de cloture V1, renseigner les preuves
dans un rapport d'execution dedie, puis lancer `CLOSE-PROJECT-V1-001` seulement
si la decision est `GO` ou `GO avec reserves`.
