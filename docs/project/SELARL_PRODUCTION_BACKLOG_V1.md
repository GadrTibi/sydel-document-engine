# SELARL production backlog V1

## Deja couvert avant ce ticket

- Clean front Track B isole dans `src/sydel_doc_engine/front_app/`.
- Creation SELARL V1 bornee, associe unique, medecin ou chirurgien-dentiste.
- Generation DOCX/ZIP pour :
  - `DOC-001` declaration de non-condamnation ;
  - `DOC-002` autorisation de domiciliation ;
  - `DOC-003` procuration ;
  - `DOC-004` PV de nomination de gerant ;
  - `DOC-034` demande d'inscription a l'ordre ;
  - `DOC-017` statuts SELARL medecin ;
  - `DOC-016` statuts SELARL chirurgien-dentiste ;
  - `DOC-005` si regime communautaire actif ;
  - `DOC-006` si regime communautaire actif.
- Correction 2026-06-01 : l'ancienne reserve `DOC-006` est levee pour le
  perimetre SELARL regime communautaire. La source DOCX existe dans
  `project/source_documents/lot_02/` et le batch regime communautaire couvre les
  deux lettres.
- Les cas cession, SCM, derogations, site distinct, SELAS et multi-associes restent hors slice Track B initiale.

## Couvert par TRACK-B-SELARL-PRODUCTION-PACK-001

- `DOC-002` : formulation de domiciliation alignee sur le cabinet et le siege :
  `dans les locaux du cabinet au [num_voie_siege] [voie_siege], [cp_siege] [ville_siege] pour 99 ans.`
- `DOC-001` : adresse personnelle reformatee en `[num_voie_perso] [voie_perso], [cp_perso] [ville_perso]`.
- `DOC-005` lettre de renonciation : correction typographique de la ville, absence de parasite RCS verifiee, ajout de `Fait pour servir et valoir ce que de droit.`
- `DOC-004` : suppression de `RCS de ...`, suppression de `EXTRAORDINAIRE`, suppression de l'heure de reunion, gestion `Nomination du gerant` / `Nomination des gerants`.
- `DOC-004` : ajout des variables president de seance :
  - `civilite_president_seance` ;
  - `prenom_president_seance` ;
  - `nom_personne_seance`.
- Clean front Track B : rattachement automatique de l'associe unique comme president de seance du PV.
- `DOC-016` statuts SELARL chirurgien-dentiste : ajout de `euros` apres `capital_social`, correction de la formulation mariage / communaute, conservation du prestataire de signature electronique variable.
- Documentation de la factory de production SELARL.

## Couvert par TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001

- Matrice des cas SELARL restants utilement industrialisables apres le lock dentiste.
- Choix du prochain cas GO : SELARL medecin unipersonnelle standard.
- Confirmation que le delta moteur/front utile est deja cable :
  - clean front `profession=medecin` ;
  - selection `DOC-017` ;
  - absence de `DOC-016` dans le pack medecin ;
  - documents courts communs conservant les corrections humaines verrouillees.
- Smoke DOCX/ZIP medecin dans `artifacts/track_b_selarl_rollout_next_case_001_medecin`.
- Statut `DOC-017` : PARTIAL en production, car source/spec et smoke OK mais pas encore lock humain ligne par ligne equivalent au dentiste.

## Couvert par TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004

- Recherche des sources medecin exploitables.
- Decision GO limite : lock source-level contre `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx`.
- `DOC-017` SELARL medecin unipersonnelle standard : 311 paragraphes source exploitables compares au rendu genere, 0 ecart.
- Ajout d'un test ligne par ligne `DOC-017` contre la source medecin.
- Smoke DOCX/ZIP medecin dans `artifacts/track_b_selarl_medecin_line_by_line_lock_004`.
- Statut `DOC-017` : LOCKED source-level, sans retour humain medecin recent equivalent au dentiste.

## Couvert par TRACK-B-SELARL-MEDECIN-REGIME-COMMUNAUTAIRE-005

- Industrialisation du cas SELARL medecin unipersonnelle avec regime communautaire.
- Confirmation que le delta est deja cable dans le clean front :
  - `profession=medecin` conserve `DOC-017` ;
  - `regime_communautaire=True` active `DOC-005` et `DOC-006`.
- Validation que le conjoint et la date du courrier d'avertissement sont requis
  uniquement si le regime communautaire est actif ; l'adresse du conjoint est
  derivee depuis l'adresse personnelle de l'associe/signataire et ne doit pas
  etre redemandee dans le front.
- Ajout de tests cibles de non-regression medecin standard et de smoke medecin + regime communautaire.
- Smoke DOCX/ZIP medecin + regime communautaire dans `artifacts/track_b_selarl_medecin_regime_communautaire_005`.
- Statut courant apres correction 2026-06-01 : documents courts, `DOC-005` et
  `DOC-006` generables ; `DOC-017` LOCKED source-level ; `DOC-034` PARTIAL.

## Couvert par TRACK-B-SELARL-MULTI-ASSOCIES-SOURCE-CONTRACT-006

- Contrat source cree : `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`.
- Perimetre precise pour la famille SELARL multi-associes / president de seance / plusieurs gerants.
- Decision de readiness :
  - GO limite pour un futur sous-cas multi-associes simple sur `DOC-004` uniquement, avec president choisi parmi les associes existants, un gerant unique et unanimite totale ;
  - GO limite pour president de seance distinct uniquement s'il est rattache a un associe existant ;
  - NO-GO pour les statuts multi-associes `DOC-016` / `DOC-017` sans reference humaine multi-associes ;
  - NO-GO pour plusieurs gerants ;
  - NO-GO pour cession medicale/dentaire et cession SCM dans ce contrat.
- Donnees cibles documentees : `associes[]`, repartition des parts, `president_seance_ref_associe_id`, derivations president de seance, gerant unique rattache a un associe.
- Aucun code, aucun front, aucun generateur et aucun wording juridique modifies.

## Couvert par TRACK-B-SELARL-MULTI-ASSOCIES-DOC004-LIMITED-007

- Implementation du sous-cas limite `DOC-004` multi-associes simple.
- Clean front Track B : mode `SELARL multi-associes simple (limite DOC-004)`.
- Donnees saisies :
  - associes necessaires au PV ;
  - repartition des parts ;
  - president de seance choisi parmi les associes existants.
- Regles appliquees :
  - generation de `DOC-004` uniquement ;
  - gerant unique rattache au praticien / associe 1 ;
  - associes presents ou representes disposant ensemble de la totalite des parts ;
  - unanimite totale ;
  - blocage si la somme des parts ne correspond pas au total.
- `DOC-004` : LOCKED sur ce sous-cas limite.
- Statuts multi-associes, plusieurs gerants, cession, SCM, regime communautaire et votes non unanimes restent hors scope.

## Couvert par TRACK-B-SELARL-DENTIST-MULTI-ASSOCIES-STATUTS-PARTIAL-008

- Implementation du sous-cas `SELARL chirurgien-dentiste multi-associes simple`.
- Clean front Track B : mode `SELARL dentiste multi-associes simple (PARTIAL statuts)`.
- Donnees reutilisees depuis le sous-cas `DOC-004` :
  - associes necessaires au PV ;
  - repartition simple des parts ;
  - president de seance choisi parmi les associes existants ;
  - gerant unique rattache au praticien / associe 1 ;
  - unanimite totale.
- Generation selectionnee :
  - `DOC-004` ;
  - `DOC-016` en mode PARTIAL.
- `DOC-016` : apports, total des apports, depot des fonds au pluriel, repartition du capital et signatures associes rendus pour le sous-cas simple.
- `DOC-016` reste PARTIAL : le preambule/comparution multi-associes complet et le bloc de signature pluriel strict ne disposent pas d'un lock humain ligne par ligne.
- Plusieurs gerants, president externe, cession, SCM, regime communautaire, votes non unanimes et medecin multi-associes restent hors scope.

## Variantes SELARL restantes

- SELARL multi-associes au-dela de `DOC-004` et du `DOC-016` dentiste PARTIAL.
- President de seance externe aux associes.
- Plusieurs gerants nommes avec bloc identite complet multi-dirigeants.
- SELARL avec cession medicale ou dentaire.
- SELARL avec cession SCM.
- SELARL avec derogation.
- SELARL avec site distinct.
- Documents manuels ou hors generation automatique :
  - `DOC-013` declaration SEL BNC, manuel ;
  - `DOC-014` attestation inscription SEL, manuel ;
  - documents marques a remplir a la main dans la source de verite.

## OPEN POINTS

- `DOC-017` statuts SELARL medecin : LOCKED source-level contre la source DOCX repo, mais aucun retour humain medecin recent equivalent au bloc dentiste n'est disponible.
- `DOC-017` statuts SELARL medecin : la ligne source incomplete `[civilite_personne_2] [prenom_personne_2] [nom_personne_2] ...` reste exclue du lock unipersonnel et ne doit pas etre inventee.
- `DOC-016` statuts SELARL chirurgien-dentiste : les articles 1 a 34 sont LOCKED ; le wrapper post-article reste OPEN GAP de perimetre car non couvert par la reference humaine article par article.
- La formulation de president de seance est sourcee pour un president rattache a un associe existant dans `DOC-004`; elle reste non sourcee pour un president externe.
- Le wording exact complet des statuts multi-associes `DOC-016` / `DOC-017` reste manquant : soussignes, comparution plurielle, signatures et accords. Pour `DOC-016`, le sous-cas dentiste PARTIAL couvre deja les apports, le capital et la repartition simple.
- Les regles documentaires multi-associes de `DOC-001`, `DOC-003` et `DOC-034` restent a arbitrer.
- Plusieurs gerants : modele `gerants[]`, resolution, ordre d'affichage, signatures et pouvoirs restent a sourcer.
- Les accords de genre au-dela des cas deja testes ne doivent pas etre inventes sans source humaine.
- `DOC-006` est actif seulement dans le perimetre regime communautaire. Les
  variantes hors regime ne doivent pas l'inclure.

## Ordre restant indicatif

1. Fermer le lock complet `DOC-016` dentiste multi-associes seulement apres reference humaine dediee sur comparution/signatures.
2. Plusieurs gerants, seulement apres reference humaine dediee.
3. SELARL cession medicale ou dentaire, apres sous-formulaire clean front complet et arbitrages sources.
4. SELARL cession SCM, apres sous-formulaire clean front complet et mapping explicite des roles.
5. Derogations, site distinct et documents manuels selon arbitrage humain.
