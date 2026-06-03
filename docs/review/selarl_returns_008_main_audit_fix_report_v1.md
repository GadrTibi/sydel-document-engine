# SELARL-RETURNS-008-MAIN-AUDIT-FIX-001 - Rapport

## Objet

Correction appliquee sur `main` apres audit des retours associe SELARL remis par
Gad le 2026-06-03.

Le point nouveau confirme etait le cas SELARL medecin marie sous separation de
biens : le front demandait insuffisamment l'identite du conjoint et la
generation pouvait partir en erreur dans les statuts, alors que ce cas ne doit
pas produire les lettres de regime communautaire.

## Corrections appliquees

- `front_app/shell.py` : le bloc conjoint est affiche des que le praticien est
  marie, pas seulement en regime communautaire.
- `front_app/selarl_slice.py` : l'identite du conjoint est obligatoire pour les
  statuts quand le praticien est marie ; l'adresse du conjoint reste exclue en
  separation de biens.
- `field_derivations.py` : `Marie(e)` sans regime communautaire derive
  maintenant `separation de biens`.
- `selarl_slice.py` : les libelles front/moteur medecin sont rendus avec leur
  version accentuee dans les documents et le capital est formate en `1 000`
  dans les documents visibles.
- `tests/unit/test_clean_front_app.py` : ajout de non-regressions separation de
  biens et controles capital/libelles.

## Audit retours associe

Audit DOCX reel execute sur trois scenarios generes :

- medecin simple ;
- medecin regime communautaire ;
- medecin marie sous separation de biens.

Points controles OK :

- DNC : ville de naissance apres la date de naissance.
- Autorisation de domiciliation : `pour 99 ans`.
- Procuration : `agissant` en minuscule dans la meme phrase.
- PV nomination gerant : forme juridique redigee et capital `1 000`.
- Lettre conjoint : forme juridique redigee, capital `1 000`, aucune adresse
  conjoint demandee/rendue.
- Renonciation : pas de date ajoutee sous la ville avant l'objet.
- Demande d'inscription a l'Ordre : `Conseil departemental de l'Ordre des
  medecins de 75` dans le rendu accentue.
- Statuts : phrase regime communautaire presente.
- Statuts : phrase separation de biens presente.
- Separation de biens : pas de `DOC-005`, pas de `DOC-006`.
- Absence de capital brut `1000` dans les mentions `Au capital`.
- Absence de `medecin` non accentue dans le texte brut genere.
- Absence de variable/adresse conjoint dans le texte genere.
- Documents courts : pas de table de signature additionnelle.

## Validations

- `python -m ruff check .` : OK.
- `python -m py_compile src/sydel_doc_engine/front_app/field_derivations.py src/sydel_doc_engine/front_app/selarl_slice.py src/sydel_doc_engine/front_app/shell.py` : OK.
- Generation reelle DOCX/ZIP : OK, 3 scenarios, 6/8/6 DOCX.
- Audit retours associe par extraction DOCX : OK, 32 controles.

Note environnement : `pytest` avec fixtures `tmp_path` est bloque dans cette
session par des permissions Windows sur les repertoires temporaires
`AppData\\Local\\Temp`, puis sur des basetemp locaux. Les controles metier ont
donc ete executes par scripts directs de generation/extraction DOCX, sans
fixture temporaire.

## Verdict

`DONE` cote correction main. La prochaine action est de faire tester l'associe
sur `main` deploye Streamlit Cloud, puis de ne rouvrir que des ecarts concrets
document par document.
