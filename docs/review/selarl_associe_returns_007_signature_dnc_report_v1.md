# SELARL associe returns 007 signature DNC report V1

Date : 2026-06-03

Ticket : `SELARL-RETURNS-007-SIGNATURE-DNC-001`

## Retours recus

Message associe transmis par Gad :

- les carres de signature sont toujours presents ;
- la ville de naissance de l'associe n'apparait pas dans la declaration de non
  condamnation ;
- point positif : la variable adresse du conjoint n'est plus visible ;
- retirer tous les carres de signature dans la mise en forme des documents ;
- la ville de naissance doit etre inscrite juste apres la date de naissance
  dans la declaration de non condamnation.

## Verdict produit

Verdict : `PARTIAL`.

Le retour signature est fonde sur le ressenti visuel : la correction precedente
avait supprime les bordures imprimees des signatures, mais conservait un tableau
invisible pour positionner les signatures. Dans Word, ce tableau peut encore
apparaitre comme une grille ou un carre a l'ecran.

Le retour declaration de non condamnation n'est pas reproduit dans le code actif
ni dans le pack 005 regenere le 2026-06-03 : les quatre scenarios affichent
`Ne le 12/04/1984 a Paris.` en version normalisee ASCII, soit visuellement
`Ne/Nee le ... a Paris.` selon le genre.

## Critique du retour associe

| Point | Critique |
| --- | --- |
| Signature | Retour suffisamment clair. Meme si le terme `carres de signature` pouvait designer les bordures imprimees ou les grilles Word, l'intention visuelle etait : aucune structure encadree visible autour des signatures. |
| Declaration non condamnation | Retour utile a verifier, mais non reproduit dans la version active. Cause probable : pack ancien, branche ancienne, ZIP genere avant correction, ou lecture d'un document non issu du pack 005 regenere. |
| Adresse conjoint | Retour positif confirme : la saisie adresse conjoint n'est plus exposee dans le front actif. |

## Auto-critique Codex

Le traitement precedent etait trop technique : j'ai considere qu'une signature
etait conforme des lors que le tableau n'avait plus de bordure imprimee. Ce
n'etait pas suffisant pour une revue humaine Word, car la grille de tableau peut
rester visible a l'ecran.

La bonne correction est de supprimer la table de signature elle-meme, pas
seulement sa bordure.

Sur la declaration de non condamnation, le code actif et le pack regenere sont
conformes. Le point a quand meme revele un probleme de process : comme les
artefacts `artifacts/` ne sont pas pousses dans Git, un associe peut tester une
ancienne version locale ou un ancien ZIP si le pack n'est pas explicitement
regenere et retransmis.

## Corrections appliquees

| Point | Correction |
| --- | --- |
| Signatures `DOC-001` / `DOC-002` / `DOC-003` | Le helper `add_simple_signature_block` ne cree plus de tableau. Il rend des paragraphes alignes a droite. |
| Tests signatures | Les tests attendent maintenant une signature sans table, pas seulement une table sans bordure. |
| Pack 005 local | Pack regenere apres correction. Controle : aucune table contenant `Fait a`, `Le 26/05/2026`, `Jean Martin` ou `Monsieur Jean Martin`. |
| DNC ville naissance | Aucun changement code requis : les quatre DNC du pack regenere affichent la ville de naissance juste apres la date. |

## Point de vigilance

Des tables bordees restent dans le pack, mais elles correspondent aux titres
encadres (`STATUTS`, `Procuration`, `DECLARATION DE NON CONDAMNATION`,
`AUTORISATION DE DOMICILIATION`, `PROCES-VERBAL...`). Elles ne sont pas des
signatures.

Si l'associe veut supprimer tous les encadres de titre, c'est une demande
distincte de mise en forme globale. Elle doit etre traitee par un ticket dedie,
car elle modifie l'apparence de plusieurs documents au-dela des signatures.

## Validations executees

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py -q`
  : OK, 23 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/rendering/docx_builder.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py`
  : OK.
- Regression SELARL ciblee :
  `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_selarl_form_schema.py -q`
  : OK, 187 tests passes.
- Controle pack 005 regenere :
  - DNC : `Ne le 12/04/1984 a Paris.` present dans les quatre scenarios
    apres normalisation ASCII ;
  - signatures : aucune table de signature restante dans le pack ;
  - tables bordees restantes : titres uniquement, pas signatures.

