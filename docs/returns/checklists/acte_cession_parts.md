# CHECKLIST MAÎTRE — Acte de cession de parts SPFPL (DOC-040)

> Code : `generators/lot_05/acte_cession_parts_spfpl.py` (token-replacement sur `Acte_cession_SPFPL_tiers_part_modele.docx`).
> Cousins à vérifier en propagation : **DOC-029** (acte de cession d'ACTIONS SPFPL, `acte_cession_actions_spfpl.py`)
> et **DOC-033** (acte de cession de parts SCM vers SEL, `acte_cession_parts_scm.py`) — trois générateurs distincts.
> S'ajoute à `_transverse.md`.

## Attentes cumulées (ticket 2026-07-06 §12 + Albane 2026-07-07)

- [x] 12.1 Mise en forme lisible, proche du modèle d'origine (restaurer paragraphes/centrage/gras du modèle) — Albane 2026-07-06 — statut : **fait** (écart mesuré 145 §§ vides + centrage/gras jetés → restauration ; à re-vérifier visuellement par Albane)
- [x] 12.2 Identité de l'acquéreur en forme LÉGALE COMPLÈTE « Société de Participations Financières de Profession Libérale de Chirurgiens-Dentistes par actions simplifiée » (pas « par action simplifié ») — Albane 2026-07-06 — statut : **fait** (`forme_sociale_complete_acquereur`)
- [ ] Identité acquéreur : « **en cours de constitution** » ; **supprimer « sous le numéro en cours »** — **Albane 2026-07-07** — statut : **contradiction résolue → à faire**. Le verbatim 12.2 (07-06) ratifiait « immatriculée au RCS de [ville] sous le numéro en cours » ; le 07-07 revient dessus (plus récent, prime). Aujourd'hui le front pose `numero_rcs="en cours"` (`front_app/spfpl_slice.py:1024`) → l'acte rend « sous le numéro en cours ». À remplacer par la mention « en cours de constitution » sans clause RCS.
- [x] 12.3 « euro(s) » sur la valeur nominale (« X parts de [valeur] euros ») + élision « d'/de » correcte — Albane 2026-07-06 — statut : **fait** (`elision_de(valeur_nominale_display)`)
- [ ] Capital de la SPFPL **et** de la SELARL en « LETTRES (chiffres) euros » avec chiffres groupés par 3 — **Albane 2026-07-07** — statut : **pas fait** (`[capital_social_cessionnaire]` = saisie brute échoée telle quelle, ni lettres ni groupement ; idem capital de la société cible SELARL)
- [x] 12.4 Préposition de/du/des devant le département de l'Ordre (« du Jura ») — Albane 2026-07-06 — statut : **fait**
- [ ] Clause Conseil de l'Ordre : département en NOM + article de/du/de la — **Albane 2026-07-07** — statut : **fait sur DOC-040** (7.4 + 12.4) ; **vérifier la clause exacte visée par le retour 07-07 sur le doc régénéré** (si le retour re-signale, l'occurrence est ailleurs — balayer DOC-029/DOC-033)
- [x] 12.5(a) Ligne de répartition à 0 part supprimée entièrement — Albane 2026-07-06 — statut : **fait** (`_repartition_lines` filtre « détenant 0 parts »)
- [ ] 12.5(b) **UNE SEULE répartition du capital** (pas deux) — **Albane 2026-07-07** — statut : **CONTRADICTION résolue → à faire**. Le tracé du 07-06 (QUESTIONS_RAFAEL « 12.5(b) ») concluait « PAS un bug : 2 recitals juridiques distincts (EXPOSÉ PRÉALABLE vs ORIGINE DE PROPRIÉTÉ) voulus, fidèles au modèle — défaut = les 2 conservés, à confirmer Albane ». **Albane a confirmé le 07-07 : une seule.** Supprimer/fusionner la seconde occurrence (préciser laquelle garder — probable : l'EXPOSÉ PRÉALABLE).
- [x] 12.6 Prix : « un euro » au singulier + ordre LETTRES puis chiffres « un euro (1 €) » — Albane 2026-07-06 — statut : **fait** (accord `euro_word` sur le montant, B1 Akainu)
- [x] 12.7 Paiement : « Le prix est payé au moyen d'un chèque ou virement. » (supprimer « par le moyen ») — Albane 2026-07-06 — statut : **fait**
- [ ] Élision « d'un euro » sur le prix (« le prix d'un euro », jamais « de un euro ») — n3 tracé 2026-07-06 + **07-07 tranche l'élision partout** — statut : **contradiction résolue → à faire** (défaut actuel « de un euro » conservé fidèle-modèle, verrouillé par test — à basculer via `elision_de` + MAJ test)
- [x] Répartition : « Dr » abrégé + civilité civile M./Mme dans la phrase d'identité (jamais « Le Docteur » en civilité) — SP2/SP3 (Albane 2026-06-25, rebuild) — statut : **fait** sur cet acte ; cf. chantier transverse « Docteur » 07-07 pour les résidus ailleurs
- [x] Conjoint/partenaire pacsé repris (« pacsé avec {partenaire} »), pas de mention sans nom — 6.3/7.3 (2026-07-06) — statut : **fait** (branché `mentions_conjoint`/`mentions_partenaire_pacse`, tests dédiés)
- [x] Plage de parts omise si vide (pas de « numérotées de … » incomplet) — Albane 13 (2026-07-06) — statut : **fait** côté PV ; sur l'acte les plages suivent la saisie/dérivation — cf. 07-07 « plage auto-déduite » (transverse, partiel)

## Cousins (propagation)

- [ ] DOC-029 (actions) : re-balayer 12.2/12.3/12.4/12.5/12.6/12.7 + « sous le numéro en cours » + capital lettres groupés — statut : **à vérifier** (générateur distinct ; le pacsé y est vérifié par régénération, test dédié = dette MINEUR tracée)
- [ ] DOC-033 (parts SCM) : prix unitaire ajusté (A26-69), numérotation cohérente (A26-68), « quatre exemplaires » (A26-70), SELAS ≠ SELARL + « président » pas « gérance » (A26-62) — statut : **fait** (lots 2026-06-26) ; **re-balayer la double répartition + groupement milliers** si le 07-07 s'y applique
