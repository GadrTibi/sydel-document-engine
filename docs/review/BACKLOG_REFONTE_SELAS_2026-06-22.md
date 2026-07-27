# Backlog refonte SELAS — sortie de la MACHINE (2026-06-22)

> Produit par la **machine bloc-gold** (2 organes, lecture seule) en banc d'essai sur la SELAS.
> Premisse : la **SELARL est le gold valide** ; la SELAS doit en deriver par difference justifiee.
> Garde-fou d'execution : **proteger le gold** — tout changement sur un fichier PARTAGE est
> **conditionne SELAS**, jamais une mutation du comportement SELARL valide. Defaut pour un retour
> ambigu « universel vs SELAS-only » : **SELAS-only** (direction reversible).

## Validation de la machine (le banc d'essai a-t-il marche ?)

- **Organe 1 — fidelite au gold** (`machine-fidelite-selas-vs-selarl`) : compare chaque bloc SELAS au
  gold SELARL. **9/15 retours onglet 24 retrouves seul, 0 faux positif**, **+ 4 bugs net-new** (B1-B4)
  que ni Rafael ni l'onglet 24 ne listaient. **Limite nommee** : aveugle aux retours qui demandent de
  S'ECARTER du gold (il lit « conforme » = « identique au gold » ≠ « rien a faire »).
- **Organe 2 — conformite a l'intention ratifiee** (`machine-organe2-conformite-intention-selas`) :
  confronte chaque item onglet 24 au code reel (l'intention voulue = reference, pas le gold).
  **Rattrape les 6 manques de l'organe 1** (#4, 9, 12, 13, 14, 15) avec preuve fichier:ligne.
- **Ensemble : 15/15 cernes + 4 bugs bonus.** La classe « anticipable » est couverte en entier.
  Reste irreductiblement humain : **#4 (UI pure)** + **1 decision de structure de saisie (#12/B3)**.
  **Aucune decision metier neuve** dans ce lot (codable sans Albane/David).

## Backlog (trie A-FAIRE > PARTIEL > FAIT)

| # | Retour | Etat | Reste a coder | Ancre | Partage ? |
|---|---|---|---|---|---|
| 1 | Retirer « lettre de mission / acompte Sydel » de l'ANNEXE 1 SPFPL | A-FAIRE | suppr. 2 lignes du `STATUTS_SPFPL_CESSION_BLOCKS` | `lot_04/statuts_spfpl_templates.py:374-375` | non (SPFPL) |
| 2 | DOC-001 (DNC) nomme avec le nom du dirigeant | A-FAIRE | `_rename_with_slug()` applique a DOC-001 | `lot_01/declaration_non_condamnation.py:19` ; `selas_multi_slice.py:1602-1623` | non |
| 9 | Supprimer le champ « profession » (garder « qualification ») | A-FAIRE | retirer form+modele+generateurs+fallback | `selas_multi_slice.py:762,785` ; `models.py:678` | **a verifier** (modele civil) |
| 10 | Menu cabinet_type → derive de la profession | A-FAIRE | suppr. champ UI + derivation medical/dentaire | `business_wizard.py:294-305,380-391` ; `selarl_form_schema.py:22,247` | **oui** (gold) |
| 11 | Cession : vendeur = associe SELECTIONNABLE (pas « unique ») | A-FAIRE | wording + selectbox + peupler depuis l'associe choisi | `shell.py:1976` ; `selas_multi_slice.py:1132-1175` | **oui** (gold) |
| 12 | Siege = « meme adresse que le lieu d'exercice » | A-FAIRE | relabel/rekey checkbox + copie depuis lieu_exercice ; **point dur** : 1 champ libre vs 4 structures | `selas_multi_slice.py:282-286,324,335-339` | non |
| 13 | CA + exercices NON facultatifs (requis) | A-FAIRE | retirer « (facultatif) » + bloqueurs `_cession_blockers` | `shell.py:2285,2289` ; `selarl_slice.py:417-485` | **oui** (gold) |
| 14 | Cession : generer ACTE ET COMPROMIS ensemble | A-FAIRE | `_cession_cabinet_enabled` ne filtre plus sur etape | `orchestrator/service.py:343-352` ; `lot_03/cession_cabinets_common.py:149-165` | **oui** (gold) |
| 15 | Retirer le bloc « acquereur » du formulaire cession | A-FAIRE | suppr. bloc UI + cle `acquereur` du payload | `shell.py:2094-2140,2528` ; `models.py:348-358` | **oui** (gold) |
| 7 | Non-cumul des roles : un seul Directeur General | PARTIEL | validation bloquant >1 « Directeur General » | `selas_multi_slice.py:694-714,968` | non |
| 8 | Date naissance + adresse saisies 2x | PARTIEL | conditionner pour ne pas redemander | `selas_multi_slice.py:654-658,757,763` | non |
| 4 | Icone « copier » par champ | A-FAIRE (NON-MOTEUR) | refonte `_ts`/`_is` (rendu UI) | `front_widgets.py:1790-1803` | UI |
| 3 | Adresses ordre saut de ligne CP/ville | FAIT | — | `selarl_slice.py:899-901` | — |
| 5 | Valeur nominale auto | FAIT | — | `field_derivations.py:110` | — |
| 6 | Repeater multi-associes 2-6 | FAIT | — | `selas_multi_slice.py:271-412` | — |

### Bugs bonus organe 1 (hors onglet 24)

| # | Bug | Reste a coder | Ancre |
|---|---|---|---|
| B1 | `acquereur.forme_sociale` reste « SELARL » dans actes/compromis cession SELAS | post-corriger le `CessionContext` en SELAS multi (cf. `selas_uni_medecin_slice.py:444-448` pour societe) | `selas_multi_slice.py` (build cession) |
| B2 | Bloc mariage SELAS MULTI : conjoint collecte mais AUCUN token injecte, statut brut | injecter tokens + reformater via `statuts_sel_matrimonial_clause` | `selas_multi_slice.py` ; `statuts_selas_multi.py` |
| B3 | Champ « Siege » libre EN PLUS des 4 champs structures (SELAS UNI est propre) | supprimer le champ siege libre, s'aligner sur `seed_siege_from_perso` | `selas_multi_slice.py:~324` |
| B4 | Triple saisie d'adresse (associe marie-communautaire ET dirigeant) | mutualiser avec #8 | `selas_multi_slice.py:654-658,763,772` |

> Recoupements : **B3 ↔ #12** (zone siege) ; **B4 ↔ #8** (zone adresse/dirigeant). A traiter ensemble.
> Fichiers chauds (edition serielle obligatoire, pas de parallele) : `selas_multi_slice.py` (10),
> `shell.py` (4), `models.py` (3).

## Ordre de chantier (machine)

1. **Suppressions seches isolees** : #1 (SPFPL), puis SELAS-only B1, B3.
2. **Zone associe/dirigeant** : #7 + #8 + B4 (meme fonction).
3. **Zone siege** : #12 + B3.
4. **Bloc mariage** : B2.
5. **Zone cession** (partage → SELAS-conditionnel) : #11 + #13 + #14 + B1 + #2 + #15.
6. **Derivation** : #9, #10.
7. **#4 → audit UI/render separe** (non-moteur).

## Deploiement

Streamlit Cloud auto-deploie sur push de `sprint/engine-completion` ; les clients testent. Donc :
**commits locaux uniquement**, **pas de push** tant que Gad n'a pas ouvert la fenetre de test.
