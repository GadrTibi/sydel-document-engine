# SPFPL — Statut de fondation

> Tâche : fondation + prompts NotebookLM SPFPL (lecture seule Drive/repo ; écriture cantonnée à
> `project/source_documents/spfpl/` et `docs/project/types/SPFPL/` ; aucun `src/`, aucun Git).
> Date : 2026-06-05. **Génération NO-GO** tant que la carte des cas et le wording ne sont pas confirmés
> (NotebookLM → Rafael). Voir `CARTOGRAPHIE_TENTATIVE.md` (la carte officielle V1 existe mais est
> partielle et a disparu en V2/V3 — c'est la question n°1).

## 1. Ce que Codex a DÉJÀ fait pour SPFPL dans `src/` — À RE-VÉRIFIER (zéro confiance)

Constaté par lecture de fichiers (existence + contenu superficiel), **non testé, non validé** :

- **Cas déclarés** dans `domain/case_catalog.py` : `CaseType.SPFPL_CESSION = "SPFPL cession"` et
  `CaseType.SPFPL_APPORT = "SPFPL apport"`, avec leurs `DocumentOccurrence` (docs « dans tous les cas »,
  statuts, PV nomination gérant, demande ordre, note d'info, régime communautaire conditionnel, PV
  agrément associé unique / plusieurs, acte cession parts vs actions, et pour l'apport : contrat
  d'apport, attestation capital, attestation commissaire). **Mappe de près la carte V1** — donc Codex a
  vraisemblablement utilisé le canon V1, PAS inventé. À confirmer fidélité ligne à ligne.
- **Statuts (lot_04)** : `statuts_spfpl_apport.py`, `statuts_spfpl_cession.py`, `statuts_spfpl_common.py`,
  `statuts_spfpl_templates.py` ; + `statuts_sas.py` (SAS / SPFPL médecins).
- **Actes & satellites (lot_05)** : `acte_cession_parts_spfpl.py`, `acte_cession_actions_spfpl.py`,
  `contrat_apport_spfpl.py`, `attestation_commissaire_apports.py`,
  `attestation_capital_liste_souscripteurs.py` (+ `_sas`), `note_information.py`,
  `pv_agrement_cession_spfpl_associe_unique.py`, `pv_agrement_cession_spfpl_plusieurs_associes.py`,
  `pv_agrement_common.py`, `spfpl_common.py`.
- **Registre** (`registry/catalog.py`) : entrées `canonical_name` pour Statuts SPFPL cession/apport,
  Statuts SAS/SPFPL médecins, Note d'information SPFPL, PV agrément (unique / plusieurs), Acte de cession
  de parts SPFPL, Acte de cession d'actions SPFPL à un tiers, Contrat d'apport SEL→SPFPL, Attestation
  capital/souscripteurs SPFPL (+ SAS), Attestation nomination commissaire aux apports.
- **`source_path` du registre** pointe vers `project/source_documents/lot_04/...` et `lot_05/...`
  (ex. `Statuts_SPFPLAS_dentistes_cession.docx`, `Acte_cession_SPFPL_tiers_modele.docx`) — donc Codex a
  déjà rangé une partie des modèles SPFPL **dans l'arbre partagé `lot_*`**, pas dans un dossier `spfpl/`.

### Points à RE-VÉRIFIER en priorité (ne jamais croire l'auto-rapport)
1. **Fidélité de la carte** : les `DocumentOccurrence` SPFPL collent-ils EXACTEMENT au canon V1 ? (Quelle
   version du canon Codex a-t-il suivie ?)
2. **Génération réelle** : chaque générateur produit-il un DOCX **sans token résiduel** `[...]`, en
   masculin ET féminin ? (Aucune preuve d'exécution constatée.)
3. **Couverture** : `acte_cession_actions_spfpl.py` existe alors que le canon V1 ne nomme PAS de modèle
   pour la cession d'actions → d'où vient sa source ? (Probable `Acte_cession_SPFPL_tiers_modele.doc`,
   legacy `.doc` non tokenisé — à vérifier.)
4. **`scenarios/`** : il n'y a **PAS** de fixtures SPFPL (`scenarios/` ne contient que `selarl.py`).
5. **Front** : il n'y a **PAS** de slice SPFPL (`front_app/` n'a que `selarl_slice.py`). SPFPL n'est donc
   **pas pilotable depuis l'UI**.

## 2. Ce qui MANQUE

### Côté sources / canon (bloquant métier)
- **Carte des cas non confirmée** : V1 contient SPFPL (cession + apport) ; V2/V3 l'ont retirée. → Bloc A
  des prompts NotebookLM. **Tant que ce n'est pas tranché, la fondation reste un dérivé non ratifié.**
- **3 modèles legacy `.doc` non récupérés** (illisibles `python-docx`, donc ni inventoriés ni copiés) :
  `Acte_cession_parts_Dr_SPFPL_modele.doc`, `Acte_cession_SPFPL_tiers_modele.doc`,
  `PV SPFPL autorisation empruntt - transforme.doc` → à reconvertir en `.docx` ou re-fournir tokenisés.
- **PV de nomination du gérant SPFPL** : réclamé par la carte, pas de modèle SPFPL tokenisé trouvé.
- **Variantes de contenu non arbitrées** : quel « Note d'information » / « Attestation » / « Contrat
  d'apport » est canonique (Bloc D).
- **Documents hors carte** (Liste souscripteurs, Appel des fonds, RM Sydel, SAS médecins/pharmaciens) :
  périmètre à confirmer (Bloc C).

### Côté technique
- Fixtures `scenarios/spfpl.py` (source unique du futur bouton « données de test »).
- Slice front `front_app/spfpl_slice.py` + câblage wizard (qualification cession/apport, sous-formulaires).
- Tests dédiés SPFPL (codes par cas, génération via chemin UI sans token résiduel, masculin/féminin).
- **Décision de placement des sources** : aujourd'hui Codex lit dans `lot_*` ; ce dépôt-ci a copié les 33
  modèles dans `project/source_documents/spfpl/` (staging par type, conforme au périmètre d'écriture
  imposé). À réconcilier : conserver l'arbre `lot_*` (convention moteur actuelle) OU migrer vers `spfpl/`.

## 3. Modèles récupérés (ce qui a été ÉCRIT par cette tâche)
- 44 `.docx` Drive → **33 distincts par contenu** copiés dans `project/source_documents/spfpl/`
  (dédup md5, noms NFC nettoyés ; variantes de contenu conservées et suffixées). Détail + tokens :
  `INVENTAIRE_MODELES.md`. (3 legacy `.doc` non copiés — cf. ci-dessus.)

## 4. PLAN DE FONDATION ordonné (à exécuter une fois les cas connus)

Suit `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. **Étape 0 = débloquer le métier ; aucune ligne de
code SPFPL n'est ratifiée avant.**

0. **Confirmer la carte (Phase 1-2 du workflow)** : envoyer Bloc A NotebookLM ; si insuffisant → message
   Rafael. Trancher : version du canon faisant foi, liste des cas, forme sociale (SARL/SAS), périmètre des
   docs hors carte. Consigner au journal de décisions (codes `SPFPL-...`).
1. **Geler les sources (Phase 1)** : choisir le modèle canonique de chaque variante (Bloc D), reconvertir
   les 3 `.doc` legacy, trouver/valider le PV nomination gérant. Décider l'emplacement (`lot_*` vs
   `spfpl/`) et l'aligner avec le registre.
2. **Cartographie ratifiée (Phase 2)** : remplacer `CARTOGRAPHIE_TENTATIVE.md` par une matrice cas→docs
   confirmée ; vérifier que `case_catalog.py` y est fidèle (corriger les écarts).
3. **Moteur (Phase 3)** : re-vérifier chaque générateur SPFPL (0 token résiduel, fidélité au modèle gelé) ;
   écrire `scenarios/spfpl.py` (contextes Pydantic complets, réutilisés par l'UI).
4. **Règles juridiques (Phase 4)** : purge coquilles inter-profession, durées (société vs domiciliation),
   origine de propriété (vendeur), commissaire aux apports paramétrable (Bloc F + D).
5. **Genre / nombre (Phase 5)** : paires de chaînes exactes (jamais de regex), genre par personne ;
   pluriel/nombre d'associés seulement après validation dédiée.
6. **UI Streamlit (Phase 6)** : `spfpl_slice.py` + sous-formulaires par cas (cession / apport / régime
   communautaire / associé unique vs plusieurs) ; étendre le bouton « données de test » sur les fixtures.
7. **Vérification (Phase 7)** : `ruff` clean + suite COMPLÈTE verte (chiffres), DOCX ouverts (0 crochet
   résiduel), masculin ET féminin, création/cession intactes. Revue de fidélité (pas d'auto-rapport).
8. **Gate juridique (Phase 8)** : génération NO-GO tant que Rafael/Albane n'a pas validé le wording neuf ;
   tests sur branche `spfpl/...` (jamais merge `main` en autonomie).
9. **Journal & clôture (Phase 9)** : décisions ratifiées (codes stables), état courant + registre tickets,
   leçons reversées dans le workflow. Merge + déploiement = geste PM.
