# CARNET — Ticket retour « mise en forme 18 » (Albane, 2026-07-03)

> **Source** : Google Doc, onglet `t.wnln7ac933px` — « Retours après tests sur les dossiers SELARL et SCI ».
> **Verbatim exact** : [`_ticket_mise_en_forme_18_verbatim.txt`](_ticket_mise_en_forme_18_verbatim.txt).
> **Objectif client** : « reprendre au plus proche la mise en forme originale des modèles Word » (rendu pro et homogène).
> **Statut** ∈ `a_faire · partiel · fait` (nous) · **Validé** (client) ∈ `⬜ · ✅`. Verbatim = mot exact.
> Triage (règle 68) : cartographie vérifiée (workflow `ticket-mise-en-forme-18-map`, 4 lecteurs, HEAD 46d40fa).

## Synthèse triage (39 points cartographiés — 2026-07-03)

- **Déjà FAIT (15)** : 1.3 (procuration signature droite), 1.5 (demande Ordre signature droite), 1.8 (domiciliation validée, ne pas toucher), 3.1 (en-tête centré+gras), 3.7 (tirets SCI art.2), 3.8 (aligner articles), 3.11 (apports SCI), 4.2-4.7/4.10 (attestation capital PRÉSENTE : SELAS uni médecin/dentiste, SELAS multi, SAS, SASU, SPFPL apport, SCS).
- **BUILDABLE à traiter (~18)** → exécution par groupes (agents) :
  - **A SELAS** : 2.1 doublon « médecin médecin », 2.2 accord genre, 2.3 art.8 « euro », 2.5 tirets, 2.6 gras siège, 2.7 gras président, 2.8 souligner sous-articles, 2.9 art.38 espace *(2.9 + 2.3-médecin faits inline)*, 2.10 saut page annexe.
  - **B SCI** : 3.2 espace cadre, 3.3 espace soussignés, 3.6 art.3 espace, 3.9 art.4 espace.
  - **C tronc** : 1.2 DNC espace parents, 1.4 PV interligne, 1.6 attestation espaces, 1.7 lettre IS gras.
  - **D transverse** : 1.1 interligne 0,5/1 (à cadrer : valeur ; touche tous docs).
- **MÉTIER (7)** → flags Albane (`QUESTIONS_RAFAEL.md`, tracé 2026-07-03) : 2.4 conjoint **pacsé**, 3.4 « Société Civile Immobilière », 3.5 soussignés « ET »/tirets, 4.1/4.9 attestation capital manquante SELARL/SCI/SCM/micro, 4.8 SPFPL cession (pas d'attestation), 4.11 revue globale QA.

## Points (verbatim condensé)

### §1 — Règles générales (tous modèles)
| ID | Verbatim / sens | État | Classif |
|---|---|---|---|
| 1.1 | Police Roboto, taille 10, interligne corps 0,5 ou 1 — sur tous les actes | à mapper | — |
| 1.2 | DNC : espace entre désignation associé/dirigeant et affiliation des parents | à mapper | — |
| 1.3 | Procurations : signature client à droite | à mapper | — |
| 1.4 | PV : interligne 0 (désignation société en-tête + désignation client + chaque décision AG) + espace entre 1re décision et texte suivant | à mapper | — |
| 1.5 | Demande inscription Ordre : signature client à droite | à mapper | — |
| 1.6 | Attestation capital / liste souscripteurs : espaces après « Le Docteur [Nom] a fait un apport de [montant] euros en numéraire » + espace entre titre / désignation société / corps | à mapper | — |
| 1.7 | Lettre option IS : nom société en gras dans la 1re ligne | à mapper | — |
| 1.8 | Autorisation domiciliation : **VALIDÉE, ne pas modifier** | fait (ne pas toucher) | buildable |

### §2 — Statuts SELAS
| ID | Verbatim / sens | État | Classif |
|---|---|---|---|
| 2.1 | Doublon « médecin médecin » dans la désignation de l'associé → supprimer | à mapper | — |
| 2.2 | Accord genre : « qu'il/elle a décidé d'instituer » | à mapper | — |
| 2.3 | Article 8 : ajouter « euro » (« 1000 parts de 1 euro chacune ») ; vérifier tous modèles similaires | à mapper | — |
| 2.4 | Ajouter le nom du conjoint quand l'associé est marié **ou pacsé** | à mapper | — |
| 2.5 | Tirets dans les énumérations (art.1, art.9, + ensemble) | à mapper | — |
| 2.6 | Article 4 : gras sur le lieu du siège social | à mapper | — |
| 2.7 | Article 15 : gras sur la désignation du président nommé | à mapper | — |
| 2.8 | Souligner les sous-articles (15.1, 15.2, …) | à mapper | — |
| 2.9 | Article 38 : supprimer l'espace en trop qui coupe la phrase en deux | à mapper | — |
| 2.10 | Sous la signature client : saut de page avant l'annexe | à mapper | — |

### §3 — Statuts SCI (SELAS = référence correcte)
| ID | Verbatim / sens | État | Classif |
|---|---|---|---|
| 3.1 | Centrer l'en-tête + nom société en gras | à mapper | — |
| 3.2 | Espace avant et après le cadre « Statuts » | à mapper | — |
| 3.3 | Espace entre chaque soussigné au début | à mapper | — |
| 3.4 | En-tête SCI : « Société Civile Immobilière » et non « Société Civile » | à mapper | — |
| 3.5 | Soussignés : supprimer espaces excessifs + « ET » (ou tirets) si plusieurs | à mapper | — |
| 3.6 | Article 3 : espace entre nom société et corps | à mapper | — |
| 3.7 | Article 2 : tirets dans l'énumération (revoir largement, comme SELAS) | à mapper | — |
| 3.8 | Aligner les articles avec le reste du texte | à mapper | — |
| 3.9 | Article 4 : espace entre adresse siège et corps | à mapper | — |
| 3.11 | Article 6 : harmoniser les apports (« Monsieur Jean Durand, la somme de quatre cents euros, ci 400 euros ») ; éviter espaces excessifs ; tirets/puces | à mapper | — |

### §4 — Documents manquants + revue globale
| ID | Verbatim / sens | État | Classif |
|---|---|---|---|
| 4 | Attestation sur le capital présente dans **toutes** les créations de société | à mapper | — |
| 5 | Revue globale mise en forme (police/taille/interlignes/espaces/alignements/cadres/signatures/tirets/sauts de page/cohérence modèles) | QA transverse | — |

## Critères d'acceptation client (12) — voir verbatim §« Critères d'acceptation »

## Notes de contexte (recoupements avec le lot R0702, déjà poussé)
- Roboto 10 : forcé sur les statuts civils par injection ; les from-scratch (SEL/SPFPL/SAS) déjà en 10. → §1.1 potentiellement partiel (tronc commun à vérifier).
- Espacements micro-holding (en-tête↔cadre, après associé, avant art.1) + saut de page annexe faits. → §3.2/3.3 (SCI) et §2.10 (SELAS) à vérifier (peut-être déjà partiels).
- Tirets SELAS (style Word) faits (N6). → §2.5 à vérifier.
