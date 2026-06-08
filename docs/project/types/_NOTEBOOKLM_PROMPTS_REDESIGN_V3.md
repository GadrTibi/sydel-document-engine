# Prompts NotebookLM — REDESIGN V3 (résiduel réel uniquement)

> **Date :** 2026-06-08 · Remplace les V2 (« c'est dans les docs ») **et** les versions V3 antérieures
> (54 questions, puis 6 prompts) **après croisement avec ce qui est DÉJÀ acquis** dans les synthèses
> `NOTEBOOKLM_ANSWERS.md`. On ne pose **que ce qui manque réellement**.
>
> **Doctrine inchangée** : on ne demande à NotebookLM que le **savoir d'Albane** (usage/montage, règles
> légales-ordinales, logique de décision, conditions des cas) — jamais le wording (modèles), la liste
> des docs (canon), ni une décision de périmètre (toi). « Si ce n'est pas dans les sources, dis-le. »
>
> **4 prompts à coller.** SCM et SCI **retirés** (voir « Déjà acquis » en bas).

---

## SAS (holding SPFPL par actions) — passe jamais faite
```
Pour la CRÉATION d'une SPFPL constituée en SAS (société par actions simplifiée), réponds point par point, uniquement à partir des sources (si un point n'y figure pas, dis-le) :
1) Dans quel cas monte-t-on une holding SPFPL en SAS plutôt qu'une autre forme, et comment s'articule-t-elle avec la/les SEL d'exercice (créée avant, après ou en même temps) ?
2) Cette forme par actions est-elle réservée aux médecins ou ouverte aux autres professions, et quelles sont les règles ordinales de détention du capital et des droits de vote (qui peut être actionnaire, proportions, rôle de l'inscription à l'Ordre) ?
3) La durée de la société et l'absence de rémunération du président jusqu'à la clôture du 1er exercice sont-elles des pratiques constantes ou des choix par dossier ? Comment se décide la durée du mandat du président, et quels points de vigilance ?
4) Crée-t-on plutôt avec un actionnaire unique ou plusieurs ; quand un apport de titres de SEL impose-t-il un commissaire aux apports (qui le désigne) ; et applique-t-on la protection du conjoint (régime communautaire) comme en SELARL ?
5) Comment accorde-t-on le genre (président/présidente, actionnaire, qualité de médecin), et le genre du président et de l'actionnaire peuvent-ils différer dans un même dossier ?
```

## SCS — résiduel multi (prompts 11-13 jamais posés) + usage
```
Pour la CRÉATION d'une SCS (société en commandite simple), réponds point par point, uniquement à partir des sources (si un point n'y figure pas, dis-le) :
1) Au-delà du montage type (commandité = praticien gestionnaire, commanditaire = SPFPL investisseuse, immobilier patrimonial), quelles autres situations conduisent à créer une SCS, et quels pièges éviter ?
2) La répartition des apports et des parts entre commandité et commanditaire suit-elle une règle (plancher, type de parts réservé au commandité) ou est-ce un choix libre ? Et la décorrélation droits de vote / droits financiers est-elle libre ou contrainte (le commandité gestionnaire doit-il garder la majorité des droits de vote) ?
3) En pratique, y a-t-il plusieurs commanditaires (et/ou commandités), avec quelles règles propres ; et quand le commanditaire est une personne morale (SPFPL), cela change-t-il les règles — une personne morale peut-elle aussi être commanditée (le commandité ayant la qualité de commerçant, responsabilité indéfinie et solidaire) ?
```

## SELAS — résiduel (usage / ordre / pièges / genre non trouvé)
```
Pour la CRÉATION d'une SELAS, réponds point par point, uniquement à partir des sources (si un point n'y figure pas, dis-le) :
1) Dans quels cas concrets oriente-t-on un praticien vers une SELAS plutôt qu'une SELARL, et comment s'articule-t-elle en pratique avec une SPFPL, une SCI ou une SCM ?
2) Quelles contraintes l'Ordre fait-il réellement respecter sur la détention du capital d'une SELAS par des personnes ou sociétés non exerçantes (seuils surveillés, refus) ?
3) Quels pièges ou erreurs récurrentes le cabinet signale-t-il à la constitution d'une SELAS ?
4) Comment féminise-t-on le titre « Directeur Général » (Directrice Générale) et le titre « Docteur » au féminin dans les actes, et quelle donnée détermine la variante ?
```

## SPFPL — résiduel (logique d'arbitrage / fiscal / ordinal / pièges)
```
Pour la CRÉATION d'une SPFPL, réponds point par point, uniquement à partir des sources (si un point n'y figure pas, dis-le) :
1) Comment arbitre-t-on en pratique entre CÉDER ses titres de SEL à la holding (numéraire) et les APPORTER (apport en nature) : quels critères de la situation du client, quelles conséquences ?
2) À quelles conditions le report d'imposition de l'article 150-0 B ter s'applique-t-il, et se perd-il, lors d'une création par apport ?
3) Quelles contraintes l'Ordre fait-il respecter sur la détention du capital d'une SPFPL (qui peut être associé non-exerçant, seuils, délais à l'inscription) ?
4) Pour le commissaire aux apports : qui le désigne, et existe-t-il des cas de dispense ?
5) Quels pièges ou erreurs récurrentes Albane signale-t-elle sur la création d'une SPFPL ?
```

---

## RETIRÉ car DÉJÀ ACQUIS (ne pas reposer — c'est dans `NOTEBOOKLM_ANSWERS.md`)
- **SCM (tout le prompt)** : les satellites (pacte, RI, contrat frais communs, liste dépenses) sont
  **déjà répondus = « opérations juridiques DISTINCTES, hors bloc création »** ; l'inscription à l'Ordre
  est **déjà répondue** (« systématique, l'Ordre doit être informé », à confirmer Rafael). Rien de
  nouveau à demander à NotebookLM pour la création SCM.
- **SCI / SCI IRIS (tout le prompt)** : SCI vs IRIS est **déjà clarifié** (IRIS = répartition dérogatoire
  du résultat par groupes de parts numérotés, et non « a une PM associée ») ; PM associée autorisée,
  capital variable = acquis. Le résiduel SCI = **wording d'actes + modèle « Lettre d'option IS »** →
  ça vient des **modèles**, pas de NotebookLM.
- **SPFPL** : commissaire (« obligatoire parcours apport, signé Président »), vocabulaire cession/apport,
  cartographie cession+apport, genre/nombre = **acquis** → retirés ; seul le résiduel ci-dessus reste.
- **SELAS** : personne morale associée (oui ; collecter dénomination + SIREN), DG optionnel, table
  genre/nombre = **acquis** → retirés ; seul le résiduel ci-dessus reste.

## Au retour
Réponses brutes par type/point → je range. Tout « pas dans les sources » → groupé pour **Rafael**.
