# CHECKLIST MAÎTRE — Attestation sur le capital / liste des souscripteurs

> ⚠️ FAMILLE ÉCLATÉE : **6 générateurs cousins SANS socle commun** — tout retour « attestation »
> se propage À LA MAIN sur chacun (règle 68 Q4) :
> DOC-042 SPFPL apport (`lot_05/attestation_capital_liste_souscripteurs.py`) ·
> DOC-051 SPFPL cession (`…_cession.py`) · DOC-045 SELAS (`attestation_capital_souscripteurs_selas.py`) ·
> DOC-024 SAS (`…_sas.py`) · DOC-050 SASU (`liste_souscripteurs_sasu_holding.py`) ·
> DOC-LSS-SCS SCS (`liste_souscripteurs_scs.py`, appel direct front).
> S'ajoute à `_transverse.md`.

## Attentes cumulées

- [x] Attestation GÉNÉRÉE dans le parcours SPFPL cession (critère d'acceptation Albane n°14, 2026-07-06) — statut : **fait** (DOC-051 bâti sur le modèle cession, câblé au bundle ; l'inférence « pas d'attestation en cession » du tracé 4.8 est CLÔTURÉE fausse 2026-07-06)
- [ ] Attestation présente dans **TOUTES** les créations de société — mise en forme §4 / critère 11 (2026-07-03) — statut : **partiel**. Présente : SELAS uni (méd/dent), SELAS multi (conditionnelle ANO-045), SAS, SASU, SPFPL apport, SPFPL cession, SCS. **MANQUANTE : SELARL, SCI, SCM, SCI IRIS, micro holding** — flag Albane tracé 4.1/4.9 (quel modèle pour les civils — apports en nature ? ne pas inventer) ; registre ligne « Attestation capital présente » = ⬜ sur ces 5 types
- [ ] « **60 000 €** » : chiffres groupés par 3 PARTOUT dans l'attestation — **Albane 2026-07-07** — statut : **pas fait** (`_format_amount` rend « 60000 » sans séparateur, `attestation_capital_souscripteurs_selas.py:279` ; vérifier les 6 cousins)
- [ ] « d'un montant de **100 euros** chacune » — jamais « 100 d'euro » / composition fautive — **Albane 2026-07-07** — statut : **pas fait** (retour 07-07 signale le défaut sur le doc généré ; corriger la composition unité + élision « d'un » via `montant_lettres_avec_unite`/`elision_de`, balayer les 6 cousins)
- [ ] « Le Docteur [Nom] a fait un apport de … » — le titre « Docteur » dans le corps — mise en forme 1.6 (verbatim modèle) ⟂ **Albane 2026-07-07 « Docteur n'est pas une civilité, retirer partout »** — statut : **contradiction** (le modèle validé porte « Le Docteur » ; le 07-07 prime a priori → confirmer avec Albane si le TITRE du corps tombe aussi, puis propager aux 6 cousins)
- [x] Espaces après la phrase « … a fait un apport de [montant] euros en numéraire » + espaces entre titre / désignation société / corps — mise en forme 1.6 (2026-07-03) — statut : **fait** (groupe C tronc du lot mise en forme ; re-vérification visuelle Albane attendue)
- [x] Montant de l'apport = apport RÉEL de l'associé, pas le capital total — A26-35/A26-40 (2026-06-26) — statut : **fait** (lot 1, gate Akainu — repli-capital corrigé)
- [x] DOC-045 SELAS : une ligne de répartition + une ligne d'apport PAR souscripteur, wording verbatim modèle Albane 2026-06-17 — statut : **fait** (câblée conditionnelle au bundle SELAS, résolution ANO-045 « le canon fait foi », Rafael 2026-07-01 ; cas souscripteur PERSONNE MORALE non émis — aucun modèle Albane, flaggé)
- [x] DOC-051 : montant = capital de la holding souscrit en NUMÉRAIRE (« en numéraire, entièrement libéré et déposé ») — sources 2026-07-06 — statut : **fait**
- [x] Civilité civile M./Mme dans DOC-051 (convention SP2) — statut : **fait**
- [x] DOC-LSS-SCS : vocabulaire adapté parts/Président (arbitrage Rafael SCS5) — statut : **fait** (Akainu RIEN À REDIRE)
- [ ] Aération satellites SASU (paragraphes vides intercalaires des modèles Albane) — Akainu m2/n1 2026-06-29 — statut : **pas fait** (cadrage visuel non reproduit, à confirmer Albane — même question que N6 pt2)

## Rappels

- Un fix de composition monétaire (« lettres (chiffres) euros », groupement, élision) doit être **régénéré et diffé sur les 6 cousins** — c'est la famille la plus siloée du moteur.
- DOC-024 (SAS) exige apports en NATURE structurés ; DOC-042/051 = numéraire — ne pas uniformiser les wordings d'apport entre cousins sans modèle.
