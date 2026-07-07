# CHECKLIST MAÎTRE — TRANSVERSE (conventions valables partout)

> Conventions à vérifier sur **CHAQUE document de CHAQUE type** avant tout TRAITÉ.
> Sources : CARNET.md (O24/LIVE/N/R0702) · CARNET_ALBANE_2026-06-26.md (A26) · CARNET_MISE_EN_FORME_18.md ·
> CARNET_FONCTIONNEL_SPFPL.md (ticket 2026-07-06) · QUESTIONS_RAFAEL.md · REGISTRE_PROPAGATION.md ·
> **retours Albane 2026-07-07 (transmis Gad — PAS encore dans les carnets à la date de ce fichier)**.
> Statuts : `fait` (TRAITÉ, ≠ validé client) · `partiel` · `pas fait` · `contradiction` (retours/décisions qui se contredisent — le plus récent prime).

## Montants

- [ ] Tous les montants en « LETTRES (chiffres) euros » — ex. « soixante mille euros (60 000 €) », jamais « 60 000 (soixante mille) » — verbatim Albane 7.5 (ticket 2026-07-06) + 2026-07-07 « six (6) euros, LETTRES puis chiffres » — statut : **partiel** (fait sur valeur nominale art.8 + prix acte via `montant_lettres_avec_unite` ; **l'en-tête capital des statuts SPFPL rend encore « [capital_social] ([capital_lettres]) euros » = chiffres (lettres) inversé**, `statuts_spfpl_templates.py:59`)
- [ ] Chiffres groupés par 3 (« 60 000 », jamais « 60000 ») dans TOUTES les figures (en-tête statuts, article APPORTS « Ci … 60 000 € », attestations, actes) — Albane 2026-07-07 — statut : **pas fait** (aucun helper de groupement des milliers ; `_format_amount` rend `60000`)
- [x] Montants en lettres écrits automatiquement partout (jamais de saisie manuelle des lettres) — N3 (2026-06-24) — statut : **fait** (46 sites auto, 0 manuel)
- [ ] Élision : « **d'un** euro », « **d'un** centime d'euro », « **d'une** part » — jamais « de un » / « de une » — Albane 2026-07-07 — statut : **contradiction résolue → à faire** (tracé n3 QUESTIONS_RAFAEL 2026-07-06 gardait « de un euro » comme défaut fidèle-modèle « à confirmer » ; **Albane a tranché le 07-07 : élision partout** ; helper `grammar.elision_de` existe, à appliquer)
- [x] Valeur nominale décimale en lettres : « un centime d'euro (0,01 €) » — Albane 7.5 (2026-07-06) — statut : **fait** (`monetary_words_from_value`, propagé SPFPL/SELAS/SAS ; SELARL uni figure-only hors périmètre, tracé)
- [x] Valeur nominale calculée automatiquement (capital ÷ parts), décimales autorisées — O24-05 + N1 — statut : **fait** (exclusion assumée : société CIBLE externe en saisie libre, tracé)

## « Docteur »

- [ ] « Docteur » N'EST PAS une civilité → retirer partout (tous cas, tout le moteur) ; civilité = M./Mme — Albane 2026-07-07 (répète SP2 du 2026-06-25 « supprimer docteur de la civilité » + A26-16 « un Docteur en trop ») — statut : **contradiction → chantier à ouvrir**. État réel : fait au front SPFPL (M./Mme, override SP2) et acte cession parts (civilité restaurée) ; **PAS fait** : `sas_slice.py` (défauts `civilite_affichage="Docteur"` lignes 554/611/665/710), `selas_multi_slice.py:1806` (fallback « Docteur »), `selas_uni_attestation.py:120`, champs praticien cession (R4 : vendeur/cédant portent « Docteur »), « Le Docteur » hardcodé dans le corpus statuts SPFPL (`statuts_spfpl_templates.py:39/51/429`) et le modèle attestation (« Le Docteur [Nom] a fait un apport »). **Contradictions à purger** : doctrine §14.2 ratifiée lot 2 (« Docteur » = titre auto en sortie) + défaut Q#9 (« titre Docteur conservé ») + fidélité-modèle (A26-45/49 demandaient d'AJOUTER « le docteur ») ⟂ 07-07 « retirer partout ». Le 07-07 prime (plus récent) ; préciser avec Albane si le TITRE dans le corps des actes de cession (« le docteur X », modèle source) tombe aussi.

## Orthographe / accords / accents

- [ ] Orthographe, accords et accents irréprochables PARTOUT — Albane 2026-07-07 (répète SP3 2026-06-25 « revoir les accents ») — statut : **partiel**. Fait : mois accentués (LIVE-03, `_MONTHS`), plages « 1 à N » accentuées (résolu Rafael 2026-07-01, commit `c609a33`), rebuild from-scratch SPFPL accentué (SP3). **Dettes connues** : `situation_maritale` rendue BRUTE non accentuée (« marie. », « pacse. ») pour les membres SELARL-multi/SCP (`statuts_sel_exercice_common.py:737`, dette transversale tracée au registre) ; typos préservées par fidélité-modèle (« effectué » contrat apport, tracé SP — décision Albane requise pour corriger un modèle source)
- [x] Accord en genre systématique (« nommée présidente », « qu'elle a décidé », « informé(e) » féminisable, « gérante associée ») — A26-21/39, mise en forme 2.2, A26-77 — statut : **fait** sur les surfaces traitées (lots 2026-06-26 + mise en forme) ; ⚠️ SAS actionnaire féminin toujours BLOQUÉ par garde pré-existante (`sas_slice.py:491`, arbitrage tracé)
- [x] Mois accentués en sortie (février/août/décembre) — LIVE-03 — statut : **fait** (convention globale)

## Sociétés en formation

- [ ] Société non immatriculée = « **en cours de constitution** » ; ne JAMAIS écrire « sous le numéro en cours » — Albane 2026-07-07 — statut : **contradiction résolue → à faire** (le verbatim 12.2 du 2026-07-06 ratifiait « immatriculée au RCS de [ville] sous le numéro en cours » ; **07-07 revient dessus** ; le front pose encore `numero_rcs="en cours"`, `spfpl_slice.py:1024` → l'acte rend « sous le numéro en cours ». Vérifier aussi A26-37 « retirer en cours d'immatriculation » dans les en-têtes)

## Répartition / associés

- [ ] Plage de parts AUTO-DÉDUITE de la répartition (20 parts → « 1 à 20 »), pas de saisie manuelle — Albane 2026-07-07 (prolonge N4 2026-06-24 + ticket 2026-07-06 §2 « supprimer les plages où inutiles ») — statut : **partiel** (auto : repeater civils `_assign_cumulative_part_ranges`, cession SCM N4, SELARL ; **SPFPL = texte libre** « écho fidèle saisie » par convention Rafael N4 → contredit par 07-07, à basculer en auto)
- [ ] Retirer un associé AU CHOIX (pas seulement le dernier) — Albane 2026-07-07 — statut : **pas fait** (`associe_repeater.py:105` : le bouton « Retirer un associé » décrémente le compteur → supprime toujours le DERNIER)
- [ ] UNE SEULE répartition du capital par acte (pas deux) — Albane 2026-07-07 — statut : **contradiction résolue → à faire** (le tracé 12.5(b) du 2026-07-06 concluait « PAS un bug : 2 recitals distincts EXPOSÉ + ORIGINE voulus, fidèle au modèle, défaut = conservés » ; **Albane a tranché le 07-07 : une seule** → reprendre l'acte de cession, cf. checklist `acte_cession_parts`)
- [x] Ajout d'un associé n'efface plus les précédents (bug rerun) — N5 Albane 2026-06-24 — statut : **fait** (3 repeaters + tests, Akainu RIEN À REDIRE)
- [ ] Omission-si-vide : plage « numérotées de … à … inclus » entièrement omise si non renseignée (jamais de phrase incomplète / « (À COMPLÉTER) ») — Albane 13 (2026-07-06) — statut : **partiel** (fait PV agrément SPFPL ; surfaces SCM `acte_cession_parts_scm.py:301` + `pv_age_cession_scm.py:226/338` rendent encore le marqueur — flag propagation tracé)

## Conjoint / matrimonial

- [x] Conjoint/partenaire affiché avec NOM quand marié OU pacsé ; jamais de mention PACS/mariage sans nom — Albane 6.3/7.3 (2026-07-06, SUPERSEDE l'exclusion PACS O24-11) + A26-18 + mise en forme 2.4 — statut : **fait** (helpers partagés `mentions_conjoint_ou_partenaire`, 942 verts, 2 tours Akainu ; ➖ˢ = statuts civils rendent le statut nu marié comme pacsé, fidèle modèle)
- [x] Menu « Régime matrimonial » identique partout (même que SELARL) — R0702-02 + LIVE-01/02 — statut : **fait** (SPFPL `7bb1f91`, SAS `b64f632`)

## Ordre professionnel

- [x] Département de l'Ordre en NOM (« Seine-et-Marne », jamais « 77 ») — Albane 7.4/9.2 (2026-07-06) — statut : **fait** (propagé ~14 surfaces, 2 tours Akainu RIEN À REDIRE, registre 2026-07-06)
- [x] Article de/du/des/de la devant le département (« du Jura », « des Bouches-du-Rhône ») — Albane 9.3/12.4 (2026-07-06) + 2026-07-07 (clause Conseil de l'Ordre de l'acte) — statut : **fait** sur acte + demande Ordre ; autres surfaces = risque faible tracé au registre (« ➖faible »)
- [x] Destinataire Ordre : « Conseil départemental de l'Ordre des {profession} de {département} » (profession PUIS département) — SU2/R5, résolu Rafael 2026-07-01 (`fc91f6f`) — statut : **fait** (la contradiction interne Albane 02/06↔25/06 est close par « comme les modèles »)

## Mise en forme (rappels durs)

- [x] Police Roboto 10 + interligne simple partout — mise en forme 1.1 + R0702-03 — statut : **fait** (⚠️ hiérarchie de titres SCI/SCI-IRIS volontairement préservée à 12/14 pt — flag Albane tracé)
- [ ] Annexe en UN SEUL cadre (pas de cadres multiples) — Albane 7.6 (2026-07-06) + 2026-07-07 « annexe en un seul cadre » — statut : **pas fait** sur SPFPL (absent du lot buildable traité) ; annexe civils validée (« l'annexe c'est top », R0702-03 ✅)
- [x] Saut de page avant l'annexe — N6 pt4 + mise en forme 2.10 — statut : **partiel** (fait SELARL/SELAS/SAS/civils ; **⬜ SPFPL cession + apport** — flag propagation tracé 2026-07-06)
- [x] Adresses sur UNE ligne (jamais de champs rue/voie séparés en sortie) — O24-03 — statut : **fait** (golden-bloc `address_oneline`, propagé tous types)
- [x] Titre du fichier statuts « Statuts [Nom société] » — A26-14 + 6.8 + Albane 2026-07-07 (« titre Statuts [Nom] ») — statut : **partiel** (fait SELARL, SELAS multi, SCS, SPFPL×2, SAS ; **noms fixes restants** : SELAS uni médecin/dentiste, SCI, SCI IRIS, SCM, micro holding, SASU — registre ligne « Titre Statuts [Nom] » = ❓)
- [x] Signature client à droite (procurations + demandes Ordre) — mise en forme 1.3/1.5 — statut : **fait**
- [x] DNC générée d'office PAR dirigeant, nom du dirigeant dans le fichier — O24-02 — statut : **fait** (tous types)
- [x] « en quatre exemplaires » retiré des courriers/PV où Albane l'a demandé — A26-30/34/51 — statut : **fait** (lots 2026-06-26) ; ⚠️ acte cession parts SCM = « quatre et non trois » (A26-70, sens inverse — par document, pas global)
- [x] Case « même adresse que … » avec report auto (cabinet/cible) — O24-12 + 6.1 — statut : **fait** (cession SELAS + société cible SPFPL)
- [x] « Prénom » usuel dans les docs courants ; « Prénoms complets » réservé aux docs qui l'exigent (DNC) — ticket 2026-07-06 §5 — statut : **fait** (registre ✅ SELARL/SELAS uni/SPFPL/SAS/SASU)
- [x] Date de naissance avec zéro devant (« 01 janvier », pas « 1 janvier ») — A26-17/48/61 — statut : **fait** (lots 2026-06-26, pad jour)
- [x] Sélecteur de date + bouton « Aujourd'hui » sur tous les champs date — RAF-D1/D2 (2026-06-29) — statut : **fait** (helper `date_input_with_today` routé partout ; 5 exceptions sémantiques tracées à valider Rafael)
- [x] Apport de l'associé unique = capital social repris automatiquement (pas de double saisie) — ticket 2026-07-06 §1 — statut : **fait** (registre ligne « Apport associé unique = capital » ✅ sur les uni)

## Ne pas toucher (validés client)

- [x] Autorisation de domiciliation : mise en forme **VALIDÉE** — mise en forme 1.8 + ticket §10 — ne pas modifier
- [x] Demande d'inscription à l'Ordre : mise en forme **VALIDÉE** (« C'est juste parfait ») — A26 §8 + 9.1
- [x] Déclaration de non-condamnation : **VALIDÉE** (« Tout est nickel ») — A26 §9
- [x] Annexe des statuts civils : **VALIDÉE** (« l'annexe c'est top ») — R0702-03
