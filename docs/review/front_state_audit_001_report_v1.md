# Rapport FRONT-STATE-AUDIT-001

Date : 2026-05-25

## 1. Objet

Audit de reprise sur l'etat reel du projet et du nouveau front Streamlit apres
`FRONT-UX-HARD-CUT-001`.

Cet audit repond a une incomprehension utilisateur : le moteur semble avance,
mais le front visible ne montre qu'un pilote SELARL avec quatre documents, et la
generation peut rester bloquee alors que les champs visibles semblent remplis.

Aucun generateur, moteur DOCX/PDF/ZIP, wording juridique ou source de verite n'a
ete modifie.

## 2. Etat reel du moteur

Le moteur documentaire n'est pas limite aux quatre documents visibles dans le
nouveau front.

Constats techniques :

- `build_seed_catalog()` expose 43 documents moteurs `DOC-001` a `DOC-043` ;
- le catalogue metier contient 46 documents attendus ;
- 43 documents sont mappes a un `DOC-XXX` unique ;
- le catalogue metier classe 41 documents en `GENERATABLE`, 4 en `MANUAL_ONLY`
  et 1 en `NOT_IMPLEMENTED`.

Conclusion : le moteur DOCX V1 est largement plus avance que le front visible.
Le probleme observe est un probleme de surface produit / orchestration front, pas
un probleme de disponibilite globale des generateurs.

## 3. Etat reel du nouveau front

La surface utilisateur normale lance uniquement le nouveau front hard-cut :

- `Type de dossier` ;
- `Donnees a saisir` ;
- `Generation`.

Le seul profil saisissable aujourd'hui est `SELARL creation simple`.

La generation du nouveau front est volontairement limitee a :

- `DOC-001` - Declaration sur l'honneur de non-condamnation ;
- `DOC-002` - Autorisation de domiciliation ;
- `DOC-003` - Procuration ;
- `DOC-004` - PV nomination gerant.

`DOC-006`, `DOC-013` et `DOC-014` restent explicitement exclus de cette action
V1. Les autres documents SELARL ne sont pas encore ouverts dans le nouveau front.

Conclusion : les quatre documents visibles ne sont pas une regression moteur ;
c'est le perimetre volontaire du pilote front actuel. En revanche, ce perimetre
n'est pas assez explicite pour un utilisateur.

## 4. Ancien front et nouveau front

Le prototype historique existe encore derriere `Outils internes` :

- `Assistant metier prototype` ;
- `Document unitaire` ;
- `Technique / diagnostic` ;
- `Debug interne`.

Cette presence est conforme a `FRONT_MIGRATION_MAP_V1.md` : le prototype doit
rester disponible comme bac a sable et diagnostic tant que le nouveau front ne
couvre pas les memes usages.

Mais le code Streamlit reste encore tres monolithique : le nouveau front est
visuellement isole, tandis que les anciens outils et la nouvelle interface vivent
encore dans `streamlit_app.py`.

Conclusion : on ne se repose plus architecturalement sur l'ancien
`business_wizard` pour la generation du nouveau front, mais la transition reste
visible dans le code et dans les outils internes. La deprecation du prototype ne
doit pas commencer avant un panneau documents fiable et une generation expliquee.

## 5. Cause probable du blocage utilisateur

Le nouveau front a deux niveaux de readiness :

1. `document_status` : verifie que les quatre documents ont les roles, adresses
   et valeurs canoniques minimales ;
2. `front_generation_actions.build_front_generation_context(...)` : transforme
   le `DossierRecord` en contexte moteur et applique des controles plus stricts.

Probleme : la surface normale affiche seulement des compteurs et un message
generique. Elle ne montre pas les `runtime_blockers`.

Reproduction en lecture seule :

| Cas | Documents generables data-layer | Runtime blocker | Generation |
|---|---:|---|---|
| valeurs exactes des tests | 4 | aucun | OK |
| date `24/05/2026` | 4 | `signature.date doit etre au format AAAA-MM-JJ` | bloquee |
| adresse `12, rue Exemple, 75001 Paris` | 4 | adresse attendue sous forme `12 rue Exemple, 75001 Paris` | bloquee |
| ville RCS absente | 4 | `societe.societe_principale.rcs.ville` manquant | bloquee |

Conclusion : l'utilisateur peut avoir l'impression d'avoir tout rempli, car les
documents passent `generable` cote data-layer, mais le bouton reste bloque par un
controle moteur non explique dans la vue normale.

## 6. Point de produit

Le ticket `FRONT-UX-HARD-CUT-001` a bien retire le bruit technique de la surface
utilisateur, mais il a aussi retire les informations qui permettaient de
comprendre pourquoi la generation est bloquee.

Le ticket `FRONT-DOCUMENTS-PANEL-001` etait marque optionnel apres test local.
Apres cet audit, il ne doit plus etre considere comme optionnel : il faut au
minimum afficher les statuts, les reserves, les documents hors perimetre et les
raisons de blocage.

Il faut aussi exposer les blocages runtime de `front_generation_actions`, car ils
ne sont pas tous visibles dans `document_status`.

## 7. Direction recommandee

Priorite immediate : `FRONT-GENERATION-READINESS-UX-001`.

Objectif : rendre la generation comprehensible avant d'etendre le perimetre.

Le ticket doit :

- afficher dans la vue normale les raisons exactes de blocage ;
- distinguer "champ manquant", "format invalide", "document hors perimetre" et
  "document manuel" ;
- rendre explicite que le pilote actuel genere seulement `DOC-001` a `DOC-004` ;
- eviter les faux blocages silencieux sur les dates et les adresses, soit par
  aide visible, soit par saisie structuree ou normalisation prudente ;
- ajouter un test AppTest reproduisant au moins un cas "tout rempli mais format
  bloque".

Ensuite seulement : `FRONT-DOCUMENTS-PANEL-001`.

Objectif : montrer la liste des documents attendus du dossier SELARL, avec les
statuts generable / manuel / reserve / hors perimetre / contexte incomplet.

Extension du perimetre SELARL a repousser apres ces deux tickets. Le prochain
bloc a ouvrir devra etre choisi par famille canonique et non par opportunisme UI
: ordre, regime communautaire, statuts ou autre bloc valide.

## 8. Validations executees

- `.\.venv\Scripts\python.exe -m pytest tests\unit\test_front_generation_actions.py -q`
  : OK, 6 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests\unit\test_front_dossier_data_entry.py -q`
  : OK, 10 tests passes.
- Script de diagnostic lecture seule sur quatre variantes de readiness :
  OK, blocages runtime identifies.

## 9. Hypotheses et garde-fous

- Aucune modification du wording juridique.
- Aucune modification du moteur DOCX/PDF/ZIP.
- Aucune modification des sources de verite.
- `docs/docssource_truth/` reste un dossier non suivi preexistant, hors perimetre.
