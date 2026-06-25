# Pack Albane — décisions métier (divergences spec ≠ modèle) · Bilan de Santé 2026-06-26

> Ces points appartiennent au **sachant juridique (Albane)** : ce sont des choix de wording / fidélité
> où la **spec ratifiée** et le **modèle source** divergent, ou des fautes/tournures du modèle préservées
> volontairement. **Aucun n'est inventé ni tranché par l'équipe** (règles 20/50). Le générateur suit
> aujourd'hui l'autorité indiquée (« défaut appliqué ») ; Albane confirme ou corrige.
>
> Détail technique complet : `docs/review/FIDELITE_LOT03_05_REGISTRE.md` §🟠. Ce pack en est la
> **vue décision** (1 ligne par point). Format : **défaut appliqué** → *question à Albane*.

## SPFPL — actes de cession / apport

| # | Document | Défaut appliqué (réversible) | Question Albane |
|---|----------|------------------------------|-----------------|
| A1 | acte_cession_actions | guillemets **droits** ASCII (la spec a remplacé les chevrons « » du modèle) | garder droits, ou rétablir « » du modèle ? |
| A2 | acte_cession_actions | symbole **€** (fidèle au modèle ; la spec écrivait « EUR ») | € (modèle) ou « EUR » (spec) ? |
| A3 | acte_cession_actions | faute source **« d'cent euros »** préservée (modèle + spec) | corriger en « de cent euros » à la source, ou garder la faute ? |
| A4 | acte_cession_actions | **« du Paris »** quand le département saisi est un nom de ville | convention de saisie (n° dépt) ou wording à adapter ? |
| A5 | acte_cession_actions | représentant cessionnaire : rôle dédié + drapeau bloquant (spec a tranché un point qu'elle marque OUVERT) | confirmer le traitement du représentant ? |
| A6 | acte_cession_parts_spfpl | **« Dr »** abrégé en répartition (le modèle abrège ; ailleurs « Docteur ») | « Dr » ou « Docteur » dans la liste de répartition ? |
| A7 | acte_cession_parts_spfpl | wording « par » ajouté + « € »→« euros » (spec corrige le modèle) | modèle verbatim (fautif) ou spec corrigée ? |
| A8 | acte_cession_parts_spfpl | **« cession d'action »** conservé dans un acte de cession de **parts** (point ouvert 5) | garder « action » ou corriger en « parts » ? |
| A9 | acte_cession_parts_spfpl | exposé de la société cible plus pauvre que le modèle | niveau de détail attendu de l'exposé ? |
| A10 | contrat_apport_spfpl | clause **« à titre pur et simple »** (qualification de l'apport) retirée par la spec | rétablir ? portée juridique sur la nature de l'apport |
| A11 | contrat_apport_spfpl | **report d'imposition art. 150-0 B ter CGI** absent du rendu | bloc à intégrer ? (enjeu fiscal) |
| A12 | contrat_apport_spfpl | clause de **sincérité art. 1837 CGI** absente | à intégrer ? |
| A13 | contrat_apport_spfpl | mention d'**annexion du rapport de valorisation** retirée | à rétablir ? (preuve / pièce) |
| A14 | contrat_apport_spfpl | **« n »** au lieu de **« n° »** (RCS) | « n° » voulu ? |
| A15 | pv_agrement (×2) | wording **« cession »** substitué à **« apport »** (ARBITRAGE-SPFPL-001) | confirmer que « cession » est bien le wording retenu ? |
| A16 | pv_agrement_plusieurs | mention **« adoptée à l'unanimité »** retirée du PV | doit-elle figurer (valeur probatoire du vote en AGE) ? |
| A17 | pv_agrement | ligne **« Dès lors, il est décidé de ce qui suit »** ajoutée (absente du squelette spec) | garder ? |

## Attestations capital / liste souscripteurs

| # | Document | Défaut appliqué | Question Albane |
|---|----------|-----------------|-----------------|
| A18 | attestation_capital (+_sas) | symbole **€** (fidèle modèle ; spec = « euros ») | € ou « euros » ? |
| A19 | attestation_sas | élision **« montant d'[valeur] »** (modèle ; spec = « de ») | « d' » (modèle) ou « de » (spec) ? |
| A20 | attestation_sas | pas de **point final** au paragraphe « Apports en nature » (fidèle modèle) | ponctuation voulue ? |
| A21 | attestation_capital | clause de certification **raccourcie** par la spec (constat souscription/apport) | rétablir le constat complet ? |

## SELARL / SCM / divers (lot_03 / lot_05)

| # | Document | Défaut appliqué | Question Albane |
|---|----------|-----------------|-----------------|
| A22 | avenant_contrat_bail | **virgule ajoutée** après « à Lyon » / « au RCS **de** {ville} » (retour ratifié §10.1/10.3, spec §6 périmée) | confirmer + mettre la spec §6 à jour ? |
| A23 | acte_cession_parts_scm | **siège de la SCM cédée = siège de la SEL acquéreuse** (erreur probable du modèle, préservée) | confirmer l'erreur, ou corriger ? |
| A24 | acte_cession_parts_scm | liaison **« et »** du modèle (X, Y et Z) perdue → virgule simple | rétablir « et » ? |
| A25 | demande_derogation_cumul | **encart de principe paraphrasé** (2 phrases) + cadre PIÈCES réduit (vs 5 lignes source, mention OBLIGATOIRE) | reproduire l'encart/pièces à l'identique, ou la curation est-elle voulue ? |
| A26 | formulaire_derogation_sites | détail métier ordinal (DESC groupe 1, VAE, capacités) + consignes impératives du modèle **supprimés** | curation voulue, ou à restaurer verbatim ? |

> **Note** : tous les défauts d'**ACCENTS** et les 2 bugs visibles (« Le Docteur Docteur », « Martincertifie »)
> ont été **corrigés** cette nuit (ce ne sont PAS des décisions métier). Ce pack ne contient QUE les
> arbitrages de wording/fidélité qui appartiennent à Albane.
