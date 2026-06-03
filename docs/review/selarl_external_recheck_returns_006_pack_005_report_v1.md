# SELARL external recheck returns 006 pack 005 report V1

Ticket : `SELARL-EXTERNAL-RECHECK-RETURNS-006-001`

Date : 2026-06-02

Demande : Gad demande une reverification presque exterieure des tout derniers
retours humains 006, en relisant les retours puis en controlant s'ils sont
resolus dans la nouvelle version.

## Amendement 2026-06-03

Ce rapport est historique. Il a ete depasse par :

- `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`

L'audit incident a trouve un ecart qui n'etait pas detecte ici : `DOC-002`
autorisation de domiciliation rendait encore `pour une duree indeterminee`.
Correction appliquee le 2026-06-03 : `DOC-002` rend maintenant `pour 99 ans`.

## Verdict

Verdict historique : `DEPASSE - ecart DOC-002 trouve ensuite et corrige`.

Le pack 005 et le front propre actif couvraient les derniers retours humains 006
dans le perimetre audite le 2026-06-02, mais le controle ne descendait pas
assez loin sur `DOC-002`. Le verdict actif est celui du rapport incident du
2026-06-03.

## Sources relues

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`
- `docs/review/selarl_human_returns_deep_audit_006_report_v1.md`
- `artifacts/selarl_closing_pack_005/`
- `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`
- `src/sydel_doc_engine/front_app/`
- `tests/unit/test_clean_front_app.py`
- `tests/unit/test_lot_04_statuts_sel_exercice.py`
- `tests/unit/test_declaration_non_condamnation.py`
- `tests/unit/test_pv_nomination_gerant.py`
- `tests/unit/test_procuration.py`
- `tests/unit/test_regime_communautaire.py`
- `tests/unit/test_demande_inscription_ordre.py`

## Methode

Le controle n'a pas repris le manifest comme preuve unique.

1. Extraction directe du texte et du XML des DOCX du pack 005.
2. Controle des 4 scenarios du pack : medecin simple, dentiste simple, medecin
   regime communautaire, dentiste regime communautaire.
3. Verification directe des points non visibles dans un pack standard par le
   code du front propre actif et les tests.
4. Separation explicite entre le nouveau front actif `front_app` et les anciens
   ecrans conserves comme reference legacy.

Faux positifs corriges pendant l'audit :

- les fichiers generes ne portent pas les prefixes `DOC-001`, `DOC-002`, etc. ;
- le mot `annexee` dans le corps des statuts ne doit pas etre confondu avec le
  titre `ANNEXE` ;
- la clause matrimoniale peut etre `mariee sous le regime...` au feminin ;
- l'adresse du conjoint dans `DOC-006` doit etre l'adresse personnelle de
  l'associee, pas l'adresse de siege.

## Checklist externe

| Retour 006 | Recheck | Preuve |
| --- | --- | --- |
| Statuts : clause communaute | OK | Texte extrait : `mariee sous le regime de la communaute avec ...` dans les scenarios regime |
| Statuts : separation de biens | OK code/test | Test dedie `test_statuts_selarl_medecin_renders_separation_de_biens_clause` |
| Statuts : article 8 accord associe | OK | Texte extrait + tests statuts |
| Statuts : annexe page suivante | OK | XML DOCX : saut de page avant le titre `ANNEXE` |
| Statuts : tiret avant `Ouverture...` | OK | Texte extrait pack 005 |
| DNC : naissance avec ville | OK | Texte extrait pack 005 |
| DNC : option `au` | OK code/test | Champ `ville_naissance_article_au` + tests clean front/DNC |
| PV : forme juridique redigee | OK | Texte extrait pack 005 |
| PV : `Au capital de {capital social}` | OK | Texte extrait pack 005, ancienne formule absente |
| Adresses : CP avant ville | OK | Extraction pack : aucun motif `Ville 750xx/690xx` detecte |
| Signatures : suppression encadres | OK | XML DOCX : aucune table de signature visible detectee dans le pack |
| Ordre : libelle compose profession + departement | OK | Texte extrait pack 005 |
| DOC-006 : forme juridique redigee | OK | Texte extrait pack 005 |
| DOC-006 : adresse conjoint = associe | OK | Adresse personnelle presente, ancienne adresse conjoint absente |
| DOC-005 : date sous ville retiree | OK | Ligne avant objet controlee |
| Duree sociale = 99 ans | OK front actif | `front_app.data_entry` et `front_app.shell` derivent `99 ans` |
| Autorisation de domiciliation = 99 ans | MANQUE HISTORIQUE, CORRIGE LE 2026-06-03 | Ce rapport n'avait pas controle le libelle `DOC-002` ; correction documentee dans le rapport incident |
| Siege identique adresse personnelle | OK front actif | Checkbox `identique a l'adresse personnelle` dans `front_app.shell` |
| Nationalite portugaise | OK front actif | Test Streamlit : `Portugaise` dans la liste |
| Nombre d'exemplaires = 4 | OK front actif/pack | Derive en `quatre`, pack `DOC-006` en quatre exemplaires |
| Qualite renoncee = associe | OK front actif | Derivee en `associe`, pas exposee dans le front propre |
| Date courrier = jour | OK front actif/test | Derivee par `date.today()` quand regime communautaire actif |
| Procuration : `..., agissant...` | OK | Texte extrait pack 005 |

## Reserve importante

Le grep large du depot retrouve encore des variables historiques comme
`signature_nombre_exemplaires`, `qualite_renoncee`, `date_courrier_avertissement`
ou `adresse_conjoint` dans des couches legacy ou des modeles internes.

Ce n'est pas un ecart dans le verdict actif tant que :

- le front propre `src/sydel_doc_engine/front_app/app.py` reste le point
  d'entree utilisateur ;
- `src/sydel_doc_engine/front_app/legacy_boundary.py` maintient explicitement
  `streamlit_app.py`, `business_wizard.py` et `single_document_mode.py` hors
  nouveau front ;
- le test `test_clean_front_entrypoint_does_not_import_legacy_screens` reste
  vert.

Si Gad veut supprimer toute trace legacy dans le depot, ouvrir un ticket separe :
`FRONT-LEGACY-RETIREMENT-001`.

## Validations lancees

- Extraction directe DOCX/XML pack 005 : 4 scenarios controles, 0 failure.
- Tests cibles :
  `pytest tests/unit/test_clean_front_app.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_demande_inscription_ordre.py -q`
  -> 84 tests passes.

## Suite recommandee

Prochaine action : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

Instruction associe : tester le pack 005 et remonter uniquement des ecarts
concrets document par document.
