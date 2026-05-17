# Cadre de recette finale V1

Ticket : `RECIPE-FRAME-001`

Date : 2026-05-17

## Objet

Ce document prepare un cadre de recette finale executable pour qualifier le flux
V1 complet :

`contexte dossier -> selection documentaire -> DOCX -> PDF -> ZIP -> revue humaine`

Il ne modifie aucun code Python, aucun fichier de pilotage projet et aucun
wording juridique. Il ne vaut pas validation juridique : il organise les
controles techniques, visuels et fonctionnels a executer avant decision finale.

## References de cadrage

- `AGENTS.md`
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`
- `docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md`
- `docs/project/18_NEXT_PHASE_FOUNDATION_V1.md`
- `docs/review/lot_02_orchestrator_smoke_review_v1.md`
- `docs/review/lot_03_batch_review_v1.md`
- `docs/review/lot_04_batch_review_v1.md`
- `docs/review/lot_05_batch_review_v1.md`

## Prerequis de recette

Avant d'executer la recette finale, verifier que :

- le moteur DOCX V1 expose bien `DOC-001` a `DOC-043` ;
- les contextes de recette sont figes et versionnes ou identifies ;
- l'UI V0 est utilisable, ou une commande de generation dossier stabilisee est disponible ;
- le convertisseur PDF retenu est installe et documente ;
- le builder ZIP est disponible ;
- les exclusions V1 sont listees : documents manuels, sources legacy bloquees,
  cas non arbitres, validation juridique fine.

Chaque controle doit produire une preuve : chemin de fichier, capture, log,
rapport de test, hash d'archive ou note de revue humaine.

## Statuts de controle

Utiliser les statuts suivants pour chaque ligne de recette :

| Statut | Sens |
|---|---|
| `OK` | Controle execute, resultat conforme, preuve disponible. |
| `KO` | Controle execute, resultat non conforme, ticket correctif requis. |
| `NA` | Controle non applicable au cas recette, justification obligatoire. |
| `BLOCKED` | Controle impossible a executer, cause precise obligatoire. |

## 1. Verifications moteur

Objectif : confirmer que la selection documentaire et la generation DOCX restent
deterministes avant de tester UI, PDF et ZIP.

| Controle | Preuve attendue | Statut |
|---|---|---|
| Catalogue et registre orchestrateur alignes sur `DOC-001` a `DOC-043`. | Sortie de test ou rapport confirmant l'alignement. | A renseigner |
| `select_documents_for_context` retourne la liste attendue pour chaque contexte de recette. | Liste des `doc_id` selectionnes par contexte. | A renseigner |
| `generate_documents` produit les DOCX attendus dans un dossier propre. | Dossier de sortie + liste des fichiers generes. | A renseigner |
| Aucun document marque manuel ou legacy bloque n'est genere automatiquement. | Liste des exclusions controlees. | A renseigner |
| Aucun placeholder source visible de type `[` / `]` ne subsiste dans les DOCX generes. | Rapport d'inspection texte/OpenXML. | A renseigner |
| Les erreurs de validation moteur sont explicites quand une donnee obligatoire manque. | Cas negatif + message d'erreur capture. | A renseigner |
| Les tests automatises de reference passent sur la branche de recette. | Sortie `ruff` / `pytest` ou justification si non executes. | A renseigner |

## 2. Verifications visuelles

Objectif : preparer la revue humaine des rendus DOCX et PDF sans la confondre
avec une validation juridique.

| Controle | Preuve attendue | Statut |
|---|---|---|
| Les titres, intertitres, listes, tableaux et signatures sont lisibles dans Word. | Note de revue par document ou par famille. | A renseigner |
| Les documents signales comme plus courts que la source sont compares aux grandes sections attendues. | Checklist de sections presentes/absentes. | A renseigner |
| Les formulaires a completer restent clairement identifiables comme incomplets. | Capture ou note de revue. | A renseigner |
| Les statuts et documents longs conservent une numerotation exploitable. | Revue humaine des articles et annexes. | A renseigner |
| Les zones de signature sont presentes et non compactees. | Revue humaine ou capture. | A renseigner |
| Les anomalies deja signalees dans les revues Lot 03, Lot 04 et Lot 05 sont reprises en points d'attention. | Tableau de suivi des points de revue. | A renseigner |

## 3. Verifications UI

Objectif : verifier que l'interface pilote le moteur sans logique metier cachee
et sans masquer les blocages.

| Controle | Preuve attendue | Statut |
|---|---|---|
| Chargement d'un contexte YAML ou JSON de recette. | Capture UI + chemin contexte. | A renseigner |
| Affichage du type de dossier, de la structure et des options principales. | Capture UI. | A renseigner |
| Previsualisation de la selection documentaire avant generation. | Capture liste `doc_id` / libelles. | A renseigner |
| Generation DOCX depuis l'UI sur au moins un dossier representatif. | Dossier de sortie + capture succes. | A renseigner |
| Affichage lisible des erreurs moteur sur un contexte incomplet. | Capture erreur + contexte negatif. | A renseigner |
| Aucun champ UI ne deduit une regle juridique non portee par le moteur ou les specs. | Note de revue fonctionnelle. | A renseigner |
| L'UI ne presente pas une revue technique comme validation juridique finale. | Revue des libelles UI. | A renseigner |

## 4. Verifications PDF

Objectif : verifier que les PDF sont derives des DOCX generes, sans modifier le
contenu juridique.

| Controle | Preuve attendue | Statut |
|---|---|---|
| Un PDF est produit pour chaque DOCX attendu dans le cas de recette. | Correspondance DOCX -> PDF. | A renseigner |
| Les echecs de conversion sont traces avec cause precise. | Log ou rapport de conversion. | A renseigner |
| Les fichiers PDF s'ouvrent localement. | Note d'ouverture ou capture. | A renseigner |
| Les titres, tableaux, signatures et sauts de page restent lisibles en PDF. | Revue visuelle PDF. | A renseigner |
| Le PDF conserve le meme nom fonctionnel que le DOCX source. | Liste des fichiers compares. | A renseigner |
| Aucun PDF partiel ou manquant n'est considere valide sans reserve explicite. | Rapport de recette PDF. | A renseigner |

## 5. Verifications ZIP

Objectif : controler que l'archive finale contient uniquement les sorties
attendues, avec une structure stable et tracable.

| Controle | Preuve attendue | Statut |
|---|---|---|
| Le ZIP est cree a partir d'un dossier de sortie identifie. | Chemin ZIP + chemin source. | A renseigner |
| Les DOCX attendus sont inclus. | Liste du contenu ZIP. | A renseigner |
| Les PDF attendus sont inclus si le sous-chantier PDF est valide. | Liste du contenu ZIP. | A renseigner |
| Les fichiers temporaires, caches et artefacts hors dossier sont exclus. | Liste negative ou inspection ZIP. | A renseigner |
| Le manifeste technique est present si retenu par la spec ZIP. | Chemin manifeste + contenu minimal controle. | A renseigner |
| Le ZIP s'ouvre et son contenu peut etre extrait dans un dossier propre. | Note d'extraction ou log. | A renseigner |
| Les noms de fichiers restent lisibles et reproductibles. | Liste des noms inclus. | A renseigner |

## 6. Criteres de go/no-go

La decision finale doit etre l'une des trois suivantes :

| Decision | Conditions minimales |
|---|---|
| `GO` | Tous les controles bloquants sont `OK`, les reserves restantes sont non bloquantes et documentees. |
| `GO avec reserves` | Le flux complet fonctionne, mais des corrections visuelles ou documentaires non bloquantes sont ouvertes et listees. |
| `NO-GO` | Au moins un controle bloquant est `KO` ou `BLOCKED`, ou une incertitude juridique/wording empeche la validation. |

Sont bloquants par defaut :

- selection documentaire incorrecte ;
- document attendu non genere ;
- document manuel genere automatiquement sans decision explicite ;
- placeholder source residuel dans une sortie finale ;
- PDF manquant ou illisible pour un document inclus dans la recette PDF ;
- ZIP incomplet, inexploitable ou contenant des fichiers hors perimetre ;
- erreur UI masquant un blocage moteur ;
- derive de wording juridique non validee ;
- absence de preuve de revue humaine pour un document sensible.

## Trame de rapport d'execution

A chaque execution de recette finale, produire un rapport avec :

- date et branche testee ;
- commit teste ;
- contextes utilises ;
- documents selectionnes ;
- chemins des DOCX, PDF et ZIP produits ;
- statuts des controles moteur, visuels, UI, PDF et ZIP ;
- reserves ouvertes ;
- decision `GO`, `GO avec reserves` ou `NO-GO` ;
- prochaine action recommandee.
