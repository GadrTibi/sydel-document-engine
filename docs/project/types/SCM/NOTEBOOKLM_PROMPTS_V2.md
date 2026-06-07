# SCM — Prompts NotebookLM DÉFINITIFS (prêts à coller) — V2

> **But.** Obtenir **toute l'information métier** nécessaire pour bâtir le type **SCM** (Société Civile
> de Moyens) — moteur **et** UI — selon la recette `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`.
> La priorité absolue est **la carte officielle « cas → documents »** de la SCM, qui n'existe nulle
> part dans le canon (il est 100 % SELARL). Aucune règle inventée : NotebookLM répond **avec citations**.
>
> **Comment s'en servir.** Chaque prompt est **autonome** (contexte suffisant pour NotebookLM seul) et
> contient **une seule question**. Copier les blocs **un par un**. **Envoyer le groupe « Cas → documents »
> EN PREMIER** : sans la carte des cas, ni le moteur ni l'UI ne peuvent être bâtis. Les réponses
> alimentent `CARTOGRAPHIE_TENTATIVE.md` puis le journal de décisions.
>
> **Routage (rule 20 — projet avec associé métier Rafael).** Cible : **[NotebookLM]** = règle/wording
> juridique sourçable · **[Rafael]** = ce que NotebookLM ne peut pas fournir (modèle manquant, décision
> propre au cabinet). **Épuiser NotebookLM avant Rafael. Ne JAMAIS poser une question métier à Gad.**

---

## DÉJÀ CONNU / ACQUIS — NE PAS REDEMANDER

Ces points sont **vérifiés dans les sources / le code** et n'ont **pas** à être posés à NotebookLM :

1. **Cession de parts de SCM → SELARL/SELAS** : cas **déjà cartographié au canon** et **codé** (`PV AGE
   cession part SCM`, `Courrier SDE`, `Acte de cession des parts de la SCM à la SELARL`, lots SELARL).
   Ne PAS le re-cartographier sous le type SCM. *(La seule zone d'ombre — cession SCM **hors** contexte
   SEL — est traitée en prompt 5, pas ici.)*
2. **Identité des 11 modèles SCM** : recensée dans `INVENTAIRE_MODELES.md` (statuts, PV gérant, pacte,
   règlement intérieur, contrat frais communs, liste dépenses communes, autorisation domiciliation,
   déclaration non-condamnation, procuration, fiche de création, avenant bail). On sait **ce que chaque
   fichier EST** ; on cherche **dans quels cas il s'assemble** et **son wording exact**.
3. **Trames « communes »** (autorisation domiciliation, déclaration non-condamnation, procuration) :
   identiques à la couche partagée SEL — à **réutiliser**, pas à re-spécifier. Ne pas en demander le wording.
4. **Dictionnaire de variables** `variables_source_scm.csv` (~165 variables, jusqu'à `_societe_3`) =
   référence transverse, **pas** le contrat de variables d'un cas. Sert d'indice pour le multi, rien de plus.

---

## Cas → documents *(PRIORITÉ ABSOLUE — envoyer ce groupe en premier)*

### 1 — [Rafael] Carte officielle des cas (préalable, NotebookLM ne l'a probablement pas)

```
Pour la SCM (Société Civile de Moyens), existe-t-il un document officiel "Documents à générer par cas"
— la liste des CAS de SCM (création, entrée/sortie d'associé, cession de parts, transfert de siège,
dissolution…) et, pour chaque cas, la liste exacte des documents à produire ? Si oui, peux-tu nous le
fournir ? Aujourd'hui nous n'avons que 11 modèles du dossier "création SCM", sans carte cas → documents,
et le canon "Documents à générer par cas" est entièrement SELARL.
```

### 2 — [NotebookLM] Liste des cas de SCM

```
D'après les sources, quels sont les différents CAS de dossier possibles pour une Société Civile de
Moyens (SCM) — par exemple création, entrée ou sortie d'associé, cession de parts, transfert de siège,
dissolution ? Cite chaque cas avec sa source.
```

### 3 — [NotebookLM] Création d'une SCM : documents exacts, ordre, et caractère systématique/optionnel

```
Pour la CRÉATION d'une SCM (Société Civile de Moyens), donne la liste EXACTE et exhaustive des documents
à produire, dans l'ordre. Pour CHAQUE document de cette liste — statuts, PV de nomination du gérant,
pacte d'associés, règlement intérieur, contrat de frais communs, liste des dépenses communes,
autorisation de domiciliation, déclaration de non-condamnation, procuration, fiche de création —
indique précisément : "systématique", "optionnel (condition : …)", ou "ne fait PAS partie de la
création d'une SCM". Cite les sources.
```

### 4 — [NotebookLM] Ce qui N'EST PAS dans un dossier de création de SCM (à exclure)

```
Pour la CRÉATION d'une SCM, ces éléments — propres aux SEL — s'appliquent-ils aussi ? (a) une "demande
d'inscription à l'Ordre" ; (b) des documents liés au régime matrimonial ou au conjoint d'un associé
(lettre de renonciation à la qualité d'associé, avertissement au conjoint en cas d'apport d'un bien
commun). Pour chacun, réponds "fait partie de la création de SCM (condition : …)" ou "ne s'applique pas
à la SCM". Cite la source.
```

### 5 — [NotebookLM] Cession de parts de SCM HORS contexte SEL

```
Existe-t-il une cession de parts de SCM réalisée HORS contexte SELARL/SELAS — par exemple entre deux
personnes physiques, ou vers une autre structure ? Si oui, quels documents produit-on et selon quel
wording ? (Le cas "cession de parts de SCM vers une SELARL/SELAS" est déjà traité ; je cherche
uniquement les autres cas de cession.) Cite la source.
```

### 6 — [NotebookLM] Cas du bail (avenant) : cas autonome ou rattaché à la création ?

```
Pour une SCM, l'"avenant au contrat de bail" (la SCM devient locataire à la place d'un ancien locataire)
est-il un document RATTACHÉ à la création de la SCM, ou un CAS distinct déclenché par sa propre condition
(ex. "si la SCM reprend un bail existant") ? Précise la condition d'émission. Cite la source.
```

### 7 — [Rafael] Filet de secours si NotebookLM reste muet sur les cas *(à n'envoyer que dans ce cas)*

```
Si NotebookLM ne contient pas la carte cas → documents de la SCM : à partir de ta pratique, peux-tu
nous indiquer la liste des documents que tu produis systématiquement pour (1) une création de SCM et
(2) l'ajout des conventions entre associés (pacte / règlement intérieur / contrat de frais communs) ?
Cela nous évite d'inventer la carte.
```

---

## Wording *(par document — confirmer le texte exact et lever les ambiguïtés)*

### 8 — [NotebookLM] Statuts SCM : comparution, apports, capital (PP + société)

```
Dans les statuts d'une SCM dont un associé est une personne physique et l'autre une société (SEL),
quel est le wording EXACT de : (a) la comparution des associés, (b) l'article Apports (qui apporte quoi,
en numéraire ou en industrie, ligne par ligne), (c) l'article Capital et répartition des parts ? Donne
le texte exact et cite la source.
```

### 9 — [NotebookLM] PV de nomination du gérant SCM (un ou plusieurs gérants)

```
Quel est le wording exact du PV de nomination du gérant d'une SCM : qui le nomme, durée du mandat,
étendue des pouvoirs ? Une SCM peut-elle avoir plusieurs gérants, et si oui comment le texte s'y
adapte-t-il ? Cite la source.
```

### 10 — [NotebookLM] Articulation pacte / règlement intérieur / contrat frais communs / liste des dépenses

```
Comment s'articulent, dans une SCM, le pacte d'associés, le règlement intérieur, le contrat de frais
communs et la liste des dépenses communes : sont-ce des documents distincts ou des annexes les uns des
autres ? Quelle est la clé de répartition des dépenses communes (rôle du seuil de dépense commune et de
l'année de référence des charges) ? Et les PARTIES au contrat de frais communs sont-elles les SEL des
praticiens ou les personnes physiques directement ? Donne le wording des clauses essentielles et cite la source.
```

### 11 — [NotebookLM] Durée de la SCM et durée de la domiciliation (ne pas confondre)

```
Pour une SCM, deux durées distinctes : (a) la DURÉE de la société dans les statuts (99 ans ? autre ? est-elle
figée ou variable ?) et (b) la DURÉE de la domiciliation du siège (est-elle "indéterminée" comme pour la
SEL ?). Donne les deux et précise où chacune est fixée. Cite la source.
```

### 12 — [NotebookLM] Avenant au contrat de bail SCM : wording

```
Quel est le wording exact de l'avenant au contrat de bail d'une SCM lorsqu'elle devient locataire à la
place d'un ancien locataire (parties, objet de l'avenant, date d'effet) ? Cite la source.
```

### 13 — [NotebookLM] Fiche de création SCM : livrable client ou outil interne ?

```
Le document "Fiche de création de SCM" est-il un livrable destiné au client, ou un formulaire de
collecte interne au cabinet qui ne doit pas être généré comme document final ? Cite la source.
```

### 14 — [Rafael] Référence "Liste des dépenses communes SCM" (.doc vs .docx)

```
Nous avons deux versions de la "Liste des dépenses communes SCM" : un fichier .doc (Word ancien, non
exploitable automatiquement) et un .docx déjà présent côté SELARL. Peux-tu confirmer laquelle est la
référence à utiliser, et nous fournir une version .docx tokenisée si la bonne est le .doc ?
```

---

## Genre / pluriel *(transverse — appliquer après confirmation Albane pour le pluriel)*

### 15 — [NotebookLM] Variations de GENRE dans les documents SCM

```
Dans les documents d'une SCM (statuts, PV de nomination du gérant, pacte, règlement intérieur), quelles
formulations varient selon le GENRE de l'associé ou du gérant (par ex. "le gérant"/"la gérante",
"associé"/"associée", "le Docteur"/"la Docteure") ? Liste les paires de chaînes EXACTES concernées,
avec leur source.
```

### 16 — [NotebookLM] Passages à mettre au PLURIEL selon le nombre d'associés

```
Dans les documents d'une SCM, quelles formulations doivent passer au PLURIEL quand il y a plusieurs
associés (comparution, apports, répartition des parts, gouvernance, signatures) ? Précise les endroits
exacts à pluraliser, et indique si la gouvernance est déjà rédigée au pluriel dans les modèles ou s'il
faut la pluraliser. Cite la source.
```

### 17 — [NotebookLM] "le Docteur"/"la Docteure" : règle universelle ou choix par personne ?

```
Pour la SCM, la formulation "le Docteur"/"la Docteure" se gère-t-elle PAR ASSOCIÉ (au cas par cas selon
la préférence de chaque personne) ou par une règle universelle valant pour tout le document ? Cite la source.
```

---

## Multi *(nombre d'associés / de sociétés à modéliser)*

### 18 — [NotebookLM] Nombre d'associés d'une SCM : minimum et borne haute à modéliser

```
Combien d'associés une SCM peut-elle compter dans des dossiers types, et quel est le nombre minimum ?
Les modèles fournis supposent 2 associés (et certaines variables vont jusqu'à 3 sociétés). Quelle est la
borne haute réaliste à modéliser pour la création d'une SCM et son contrat de frais communs ? Cite la source.
```
