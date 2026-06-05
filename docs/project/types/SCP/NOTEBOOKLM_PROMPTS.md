# SCP — Prompts NotebookLM (prêts à envoyer) — V1

> **But.** Obtenir d'abord **ce qu'EST réellement le type « SCP »**, puis **LA carte officielle « cas →
> documents »** (qui n'existe nulle part : le canon est 100 % SELARL), puis confirmer variables, wording,
> genre/pluriel et les points ambigus. **Aucune règle inventée ici.** Les questions sont **copiables
> telles quelles**.
>
> **Routage (rule 20 — projet avec associé métier Rafael).** Cible :
> **[NotebookLM]** = règle/wording juridique (réponse avec citations) ·
> **[Rafael]** = élément que NotebookLM ne peut pas fournir (modèle manquant, décision métier propre au
> cabinet). **NE JAMAIS poser une question métier à Gad.** Épuiser NotebookLM avant Rafael.
>
> **Méthode.** Envoyer **par blocs, dans l'ordre**. **Bloc 1 d'abord, et 1.0 en tout premier** : tant
> qu'on ne sait pas ce qu'EST ce « SCP » ni la liste des cas, le reste ne peut pas être bâti. Les réponses
> alimentent `CARTOGRAPHIE_TENTATIVE.md` puis le journal de décisions (codes `SCP-...`).
>
> **Acquis (NE PAS reposer) :** le canon `Documents_a_generer_par_cas` (V1/V2/V3) **ne mentionne jamais
> la SCP** ; on ne dispose que des modèles du dossier Drive « Création SCP » (5 `.docx` + 1 `.doc` legacy
> + 1 PDF), tous de **constitution**.

---

## BLOC 1 — NATURE DU TYPE + LISTE DES CAS + carte cas → documents *(PRIORITÉ ABSOLUE)*

**1.0 [NotebookLM] — Qu'est-ce que « SCP » dans nos dossiers ? *(question décisive)*** —
> « Dans nos sources, que désigne exactement le sigle "SCP" : une **Société Civile Professionnelle**
> (exercice en commun d'une profession réglementée), une **société civile de détention de participations
> / de portefeuille de titres**, ou une autre forme de société civile ? Le modèle de statuts dont nous
> disposons a pour objet "la prise de participation et la gestion d'un portefeuille de titres, à
> l'exclusion de toute opération commerciale", ce qui ressemble à une société civile patrimoniale plus
> qu'à une société d'exercice professionnel. Précise la forme réelle et cite la source. »

**1.1 [Rafael]** — *Question préalable de cadrage (NotebookLM ne l'a probablement pas) :*
> « Pour le type que nous appelons "SCP" (dossier "Création SCP"), existe-t-il un document équivalent à
> "Documents à générer par cas" — c'est-à-dire la liste officielle des CAS (ex. création, entrée/sortie
> d'associé, cession de parts, modification…) et, pour chaque cas, la liste exacte des documents à
> produire ? Si oui, peux-tu nous le fournir ? Aujourd'hui nous n'avons que les modèles du dossier
> "Création SCP", sans carte cas → documents. Et peux-tu confirmer si "SCP" désigne ici une société
> civile professionnelle d'exercice ou une société civile de portefeuille ? »

**1.2 [NotebookLM]** —
> « D'après les sources, quels sont les différents CAS de dossier possibles pour ce type "SCP" — par
> exemple création, entrée d'un nouvel associé, retrait/cession de parts, transfert de siège,
> modification statutaire, dissolution ? Cite chaque cas avec sa source. »

**1.3 [NotebookLM]** —
> « Pour la CRÉATION d'une SCP, quelle est la liste EXACTE et exhaustive des documents à produire, et dans
> quel ordre ? Pour chaque document, indique s'il est systématique ou conditionnel, et à quelle condition.
> Cite les sources. »

**1.4 [NotebookLM]** —
> « Les documents suivants font-ils partie d'un dossier de création de SCP, et à quelle condition :
> statuts, fiche de création, PV de nomination du gérant, autorisation de domiciliation, déclaration de
> non-condamnation, procuration ? Pour chacun, réponds "systématique", "optionnel (condition : …)" ou "ne
> fait pas partie de la création de SCP". Cite la source. »

**1.5 [NotebookLM]** —
> « Un dossier de création de SCP comporte-t-il une "demande d'inscription à l'ordre" ? (Ce document
> existe pour les SEL ; il est ABSENT de notre dossier "Création SCP" — nous voulons savoir s'il
> s'applique aussi à ce type.) Cite la source. »

**1.6 [NotebookLM]** —
> « La SCP nécessite-t-elle des documents liés au régime matrimonial / au conjoint d'un associé (lettre de
> renonciation, avertissement au conjoint en cas d'apport d'un bien commun), comme pour une SEL ? (Ces
> documents sont ABSENTS de notre dossier "Création SCP".) Cite la source. »

**1.7 [NotebookLM]** —
> « Combien d'associés une SCP peut-elle compter dans nos dossiers types, et quel est le nombre minimum ?
> Notre fiche de création prévoit jusqu'à 5 associés et 2 gérants, mais le modèle de statuts n'en détaille
> que 2. Quelle est la borne haute à modéliser, et combien de gérants au maximum ? Cite la source. »

**1.8 [NotebookLM]** —
> « Existe-t-il pour la SCP un pacte d'associés et/ou un règlement intérieur, comme pour la SCM ? (Ces
> documents sont ABSENTS de notre dossier "Création SCP".) Si oui, font-ils partie de la création ou d'un
> cas distinct ? Cite la source. »

---

## BLOC 2 — Confirmer variables / wording PAR MODÈLE

> Les variables réellement présentes dans chaque modèle sont listées dans `INVENTAIRE_MODELES.md`.
> Objectif : confirmer leur signification et détecter les variables manquantes / en trop.

**2.1 [NotebookLM] — Statuts SCP (objet social)** —
> « Quel doit être l'OBJET SOCIAL des statuts de notre SCP ? Le modèle actuel décrit une société de
> participations / portefeuille de titres ("prise de participation, détention et gestion d'un portefeuille
> de titres, à l'exclusion de toute opération commerciale"). Est-ce le bon objet, ou faut-il un objet
> d'exercice professionnel ? Donne le wording exact attendu et cite la source. »

**2.2 [NotebookLM] — Statuts SCP (comparution / apports / capital)** —
> « Dans les statuts de notre SCP, comment sont rédigés : (a) la comparution des associés, (b) l'article
> Apports (`apport_personne_1`, `apport_lettres_personne_1`…), (c) l'article Capital / répartition des
> parts et leur numérotation (`numero_part_debut/fin_personne_1`, `nb_parts_total`) ? Donne le wording
> exact et cite la source. »

**2.3 [NotebookLM] — Statuts SCP (durée et exercice social)** —
> « Quelle est la DURÉE statutaire de la SCP (`duree_societe` est une variable dans notre modèle, pas une
> valeur figée) : faut-il la figer (ex. 99 ans) ou la laisser variable ? Et l'exercice social
> (`debut_exercice` / `fin_exercice`) est-il libre ou normé ? Cite la source. »

**2.4 [Rafael] — PV de nomination du gérant SCP** —
> « Notre modèle "PV nomination gérant" pour la SCP est un fichier .doc ancien (non exploitable
> automatiquement) ; peux-tu nous le fournir en version .docx tokenisée ? Par ailleurs, ce PV contient des
> variables d'emprunt et d'adresse d'un bien (`montant_emprunt`, `voie_bien`, `ville_bien`…) : ce PV
> combine-t-il la nomination du gérant AVEC une autorisation d'emprunt / d'acquisition d'un bien, ou
> faut-il deux documents distincts ? »

**2.5 [NotebookLM] — Fiche de création** —
> « La "Fiche de création de société civile" est-elle un livrable destiné au client, ou un formulaire de
> collecte interne (qui ne doit pas être généré comme document final) ? Cite la source. »

**2.6 [NotebookLM] — Procuration** —
> « Quel est l'objet exact de la procuration produite pour la création d'une SCP (mandat aux formalités
> auprès de qui, pour quels actes), et son wording exact ? Cite la source. »

**2.7 [NotebookLM] — Autorisation de domiciliation** —
> « Pour la SCP, la durée de la domiciliation du siège est-elle "indéterminée" comme pour la SEL, ou
> autre ? (Ne pas confondre avec la durée de la société.) Cite la source. »

---

## BLOC 3 — Genre / pluriel (transverse)

**3.1 [NotebookLM]** —
> « Dans les documents SCP, quelles formulations varient selon le GENRE de l'associé ou du gérant (ex. "le
> gérant" / "la gérante", "associé" / "associée", "né(e)", "domicilié(e)", "le Docteur" / "la Docteure") ?
> Liste les paires de chaînes exactes concernées, avec leur source. »

**3.2 [NotebookLM]** —
> « Dans les documents SCP, quelles formulations doivent passer au PLURIEL quand il y a plusieurs associés
> (comparution, apports, répartition des parts, signatures) ? La gouvernance est-elle déjà rédigée au
> pluriel dans les modèles, ou faut-il pluraliser ? Indique précisément les endroits à modifier. »

**3.3 [NotebookLM]** —
> « La préférence "le Docteur" / "la Docteure" (et plus largement le titre du praticien) est-elle gérée
> par associé (au cas par cas) ou par une règle universelle pour la SCP ? Cite la source. »

---

## BLOC 4 — Points AMBIGUS / pièges à trancher

**4.1 [NotebookLM]** —
> « `forme_sociale` est une VARIABLE (non figée) dans nos statuts, notre fiche et notre PV SCP. Cela
> signifie-t-il qu'une même trame couvre plusieurs formes de société civile (SCP, SC patrimoniale, SCM…),
> ou la forme doit-elle être figée à "Société Civile Professionnelle" ? Cite la source. »

**4.2 [NotebookLM]** —
> « Le PDF "SCP IR Note assistance à la déclaration" : est-ce un livrable à PRODUIRE pour le client (note
> d'assistance à la déclaration d'impôt sur le revenu), ou une simple note d'information interne qui ne
> doit pas être générée comme document du dossier ? Cite la source. »

**4.3 [NotebookLM]** —
> « Le modèle de statuts mentionne "le constat par un médecin d'une incapacité du gérant" : est-ce une
> clause générique de gouvernance (valable quelle que soit la profession), ou un reliquat spécifique à une
> profession à corriger ? Cite la source. »

**4.4 [NotebookLM]** —
> « Y a-t-il une exigence de capital minimum, ou des règles de libération du capital
> (`apport_personne_1`, numéraire vs nature) spécifiques à la SCP ? Cite la source. »

**4.5 [Rafael]** — *(uniquement si NotebookLM reste muet sur le Bloc 1)*
> « Si NotebookLM ne contient pas la carte cas → documents de la SCP, peux-tu nous indiquer, à partir de ta
> pratique : (1) la liste des documents que tu produis systématiquement pour une création de SCP, (2) les
> autres cas que tu traites pour ce type (cession de parts, entrée/sortie d'associé, dissolution…) et les
> documents associés, et (3) confirmer s'il manque des modèles dans le dossier "Création SCP" (ex. pacte
> d'associés, demande d'inscription à l'ordre) ? Cela nous évite d'inventer. »
