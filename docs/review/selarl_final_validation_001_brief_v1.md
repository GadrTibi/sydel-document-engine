# SELARL final validation 001 brief V1

Ticket : `SELARL-FINAL-ASSOCIE-VALIDATION-001`

Date : 2026-06-03

Statut : `IN_PROGRESS - attente validation finale associe`

## Decision

`GO validation finale`, `NO-GO nouvelles questions abstraites`.

Ce brief remplace les briefs des packs 001, 002, 003 et 004. Le pack 005
integre les retours humains 006, l'audit pack 005, l'incident front adresse
conjoint et l'amendement `DOC-002` du 2026-06-03.

## Pack a revoir

Racine :

- `artifacts/selarl_closing_pack_005/`

Manifest :

- `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`

Rapport :

- `docs/review/selarl_closing_pack_005_report_v1.md`
- `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`
- `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`

## Scenarios a ouvrir

| Scenario | Dossier | Nombre DOCX attendu |
| --- | --- | ---: |
| Medecin simple | `artifacts/selarl_closing_pack_005/medecin_simple/` | 6 |
| Dentiste simple | `artifacts/selarl_closing_pack_005/dentiste_simple/` | 6 |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_005/medecin_regime_communautaire/` | 8 |
| Dentiste regime communautaire | `artifacts/selarl_closing_pack_005/dentiste_regime_communautaire/` | 8 |

## Regle de revue

L'associe ne doit pas etre sollicite pour repondre a des questions dont la
reponse est deja dans les sources ou evidente dans la regle documentaire.

La revue demandee est une revue d'ecarts :

- texte non conforme a la source ;
- variable mal placee ;
- document attendu absent ;
- document en trop ;
- incoherence dans le ZIP ;
- correction juridique concrete a appliquer.

## Points critiques

1. Hors regime communautaire, `DOC-005` et `DOC-006` doivent etre absents.
2. En regime communautaire, `DOC-005` et `DOC-006` doivent etre presents.
3. `DOC-006` doit utiliser l'identite et l'adresse du conjoint.
4. Les textes doivent respecter les sources sans reformulation libre.
5. Les parasites historiques `RCS PARIS 788 531 432` et `0153814303` ne doivent
   pas reapparaitre.
6. Le PV nomination gerant doit conserver `En cours d’immatriculation`, garder
   `DE L’ASSEMBLEE GENERALE`, supprimer `EXTRAORDINAIRE` et ne pas afficher
   `SELARL SELARL`.
7. La procuration ne doit pas afficher `SELARL SELARL` quand la denomination
   contient deja la forme sociale.
8. Les retours humains 006 doivent etre controles par ecarts concrets :
   naissance avec ville, conseil de l'Ordre compose, quatre exemplaires,
   adresse conjoint derivee, signatures sans encadre, adresses CP avant ville,
   accords `associe/associee`, et autorisation de domiciliation `pour 99 ans`.

## Format de retour souhaite

```text
Verdict global : VALIDE / CORRECTIONS / BLOQUE
Scenario :
Document :
Ecart constate :
Correction demandee :
Source ou emplacement :
```

Si tout est bon :

```text
Verdict global : VALIDE
Reserve eventuelle :
```

## Ce que Codex fera au retour

- Si le verdict est `VALIDE`, lancer `SELARL-CANONICAL-CLOSE-001`.
- Si des corrections concretes sont donnees, ouvrir un ticket de correction
  borne et tester le pack a nouveau.
- Si le retour ouvre une variante complexe, la reporter vers
  `SELARL-NEXT-SUBCASE-SELECTION-001`.
