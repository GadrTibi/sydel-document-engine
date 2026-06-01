# SELARL three-source alignment 004 report V1

Date : 2026-06-01

Ticket : `SELARL-THREE-SOURCE-AUDIT-004`

## Objet

Verifier le perimetre SELARL actif avec les trois sources demandees par Gad :

1. le document de reference `project/source_truth/Documents_a_generer_par_cas.docx` ;
2. les retours modele / NotebookLM deja notes dans le repo, notamment
   `project/source_truth/notebooklm_selarl_10_prompts_v1.md`,
   `docs/review/selarl_notebooklm_reconciliation_001_report_v1.md` et
   `docs/project/SELARL_SOURCE_HIERARCHY_V2.md` ;
3. le retour humain `C:\Users\Gad\Downloads\Retours humains .docx`.

## Verdict

Verdict : `GO validation associe` uniquement sur le perimetre actif
SELARL simple medecin / chirurgien-dentiste + regime communautaire.

Verdict : `NO-GO cloture globale SELARL 100 %` pour tous les cas complexes.

Le controle trois sources a trouve un vrai ecart dans le pack 003 :

- `DOC-003` procuration contenait encore `SELARL SELARL MARTIN`.

Le pack 003 est donc supplante. La correction est appliquee dans le generateur
`DOC-003`, et le pack actif devient :

- `artifacts/selarl_closing_pack_004/`
- `artifacts/selarl_closing_pack_004/manifest_selarl_closing_pack_004.json`

## Alignement par source

### Source 1 - Documents a generer par cas

La source de reference liste pour SELARL :

- documents dans tous les cas : declaration de non-condamnation et autorisation
  de domiciliation ;
- coeur SELARL : PV nomination gerant, demande d'inscription a l'ordre,
  declaration de non-condamnation et autorisation de domiciliation ;
- statuts selon profession : chirurgien-dentiste ou medecin ;
- regime communautaire : lettre de renonciation et lettre d'avertissement ;
- branches conditionnelles non fermees ici : site distinct, SCM, derogation,
  cession, bail, appel de fonds.

Pack 004 :

- medecin simple : 6 DOCX ;
- dentiste simple : 6 DOCX ;
- medecin regime communautaire : 8 DOCX ;
- dentiste regime communautaire : 8 DOCX.

Conclusion : conforme au perimetre actif. Les branches complexes restent hors
cloture et ne doivent pas etre presentees comme terminees.

### Source 2 - Retours modele / NotebookLM

NotebookLM et la reconciliation deja versionnee fixent surtout :

- vocabulaire : `Fiche Client`, `Praticien`, `Associe`, `Gerant`,
  `Mandataire` ;
- logique unipersonnelle : le praticien peut alimenter associe unique, gerant
  et signataire quand le dossier est unipersonnel ;
- distinction des adresses : personnelle, siege, domiciliation, conjoint ;
- prudence produit : un document techniquement generable n'est pas
  automatiquement juridiquement final ;
- documents manuels ou complexes : ne pas les lancer en generation automatique.

Pack 004 et front Track B :

- le dossier simple reuse le praticien comme associe unique / gerant /
  signataire ;
- la domiciliation utilise le siege ;
- l'adresse personnelle reste distincte dans `DOC-001` et `DOC-003` ;
- l'adresse du conjoint est presente dans `DOC-006` ;
- les cas cession / SCM / site distinct / derogation restent exclus ou bloques.

Conclusion : conforme au role de NotebookLM sur le perimetre actif. Les pistes
NotebookLM non arbitrees, comme le mode projet generalise ou les 62 variantes,
restent hors cloture.

### Source 3 - Retours humains

Retours humains controles dans le pack 004 :

| Document | Retour humain | Resultat pack 004 |
| --- | --- | --- |
| `DOC-001` | adresse personnelle `demeurant au ... cp ville` | OK |
| `DOC-002` | domiciliation `dans les locaux du cabinet au ...` | OK |
| `DOC-003` | pas de parasite RCS/telephone, clause finale, pas de `SELARL SELARL` | OK |
| `DOC-004` | conserver `En cours d'immatriculation`, retirer `au RCS de ...`, retirer seulement `EXTRAORDINAIRE`, garder `DE L'ASSEMBLEE GENERALE` | OK |
| `DOC-005` | `A/À` ville corrige, communaute corrigee, clause finale | OK |
| `DOC-006` | present avec `DOC-005` si regime communautaire | OK |
| `DOC-016` | capital en euros, regime communaute, articles 1 a 34 | OK sur le perimetre verrouille |

Conclusion : les retours humains connus sont traites sur le pack 004.

## Ce qui reste vrai

Le pack 004 est le bon pack a transmettre a l'associe pour une validation finale
concrete.

Il ne faut plus transmettre le pack 003, car il contenait un ecart dans
`DOC-003`.

La SELARL globale tous cas confondus reste partielle : cession, SCM, site
distinct, derogations, plusieurs gerants et statuts multi-associes complets
restent a traiter par sous-cas separes.

