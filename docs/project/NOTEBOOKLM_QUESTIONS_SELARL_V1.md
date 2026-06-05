# Batch de questions NotebookLM — Finir la SELARL (V1, 2026-06-04)

Cartographie exhaustive (canon `Documents_a_generer_par_cas_V3` + modèles sources + escalades du build).
Cible : **[NotebookLM]** = règle/wording juridique (réponse avec citations) · **[Rafael]** = localisation
d'un fichier / donnée projet · **[Gad]** = décision produit à trancher.
**Acquis (NE PAS reposer)** : une personne morale PEUT être associée d'une SELARL ; les champs de saisie
d'une PM associée sont connus (dénomination, forme, capital, RCS, SIREN, nb parts, représentant légal).

> Méthode conseillée : relayer **par vagues de priorité** (P0 d'abord = débloque le multi-associés + le
> genre), pas les 40 d'un coup. Les réponses alimenteront le journal de décisions + le canon.

---

## P0 — Multi-associés PERSONNES PHYSIQUES (cœur SELARL bloquant)

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Q1 à Q6 ne sont plus à poser
> pour la SELARL ; conservées pour mémoire. (La SELAS multi-actionnaire n'est pas concernée par cet abandon.)

1. **[NotebookLM]** Wording exact de la **comparution** des statuts SELARL à **plusieurs associés physiques** (« LES SOUSSIGNÉS … qu'ils ont décidé d'instituer ») + structure de répétition (un bloc identité par associé).
2. **[NotebookLM]** Wording exact de **l'article 7 (Apports)** en multi-associés (une ligne d'apport par associé + « Total des apports en numéraire » ; tableau ?).
3. **[NotebookLM]** Wording exact de **l'article 8 (Capital / répartition)** en multi-associés (« réparties entre les associés comme suit » + tableau ; phrase qui remplace « attribuées en totalité à … associé unique »).
4. **[NotebookLM]** Wording exact du **bloc de signatures** multi-associés (« Lu et approuvé », une signature par associé, ordre, mention manuscrite).
5. **[Gad/NotebookLM]** **Borne réelle du nombre d'associés** (canon « 1 à 6 », inventaire plafonne à 4) — limite haute à modéliser ?
6. **[NotebookLM]** La pluralisation est-elle **dérivable** du modèle singulier, ou existe-t-il un **modèle « SELARL plusieurs associés »** distinct (clauses agrément entre associés, décisions collectives…) ?

## P0 — Genre / accords grammaticaux (transverse)
7. **[NotebookLM]** **Table d'accord de genre** (pilotée par civilité) pour : soussigné(e), né(e) le, associé(e), associé(e) unique, gérant(e), apporteur.
8. **[NotebookLM]** « **Docteur** » au féminin (statuts médecin) : « à la Docteur » / « au Docteur » invariant / « Doctoresse » / reformuler ?
9. **[NotebookLM]** **Article devant la civilité** dans les cessions (« Le [civilité_vendeur] » → « Le Madame… ») : forme correcte (M./Mme sans article, Le/La piloté, suppression) ?
10. **[Gad]** Confirmer qu'on **capture le genre** (ou le dérive de la civilité) pour : associé(s), gérant(s), vendeur, cédant, représentant, conjoint, salarié(s), destinataire.

## P1 — Associé PERSONNE MORALE dans les statuts (wording)

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Q11 à Q17 (associé personne
> morale + gérance plurielle) ne sont plus à poser **pour la SELARL** ; conservées pour mémoire.
> (L'associé personne morale **en SELAS** via micro-holding reste valable et hors de cet abandon.)

11. **[NotebookLM/Albane]** Existe-t-il un **wording de référence** pour une associée PM en comparution (« La société X, [forme], au capital de…, RCS…, représentée par … en sa qualité de … ») ? (NotebookLM = NON TROUVÉ — Albane peut-il fournir, ou personnalisation manuelle ?)
12. **[NotebookLM/Albane]** Si bloc PM généré : wording de sa **ligne de répartition (art.8)** + **signature** (« Pour la société X, [représentant], [fonction] ») ?
13. **[Gad]** À défaut de wording : pour une PM, le moteur **(a)** génère via gabarit interne, **(b)** laisse un emplacement à compléter, ou **(c)** PM hors périmètre des statuts générés ?
> Gabarit existant : SCM, SCS, PV agrément SPFPL présentent déjà une associée PM — voir Q40.

## P1 — Gérance (co-gérance / pluralité)

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle (gérant unique). Q14 à Q17
> (co-gérance / pluralité) ne sont plus à poser pour la SELARL ; conservées pour mémoire.

14. **[NotebookLM]** Wording de **nomination de plusieurs gérants** (statuts art.16 + PV) — « sont nommés gérants … » + bloc par gérant.
15. **[NotebookLM]** **Pouvoirs en co-gérance** (art.17) : « ensemble » ou « séparément » ? formulation + paramétrage.
16. **[NotebookLM]** **Art.18 (Responsabilité) — vérifier l'inversion** : le modèle écrit « deviendrait **UNI**personnelle … solidairement en cas de pluralité de gérants ». Déclencheur correct = « pluripersonnelle » ? Donner l'alinéa correct. *(bug source probable)*
17. **[NotebookLM]** **Bloc de signatures en co-gérance** (« le gérant / les gérants », une signature par gérant) + accord du titre Gérance.

## P1 — Droits de vote vs droits financiers
18. **[Gad]** SELARL : droits de vote **proportionnels aux parts** (rien à générer) ou texte de répartition des voix ? cas voix ≠ parts ?
19. **[Gad]** Actions/parts de **préférence** (SELAS art.10, logique SCS) : intégrer maintenant ou **reporter** à SPFPL/SELAS ?

## P2 — Cession (cabinet + SCM)
20. **[NotebookLM/Gad]** **Crédit-vendeur — unité** : modèles « délai de [durée] **ans** », donnée souvent en **mois**, version modèle = token nu. Unité qui fait foi + portée par token ou wording ?
21. **[NotebookLM]** **Périodicité crédit-vendeur** (échéance mensuelle / intérêt annuel / délai en ans) : périodicité réelle + wording cohérent ?
22. **[NotebookLM]** **Clauses conditionnelles laissées en clair** (« Ajouter en cas de CV : », « Du 01/01/2023 au … » + [exercice_1], « CMS »/« 1000 parts »/« 510 € »/« 3 points » en dur) : wording/token + condition pour chacune.
23. **[NotebookLM]** **Reprise des salariés** (cession) : 0 à N salariés (médical inachevé, dentaire figé à 2) — wording pour 0/1/N + clause si aucun.
24. **[NotebookLM]** **Acte cession parts SCM — tokens de parts** : les 3 associés partagent le même token. Confirmer **un token de parts propre par associé** + structure liste d'origine de propriété N associés. *(bug tokenisation)*
25. **[Gad]** **Auto-cession vs acquéreur tiers** : plusieurs modèles codent le représentant SELARL acquéreur sur les tokens du vendeur. Gérer **uniquement** la cession à sa propre SELARL, ou aussi un **tiers** ?
26. **[NotebookLM]** **Inversions vendeur/acquéreur** (compromis médical) : origine de propriété décrivant l'ACQUÉREUR comme propriétaire ; mentions dentaires dans un compromis médical ; exercice 2 réutilisant CA1/résultat1 ; titre « [date_origine_propriete] PRÉVUE DE RÉALISATION » malformé. *(erreurs copier-coller source)*
27. **[NotebookLM]** **Transfert de propriété (cession médicale)** : « Le transfert de propriété a lieu ______ » — token attendu (date d'entrée en jouissance, comme dentaire) ?
28. **[NotebookLM]** **Avenant au bail — signataires** : bloc « Le nouveau locataire » des deux côtés. Qui signe (bailleur + ancien + nouveau locataire) + libellé exact ?
29. **[NotebookLM]** **Appel de fonds SEL** : « cabinet **dentaire** » figé, « exploité **au** [denomination_societe] », destinataire « Cher Monsieur » figé — wording correct + accord de genre destinataire ?

## P2 — Profession / sélecteur
30. **[Rafael/Gad]** **Mapping profession → fichier** : le canon dit « dentiste → Modèle statuts SELARL **médecins**.docx ». Confirmer : dentiste → statuts chirurgien-dentiste, médecin → statuts médecins.
31. **[Gad]** **Tout variabiliser vs champs manuels** : les infos apparaissant une seule fois (CA, montant prêt) restent-elles **manuelles** ou variabilisées ? lesquelles ?

## P2 — Régime communautaire / conjoint
32. **[NotebookLM/Gad]** **Lettre avertissement conjoint** : limitée à l'apport **numéraire** (1832-2), « trois exemplaires » figé. Gérer l'apport d'un **bien commun non numéraire** ? homogénéiser en [nombre_exemplaires] ?
33. **[NotebookLM]** **Lettre renonciation** : tutoyée, singulier (un apport). Wording si **plusieurs apports** + accord de [qualite_associe] (associé/associée).

## P3 — Documents non tokenisés / hors périmètre
34. **[Gad]** Documents « à la main » / non fournis (avertissement conjoint si non tokenisé, dérogations procuration / multi-sites / SEL-BNC) : **(a)** générés vides, **(b)** PJ statique, **(c)** hors périmètre ?
35. **[Gad]** **« Site distinct » vs « dérogation multi-sites »** : deux cas cumulables ou un seul axe du wizard ?
36. **[NotebookLM]** **Dérogation cumul SELARL-BNC** : motifs selon **uni** vs **pluri**personnel ?
37. **[NotebookLM]** **Formulaire dérogation multi-sites** : « l'associé / des associés » mais champs limités à 1, signature « Monsieur » figée — wording N associés + genre.

## P3 — Modèles sources manquants / mauvais (Rafael)
38. **[Rafael]** **Vrai modèle SELARL du PV de nomination de gérant** : le fichier fourni (`lot_02/PV nomination gérant - transforme.docx`) est un **PV d'AGE de SCI**. Où est le PV gérant **SELARL** ?
39. **[Rafael/Gad]** **Périmètre autres structures** (SELAS, SPFPL, SCS, SCI, SCM, SAS) présentes en V1 mais retirées en V2/V3 : **backlog** ou **abandonné** ? `docs/docssource_truth` encore source, ou seul V3 (SELARL) fait foi ?
40. **[Rafael]** Les **gabarits PM** (comparution/répartition/signature) des modèles **SCM/SCS/PV agrément SPFPL** sont-ils réutilisables comme référence pour le bloc PM des statuts SELARL (Q11-13), et sont-ils validés/à jour ?

---

## Synthèse des arbitrages [Gad] (à trancher en bloc)
Q5 borne associés · Q10 capture du genre · Q13 stratégie bloc PM · Q18-19 droits de vote/préférence · Q25 auto-cession vs tiers · Q30-31 mapping profession + variabiliser/manuel · Q32 bien commun non numéraire · Q34-35 documents non tokenisés + axe site/dérogation · Q39 périmètre autres structures.

## Fichiers de référence (lecture seule)
- Canon courant : `project/source_truth/Documents_a_generer_par_cas_V3.docx`
- Modèles statuts : `lot_04/Modèle statuts SELARL médecins.docx`, `lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- Gabarits PM de référence : `lot_04/Statuts SCM.docx`, `lot_04/Statuts_SCS_modele.docx`, `lot_05/PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx`
- Mauvais modèle à remplacer : `lot_02/PV nomination gérant - transforme.docx` (PV de SCI, pas SELARL)
