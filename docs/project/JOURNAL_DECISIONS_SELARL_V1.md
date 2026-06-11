# Journal de décisions — SELARL (V1, 2026-06-05)

Décisions produit/métier **ratifiées**, à code stable. Source de vérité durable (ne pas enterrer en chat).
Les décisions de **méthode / comportement d'agent** vont au bilan DRH (`method-steward`), pas ici.

| Code | Décision | Source | Statut |
|---|---|---|---|
| **SELARL-SCOPE-1** | La SELARL est **UNIPERSONNELLE**. Multi-associés + associé personne morale **ABANDONNÉS**. | Gad 2026-06-04 | acté |
| **SELARL-D1** | Une personne morale **peut** être associée d'une SELARL (le canon « société associée » est correct légalement, NotebookLM). **Mais hors périmètre V1** (cf. SCOPE-1). | NotebookLM 2026-06-04 | acté → **superseded** par SCOPE-1 pour la V1 |
| **SELARL-DUR-1** | Durée de la **SOCIÉTÉ** (statuts art. 6) = « **99 ans** », **figée en dur** (pas une variable). | retour humain 006 (02/06) | appliqué |
| **SELARL-DUR-2** | **Autorisation de domiciliation** = « pour une **durée indéterminée** ». L'amendement « 99 ans » (03/06) était **ERRONÉ** (contredisait la source humaine primaire du 31/05). | Retours humains 31/05 | appliqué |
| **SELARL-ORIG-1** | **Origine de propriété** (cession) décrit le **VENDEUR** (créé par défaut, ou acheté). Cas complexes → relecture humaine (garde-fou). | NotebookLM 2026-06-05 | appliqué |
| **SELARL-SAL-1** | **Reprise des salariés** (cession) : 0 → « Néant. » ; 1..N → liste nom/prénom/poste. | NotebookLM 2026-06-05 | **superseded** par SELARL-SAL-2 (0 → phrase supprimée) |
| **SELARL-CV-1** | **Crédit-vendeur** : unité = **années**. Taux 5 % conservé tel quel (fixe/variable non tranché). | NotebookLM 2026-06-05 | appliqué (taux = dette mineure) |
| **SELARL-AF-1** | **Appel de fonds** = **COMMUN à toute cession** (médical + dentaire). Le « dentaire-only » était une **dérive du canon**. | canon « Si cession » + NotebookLM (coquilles) | appliqué |
| **SELARL-GENRE-1** | « **Docteur** » invariant (« le Docteur », même au féminin) ; « la Docteure » = préférence par personne, **future**. Couche genre (soussigné/né/associé) appliquée. | Rafael 2026-06-04 | appliqué |
| **SELARL-FID-1** | **Fidélité** : remplissage de template du modèle source tokenisé, jamais de paraphrase/invention ; corrections = lock humain. Cas complexes/« ultra personnalisés » → garde + relecture humaine. | ADR-0004 | en vigueur |

## Lot post-réunion 2026-06-09 (multi-type : SCI / SCI IRIS / SCS / SELAS)
1re validation humaine (Albane + David). Constructible **livré et testé** ; juridique fin = en attente
des cas concrets de Rafael (cf. `_RAFAEL_PACKET_V1.md`, `_REUNION_2026-06-09_ALBANE_DAVID.md`).

| Code | Décision | Source | Statut |
|---|---|---|---|
| **MULTI-N-1** | Les types multi-associés (SCI, SCI IRIS, SCS, SELAS) gèrent **N associés** (bornes nommées : civils 1–2 → 6 ; SELAS 2 → 5) ; statuts / PV / annexes s'adaptent. Prouvé par tests à 3 et 5. | Réunion 2026-06-09 | appliqué (`sprint/engine-completion`) |
| **DIRIGEANT-1** | **Associé ≠ dirigeant** : case « Dirigeant » par associé physique → choix du dirigeant **sélectionnable** parmi les associés : **président** (SELAS) et **gérant** (civils SCI/SCI IRIS/SCS/SCM). Rôle SELAS limité à **« Président »** ; **DG / DG délégué = en attente wording Rafael** (aucun modèle source ne le porte → pas d'invention). | Réunion 2026-06-09 | appliqué (président + gérant) / **open** (DG) |
| **DNC-COND-1** | Les champs **DNC + filiation** ne sont demandés **que pour l'associé coché dirigeant** (saisis sous lui — SELAS **et** civils ; plus de bloc signataire séparé). **Défaut documenté** : « dirigeant coché ». Règle exacte (dirigeant seul vs tout associé) = **en attente Rafael**. | Réunion 2026-06-09 | appliqué (défaut) / **open** (règle) |
| **INJECT-1** | **Variables mal injectées** (retour réunion #7) — corrigées : SPFPL apport, capital dupliqué « [montant] € [montant]euros » → « [montant] euros » ; SAS, « Le Docteur » en dur + civilité déjà incluse → « Le {président} ». Coquilles de **modèles source** (≠ injection) flaguées Rafael : SCM en-tête « [capital]euros » collé, SCS « tous les associé commandités » (verbatim modèle), SELARL acte cession RCS/SIRET juxtaposés. | Audit 2026-06-09 | corrigé (injection) / **open** (coquilles modèles → Rafael) |
| **NO-RETRO-1** | **Pas de mise à jour rétroactive** des dossiers historiques : produire les bons docs **à la création** (aligné V1 = création). | Réunion 2026-06-09 | acté |
| **SCM-SAT-N** | Satellites SCM (pacte DOC-026 + liste dépenses DOC-030) **verrouillés à exactement 2 associés** (modèles bâtis pour 2) ; à N>2 ils disparaissent, le bundle de base reste propre. Généraliser = **FLAG Rafael**. | Rafael 2026-06-08 + plan | acté (verrou testé) |

## Lot retours client 2026-06-11 (Albane — SELARL dentiste unipersonnelle + cession de fonds libéral)
Ticket client complet (35 critères d'acceptation) traité sur `sprint/engine-completion`. Philosophie
ratifiée par le ticket : **seuls les champs réellement indispensables bloquent la génération** ; tout
champ facultatif vide laisse une **zone à compléter à la main** (jamais de phrase incomplète).

| Code | Décision | Source | Statut |
|---|---|---|---|
| **SELARL-SAL-2** | **0 salarié → la phrase relative aux salariés est SUPPRIMÉE de l'acte dentaire** (remplace « Néant », SELARL-SAL-1). UI : case « Aucun salarié » (défaut) + nombre de salariés libre 1..N avec civilité/prénom/nom/poste. Aucun blocage sans salarié. | Ticket client 2.12/3.3 (Albane 2026-06-11) | appliqué |
| **SELARL-MAT-1** | **Régimes matrimoniaux explicites** dans la situation matrimoniale : légal/communauté, séparation de biens, communauté universelle, participation aux acquêts. **Seul le régime légal/communauté** déclenche DOC-005/DOC-006 (case à cocher dédiée supprimée, dérivation automatique). Les autres régimes sont rendus dans les statuts sans document supplémentaire. | Ticket client 1.2 | appliqué |
| **SELARL-CESS-2** | **Cession pilotée par les données réelles du dossier** : vendeur = associé unique (repris auto, modifiable via mode manuel), acquéreur = fiche société (dénomination, siège, RCS, capital, représentant = associé unique gérant(e)). **Plus aucune donnée de fixture de test dans les documents générés.** | Ticket client 2.1/2.2 | appliqué |
| **SELARL-CESS-3** | Cadre **Cabinet réduit** : nature = profession (dérivée), adresse = siège social (préremplie, modifiable), téléphone facultatif ; champ superficie remplacé par le **descriptif libre du local**. | Ticket client 2.3 | appliqué |
| **SELARL-LOC-1** | **Descriptif libre du local** (bail) : rempli → inséré tel quel à la place de la phrase type « Les locaux sont composés… » ; vide → phrase **supprimée** (aucune phrase incomplète, jamais bloquant). | Ticket client 2.5 | appliqué |
| **SELARL-OPT-1** | **Champs facultatifs non bloquants** : adresse banque (statuts médecin → zone vide), loyer/CA/résultat/prêt/dates bail/banque cession/destinataire/montant déblocage vides par défaut → blancs à compléter. Restent bloquants : identité vendeur, prix total (+ lettres), identités des salariés listés. | Ticket client 2.6/2.8/2.11/3.1/3.2 | appliqué |
| **SELARL-UI-1** | Questionnaire : libellé « **Cession de fonds libéral** » ; époux/partenaire à côté de la situation matrimoniale ; Ordre + RPPS sur une ligne ; « Nom et prénom du père » / « Nom de jeune fille et prénom de la mère » ; **Numéro et voie fusionnés** (perso + siège, découpe auto pour les générateurs) ; lieu de signature prérempli = ville du siège ; exercice 1er janv./31 déc. + clôture **31 déc. N+1 dynamique** ; « Autre lieu d'exercice » après l'adresse du siège ; année des exercices en **liste déroulante dynamique** (N..N-10, défaut N-3/N-2/N-1) ; montants formatés « 200 000 » ; **prix en lettres dérivé automatiquement** du montant saisi. | Ticket client 1.1→1.8, 2.7, 2.9, 2.10 | appliqué |
| **SELARL-SCM-2** | Cédant SCM prérempli = associé unique (modifiable) ; le **représentant de la SEL cessionnaire = cédant** (cohérence wording V1). | Ticket client 2.13 | appliqué |
| **SELARL-CV-2** | **Clause crédit-vendeur de l'acte médical figée dans le modèle** (multi-paragraphes sans ancre) : la désactiver = bloqueur explicite au plan (pas de génération trouée). Clause **parts SCM** de l'acte médical : paragraphe unique ancré → **supprimé** quand l'option est décochée. | Contrainte modèle + ticket 3.1 | appliqué / **open** (wording sans CV → Rafael) |
| **SELARL-AVB-1** | **Avenant de bail** : locataire = associé unique (dérivé), bailleur saisi (champs facultatifs, segments omis si vides) ; date d'effet du bail (2.4) alimente début/fin/reconductions (durée 6 ans par défaut conservée). | Ticket client 2.4/2.6 | appliqué |

## Dettes mineures (non bloquantes)
- Champ `CessionValidations.salaries_dentaire_deux_valides` non enforced → à retirer lors d'un nettoyage.
- Appel de fonds : préposition « exploité **au** » + « **Cher Monsieur** » figé — **non sourcés** (NotebookLM/Rafael si on veut peaufiner ; cosmétique).
- `date_entree_jouissance` (dentaire) : commentaire « à confirmer côté métier » préexistant.

## Périmètre livré (réf.)
SELARL **unipersonnelle** : création (statuts médecin/dentiste, PV gérant, autorisation, déclaration, procuration, demande ordre, régime communautaire) + cession (cabinet médical/dentaire acte+compromis, parts SCM, avenant bail, appel de fonds commun). 325 tests verts sur `review/selarl`.
