# Carnet de retours Rafael — 2026-06-29 (UAT SELAS pluri + transverse moteur)

> Retours reçus par screens WhatsApp (Rafael, en cours — d'autres peuvent arriver). Triage règle 68 :
> ANTICIPABLE ? · NOUVEAUTÉ ou CORRECTION ? · PÉRIMÈTRE de propagation ?
> TRAITÉ ≠ VALIDÉ (sort du carnet seulement à validation).

| ID | Verbatim Rafael | Triage (anticipable / nature) | Périmètre | État |
|---|---|---|---|---|
| RAF-D1 | « mets un sélecteur de date quand on fait référence à une date PARTOUT DANS LE MOTEUR » | **DÉJÀ FAIT le 24/06** (helper `date_input_with_today` porte calendrier `st.date_input` + « R3/N2 Rafael 24/06 »). Si encore visible = **trou de PROPAGATION** (anticipable : aurait dû couvrir tous les champs date) | tous les champs date | À VÉRIFIER (cartographie en cours) |
| RAF-D2 | « et toujours la possibilité de mettre aujourd'hui partout dans le moteur » | Idem RAF-D1 : le bouton « Aujourd'hui » est dans le même helper → couvert là où le helper est appliqué | tous les champs date | À VÉRIFIER |
| RAF-D3 | « Pourquoi y a ça sur la selas pluriperso » (bloc « Documents communs (décision, ordre professionnel) », « Date de décision (PV gérant) ») | AMBIGU — probable : le label « PV gérant » sur une SELAS (qui nomme des dirigeants, pas des gérants) = lié au renommage gérant→dirigeant déjà flaggé (A26-label) | SELAS (+ types nommant des dirigeants) | À CLARIFIER |
| RAF-D4 | « dans selas pluripersonnel il manque le champ numéro RCS, il ne se met pas dans les docs » | À TRIER — `ville_rcs` présent mais `numero_rcs` société absent en SELAS pluri. Nuance : société EN CRÉATION = pas de numéro (« en cours d'immatriculation »). Lequel doc l'attend ? | SELAS pluri (société créée) | À INVESTIGUER (cartographie en cours) |
| (méthode) | « je suis persuadé qu'on a pas la bonne méthode, c beaucoup trop long, ya beaucoup trop d'erreurs » | Commentaire process, pas un item de build. Levier proposé : **contrat d'inputs par type** (lister les champs attendus) pour découvrir les trous nous-mêmes, pas en test. | n/a | NOTÉ (avis donné à Gad) |

## Note de triage
RAF-D1/D2 = **trou de propagation** confirmé (le calendrier+aujourd'hui existe depuis le 24/06 mais n'était appliqué qu'à une partie des champs date) → cartographie faite, champs date résiduels routés au helper partagé (cf. ci-dessous). RAF-D4 (RCS) = à investiguer (société en création vs entité immatriculée). RAF-D3 = à clarifier avec Rafael.

## RAF-D1/D2 — routage des champs date (TRAITÉ, gate Akainu derrière)

Tous via le helper partagé `date_input_with_today` (calendrier `st.date_input` + bouton « Aujourd'hui » + champ texte JJ/MM/AAAA éditable). Clés session_state CONSERVÉES, post-traitement (accentuation des mois / pad jour) PRÉSERVÉ, saisie verbatim française toujours possible. `seed=False` ajouté au helper pour ne PAS pré-remplir une date de naissance avec la date du jour.

Champs **routés ce sprint** :
- `associe_repeater.py` — date de naissance des associés (SCM / SCI / SCI IRIS / SCS / SELAS pluri / dirigeant) [champ central, majorité des types].
- `selas_multi_slice.py` — date de naissance associés SELAS multi.
- `shell.py` — date de naissance (associé personne physique d'une personne morale / SELARL multi).
- `shell.py` `_cession_date` (refondé sur le helper) → **toute la famille cession/bail** : date de naissance vendeur, date d'immatriculation, date d'inscription à l'ordre, date d'origine de propriété, date du bail, date d'effet du bail, date limite de réalisation.
- `civil_statuts_slice.py` — date d'effet du contrat de frais communs, fin de gestion administrative.
- `sas_slice.py` — date de naissance (président, verbatim statuts).
- `spfpl_slice.py` — date de naissance actionnaire SPFPL.

Champs **déjà routés** (helper déjà en place, RAS) : shell.py SELARL naissance + signature/decision ; selas_multi `_date` (signature) ; civil_statuts `_date_input` (signature/décision PV) ; SAS `date_naissance_iso` (DNC) ; selas uni dentiste/médecin naissance.

## EXCEPTIONS à NE PAS convertir — À VALIDER RAFAEL

Ces champs portent un libellé **PARTIEL** (pas d'année, ou récurrent) qu'un `st.date_input` ne peut pas représenter sans imposer une année factice. **NON convertis**, conservés en saisie texte. À confirmer par Rafael que c'est bien voulu :
- `shell.py` « Début exercice » (« 1er janvier » sans année).
- `shell.py` « Fin exercice » (« 31 décembre » sans année).
- `shell.py` « Clôture du premier exercice » (« 31 décembre N+1 »).
- `civil_statuts_slice.py` « Clôture du premier exercice » (idem).
- `civil_statuts_slice.py` « Attribution des responsabilités » (hint « 1er janvier » — récurrent sans année).

Raison : un date picker imposerait une année, ce que ces champs récurrents/relatifs ne veulent pas. Exception sémantique légitime. Si Rafael veut quand même un picker dessus → décision produit (choisir un format année-incluse).
