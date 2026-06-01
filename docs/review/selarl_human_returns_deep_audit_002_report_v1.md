# SELARL human returns deep audit 002 report V1

Date : 2026-06-01

Ticket : `SELARL-HUMAN-RETURNS-DEEP-AUDIT-002`

## Objet

Relire `C:\Users\Gad\Downloads\Retours humains .docx` et verifier le pack
SELARL courant contre les corrections humaines explicites.

## Verdict

Verdict historique : `CORRIGE - pack 003 requis`.

Note 2026-06-01 : le pack 003 a ensuite ete remplace par le pack 004 apres
audit trois sources, car `DOC-003` contenait encore un doublon `SELARL SELARL`
dans la procuration.

Le pack 002 corrigeait bien `DOC-006`, mais l'audit approfondi a trouve trois
ecarts reels dans le `DOC-004` PV nomination gerant :

- la ligne `En cours d’immatriculation` avait ete supprimee au lieu de rester
  sans la mention `au RCS de Lyon` ;
- le titre avait perdu `DE L’ASSEMBLEE GENERALE` alors que seul
  `EXTRAORDINAIRE` devait etre supprime ;
- le scenario de test affichait `SELARL SELARL MARTIN` quand la denomination
  contenait deja la forme sociale.

Ces ecarts sont corriges dans le generateur.

## Corrections appliquees

Fichier code :

- `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`

Corrections :

- ajout de `En cours d’immatriculation` dans l'en-tete ;
- titre rendu :
  - `PROCES-VERBAL DES DECISIONS`
  - `DE L’ASSEMBLEE GENERALE`
  - `DU {date_decision}`
- garde-fou anti-doublon : si la denomination commence deja par `SELARL`, le
  PV n'ajoute pas une seconde fois la forme dans l'introduction.

Tests ajustes :

- `tests/unit/test_pv_nomination_gerant.py`
- `tests/unit/test_clean_front_app.py`

## Points controles depuis les retours humains

| Document | Controle | Resultat pack 003 |
| --- | --- | --- |
| `DOC-002` Autorisation domiciliation | `dans les locaux du cabinet au [adresse siege]` | OK |
| `DOC-001` Declaration non-condamnation | adresse personnelle avec virgule puis code postal ville | OK |
| `DOC-005` Renonciation conjoint | `À {ville}`, communaute, clause finale | OK |
| `DOC-003` Procuration | suppression RCS/telephone parasite, clause finale apres mandat | OK |
| `DOC-004` PV gerant | pas de RCS ville, pas d'heure, pas d'EXTRAORDINAIRE, titre AGE corrige, en cours d'immatriculation conserve | OK |
| `DOC-016` Statuts dentiste | capital en euros, regime communaute, articles 1 a 34 | OK |
| `DOC-006` Avertissement conjoint | present en regime communautaire, adresse conjoint presente | OK |

## Pack actif apres audit

- Racine : `artifacts/selarl_closing_pack_003/`
- Manifest : `artifacts/selarl_closing_pack_003/manifest_selarl_closing_pack_003.json`
- Rapport pack : `docs/review/selarl_closing_pack_003_report_v1.md`

## Validation technique

- `pytest tests/unit/test_pv_nomination_gerant.py tests/unit/test_clean_front_app.py -q` : 34 passes.
- Tests cibles retours humains/documents : 76 passes.
- `ruff check .` : OK.
- `pytest -q` : 415 passes.

Le pack 004 remplace maintenant le pack 003 pour la validation associe.
