# Journal de bord — Sydel Document Engine

> Le **« backlog » complet** voulu par Gad (2026-06-22) : un journal **chronologique horodaté
> unique** qui capture TOUT — chaque action/implémentation, chaque **question posée à Rafael**,
> chaque **réponse de Rafael**, chaque décision — pour **rejouer l'histoire du projet** et
> **remonter** quand Rafael a fait une connerie.
>
> **Sources croisées** (ce journal les unifie, il ne les remplace pas) :
> - `git log` = chronologie exacte des implémentations (horodatée, faisant foi pour les actions code) ;
> - `docs/review/retours/REGISTRE_RETOURS.md` = détail des remarques Rafael/Albane + statut + SHA ;
> - mémoire privée `rafael-collaboration-grievances` = les conneries de Rafael (G1/G2/G3), HORS repo.

## Règle de tenue (codifiée — appliquée systématiquement)
À chaque **action significative**, **question à Rafael**, **réponse de Rafael**, ou **décision**,
j'ajoute UNE ligne ici : `- [AAAA-MM-JJ HH:MM] [TYPE] description (réf : SHA / fichier)`.
- TYPE ∈ `ACTION` (code/commit) · `Q-RAFAEL` (question posée) · `R-RAFAEL` (réponse reçue) ·
  `DÉCISION` · `AUDIT` · `INCIDENT` (connerie/erreur, Rafael ou nous) · `MÉTHODE` (règle codifiée).
- Heure exacte pour les commits (git) ; approximative (`~`) pour les échanges non horodatés.
- Append-only : on ne réécrit pas l'histoire, on ajoute.

---

## 2026-07-10/12 — Lot SELARL unipersonnelle (mail direct Albane « on touche au bout »)
Carnet verbatim : `docs/returns/CARNET_ALBANE_SELARL_2026-07-10.md` (~26 retours + 4 flags métier).
- [2026-07-12] [ACTION] (`6455b26`) Lot SELARL intégré + poussé sur `sprint/engine-completion` :
  5 chantiers parallèles (statuts / procuration / acte cession cabinet dentaire / acte cession
  parts SCM / front+wiring+docs manquants) + helper `accord_terme_genre` (accord genre par
  INTENTION : inscrit→inscrite, soussigné→soussignée, il→elle, le cédant→la cédante) + règle
  conformité **R15 étendue** (comparution à SUJET féminin ⇒ aucun terme masculin résiduel ;
  0 faux positif conjoint/homme). **1384 verts, ruff propre.**
  - Statuts : cadre STATUTS descendu+agrandi (ST1), soussigné en gras (ST2), espaces (ST3/ST7),
    « inscrite » (ST4), point après régime (ST5), préposition ordre « du » (ST6, token connecteur).
  - Procuration : 1re ligne justifiée (PR1), « gérante » (PR2), préposition « du » (PR3).
  - Acte cabinet : cédant en gras (AC1), origine créé/acquis branchée (O1/AC2), révision Word
    neutralisée (AC3), date transfert vierge (AC4), « sur sept pages » (AC5, était 20).
  - Acte parts SCM : parties espacées + noms/SCM en gras (SC1), gérants inventés → VIERGE (SC2),
    « qu'elle »/« soussignée » (SC3/SC4), puces dans les listes (SC5), 2 cadres signature (SC6).
  - Front : origine créé/acquis exposée (O1), corporel dérivé total−incorporel (O2, défaut),
    seeds SCM retirés (F1), blocages référence-dossier/banque levés (F2/F3). Procuration SEL 2e
    génération (SPFPL cession). Compromis (MD1) + PV nomination (MD2) câblés ; MD2 = faux manquant.
- [2026-07-12] [DÉCISION] fb8b : l'ancien test verrouillait 3 cogérants INVENTÉS (Paul Bernard /
  Jean Dupont / Anne Martin) — c'était exactement le bug Albane SC2. Test corrigé → `cogerants == []`
  (Albane supersede l'ancien lock Akainu). Leçon : le plus récent fait foi (règle 68).
- [2026-07-12] [Q-ALBANE] 4 flags métier non-constructibles tracés dans `QUESTIONS_RAFAEL.md` :
  MD3 attestation capital SELARL (aucun modèle → besoin du .docx), Q1 courriers 1 page (à
  re-récupérer), O2 dérivation corporel (à confirmer), AC3 wording final clause « au bail ».
- [2026-07-12] [AUDIT] gate Akainu doc-entier lancé sur le lot SELARL (régénération réelle des
  .docx, chaque retour vs verbatim + cohérence inter-docs) → boucle fix jusqu'à RIEN À REDIRE.

## 2026-06-26 — Lot « Formulaire-A » Albane (Chopper) : préremplissages + bugs front cession

> Sous-formulaire cession PARTAGÉ SELARL/SELAS (`front_app/shell.py::_render_cession_form`
> + `_render_scm_cession_form`). Zéro générateur touché. Fix prouvés via streamlit AppTest
> (parcours SELAS pluri = celui d'Albane) + régénération réelle des DOCX. Tests :
> `tests/unit/test_cession_formulaire_a.py` (13 verts). Périmètre régression
> `front|cession|scm|multi_type|selarl|selas` = **538 verts**, ruff propre, mypy shell.py 0 erreur.
> **GATE AKAINU pas encore passé → rien déclaré TRAITÉ.**

- [16:20] **ACTION** FA1 (A26-03) « montant du prêt = prix de cession » : `pret_montant`
  préremplie = prix total saisi (auto, modifiable). Preuve : prix 300000 → prêt « 300 000 ».
- [16:20] **ACTION** FA2 (A26-04) « taux du prêt : 5,5 % » : défaut `5,5 %`. FA3 (A26-05)
  « durée : 10 ans » : défaut `10 ans`. Préremplissages éditables.
- [16:20] **ACTION** FA4 (A26-06) majoration intérêts retard crédit-vendeur : champ de saisie
  RETIRÉ, valeur FIGÉE = `"2"` (modèle source SELARL « majoré de 2 points » + scénario validé).
  ⚠️ **FLAG PM** : la consigne disait « 3 points » (indication approx.) ; le verbatim Albane
  = « reprendre ce qu'il y avait dans le modèle » → modèle source = **2 points**. Aligné sur la
  source de vérité (2), pas sur l'indication (3). À confirmer si Albane veut 3.
- [16:20] **ACTION** FA5 (A26-07) + FB3 (A26-46) date limite réalisation : préremplie =
  date des actes (`signature_date`) + 6 mois via nouveau helper `_add_months` + `format_french_date`
  (« %d/%m/%Y » propre). Double slash « 01/01//2027 » éliminé (compromis régénéré : `//` absent).
- [16:20] **ACTION** FA6 (A26-02) montant déblocage minimum : reste vide par défaut (confirmé).
- [16:20] **ACTION** FA7 (A26-09) prix global SCM en lettres : dérivé d'office de `global` via
  `number_words_from_value` (même helper que la valeur nominale), champ auto affiché.
- [16:20] **ACTION** FB1 (A26-42) « Lyon (France) » → département : le COMPROMIS médical rend
  `[pays_naissance_vendeur]` dans la parenthèse de naissance ; on y câble le DÉPARTEMENT saisi
  (fallback « France » si absent). Compromis régénéré : « Lyon (69) ». L'acte (token département)
  restait correct. Aucun générateur/modèle touché.
- [16:20] **ACTION** FB2 (A26-43) origine de propriété vide : la date+mode (créé) étaient déjà
  câblés ; la phrase ne se construit QUE si la date est saisie (générateur ligne 979). Preuve e2e :
  date renseignée → « ... pour l'avoir régulièrement créé le 01/01/2020. » Le vide d'Albane venait
  de la date non saisie (elle n'avait plus accès à son formulaire, cf. note carnet). Cabling OK,
  test de non-régression ajouté. **NB** : le générateur n'accentue pas une date JJ/MM/AAAA
  (échoue le mois en lettres) — il l'écho « 01/01/2020 » ; comportement générateur, hors périmètre front.

- [16:20] **AUDIT (à lancer)** Gate Akainu sur les 10 items du lot (FA1-FA7, FB1-FB3) contre
  leur verbatim propre, avant toute déclaration TRAITÉ (règle 66).

---

## 2026-06-22 — session retours R22 + audits

- [~10:00] **R-RAFAEL** Rafael répond au lot précédent : « toute la première page du document - oui ajuste » (réponse R22-06 + accents).
- [10:24] **ACTION** RAF-004 : exemples de réponse attendue (`help=`) sur les champs à risque, tous types (`6934b2d`).
- [11:03] **ACTION** SPFPL cession : note DOC-037 + PV agrément DOC-038/039 + acte DOC-040 (`28c96ad`).
- [11:20] **ACTION** SCM inter-SEL : contrat frais communs DOC-027 + règlement DOC-028 (`e859a2c`).
- [~11:30] **Q-RAFAEL → R-RAFAEL** batch de 6 remarques reçu (SELARL accents + conjoint fantôme ; SCM 2 docs manquants ; SCI option IS ; SCI IRIS mise en forme + [centre_impots]). Consigné REGISTRE_RETOURS R22-01→07.
- [11:50] **ACTION** R22-03/04 : SCM frais communs + règlement générés par défaut + champs visibles (`c2d3498`).
- [11:58] **ACTION** R22-05/07 : option IS démontrée au bouton SCI/IRIS + centre des impôts figé « Centre des Finances Publiques » (`e994127`).
- [12:11] **ACTION** R22-02 : pas de conjoint fantôme quand le cédant n'est pas marié (helper partagé `mentions_conjoint`, 2 actes de cession) (`c197875`).
- [12:20] **ACTION** R22-01 : accents « composés d'une pièce » (descriptif local cession) (`08542f3`).
- [12:23] **DÉCISION** R22-06 d'abord bloqué « précisions Rafael » : moteur déjà structuré, from-scratch ratifié → besoin du pointeur exact (`8123de9`). Puis Rafael précise « toute la première page ».
- [12:36] **MÉTHODE** garde-fou « périmètre exact, zéro extrapolation » gravé (validation Rafael avant tout choix neuf non sourcé) (`5e6edb7`).
- [13:32] **ACTION** R22-06 : statuts civils respectent la mise en forme de la 1re page source (en-tête centré, « LES SOUSSIGNES » gras+souligné, comparution gras) — moteur partagé, 4 types civils (`ae53bb8`).
- [13:33] **ACTION** untrack + gitignore des scripts repro `_audit_*.py` d'agents (`991f314`).
- [13:42 / 13:49] **MÉTHODE** Phase 6 RESTITUTION : format message retest Rafael (court/froid/puces/copier-collable ; reboot Streamlit = action de GAD) (`6c57dce`, `79e7936`).
- [~13:00→14:00] **AUDIT** 3 audits read-only lancés (opus, fan-out 10 types + vérif adversariale) :
  - cohérence inter-docs (`w767ud7w7`) → **fini** : « bloquant SCM » = **FAUX POSITIF vérifié** (source utilise `[adresse_locaux]` pour la partie 2, spec confirme) ; 4 « majeur » à recouper.
  - dogfood robustesse (`wrb1xv6kq`) → **fini** : 7 bloquants + 11 majeurs (asymétrie front/générateur + divisibilité + 0-passant).
  - propagation des corrections (`wbr7yj7cl`) → **fini** : 6/15 corrections ont des trous de code (R22-02 incomplet sur SPFPL ; ALB-numéro-ordre ; etc.).
- [13:59] **ACTION** garde de divisibilité capital/parts partagée → ferme 2 bloquants + 2 majeurs sur 4 types (`ec45978`). Bug confirmé empiriquement avant fix (règle 65).
- [~14:00] **INCIDENT (nous)** la passe propagation montre que R22-02 n'avait PAS été propagé aux statuts/apport SPFPL (mon sous-scopage) → à compléter.
- [14:04] **MÉTHODE** création de ce journal de bord (demande Gad : tracer la totale, rejouer l'histoire, remonter les conneries Rafael).
- [~14:20] **R-RAFAEL** batch 2026-06-22b : (1) `courrier_sde_cession_scm` retirer surlignage/rouge ; (2) « compromis cession cabinet médical manquant ».
- [~14:30] **MÉTHODE** RÈGLE ABSOLUE gravée (global 07 + mémoire) : traiter en continu jusqu'à épuisement, sans pause ni « je continue ? ».
- [~14:40] **ACTION** R22b-01 : rouge + surlignages retirés du courrier SDE (générateur + 3 tests inversés). 509 verts.
- [~14:45] **INCIDENT (Rafael)** R22b-02 « compromis médical manquant » = NON-BUG vérifié (DOC-010 généré quand étape=compromis ; testé en acte = G2 test partiel).
- [~15:00] **INCIDENT (Rafael) — G4** Rafael a demandé par mail à **Albane + David (clients)** de tester la SCM AVANT que le fix soit confirmé prêt/déployé côté dev (Streamlit pas rebooté → ancienne version cassée). Exposition prématurée du décideur + de la direction juridique, sans coordination dev. Noté en mémoire grievances G4.
- [~15:05] **ACTION** 3 bloquants dogfood civils corrigés (capital=0, banque_adresse, associé PM sans représentant) (`912b89e`). 512 verts.
- [~15:20] **R-GAD** « reboot fait » (Streamlit) ; les clients tombent sur la version corrigée.
- [~15:30] **ACTION** bloquants SPFPL cession (chaîne cible) + 0-guard nb_actions (`5178be4`). 514 verts.
- [~15:50] **ACTION** 2 derniers bloquants dogfood : SELARL multi (Ordre membre) + SELAS uni (conjoint vide). **7/7 bloquants dogfood corrigés.** 516 verts (`b68be80`).
- [~16:05] **INCIDENT (Rafael) — G4** Rafael demande aux clients (Albane+David) de tester la SCM avant fix confirmé/déployé. Noté grievances G4. Mon avis : ~80% légitime (exposition prématurée + pas de coordination dev). Gad reboote pour mitiger.
- [~16:20] **ACTION** SAS apports↔capital (majeur) + trace R22-02 SPFPL (différence justifiée marié-only) (`eb0bf70`). 517 verts.
- [~16:35] **ACTION** Cohérence : PV nomination dit « actions » pour une SELAS (pas « parts ») — ignorait `capital.type_titre` (`cbd8aa1`). 517 verts.
- [~16:40] **DÉCISION** recoupe des gaps restants un par un (règle absolue + « revérifie les sources »).
- [~17:00] **ACTION** Métier SOURCÉ : SCS gérant=commandité (NotebookLM) + SAS cohérence civilité↔genre (`06a4b1e`). 520 verts.
- [~17:15] **ACTION** Cohérence : en-tête PV SCI IRIS affiche « SCI » (pas la clé interne « SCI IRIS ») (`a6b52c2`). 521 verts.
- [~17:25] **RECOUPE (vérifié, flag)** SELAS conjoint-adresse : `_associe_signataire_address` retombe DÉLIBÉRÉMENT (documenté) sur l'adresse du président quand le foyer est vide → imparfait mais pas un crash ; le bon fix (retomber sur l'adresse de l'associé marié) touche le contexte SELAS multi → passe dédiée.
- [~17:40] **RECOUPE des ALB-gaps un par un (règle 65)** :
  - **ALB-numéro-ordre** = FAUX POSITIF (le n° d'ordre EST requis en validation → « rendu cassé si vide » impossible).
  - **ALB-euros art.8** = RÉEL (correction Albane 2026-06-10 non propagée au médecin) → corrigé « de [capital_lettres] euros » + lock ajusté (`7268220`). 521 verts.
  - **ALB-genre-professionnalité** = non-bug (sortie correcte « Monsieur Camille Martin », propreté de code).
  - **ALB-nationalité-dropdown** = non-bug (même valeur en sortie ; incohérence UX seulement).
- [~17:45] **BILAN** findings d'audit ÉPUISÉS : tous bloquants + majeurs réels corrigés ; faux positifs écartés (règle 65) ; non-bugs notés. **Seul reste fonctionnel = SELAS conjoint-adresse** (repli président documenté, edge étroit, fix = contexte SELAS multi → passe dédiée).

## 2026-06-22 (suite) — MACHINE bloc-gold + refonte SELAS

- [~18:30] **DÉCISION (Gad)** premisse cadrée : **SELARL = gold valide**, **on retravaille la SELAS** avec la machine bloc-gold. Construire la machine puis la valider en lecture seule sur la SELAS (doit retrouver l'onglet 24 seule).
- [~18:45] **AUDIT/MÉTHODE** organe 1 de la machine = **audit de fidélité au gold** (`machine-fidelite-selas-vs-selarl`, 17 agents, read-only). Résultat : **9/15 onglet 24 retrouvés seul, 0 faux positif** + **4 bugs net-new (B1-B4)** hors onglet 24. **Limite nommée** : aveugle aux retours qui demandent de S'ÉCARTER du gold (lit « conforme » = « identique au gold »).
- [~18:55] **AUDIT/MÉTHODE** organe 2 = **conformité à l'intention ratifiée** (`machine-organe2-conformite-intention-selas`, 16 agents, read-only). Rattrape les 6 manques de l'organe 1 (#4,9,12,13,14,15). **Ensemble : 15/15 cernés + 4 bugs.** Aucune décision métier neuve dans le lot (codable sans Albane/David).
- [~19:00] **DÉCISION** machine validée → backlog figé en canon `docs/review/BACKLOG_REFONTE_SELAS_2026-06-22.md`. Garde-fou d'exécution : **protéger le gold** (changements sur fichiers partagés = conditionnés SELAS) ; **commits locaux, pas de push** (Streamlit auto-deploy + clients testent → fenêtre = Gad).
- [~19:10] **ACTION** refonte SELAS lot 1 : **#1** (annexe SPFPL — retrait « lettre de mission / acompte Sydel », lignes uniques 374-375) + **B1** (`acquereur.forme_sociale` post-corrigé « SELAS » en cession SELAS multi, gold intact). +2 tests non-régression. **523 verts.** Commit local `d085287` (pas de push : Streamlit auto-deploy + clients testent → fenêtre = Gad).
- [~19:30] **ACTION** refonte SELAS lot 2 (zone associé/dirigeant) : **#7** (validateur non-cumul — 1 Président, 1 DG max) + **#8 / B4** (adresse personnelle STRUCTUREE saisie UNE seule fois au niveau associé, calquée sur le gold ; réutilisée par la DNC du dirigeant, les DG du PV et l'avertissement conjoint ; date DNC dérivée du champ texte via parseur étendu « 1 janvier 1980 » ; champ foyer séparé supprimé → corrige aussi le repli-président B4). **Refactor de FORMULAIRE pur : docs générés identiques** (suite verte le prouve). +2 tests + 1 migré. **524 verts.** Commit local `1c0e448`.
- [~22:30] **DÉCISION** refonte SELAS **#4** (icône copier par champ) **DIFFÉRÉ** : pure UI, SELAS-only (helpers locaux `_ts`/`_is`, **pas** le chemin `front_widgets.py:1790-1803` halluciné par la machine). La copie presse-papier sur Streamlit exige un **composant JS par champ** (iframe) → lourd + fragile sur un formulaire vu par les clients. Per consigne « le plus simple, ne rien casser » : posé en **suivi UI dédié**, pas de hack fragile. **14/15 onglet 24 livrés** (le 15e = ce cosmétique).
- [~22:35] **ACTION (push)** refonte SELAS poussée sur `sprint/engine-completion` (Streamlit auto-deploy) : **14/15 onglet 24 + B1/B4**, 532 verts, ruff propre. B2 = faux positif écarté. Questions métier accumulées dans `QUESTIONS_RAFAEL.md` (#9 wording, #2 DNC par dirigeant, DOC-008, #12 lieu_exercice, B3). Message retest Rafael préparé (Gad envoie).
- [~22:15] **ACTION** refonte SELAS **#12** (onglet 24) : case « Siège social = même adresse que le lieu d'exercice » (remplace l'ancienne « = adresse président ») ; recopie cross-rerun du lieu d'exercice vers le siège structuré via parse best-effort `_parse_one_line_address` (« voie, cp ville »). **B3** (retrait du champ siège libre redondant) : conservé pour l'instant (dette technique, éviterait la validation « Siège requis » — noté QUESTIONS_RAFAEL). +2 tests, ruff propre. **532 verts. 14/15.**
- [~21:55] **MÉTHODE (Gad)** « arrête de me poser des questions » : pour un arbitrage Rafael/Albane inconnu → faire le plus simple + accumuler dans `docs/review/QUESTIONS_RAFAEL.md`, JAMAIS demander à Gad ni carte, continuer jusqu'au bout. Codifié (mémoire `feedback-no-questions-to-gad-accumulate-rafael`).
- [~22:00] **ACTION** refonte SELAS **#9** (onglet 24) : champ « profession » de l'associé RETIRÉ du formulaire (redondant avec la qualification) ; titre « Docteur » DÉRIVÉ côté moteur → **comparution inchangée** (« Docteur [qualification] »). Question wording accumulée pour Rafael (QUESTIONS_RAFAEL #9). +1 test, ruff propre. **530 verts.**
- [~21:35] **AUDIT (règle 65) — chemin halluciné par la machine.** L'organe 2 citait `business_wizard.py:294-305` pour #10 : **ce fichier n'existe pas** dans le clone (vérifié). Le `cabinet_type` n'est qu'un vestige du catalogue legacy (`case_catalog.py`). Cible réelle = le menu « Type de cabinet » du formulaire cession (shell.py). Recoupé avant d'agir.
- [~21:40] **ACTION** refonte SELAS **#10** (onglet 24) : en SELAS, le type de cabinet (médical/dentaire) est DÉRIVÉ de la profession → menu « Type de cabinet » supprimé (caption à la place), SELAS-conditionnel. +1 assertion. **529 verts.**
- [~21:20] **ACTION** refonte SELAS **#11** (onglet 24) : le vendeur du cabinet est un associé SELECTIONNABLE (menu) parmi les associés physiques (défaut = président, byte-identique pour le cas courant) ; le wording « associé unique » de la case partagée est remplacé en SELAS par « le vendeur est l'associé sélectionné ci-dessus ». Cluster CESSION complet (#11/#13/#14/#15). +1 test, ruff propre. **529 verts.**
- [~21:00] **ACTION** refonte SELAS **#14** (onglet 24) : en SELAS, l'ACTE ET le COMPROMIS de cession sont produits ENSEMBLE pour le type de cabinet (l'étape n'est plus filtrante). 2 édits SELAS-conditionnels : `_cession_codes` émet les deux codes (type seul), `orchestrator._cession_cabinet_enabled` génère les deux quand `structure==SELAS` (étape filtrante conservée hors SELAS). +1 test. **528 verts.**
- [~20:45] **ACTION** refonte SELAS **#13** (onglet 24) : en cession SELAS, le CA + le résultat des exercices ne sont plus facultatifs → validation `_validate_cession_exercices` (bloque tant qu'un exercice saisi a un CA/résultat vide) + mention « (facultatif) » retirée des labels (SELAS-conditionnel). +1 test. **527 verts.**
- [~20:30] **ACTION** refonte SELAS **#15** (onglet 24) : en SELAS, l'acquéreur EST la société en cours de création → le bloc de SAISIE acquéreur (RCS/SIRET/dates) n'est plus rendu (conditionné `prefix != "selas"` dans le formulaire cession partagé) ; payload entièrement dérivé de la fiche société (forme corrigée « SELAS » par B1). **Gold SELARL intact.** +1 test. **526 verts.**
- [~20:00] **ACTION** refonte SELAS **#2** (onglet 24) : la DNC porte le NOM DU DIRIGEANT dans son nom de fichier (`declaration_non_condamnation_Durand.docx`) — renommage de la DNC du président produite par l'orchestrateur. **[MÉTIER À CONFIRMER Albane :** si CHAQUE dirigeant (DG inclus) doit déposer SA propre DNC → générer une par dirigeant ; non tranché ici, no-extrapolation.] 4 tests SELAS alignés + 1 test dédié. **525 verts.**
- [~19:45] **AUDIT (règle 65) — B2 = FAUX POSITIF de l'organe 1.** La comparution SELAS multi (`statuts_selas_multi._add_physical_comparution`, « Source para 16 ») rend `[situation_maritale]` **brut par conception de SA source** (≠ le template gold sel_exercice qui injecte la clause conjoint). Le conjoint **est** bien utilisé là où la source SELAS l'exige (DOC-005/006 renonciation/avertissement via `_conjoint_person`). Injecter le conjoint dans la comparution **dévierait** de la source SELAS → on ne touche pas. C'est précisément la limite nommée de l'organe 1 (gold = seule vérité). **B2 non corrigé : par décision de source, pas par oubli.**

## 2026-06-23 (nuit) — CAMPAGNE FIX AKAINU (boucle fix → re-Akainu jusqu'à RIEN À REDIRE)

- [~] **AUDIT** Sweep Akainu (18 auditeurs) sur les retours « traités » : **8 BLOQUANT + 16 MAJEUR**, 10 retours re-ouverts. Le carnet déclarait O24-01 « propagé tous types » = FAUX (prouvé sur DOCX régénérés). Verdict : `AKAINU_VERDICT_2026-06-23.md`.
- [~] **MÉTHODE** (Gad) : boucle `fix → Akainu → fix` jusqu'à RIEN À REDIRE codifiée (règle 66 + GATE 4 Operating Model). + règle Q4 propagation (un retour se propage à tous les cas concernés). + dashboard à chaque complétion.
- [~] **FIX O24-01** (annexe Sydel) : golden-bloc — prédicat partagé `annexe_filter.is_creation_fee_annexe_line` dans les 3 boucles de rendu + garde `_assert_clean`. **re-Akainu RIEN À REDIRE** (12 DOCX régénérés, ligne « compte bancaire » conservée). `dc530c8`.
- [~] **FIX O24-10** (dérivation profession→type) : `"dentiste" in casefold()` (tiret vs underscore) → dentaire produit du dentaire (DOC-011/012). **re-Akainu RIEN À REDIRE**. `be7ee6c`.
- [~] **FIX LIVE-03** (mois accentués) : fixture prod `scm_cession` « 15 aout » → « août » + test sur la vraie fixture (le test existant la masquait). `8e14d7c`.
- [~] **DETTE (latente, hors prod)** : course de fichiers sur le rename DNC (`rename_dnc_with_signataire`, `path.replace`) en exécution pytest **parallèle** (passe en séquentiel ; chaque dossier prod a son output_dir → pas un bug prod). À durcir si la CI passe en `-n`.
- [~] **RESTE** (bloquant/majeur) : O24-03, O24-14 (bloquant) ; O24-05/07/11/12, LIVE-02 (majeur).

## 2026-06-23 (soir) — TEST GRANDEUR NATURE : retours traités VIA la machine (WF-RETOUR)

- [~] **R-GAD** : feu vert pour traiter les retours onglet 24 + live AVEC la machine (Operating Model) ; les résultats diront si la machine a marché.
- [~] **R-GAD (méthode)** : ajouter un **agent « méchant »** adversarial qui passe sur CHAQUE livrable et remonte le moindre défaut, sans complaisance (Gad en a marre de passer pour un idiot devant Rafael). → Franky crée l'agent + règle gate. PUIS re-vérifier TOUS les retours (même traités/validés) avec un méchant par retour.
- [~] **ACTION O24-02** (WF-RETOUR) : « dans tous les cas où il y a une DNC, générée d'office par dirigeant, nom du dirigeant dans le fichier ». Align via Explore (carto par type) : 9 types produisent la DNC en nom générique (mono-dirigeant) ; SELAS multi seul fait. Helper partagé `rename_dnc_with_signataire(paths, ctx)` (ui_runtime) câblé dans les 5 entrées `generate_dossier` (SELARL, SAS, SPFPL, civil SCI/IRIS/SCS/SCM, SELAS-uni) → DNC = `declaration_non_condamnation_<Nom>.docx`. Le test gate a **cassé 22 tests** (preuve que le renommage marche) → corrigés (`_assert_bundle_clean` normalise pour la complétude, tests SELARL/SELAS dédiés vérifient le nommage). **Verbatim gate OK. 535 verts, ruff propre.** TRAITÉ (≠ validé).
- [~] **ACTION O24-12** (WF-RETOUR) : « adresse du cabinet → case "même adresse que le lieu d'exercice" + report ». Case posée sur le CABINET de la cession (pas le siège), SELAS, quand un lieu d'exercice existe ; cochée → recopie le lieu d'exercice (1 ligne, O24-03) dans l'adresse du cabinet. Lieu d'exercice câblé `_render_selas_cession` → `societe`. +1 test. **Verbatim gate OK. 535 verts, ruff propre.** TRAITÉ (≠ validé).
- [~] **ACTION O24-03** (WF-RETOUR) : « toutes les adresses sur UNE ligne, pas de champ séparé ». Align = les générateurs (DNC/domiciliation `[num_voie_siege]`/régime communautaire) exigent `num_voie/voie/cp/ville` → saisie 1 ligne **+ parse interne** (`_parse_address_full`, sépare le n° de la voie). Perso + siège SELAS passés en 1 champ ; **fausse case « siège = lieu d'exercice » retirée** (migrera sur le CABINET en O24-12, conforme verbatim) ; prefills + test alignés. **Verbatim gate OK** (relu clause par clause). **534 verts, ruff propre.** Statut TRAITÉ (≠ validé). O24-12 débloqué.

## 2026-06-23 (après-midi) — PIVOT : bureau des retours (« comme une petite entreprise »)

- [~12:00] **R-GAD** : « la majorité des retours pas traités » → 5 retours marqués « fait » à tort (vérifiés contre la **paraphrase** de la machine, pas le **verbatim** client). Process imposé : carnet, **traité ≠ validé**, re-montrer la liste avant chaque item, point RH.
- [~12:10] **ACTION** O24-05 (valeur nominale) généralisée à SAS/SPFPL/SELAS-uni/Civil (retrait `key=` qui figeait l'affichage). **534 verts.**
- [~12:15] **MÉTHODE** point RH (Franky) appliqué : patch `uat-fix-loop` (verbatim gate + deployment-before-stale), mémoires `feedback-carnet-traite-vs-valide` + `feedback-machine-decouverte-pas-spec`.
- [~12:20] **R-GAD** : monter un vrai **bureau des retours** « comme une entreprise » (collecte → classe → dispatche → suit) + un **agent grand organisateur** + des bibliothèques rangées ; **stopper le dev** tant que ce n'est pas carré à 100 %.
- [~12:25] **DÉCISION** agent **Vivi** (`returns-intake-organizer`) créé par Franky (anti-surcharge OK, 19/20) + règle globale `68-returns-triage-gate` (les 3 questions). Casting Manifeste mis à jour.
- [~12:30] **R-GAD** : outil « Claude Taskmaster » ? → **éval à froid** : ne pas adopter (fait pour décomposer un PRD, reformule = perte de fidélité, duplique le carnet, pas de double état) ; **5 idées volées** (source unique versionnée, statut grep-able, dépendances explicites, IDs hiérarchiques, contextes par branche).
- [~12:35] **R-GAD** : exige une **méthode de classement professionnelle avec règles**. → hub `docs/returns/` monté : `README` (carte), `METHODE` (rulebook : IDs, schéma, statut fermé, dépendances, double axe), `CARNET` (file active, ré-ancrée au verbatim exact de l'onglet 24), `TRIAGE` (3 questions par retour), `JOURNAL`, `VALIDES`, `SOURCES_DE_VERITE` (test d'anticipabilité + trou confirmé = parité SELAS↔gold).
- [~12:40] **AUDIT (verbatim)** O24-12 = « adresse du **cabinet** » (pas le siège) : mon implémentation précédente sur le siège était fausse → reclassée, à refaire après O24-03. **Dev en pause** : O24-02/03/04/12 + LIVE-05/06 restent dans le carnet.

## 2026-06-23 — retours Rafael (live retest)

- [~00:30] **R-RAFAEL** retours sur la SELAS testée : (R1) supprimer le cas « multi-associés création v1 » ; (R2) renommer « SELAS dentiste pluripersonnelle » → « SELAS pluripersonnelle » (profession choisie dans le cas) ; (R3) dirigeants — il MANQUE le rôle « Directeur Général Associé » (chaque associé = Président OU DG OU DGA) ; (R4) « la date de naissance est toujours deux fois » ; (R5) « tu as mis les modifs sur le mauvais cas ».
- [~00:40] **AUDIT (règle 65) — diagnostic « mauvais cas ».** Vérifié : `selas_multi_v1` ET `selas_dentiste_pluri_v1` partagent **la même slice** `selas_multi_slice` → mes modifs étaient sur **les deux** (dont la pluripersonnelle). Le 3e cas (`selas_uni_medecin_v1`) = slice à part, non concerné. **R4 = version pré-reboot** : le code n'a QU'UNE date (ligne 821, vérifié). **R5 = pas une erreur de code** : confusion née de 2 cas redondants (notre part) + test sur version pas déployée. Restitué à Gad.
- [~01:00] **ACTION** R1+R2 : **fusion en UN seul cas « SELAS pluripersonnelle creation V1 »** (clé interne `selas_multi_v1` conservée, déjà en profession libre) ; suppression de l'entrée `selas_dentiste_pluri_v1` + de son pré-réglage profession + de son prefill par-clé. Corpus dentiste/médecin piloté par la profession (choisie au menu). Tests alignés (label + corpus dentiste via choix de profession).
- [~01:10] **ACTION** R3 : rôle **« Directeur Général Associé »** ajouté au menu (manquait) ; cardinalité 1 Président / 1 DG / plusieurs DGA (validateur inchangé : ne bloque que >1 Président ou >1 DG ; le PV rend le rôle génériquement). +1 test. **532 verts, ruff propre.**

- [~02:00] **R-RAFAEL (2e salve)** : R6 retirer le cas multi-associés ; R7 DNC de TOUS les dirigeants ; R8 ne pas demander le régime matrimonial (case = communauté par défaut) ; R9 le DGA n'est toujours pas inclus.
- [~02:10] **ANALYSE (demande Gad « déjà eu ou nouveau ? »)** : **R6 = R1 déjà fait** (`ae234e9`, version non déployée) ; **R9 = R3 déjà fait** (idem) → Rafael teste encore une **version pré-reboot** (re-signale des choses corrigées). **R7 = anticipé** (c'était notre question #2 dans QUESTIONS_RAFAEL). **R8 = nouveau** mais redondance repérable (la case implique déjà communauté). Restitué à Gad + tableau « validé par le silence ».
- [~02:30] **ACTION R8** : champ « régime matrimonial » du conjoint RETIRÉ (la case « marié sous régime communautaire » l'implique) ; régime fixé « la communauté légale » (la renonciation le rend « communauté »).
- [~02:45] **ACTION R7** : **une DNC PAR dirigeant** (Président renommé + une générée par DG / DG Associé via `_dnc_context_for_dirigeant`, signataire = ce dirigeant ; identité/adresse/date de l'associé, filiation de sa case). Validation : filiation requise pour chaque dirigeant non-président (évite le crash DNC). +2 tests (DNC×2 nommées). **533 verts, ruff propre.** Remplace le défaut #2 (1 DNC) par la version pleine demandée.

- [~03:00] **R-RAFAEL (3e salve)** : R10 situation matrimoniale → menu (comme SELARL), communauté → conjoint + docs ; R11 retirer la case « marié sous régime communautaire » ; R12 « decembre → décembre » ; R13 valeur nominale toujours pas affichée.
- [~03:10] **ANALYSE (Gad)** : **R13 = #5 déjà demandé mais MAL FAIT** (champ `value=`+`key=` figé par Streamlit → jamais rafraîchi) ; **R10/R11 = alignement-gold qu'on aurait pu anticiper** (le SELAS divergeait du pattern SELARL : texte libre + case au lieu d'un menu pilote) ; **R12 = vrai nouveau** (typo). Motif récurrent confirmé : SELAS construit en divergeant du gold.
- [~03:20] **ACTION R13** : retrait de la `key` du champ valeur nominale → il affiche la valeur courante recalculée (capital/nb actions).
- [~03:40] **ACTION R10/R11** : situation matrimoniale = **menu** `MATRIMONIAL_STATUS_PRESETS` (réutilise les helpers gold `matrimonial_status_value` / `regime_communautaire_from_status`) ; quand un régime de COMMUNAUTÉ est choisi → champs conjoint + DOC-005/006 (`_render_conjoint_si_communaute`). **Les DEUX cases régime retirées** (per-associé ET globale `_render_common_docs_form`). `_situation_display` = mot d'état civil accordé/accentué pour la comparution. +1 test (communauté → docs conjoint). **534 verts, ruff propre.** [Flag Rafael : j'ai retiré AUSSI la case globale « Régime communautaire » — dis si tu la voulais.]

- [~04:00] **ACTION R12 + RÈGLE GLOBALE (Gad « modifie de partout + règle globale mois »)** : noms de mois en SORTIE toujours accentués (`_MONTHS` → février/août/décembre ; seeds `front_widgets` → « 31 décembre » ; prefills shell.py « 2 février 1982 », etc.). **Maps de PARSING gardées sans accent** (le parseur normalise NFKD). 2 assertions de form mises à jour. Règle codifiée (mémoire `convention-mois-accentues` + commentaire dans `_MONTHS`). **534 verts, ruff propre.**

## 2026-06-23 — machine des retours + boucle Akainu (perfectionnement avant reprise)

- [~T1] **AUDIT (Akainu, gate règle 66)** : passe adversariale sur les 18 retours « traités » → 10 défauts RE-OUVERTS (traité ≠ validé). Corrigés un par un en boucle fix→Akainu.
- [~T1] **ACTION** 10 défauts corrigés ; O24-01 (annexe Sydel) + O24-10 (dérivation dentaire) + LIVE-02 re-Akainu = RIEN À REDIRE. Registre golden-blocs créé (`docs/operations/GOLDEN_BLOCS.md`).
- [~T2] **AUDIT (batch re-Akainu, 8 items)** : re-vérification adversariale par RÉGÉNÉRATION réelle → **5 MAJEUR** prouvés (mes fixes O24-07/11/12 = surface UI, pas racine ; + régression que J'avais introduite sur O24-03 : le parser prenait « 8 Mai 1945 » pour un CP). Vindication de la boucle : Akainu a attrapé avant Rafael.
- [~T2] **ACTION** corrections **à la racine** (`1702638`) : O24-03 parser (CP = dernier groupe de 5 chiffres) ; O24-07 plus de requalification DG→Président ; O24-11 conjoint capté tout régime marié + dissociation situation/régime ; O24-12 case cabinet réversible. Tests durcis (cas-limites, cardinalité rôles, dissociation, acte+compromis ensemble). **545 verts, ruff propre.**
- [~T2] **Q-RAFAEL** (accumulées, jamais demandées à Gad) : Président obligatoire en SELAS ? cumul Président+DG+DGA ? numéro de voie optionnel ? wording case cabinet ? « SELARL » figé dans les modèles de cession SELAS → `QUESTIONS_RAFAEL.md`.
- [~T2] **AUDIT** re-Akainu tour 2 relancé sur les 7 items re-corrigés (objectif RIEN À REDIRE).
- [~T2-verdict] **AUDIT (re-Akainu tour 2)** : O24-07 = RIEN À REDIRE (fermé ✅). 6 autres = DEFAUTS, dont 3 MAJEUR : O24-03 (incohérence parser↔validateur sur le numéro — issue de MON extrapolation « numéro optionnel »), O24-11 (PACS capté mais droppé à l'acte — MON extrapolation), O24-14 (VRAI bug : salariés repris → compromis crashe dans le bundle). + MINEUR/NITPICK (SCM valeur nominale, édition cabinet, tables mois).
- [~T3] **ACTION** corrections tour 2 (`a152bf4`) : O24-03 REVERT numéro requis (verbatim-exact, cohérent validateur) ; O24-11 PACS retiré + fallback régime corrigé ; O24-14 le compromis IGNORE les salariés du contexte partagé (plus de crash) ; O24-05 SCM valeur nominale auto-calc ; O24-12 édition manuelle cabinet préservée ; LIVE-03 garde DOCX + parité mois. **550 verts, ruff propre.** Leçon : ne pas extrapoler hors verbatim (numéro, PACS) — mémoire `feedback-fixes-racine-pas-surface`.
- [~T3] **Q-RAFAEL** ajoutées : lieu-dit sans numéro (O24-03), périmètre PACS (O24-11) → `QUESTIONS_RAFAEL.md`.
- [~T3] **AUDIT** re-Akainu tour 3 relancé sur les 6 items résiduels (objectif RIEN À REDIRE).

## 2026-06-25 — lot Albane 14 items (Lot A/B/C/D) + boucle Akainu

- [~] **ACTION** Lot A (SU3 ville signature=siège ; SU4 date nomination=signature ; SCS2 date PV=signature), Lot B SCS (SCS1 retirer conseiller ; SCS3 Fonction→gérant ; SCS4 bloc régime matrimonial repris de SELAS pluri ; SCS5 liste souscripteurs actions→parts ; SCS6 nom statuts dynamique), Lot C (SU1 situation matrimoniale 1 champ déroulé SELARL ; SU2 « conseil départemental {dept} » sans « de l'Ordre »), Lot D SP2 (civilité M./Mme défaut front) → tous **Akainu RIEN À REDIRE**, poussés.
- [~] **ACTION** Lot D cessions : acte_cession_parts_spfpl + acte_cession_actions_spfpl rebâtis/confirmés token-replacement fidèles + helper partagé `elision_de` (utils/grammar) appliqué à 6 sites (« de cent euros »/« d'un euro ») → Akainu RIEN À REDIRE exhaustif. SP4 (« réutiliser les blocs validés SELARL ») = satisfait par ces rebuilds fidèles.
- [~] **AUDIT (Akainu)** contrat_apport : MAJEUR M1 round 2 — `_addr_display` rendait un BLANC silencieux (« Siège social :  ») sur `Address(adresse_affichee="")` + sous-champs vides (cas atteignable en prod, front `Address(adresse_affichee=str(...) or "")`).
- [~] **ACTION** (`d3329d0`) contrat_apport M1 r2 : `_addr_display` repli sur `required_text` (marqueur « (À COMPLÉTER : …) », R10) — jamais de blanc, cohérent avec jumeaux `company_siege_display`/`person_address_display` ; test cas adresse vide ajouté.
- [~] **AUDIT (Akainu)** 2 PV agrément cession SPFPL : BLOQUANT B1 — accentuation SP3 (« revoir les accents ») massivement incomplète (from-scratch entièrement non accentué) ; MAJEUR M1 « la SPFPL » hardcodé (dénomination ignorée) ; MAJEUR M2 test faible (aucune assertion accents).
- [~] **ACTION** (`d3329d0`) PV B1/M1/M2 : accentuation exhaustive pv_agrement_common + 2 PV + `capital_after_lines` (numérotée/numérotées) ; `add_ordre_du_jour(docx, ctx)` rend `ctx.societe_spfpl.denomination` réelle ; garde-fou `_assert_french_accents` (liste noire) + assertion dénomination. Re-génération réelle re-scannée = zéro résidu. **627 verts randomisés.**
- [~] **AUDIT** re-gate Akainu relancé sur contrat_apport (M1 r2) + 2 PV (B1/M1/M2), objectif RIEN À REDIRE (boucle règle 66).

## Conneries / incidents Rafael (résumé — détail dans la mémoire privée)
- **G1** (2026-06-22) : nouvelle remarque sur la SELARL « validée 100 % » et socle de tous les types (confirmé par Rafael : nouvelle remarque, pas régression).
- **G2** : ne teste pas réellement — preuve : 4 docs sur 7 produits non remarqués (docs non téléchargés).
- **G3** : source de vérité incomplète (NotebookLM caché) → 1er travail entièrement refait. Voir `rafael-collaboration-grievances`.

## Antérieur (2026-06-19 et avant)
Chronologie exacte dans `git log` (vague parité gold-anchored : 7 règles imposées `1d8ae1d`,
couche partagée `front_widgets`, consommation par tous les types `9f726dc`→`f5baf27`). Retours
antérieurs Rafael/Albane : `REGISTRE_RETOURS.md` + locks `docs/review/albane_*`.
