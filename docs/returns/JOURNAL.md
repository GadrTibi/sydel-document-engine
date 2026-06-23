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

## Conneries / incidents Rafael (résumé — détail dans la mémoire privée)
- **G1** (2026-06-22) : nouvelle remarque sur la SELARL « validée 100 % » et socle de tous les types (confirmé par Rafael : nouvelle remarque, pas régression).
- **G2** : ne teste pas réellement — preuve : 4 docs sur 7 produits non remarqués (docs non téléchargés).
- **G3** : source de vérité incomplète (NotebookLM caché) → 1er travail entièrement refait. Voir `rafael-collaboration-grievances`.

## Antérieur (2026-06-19 et avant)
Chronologie exacte dans `git log` (vague parité gold-anchored : 7 règles imposées `1d8ae1d`,
couche partagée `front_widgets`, consommation par tous les types `9f726dc`→`f5baf27`). Retours
antérieurs Rafael/Albane : `REGISTRE_RETOURS.md` + locks `docs/review/albane_*`.
