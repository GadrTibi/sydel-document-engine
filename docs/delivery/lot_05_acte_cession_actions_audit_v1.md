# DAAT x SYDEL - AUDIT SOURCE V1
## Acte de cession d'actions SPFPL

Ticket : `PREP-ACTE-ACTIONS-001`

## 1. Objet

Confirmer documentairement si une vraie source d'acte de cession d'actions existe pour le batch SPFPL.

Ce fichier ne code rien, ne modifie aucun wording juridique source et ne remplace pas une future analyse/spec dediee.

## 2. Sources lues

Memoire projet et cadrage :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_05_spfpl_arbitrages_v1.md`

ADR applicables :
- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0005-codex-working-mode.md`

Corpus documentaire :
- `project/source_truth/Documents_a_generer_par_cas.docx`
- tout le contenu inventorie de `project/source_import/raw_drive_dump/` : 144 fichiers
- tout le contenu inventorie de `project/source_documents/` : 37 fichiers

## 3. Methode

Recherches effectuees :
- inventaire des chemins avec `rg --files` ;
- recherche texte/fichier sur `cession`, `actions`, `acte`, `SPFPL`, `titre`, `titres` ;
- extraction texte des `.docx` et du document de reference ;
- extraction best-effort des anciens `.doc` Word pour les candidats SPFPL ;
- comparaison des candidats avec les documents proches deja places dans `source_documents/lot_05`.

Termes de controle principaux :
- `Cession d'actions`
- `OBJET DU CONTRAT : CESSION D'ACTIONS`
- `nb_actions_cedees`
- `Actions Cedees`
- `cession de parts`
- `parts sociales`

## 4. Constat source de verite

Dans `project/source_truth/Documents_a_generer_par_cas.docx`, le bloc `SPFPL cession` inventorie :
- `Acte de cession de parts` avec le fichier `Acte_cession_SPFPL_tiers_part_modele.docx` ;
- `Acte de cession d'actions` sans fichier source explicite associe.

Le document est donc bien inventorie, mais la source de verite ne donnait pas le nom du fichier attendu pour l'acte d'actions.

## 5. Candidats plausibles verifies

| Candidat | Emplacement | Verdict | Justification |
|---|---|---|---|
| `Acte_cession_SPFPL_tiers_modele.doc` | `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Cession/` | source trouvee | Le corps contient un titre `Cession d'actions`, la formule `cession des actions de la Societe`, une societe au capital divise en `[nb_actions] actions`, le bloc `OBJET DU CONTRAT : CESSION D'ACTIONS`, puis `[nb_actions_cedees] actions`, `Actions Cedees` et `Titres Cedes`. |
| `Acte_cession_SPFPL_tiers_part_modele.docx` | `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Cession/` et `project/source_documents/lot_05/` | non retenu pour actions | Source confirmee d'acte de cession de parts. Le texte vise des parts/parts sociales, pas l'acte d'actions. |
| `Acte_cession_parts_Dr_SPFPL_modele.doc` | `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Cession/` | non retenu pour actions | Le titre extrait est `Acte de cession Des parts sociales de la SELARL`. |
| PV agrement cession SPFPL | `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/PV agrément cession/` et `project/source_documents/lot_05/` | non retenu | PV d'agrement, pas acte de cession. |
| Statuts SPFPL / attestation capital / contrat d'apport / listes souscripteurs | raw dump et `source_documents/lot_04` / `source_documents/lot_05` | non retenu | Ces fichiers peuvent mentionner des actions ou des titres, mais ne constituent pas un acte de cession d'actions. |
| Actes de cession de cabinets et cessions SCM | lots 03 et raw dump SELARL/SELAS | non retenu | Documents d'autres familles documentaires, hors acte de cession d'actions SPFPL. |

Hash SHA-256 du candidat retenu :

```text
CEB0B34231993E5054C450A1EAB4C6EA2C2E9929C117A3AE312F769486BEC674
```

## 6. Conclusion

Source trouvee : oui.

Source confirmee comme DOCX placee dans `project/source_documents/lot_05/` : non.

Source retenue :
- `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Cession/Acte_cession_SPFPL_tiers_modele.doc`

Niveau de confiance : eleve.

Raisons :
- le titre, l'objet du contrat et le vocabulaire central convergent vers un acte de cession d'actions ;
- les variables source sont coherentes avec des actions : `[nb_actions]`, `[nb_actions_cedees]`, actions de la societe cedee ;
- les candidats voisins `tiers_part` et `parts_Dr` sont explicitement des actes de cession de parts et ne doivent pas servir de substitut.

Reserve :
- le fichier trouve est un ancien `.doc` present uniquement dans le raw dump ;
- il n'est pas encore converti ou place comme source canonique dans `project/source_documents/lot_05/` ;
- les specs/arbitrages SPFPL existants doivent etre mis a jour avant tout codage, car ils constataient auparavant une absence de source confirmee.

## 7. Prochaine action recommandee

1. Valider humainement que `Acte_cession_SPFPL_tiers_modele.doc` est bien la source canonique attendue pour `Acte de cession d'actions`.
2. Convertir ou remplacer ce `.doc` par un DOCX source propre, puis le placer dans `project/source_documents/lot_05/`.
3. Creer une spec canonique et une spec texte dediees avant toute implementation.
4. Maintenir le blocage code tant que la source n'est pas placee/validee et que les specs ne sont pas ecrites.
