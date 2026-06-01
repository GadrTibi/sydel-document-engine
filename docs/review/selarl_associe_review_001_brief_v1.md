# SELARL associe review 001 brief V1

Ticket : `SELARL-ASSOCIE-REVIEW-001`

Date : 2026-06-01

Statut : `IN_PROGRESS - attente retour humain`

## Decision

`GO revue humaine`, `NO-GO dev`.

Ce ticket sert a faire relire ou tester le pack SELARL simple par l'associe ou
juriste. Il ne modifie ni le code, ni les generateurs, ni le moteur, ni les
sources de verite, ni le wording juridique.

La regle est stricte :

```text
On ne corrige rien avant d'avoir recu puis classe le retour humain.
```

## Base humaine deja disponible

Le fichier `C:\Users\Gad\Downloads\Retours humains .docx`, date du
31/05/2026, contient deja des retours humains SELARL exploites dans les tickets
precedents.

Ce fichier couvre notamment :

- `DOC-002` autorisation de domiciliation : formulation siege / cabinet ;
- `DOC-001` declaration de non-condamnation : format adresse personnelle ;
- `DOC-005` renonciation conjoint : ville, communaute, suppression parasite et
  formule finale ;
- `DOC-003` / procuration selon le rattachement deja traite : suppression du
  parasite `RCS PARIS 788 531 432 0153814303` et ajout de la formule finale ;
- `DOC-004` PV nomination gerant : suppression RCS/heure/extraordinaire,
  president de seance, ordre du jour, resolutions et pouvoirs ;
- `DOC-016` statuts SELARL chirurgien-dentiste : texte complet des articles 1 a
  34 et corrections visibles.

Conclusion : l'associe / juriste ne doit pas etre sollicite comme si rien
n'avait ete relu. La revue actuelle doit seulement confirmer que le pack genere
le 2026-06-01 restitue correctement ces retours, et trancher les points encore
non couverts.

## Pack a revoir

Racine :

- `artifacts/selarl_closing_pack_001/`

Manifest :

- `artifacts/selarl_closing_pack_001/manifest_selarl_closing_pack_001.json`

Rapport de generation :

- `docs/review/selarl_closing_pack_001_report_v1.md`

## Scenarios a ouvrir

| Scenario | Dossier | ZIP | Nombre DOCX attendu |
| --- | --- | --- | ---: |
| Medecin simple | `artifacts/selarl_closing_pack_001/medecin_simple/` | `dossier_generation.zip` | 6 |
| Dentiste simple | `artifacts/selarl_closing_pack_001/dentiste_simple/` | `dossier_generation.zip` | 6 |
| Medecin regime communautaire | `artifacts/selarl_closing_pack_001/medecin_regime_communautaire/` | `dossier_generation.zip` | 7 |

## Checklist par scenario

### Medecin simple

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-017` statuts SELARL medecin

### Dentiste simple

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-016` statuts SELARL chirurgien-dentiste

### Medecin regime communautaire

- `DOC-001` declaration de non-condamnation
- `DOC-002` autorisation de domiciliation
- `DOC-003` procuration
- `DOC-004` PV nomination gerant
- `DOC-034` demande d'inscription a l'ordre
- `DOC-005` lettre de renonciation a revendiquer la qualite d'associe
- `DOC-017` statuts SELARL medecin

## Points de verification prioritaires restants

1. `DOC-034` : le fichier `Retours humains .docx` ne contient pas de validation
   specifique de la demande d'inscription a l'ordre. Il faut confirmer si le
   rendu est acceptable ou lister les corrections.
2. `DOC-017` : le fichier `Retours humains .docx` ne contient pas de retour
   humain medecin equivalent au lock dentiste. Il faut confirmer le niveau de
   confiance des statuts medecin.
3. `DOC-016` : les articles 1 a 34 sont couverts par le retour humain ; la revue
   actuelle doit surtout verifier que le rendu du pack correspond a ce lock et
   que le wrapper post-article ne pose pas de probleme.
4. `DOC-005` : verifier que le scenario regime communautaire restitue les
   corrections humaines deja donnees.
5. `DOC-006` : confirmer seulement la decision projet actuelle, c'est-a-dire
   exclusion du pack tant qu'il reste reserve.
6. `DOC-001` a `DOC-004` : ne pas refaire une revue de fond complete ; verifier
   que le pack genere reprend bien les corrections humaines deja donnees.
7. ZIP : confirmer que les documents attendus sont presents et qu'aucun document
   reserve ou manuel n'est inclus par erreur.

## Format de retour demande

L'associe peut repondre librement, mais le format le plus exploitable est :

```text
Verdict global : VALIDE / CORRECTIONS / BLOQUE
Scenario :
Document :
Type retour : bug / wording valide / wording a arbitrer / source manquante / UX / hors scope
Commentaire :
Correction demandee :
Piece jointe ou emplacement :
```

Si le pack est valide sans correction :

```text
Verdict global : VALIDE
Reserve eventuelle :
```

## Ce que Codex fera au retour

Le retour humain ouvrira le ticket suivant :

- `SELARL-REVIEW-TRIAGE-001`

Codex classera chaque retour en :

- bug ;
- wording valide ;
- wording a arbitrer ;
- source manquante ;
- UX ;
- hors scope ;
- nouveau sous-cas.

Ensuite seulement, Gad pourra donner un `GO dev` limite pour
`SELARL-REVIEW-FIXES-001`.

## Interdits pendant cette attente

- pas de correction automatique ;
- pas de modification de wording juridique ;
- pas d'ouverture de cession, SCM, multi-associes complet, plusieurs gerants,
  derogation ou site distinct ;
- pas de cloture SELARL a 100 % ;
- pas de `SELARL-CLOSING-SMOKE-001` tant que les retours ne sont pas traites ou
  explicitement absents.

## Prochaine action

Transmettre le pack et ce brief a l'associe / juriste, puis revenir avec son
verdict brut ou ses retours annotes.
