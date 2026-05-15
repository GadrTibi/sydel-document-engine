# DAAT x SYDEL - STRATEGIE V1
## Sous-famille `cumul_salariee`

## 1. Objet

Ce fichier formalise la strategie V1 du cas `cumul_salariee` pour la famille
documentaire `derogations`.

Il ne code rien, ne modifie aucun wording juridique source et ne modifie aucun
fichier de pilotage partage.

Ticket couvert :
- `SPEC-DEROG-SALARIEE-MANUAL-001`

## 2. Sources relues

Memoire projet et workflow :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Specs et preparation Lot 03 :
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`
- `docs/delivery/lot_03_derogations_spec_texte_v1.md`
- `docs/delivery/lot_03_derogations_arbitrages_v1.md`
- `docs/delivery/lot_03_derogations_preparation_v1.md`
- `docs/delivery/lot_03_derogations_legacy_conversion_report_v1.md`

Source legacy concernee :
- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

## 3. Pourquoi le cas reste bloque

Le cas `cumul_salariee` reste bloque en V1 pour une raison documentaire et non
fonctionnelle :

- la seule source identifiee est un ancien fichier Word binaire `.doc` ;
- aucune conversion locale fiable en DOCX propre n'a ete produite ;
- aucun fichier cible
  `project/source_documents/lot_03/Demande_derogation_cumul_SELARL_salariee.docx`
  n'est disponible ;
- la tentative de conversion Word COM documentee a expire et n'a pas livre de
  DOCX validable ;
- les outils headless alternatifs n'etaient pas disponibles localement au moment
  du rapport de conversion ;
- le pipeline documentaire interdit de coder un document depuis une source legacy
  non stabilisee ;
- le contenu source couvre aussi une `activite externe`, ce qui doit rester
  visible dans les futurs tickets meme si la cle canonique V1 reste
  `cumul_salariee`.

Decision V1 :
- ne pas creer de generateur pour `cumul_salariee` ;
- ne pas convertir approximativement le `.doc` ;
- ne pas reconstruire le texte a la main depuis l'extraction ;
- ne pas presenter ce document comme automatisable tant qu'une source DOCX
  propre n'est pas fournie ou qu'une conversion fiable n'est pas validee.

## 4. Ce qui peut etre automatise autour

Le moteur peut gerer le cas autour du document sans automatiser le document
lui-meme.

Automatisation documentaire autorisee autour de `cumul_salariee` :
- conserver la cle canonique `derogation.type = cumul_salariee` dans la strategie
  documentaire V1 ;
- identifier le cas comme une piece attendue lorsque le contexte dossier indique
  une derogation de cumul salariee ou d'activite externe ;
- documenter le statut `bloque_source_legacy` ou equivalent dans un futur
  registre de suivi ;
- orienter l'utilisateur vers une production manuelle ou une fourniture de source
  propre ;
- inclure, dans un futur ZIP dossier, une note de piece manuelle attendue si le
  registre le prevoit explicitement ;
- bloquer explicitement toute generation finalisee de ce document avec un message
  de cause source, plutot qu'echouer silencieusement.

Pre-remplissage qui deviendra possible uniquement apres deblocage source :
- `ordre.ville` ;
- `signataire.prenom` ;
- `signataire.nom` ;
- `signataire.numero_inscription_ordre` ;
- `signataire.qualification_principale` ;
- `societe.siege.adresse_affichee` ;
- `site_declare.adresse_affichee` ;
- `signature.date`.

Ces champs sont deja identifies dans la spec texte, mais ils ne suffisent pas a
autoriser un generateur sans source DOCX propre.

## 5. Ce qui doit rester manuel

Restent manuels en V1 :

- la production effective de la demande `cumul_salariee` ;
- la validation du wording apres conversion ou remplacement de source ;
- les cases cochees sur les criteres de demande ;
- l'explication associee a chaque case cochee ;
- les renseignements sur l'activite a la residence professionnelle habituelle ;
- les dispositions de continuite des soins ;
- la reponse aux urgences ;
- l'organisation pratique pour les patients pris en charge dans le cadre de la
  SEL ;
- la signature manuscrite ;
- toute qualification metier entre `salariee` et `activite externe` si elle
  implique un renommage moteur ou une variante texte.

Regle :
- aucune zone narrative sensible ne doit etre inventee par le moteur ;
- aucune case ne doit etre cochee par inference ;
- aucune formulation juridique ne doit etre corrigee, feminisee ou enrichie sans
  ticket explicite de validation.

## 6. Condition exacte de deblocage futur

Le cas `cumul_salariee` pourra etre debloque seulement si toutes les conditions
suivantes sont reunies :

1. un DOCX propre est fourni ou produit de maniere reproductible depuis la source
   legacy ;
2. le DOCX est place dans `project/source_documents/lot_03/` ou son emplacement
   executable est arbitre explicitement ;
3. le DOCX est relu techniquement comme archive OpenXML valide avec
   `word/document.xml` present ;
4. les placeholders attendus sont compares avec la source legacy et confirmes
   sans perte fonctionnelle ;
5. le texte extrait est compare au wording source et toute derive est signalee
   pour validation ;
6. la strategie de rendu est tranchee entre `document finalise` et
   `formulaire a completer` ;
7. les champs narratifs obligatoires, cases cochees et explications sont soit
   fournis explicitement par le contexte, soit la generation finalisee bloque ;
8. un ticket de code dedie autorise explicitement l'implementation de
   `cumul_salariee`.

Tant que l'une de ces conditions manque, le statut V1 reste :

- `cumul_salariee` identifie ;
- source legacy localisee ;
- document non automatisable ;
- production manuelle ou attente de source propre.

## 7. Strategie retenue

La strategie V1 est donc une strategie de blocage explicite et tracable :

- maintenir `cumul_salariee` comme sous-famille canonique V1 ;
- ne pas renommer automatiquement en `cumul_activite_externe` ;
- ne pas coder depuis le `.doc` legacy ;
- autoriser seulement le suivi, le signalement et le blocage propre autour du
  cas ;
- reporter toute generation DOCX a un futur ticket apres livraison ou conversion
  validee d'une source DOCX propre.
