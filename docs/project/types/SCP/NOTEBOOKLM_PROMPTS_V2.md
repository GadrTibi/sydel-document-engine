# SCP — Prompts NotebookLM DÉFINITIFS (prêts à coller) — V2

> **But.** Obtenir **toute l'information métier** nécessaire pour bâtir le type **SCP** — moteur **et**
> UI — selon la recette `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. Deux priorités enchaînées :
> (0) **trancher ce qu'EST réellement le « SCP »** de nos dossiers (le piège n°1), puis (1) obtenir
> **la carte officielle « cas → documents »**, qui n'existe nulle part (le canon est 100 % SELARL).
> Aucune règle inventée : NotebookLM répond **avec citations**.
>
> **Comment s'en servir.** Chaque prompt est **autonome** (contexte suffisant pour NotebookLM seul) et
> contient **une seule question**. Copier les blocs **un par un**. **Envoyer le prompt 1 EN TOUT
> PREMIER** : tant qu'on ne sait pas de quel type d'entreprise on parle, ni le moteur ni l'UI ne
> peuvent être bâtis. Les réponses alimentent `CARTOGRAPHIE_TENTATIVE.md` puis le journal de décisions
> (codes `SCP-…`).
>
> **Routage (rule 20 — projet avec associé métier Rafael).** Cible : **[NotebookLM]** = règle/wording
> juridique sourçable · **[Rafael]** = ce que NotebookLM ne peut pas fournir (modèle manquant, décision
> propre au cabinet). **Épuiser NotebookLM avant Rafael. Ne JAMAIS poser une question métier à Gad.**

---

## DÉJÀ CONNU / ACQUIS — NE PAS REDEMANDER

Ces points sont **vérifiés dans les sources / le code** et n'ont **pas** à être posés à NotebookLM :

1. **Le canon ne contient aucune carte « cas → documents » SCP.** Vérifié : `Documents_a_generer_par_cas`
   (V1/V2/V3) est **100 % SELARL** ; « SCP » n'y apparaît jamais. Inutile de demander « où est la carte
   dans le canon » — elle n'existe pas (c'est pourquoi les prompts 1 à 6 la **reconstruisent**).
2. **Identité des 5 modèles `.docx` + 1 `.doc` legacy** : recensée dans `INVENTAIRE_MODELES.md` (Statuts,
   Fiche de création, Autorisation de domiciliation, Déclaration de non-condamnation, Procuration, +
   PV nomination gérant en `.doc`). On sait **ce que chaque fichier EST** ; on cherche **dans quels cas
   il s'assemble** et **son wording exact**.
3. **Trames « communes »** (Autorisation de domiciliation, Déclaration de non-condamnation, et la partie
   générique de la Procuration) : identiques à la couche partagée SEL/SCM — à **réutiliser**, pas à
   re-spécifier. Ne pas en demander le wording (seul un point de durée subsiste : prompt 14).
4. **Dictionnaire de variables** `variables_source_scp.csv` (123 variables, jusqu'à `_personne_5`) =
   référence transverse, **pas** le contrat de variables d'un cas. Sert d'indice pour le multi, rien de plus.
5. **Clause « médecin » des statuts** (« constat par un médecin d'une incapacité du gérant ») = clause de
   gouvernance **neutre**, PAS une coquille inter-profession. Déjà tranché à l'inventaire — ne pas la
   signaler comme défaut (ne reste que la question de fond du prompt 8 sur l'objet social).
6. **Aucun acquis technique côté `src/`** : Codex n'a posé aucun cas/générateur/UI SCP (page blanche).
   C'est un fait de code, pas une question métier — rien à demander à NotebookLM.

---

## Cas → documents *(PRIORITÉ ABSOLUE — envoyer ce groupe en premier, prompt 1 d'abord)*

### 1 — [NotebookLM] Nature réelle du type « SCP » *(question décisive — AVANT tout le reste)*

```
Dans nos sources, que désigne exactement le sigle "SCP" : une Société Civile Professionnelle (exercice
en commun d'une profession réglementée), une société civile de détention de participations / de
portefeuille de titres, ou une autre forme de société civile ? Le modèle de statuts dont nous disposons
a pour objet "la prise de participation et la gestion d'un portefeuille de titres, à l'exclusion de
toute opération commerciale", ce qui ressemble à une société civile patrimoniale plus qu'à une société
d'exercice professionnel. Précise la forme réelle de ce "SCP" et cite la source.
```

### 2 — [Rafael] Carte officielle des cas + confirmation de la nature *(préalable, NotebookLM ne l'a probablement pas)*

```
Pour le type que nous appelons "SCP" (dossier "Création SCP"), deux questions : (1) "SCP" désigne-t-il
une société civile professionnelle d'exercice ou une société civile de portefeuille / patrimoniale ?
(2) Existe-t-il un document officiel "Documents à générer par cas" pour ce type — la liste des CAS
(création, entrée/sortie d'associé, cession de parts, transfert de siège, modification, dissolution…)
et, pour chaque cas, la liste exacte des documents à produire ? Si oui, peux-tu nous le fournir ?
Aujourd'hui nous n'avons que les modèles de "Création SCP", sans carte cas → documents, et le canon
"Documents à générer par cas" est entièrement SELARL.
```

### 3 — [NotebookLM] Liste des cas du type « SCP »

```
D'après les sources, quels sont les différents CAS de dossier possibles pour ce type "SCP" — par exemple
création, entrée ou sortie d'associé, cession de parts, transfert de siège, modification statutaire,
dissolution ? Cite chaque cas avec sa source. Si les sources ne couvrent que la création, dis-le
explicitement.
```

### 4 — [NotebookLM] Création d'une SCP : documents exacts, ordre, et caractère systématique/optionnel

```
Pour la CRÉATION d'une SCP, donne la liste EXACTE et exhaustive des documents à produire, dans l'ordre.
Pour CHAQUE document — statuts, fiche de création, PV de nomination du gérant, autorisation de
domiciliation, déclaration de non-condamnation, procuration — indique précisément : "systématique",
"optionnel (condition : …)", ou "ne fait PAS partie de la création d'une SCP". Cite les sources.
```

### 5 — [NotebookLM] Ce qui N'EST PAS dans un dossier de création de SCP (à exclure)

```
Pour la CRÉATION d'une SCP, ces éléments — présents pour les SEL ou la SCM — s'appliquent-ils aussi ?
(a) une "demande d'inscription à l'Ordre" ; (b) des documents liés au régime matrimonial ou au conjoint
d'un associé (lettre de renonciation à la qualité d'associé, avertissement au conjoint en cas d'apport
d'un bien commun) ; (c) un pacte d'associés et/ou un règlement intérieur. Pour chacun, réponds "fait
partie de la création de SCP (condition : …)" ou "ne s'applique pas à la SCP". Cite la source.
```

### 6 — [Rafael] Filet de secours si NotebookLM reste muet sur les cas *(à n'envoyer que dans ce cas)*

```
Si NotebookLM ne contient pas la carte cas → documents de la SCP : à partir de ta pratique, peux-tu
nous indiquer (1) la liste des documents que tu produis systématiquement pour une création de SCP,
(2) les autres cas que tu traites pour ce type (cession de parts, entrée/sortie d'associé, dissolution…)
et les documents associés, et (3) s'il manque des modèles dans le dossier "Création SCP" (ex. pacte
d'associés, demande d'inscription à l'Ordre) ? Cela nous évite d'inventer la carte.
```

---

## Wording *(par document — confirmer le texte exact et lever les ambiguïtés)*

### 7 — [Rafael] PV de nomination du gérant SCP : modèle exploitable + emprunt/bien

```
Notre modèle "PV nomination gérant" pour la SCP est un fichier .doc ancien, non exploitable
automatiquement : peux-tu nous le fournir en .docx tokenisé ? Par ailleurs ce PV contient des variables
d'emprunt et d'adresse d'un bien (montant d'emprunt, voie/ville/code postal d'un bien) : ce PV combine-
t-il la nomination du gérant AVEC une autorisation d'emprunt ou d'acquisition d'un bien, ou faut-il deux
documents distincts ? Précise lequel.
```

### 8 — [NotebookLM] Statuts SCP : objet social exact (le point décisif du wording)

```
Quel doit être l'OBJET SOCIAL des statuts de notre SCP ? Le modèle actuel décrit une société de
participations / portefeuille de titres ("prise de participation, détention et gestion d'un portefeuille
de titres, à l'exclusion de toute opération commerciale"). Est-ce le bon objet, ou faut-il un objet
d'exercice professionnel en commun ? Donne le wording EXACT attendu de l'article "Objet" et cite la source.
```

### 9 — [NotebookLM] Statuts SCP : comparution, apports, capital, répartition des parts

```
Dans les statuts de notre SCP, quel est le wording EXACT de : (a) la comparution des associés, (b)
l'article Apports (qui apporte quoi, montant en chiffres et en lettres, numéraire ou nature), (c)
l'article Capital, valeur nominale de la part, nombre total de parts et leur répartition / numérotation
(numéro de début et de fin de parts par associé) ? Donne le texte exact et cite la source.
```

### 10 — [NotebookLM] Statuts SCP : durée de la société et exercice social (figés ou variables ?)

```
Pour notre SCP, dans les statuts : (a) la DURÉE de la société est-elle figée (ex. 99 ans) ou laissée
variable ? — c'est aujourd'hui une variable libre dans notre modèle, contrairement à la SELARL où elle
est figée à 99 ans ; (b) l'exercice social (date de début et de clôture) est-il libre ou normé ?
Donne les valeurs attendues et cite la source.
```

### 11 — [NotebookLM] forme_sociale variable : une trame pour plusieurs sociétés civiles ?

```
Dans nos statuts, notre fiche et notre PV "SCP", la "forme sociale" est une VARIABLE (non figée). Cela
signifie-t-il qu'une même trame couvre plusieurs formes de société civile (SCP, société civile
patrimoniale, SCM…), ou la forme doit-elle être figée à une valeur précise pour ce type ? Cite la source.
```

### 12 — [NotebookLM] Procuration SCP : objet et wording exact

```
Quel est l'objet exact de la procuration produite pour la création d'une SCP (mandat aux formalités
auprès de qui, pour quels actes) et son wording exact, notamment la fonction du dirigeant qui donne
mandat ? Cite la source.
```

### 13 — [NotebookLM] Fiche de création SCP : livrable client ou outil interne ?

```
Le document "Fiche de création de société civile" est-il un livrable destiné au client, ou un
formulaire de collecte interne au cabinet qui ne doit pas être généré comme document final ? Cite la source.
```

### 14 — [NotebookLM] Durée de la domiciliation du siège SCP (à ne pas confondre avec la durée de société)

```
Pour la SCP, la durée de la domiciliation du siège est-elle "indéterminée" comme pour la SEL, ou autre ?
(Il s'agit bien de la durée de la domiciliation du siège, à ne pas confondre avec la durée de la
société.) Cite la source.
```

### 15 — [NotebookLM] Statut du PDF "SCP IR Note assistance à la déclaration"

```
Le document "SCP IR Note assistance à la déclaration" (un PDF) est-il un livrable à PRODUIRE pour le
client (note d'assistance à la déclaration d'impôt sur le revenu), ou une simple note d'information
interne qui ne doit pas être générée comme document du dossier ? Cite la source.
```

---

## Genre / pluriel *(transverse — appliquer le pluriel après confirmation Albane)*

### 16 — [NotebookLM] Variations de GENRE dans les documents SCP

```
Dans les documents d'une SCP (statuts, PV de nomination du gérant, déclaration, procuration), quelles
formulations varient selon le GENRE de l'associé ou du gérant (par ex. "le gérant"/"la gérante",
"associé"/"associée", "né"/"née", "domicilié"/"domiciliée", "le Docteur"/"la Docteure") ? Liste les
paires de chaînes EXACTES concernées, avec leur source.
```

### 17 — [NotebookLM] Passages à mettre au PLURIEL selon le nombre d'associés

```
Dans les documents d'une SCP, quelles formulations doivent passer au PLURIEL quand il y a plusieurs
associés (comparution, apports, répartition des parts, gouvernance, signatures) ? Précise les endroits
exacts à pluraliser, et indique si la gouvernance est déjà rédigée au pluriel dans les modèles ou s'il
faut la pluraliser. Cite la source.
```

### 18 — [NotebookLM] "le Docteur"/"la Docteure" : règle universelle ou choix par personne ?

```
Pour la SCP, la formulation "le Docteur"/"la Docteure" (et plus largement le titre du praticien) se
gère-t-elle PAR ASSOCIÉ (au cas par cas selon la préférence de chaque personne) ou par une règle
universelle valant pour tout le document ? Cite la source.
```

---

## Multi *(nombre d'associés / de gérants à modéliser)*

### 19 — [NotebookLM] Nombre d'associés et de gérants d'une SCP : minimum et borne haute

```
Combien d'associés une SCP peut-elle compter dans nos dossiers types, et quel est le nombre minimum ?
Notre fiche de création prévoit jusqu'à 5 associés et 2 gérants, mais le modèle de statuts n'en détaille
que 2. Quelle est la borne haute réaliste à modéliser pour la création d'une SCP, et combien de gérants
au maximum ? Cite la source.
```
