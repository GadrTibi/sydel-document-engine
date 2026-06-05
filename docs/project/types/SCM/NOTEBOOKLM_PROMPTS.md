# SCM — Prompts NotebookLM (prêts à envoyer) — V1

> **But.** Obtenir d'abord **LA carte officielle « cas → documents » de la SCM** (qui n'existe nulle
> part dans le canon : il est 100 % SELARL), puis confirmer variables, wording, genre/pluriel et les
> points ambigus. **Aucune règle inventée ici.** Les questions sont **copiables telles quelles**.
>
> **Routage (rule 20 — projet avec associé métier Rafael).** Cible :
> **[NotebookLM]** = règle/wording juridique (réponse avec citations) ·
> **[Rafael]** = élément que NotebookLM ne peut pas fournir (modèle manquant, décision métier propre au
> cabinet). **NE JAMAIS poser une question métier à Gad.** Épuiser NotebookLM avant Rafael.
>
> **Méthode.** Envoyer **par blocs**, dans l'ordre : **Bloc 1 d'abord** (sans la carte des cas, le
> reste ne peut pas être bâti). Les réponses alimentent `CARTOGRAPHIE_TENTATIVE.md` puis le journal de
> décisions.
>
> **Acquis (NE PAS reposer) :** la SCM apparaît dans le canon SELARL **uniquement** comme cession de
> parts de SCM vers la SELARL (`PV AGE cession part SCM`, `Courrier SDE`, `Acte de cession des parts
> de la SCM à la SELARL`) — ce bloc-là est déjà cartographié et codé côté SELARL/SELAS.

---

## BLOC 1 — LISTE DES CAS DE LA SCM + carte cas → documents *(PRIORITÉ ABSOLUE)*

**1.1 [Rafael]** — *Question préalable de cadrage (NotebookLM ne l'a probablement pas) :*
> « Pour la SCM (Société Civile de Moyens), existe-t-il un document équivalent à
> "Documents à générer par cas" — c'est-à-dire la liste officielle des CAS de SCM (ex. création,
> cession de parts, modification…) et, pour chaque cas, la liste exacte des documents à produire ?
> Si oui, peux-tu nous le fournir ? Aujourd'hui nous n'avons que les 11 modèles du dossier
> "création scm", sans carte cas → documents. »

**1.2 [NotebookLM]** —
> « D'après les sources, quels sont les différents CAS de dossier possibles pour une Société Civile
> de Moyens (SCM) — par exemple création, entrée/sortie d'associé, cession de parts, transfert de
> siège, dissolution ? Cite chaque cas avec sa source. »

**1.3 [NotebookLM]** —
> « Pour la CRÉATION d'une SCM, quelle est la liste EXACTE et exhaustive des documents à produire, et
> dans quel ordre ? Pour chaque document, indique s'il est systématique ou conditionnel, et à quelle
> condition. Cite les sources. »

**1.4 [NotebookLM]** —
> « Les documents suivants font-ils partie d'un dossier de création de SCM, et à quelle condition :
> statuts, PV de nomination du gérant, pacte d'associés, règlement intérieur, contrat de frais
> communs, liste des dépenses communes, autorisation de domiciliation, déclaration de non-condamnation,
> procuration, fiche de création ? Pour chacun, réponds "systématique", "optionnel (condition : …)" ou
> "ne fait pas partie de la création de SCM". »

**1.5 [NotebookLM]** —
> « Un dossier de création de SCM comporte-t-il une "demande d'inscription à l'ordre" ? (Ce document
> existe pour les SEL ; nous voulons savoir s'il s'applique aussi à la SCM.) Cite la source. »

**1.6 [NotebookLM]** —
> « La SCM nécessite-t-elle des documents liés au régime matrimonial / au conjoint d'un associé
> (lettre de renonciation, avertissement au conjoint en cas d'apport d'un bien commun), comme c'est le
> cas pour une SEL ? Cite la source. »

**1.7 [NotebookLM]** —
> « Combien d'associés une SCM peut-elle compter dans nos dossiers types, et quel est le nombre
> minimum ? Les modèles fournis supposent 2 associés ; certaines variables vont jusqu'à 3 sociétés.
> Quelle est la borne haute à modéliser ? Cite la source. »

---

## BLOC 2 — Confirmer variables / wording PAR MODÈLE

> Les variables réellement présentes dans chaque modèle sont listées dans `INVENTAIRE_MODELES.md`.
> Objectif : confirmer leur signification et détecter les variables manquantes / en trop.

**2.1 [NotebookLM] — Statuts SCM** —
> « Dans les statuts d'une SCM, comment sont rédigés : (a) la comparution des associés, (b) l'article
> Apports, (c) l'article Capital / répartition des parts, lorsqu'un associé est une personne physique
> et l'autre une société (SEL) ? Donne le wording exact et cite la source. »

**2.2 [NotebookLM] — Statuts SCM (apports)** —
> « Dans les statuts SCM fournis, on trouve à la fois des apports d'une personne physique
> (`apport_lettres_personne_2`) et d'une société (`apport_societe_1`, `apport_lettres_societe_1`).
> Confirme le modèle d'apport attendu : qui apporte quoi, en numéraire ou en industrie, et le wording
> exact de chaque ligne d'apport. »

**2.3 [NotebookLM] — PV nomination gérant SCM** —
> « Quel est le wording exact du PV de nomination du gérant d'une SCM (qui nomme, durée du mandat,
> pouvoirs) ? La SCM peut-elle avoir plusieurs gérants ? Cite la source. »

**2.4 [NotebookLM] — Pacte d'associés SCM** —
> « Le pacte d'associés SCM fourni suppose exactement deux associés. Est-ce le standard, et quel est le
> wording des clauses essentielles (sortie, agrément, répartition des charges) ? Cite la source. »

**2.5 [NotebookLM] — Contrat de frais communs + Règlement intérieur + Liste des dépenses communes** —
> « Comment s'articulent le contrat de frais communs, le règlement intérieur de la SCM et la liste des
> dépenses communes ? Sont-ils trois documents distincts ou des annexes l'un de l'autre ? Quelle est la
> clé de répartition des dépenses communes (le seuil `seuil_depense_commune`, l'`annee_reference_charges`) ?
> Cite la source. »

**2.6 [NotebookLM] — Avenant au contrat de bail (SCM)** —
> « Dans quel cas un avenant au contrat de bail est-il produit pour une SCM (la SCM devient locataire à
> la place d'un ancien locataire) ? Est-ce un document de création ou un cas distinct ? Quel est son
> wording exact ? Cite la source. »

**2.7 [NotebookLM] — Autorisation de domiciliation (SCM)** —
> « Pour la SCM, la durée de la domiciliation du siège est-elle "indéterminée" comme pour la SEL, ou
> autre ? (Ne pas confondre avec la durée de la société.) Cite la source. »

---

## BLOC 3 — Genre / pluriel (transverse)

**3.1 [NotebookLM]** —
> « Dans les documents SCM, quelles formulations varient selon le GENRE de l'associé ou du gérant
> (ex. "le gérant" / "la gérante", "associé" / "associée", "le Docteur" / "la Docteure") ? Liste les
> paires de chaînes exactes concernées, avec leur source. »

**3.2 [NotebookLM]** —
> « Dans les documents SCM, quelles formulations doivent passer au PLURIEL quand il y a plusieurs
> associés (comparution, apports, répartition des parts, signatures) ? La gouvernance est-elle déjà
> rédigée au pluriel dans les modèles, ou faut-il pluraliser ? Indique précisément les endroits à
> modifier. »

**3.3 [NotebookLM]** —
> « La préférence "le Docteur" / "la Docteure" est-elle gérée par associé (au cas par cas) ou par une
> règle universelle pour la SCM ? Cite la source. »

---

## BLOC 4 — Points AMBIGUS / pièges à trancher

**4.1 [NotebookLM]** —
> « Le document "Fiche de création de SCM" est-il un livrable destiné au client, ou un formulaire de
> collecte interne (qui ne doit pas être généré comme document final) ? Cite la source. »

**4.2 [Rafael]** —
> « Nous avons deux versions de la "Liste des dépenses communes SCM" : un fichier .doc (Word ancien,
> non exploitable automatiquement) et un .docx déjà présent côté SELARL. Peux-tu confirmer quelle
> version est la référence à utiliser, et nous fournir une version .docx tokenisée si la bonne est le .doc ? »

**4.3 [NotebookLM]** —
> « Le "contrat de frais communs" lie deux SOCIÉTÉS (les SEL des praticiens), pas les personnes
> physiques directement. Confirme : les parties au contrat de frais communs sont-elles bien les SEL, et
> non les associés en nom propre ? Cite la source. »

**4.4 [NotebookLM]** —
> « Existe-t-il une cession de parts de SCM réalisée HORS contexte SELARL/SELAS (par ex. entre deux
> personnes physiques, ou vers une autre structure) ? Si oui, quels documents et quel wording ? (Nous
> avons déjà le cas "cession de parts de SCM vers une SELARL/SELAS".) Cite la source. »

**4.5 [NotebookLM]** —
> « Quelle est la DURÉE statutaire d'une SCM (99 ans, autre) et où est-elle fixée ? Est-elle figée dans
> les statuts ou variable ? Cite la source. »

**4.6 [Rafael]** — *(uniquement si NotebookLM reste muet sur le bloc 1)*
> « Si NotebookLM ne contient pas la carte cas → documents de la SCM, peux-tu nous indiquer, à partir de
> ta pratique, la liste des documents que tu produis systématiquement pour : (1) une création de SCM,
> (2) l'ajout d'un pacte/règlement/contrat de frais communs ? Cela nous évite d'inventer. »
