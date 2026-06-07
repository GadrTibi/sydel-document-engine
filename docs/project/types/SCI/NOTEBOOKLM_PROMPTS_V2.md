# SCI — Prompts NotebookLM DÉFINITIFS (prêts à coller) — V2

> **Date :** 2026-06-07 · **Branche :** `sprint/engine-completion` · **Type :** SCI (Société Civile
> Immobilière), 2 variantes structurelles : **SCI** et **SCI IRIS**.
> **Objet :** obtenir la TOTALITÉ de l'info métier nécessaire pour bâtir le type **SCI** (moteur + UI)
> selon `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. Set **dédoublonné, priorisé, prêt à coller**.
>
> **Comment s'en servir.** Chaque prompt est **autonome** (contexte suffisant pour NotebookLM seul) et
> contient **une seule question**. Copier les blocs **un par un**. **Envoyer le groupe « Cas → documents »
> EN PREMIER** : sans la carte des cas confirmée, ni le moteur ni l'UI ne peuvent être figés.
> **NotebookLM TOUJOURS avant Rafael.** Si NLM répond « non présent dans les sources » → ne pas combler :
> c'est exactement ce qui partira dans le message Rafael.
>
> **Routage (rule 20 — projet avec associé métier Rafael).** Cible : **[NotebookLM]** = règle/wording
> juridique sourçable · **[Rafael]** = ce que NotebookLM ne peut pas fournir (modèle manquant, décision
> propre au cabinet). **Épuiser NotebookLM avant Rafael. Ne JAMAIS poser une question métier à Gad.**
> **Garde-fou :** ne rien reformuler, ne pas inventer de cas ni de wording.

---

## DÉJÀ CONNU / ACQUIS — NE PAS REDEMANDER

Ces points sont **vérifiés dans les sources et le code** (`statuts_civils_common.py`,
`registry/catalog.py`, canon `Documents_a_generer_par_cas.docx` V1, modèles tokenisés `lot_04`). Ils
servent de **contexte** aux prompts mais ne sont **pas** à reposer à NotebookLM.

1. **Carte cas → documents SCI : PARTIELLEMENT au canon (V1 seulement).** La version V1 de
   `Documents à générer par cas` contient un bloc SCI : **Si SCI → statuts SCI** · **Si SCI IRIS →
   statuts SCI IRIS** · **Si IS → Lettre option IS** · puis le tronc commun **Déclaration de
   non-condamnation, Procuration, Autorisation de domiciliation, PV de nomination du gérant**.
   ⚠️ Ce bloc a **DISPARU des versions V2 et V3** du canon (0 occurrence SCI). Le prompt 1 sert
   uniquement à **trancher la version qui fait foi** ; le reste de la carte est donc déjà connu.
2. **2 variantes structurelles** : `SCI` et `SCI IRIS`, déjà codées (`StatutsSciGenerator`,
   `StatutsSciIrisGenerator`) et déclarées au registre (`DOC-019/020/021`, structures `SCI` / `SCI IRIS`).
3. **Capital en PARTS** (jamais en actions) ; **capital VARIABLE** structurel (mention de capital
   variable + capital autorisé/maximal présents dans les deux modèles ; ARTICLE 8 « Modifications du
   capital »). Modèles tokenisés à **3 personnes physiques** + (SCI IRIS) **1 société associée**.
4. **SCI standard : personnes morales associées BLOQUÉES en V1** faute de source observée (le code lève).
   La SCI IRIS, elle, **requiert** un associé personne morale + une table « quote-part de résultat
   exceptionnel par groupe de parts ». Différence structurelle déjà actée — voir prompt 9.
5. **Trames « communes »** (Déclaration de non-condamnation, Procuration, Autorisation de domiciliation)
   = couche partagée SEL déjà existante, à **réutiliser**. Ne pas en redemander le wording général ;
   seules les **spécificités SCI** sont à confirmer (prompt 6).
6. **Plafond technique** = 6 associés (`MAX_ASSOCIES`) ; les modèles fournis en exposent 3. La borne
   métier réelle reste à confirmer (prompt 11).
7. **PAS de bloc conjoint / régime matrimonial** ni de **« demande d'inscription à l'Ordre »** dans les
   statuts SCI (absents des modèles ET du bloc canon V1 — la SCI n'est pas une structure d'exercice
   professionnel). Ne pas demander ces documents pour la SCI.

---

## Cas → documents *(PRIORITÉ ABSOLUE — envoyer ce groupe en premier)*

### 1 — [NotebookLM] Version du canon qui fait foi pour la SCI (V1 vs V2/V3)

```
Le document « Documents à générer par cas » existe en plusieurs versions. Dans sa version la plus
ancienne, il contient un bloc SCI : « Si SCI → statuts SCI », « Si SCI IRIS → statuts SCI IRIS »,
« Si IS → Lettre option IS », puis Déclaration de non-condamnation, Procuration, Autorisation de
domiciliation, PV de nomination du gérant. Ce bloc SCI semble avoir disparu des versions plus
récentes. Quelle version fait foi aujourd'hui, et la SCI fait-elle toujours partie du périmètre
Sydel ? Si le bloc SCI a été retiré volontairement, pour quelle raison ? Réponds uniquement à partir
des sources, en citant la version exacte.
```

### 2 — [NotebookLM] Liste exhaustive des CAS de SCI (au-delà de la création)

```
Pour une SCI (Société Civile Immobilière) chez Sydel, quels sont les différents CAS de dossier
possibles au-delà de la création : entrée ou sortie d'associé, cession de parts, transfert de siège,
augmentation/réduction de capital, dissolution, option fiscale (IR/IS) ? Pour chaque cas, indique s'il
est traité par Sydel et les documents associés. Je n'ai aujourd'hui que le dossier de CRÉATION (statuts
SCI / SCI IRIS + tronc commun). Réponds uniquement à partir des sources et cite-les ; si un cas n'est
pas couvert, dis-le explicitement.
```

### 3 — [NotebookLM] Création d'une SCI : documents exacts, ordre, systématique vs conditionnel

```
Pour la CRÉATION d'une SCI, donne la liste EXACTE et exhaustive des documents à produire, dans l'ordre.
Pour CHAQUE document — statuts SCI (ou SCI IRIS), PV de nomination du gérant, Lettre d'option IS,
Déclaration de non-condamnation, Procuration, Autorisation de domiciliation — indique précisément :
« systématique » (dans tous les cas), « conditionnel (condition : …) », ou « ne fait PAS partie de la
création d'une SCI ». Précise notamment la condition d'émission de la « Lettre d'option IS » (régime
fiscal) et du choix entre statuts SCI et statuts SCI IRIS. Cite les sources.
```

### 4 — [NotebookLM] SCI standard vs SCI IRIS : ce qui déclenche le choix de variante

```
Il existe deux modèles de statuts de SCI : un modèle « SCI » et un modèle « SCI IRIS ». Qu'est-ce qui
distingue concrètement les deux, et quel critère métier détermine lequel utiliser pour un dossier
donné ? La variante « IRIS » correspond-elle au cas où l'un des associés est une société (personne
morale), et/ou à un mode particulier de répartition du résultat (quote-part de résultat exceptionnel
par groupe de parts) ? Réponds uniquement à partir des sources et cite-les.
```

### 5 — [Rafael] Filet de secours si NotebookLM reste muet *(à n'envoyer que dans ce cas)*

```
Si NotebookLM ne confirme pas la carte cas → documents de la SCI : à partir de ta pratique, peux-tu
nous indiquer (1) la liste des documents que tu produis systématiquement pour une création de SCI,
(2) le critère qui te fait choisir entre une SCI « standard » et une SCI « IRIS », et (3) les autres
cas de SCI que tu traites (cession de parts, entrée/sortie d'associé, option IS) avec leurs documents.
Cela nous évite d'inventer la carte.
```

---

## Wording *(par document — confirmer le texte exact et lever les ambiguïtés)*

### 6 — [NotebookLM] Spécificités SCI des trois trames communes (DNC, domiciliation, procuration)

```
Pour une SCI, les modèles « Déclaration sur l'honneur de non-condamnation », « Autorisation de
domiciliation » et « Procuration » sont-ils identiques à ceux des autres sociétés (SELARL, SCM), ou
comportent-ils des spécificités SCI : terme « gérant » de la SCI, forme « société civile »,
qualification d'associé non-professionnel ? Dans l'autorisation de domiciliation, confirme que la
durée de domiciliation est « indéterminée » (à ne pas confondre avec la durée de la société). Réponds
à partir des sources et cite-les.
```

### 7 — [NotebookLM] PV de nomination du gérant de SCI : wording, durée, pouvoirs, pluri-gérance

```
Quel est le wording exact du PV de nomination du gérant d'une SCI : qui nomme le gérant (les associés),
durée du mandat (figée ou à saisir ?), étendue des pouvoirs, et le gérant doit-il être lui-même
associé ? Une SCI peut-elle avoir plusieurs gérants, et si oui comment le texte du PV et des statuts
(article Administration de la société) s'y adapte-t-il ? Le nom du gérant figure-t-il aussi dans les
statuts ou uniquement dans le PV ? Cite la source.
```

### 8 — [NotebookLM] Durée de la SCI et capital variable : valeurs figées ou variables ?

```
Pour les statuts de SCI, deux points à confirmer car ils n'apparaissent pas comme variables à saisir
dans nos modèles : (1) la DURÉE de la société (article « Durée ») est-elle figée à une valeur précise
(par ex. 99 ans) ou variable selon le dossier ? (2) Le capital est présenté comme VARIABLE, avec un
capital social initial, un capital autorisé/maximal et un article « Modifications du capital social » :
confirme que la SCI Sydel est systématiquement à capital variable, et précise comment se déterminent le
capital initial et le capital autorisé (montant figé, formule, ou libre). Cite la source.
```

### 9 — [NotebookLM] SCI IRIS : associé société + quote-part de résultat exceptionnel

```
Le modèle de statuts « SCI IRIS » prévoit un associé qui est une SOCIÉTÉ (personne morale, avec
dénomination, forme juridique, capital, siège, RCS, représentant) et une table de répartition d'une
« quote-part de résultat exceptionnel » par groupe de parts. Quel est le wording exact : (1) de
l'identification de l'associé personne morale dans la comparution et la répartition des parts, (2) de
l'article qui définit la quote-part de résultat exceptionnel par groupe de parts ? Dans quel cas
métier la SCI IRIS s'emploie-t-elle ? Cite la source.
```

### 10 — [Rafael] Modèle de la « Lettre d'option IS » pour la SCI

```
Le bloc SCI du canon mentionne une « Lettre d'option IS » (à produire si la SCI opte pour l'impôt sur
les sociétés). Nous n'avons pas ce modèle dans notre corpus de documents tokenisés. Peux-tu nous
fournir le modèle « Lettre d'option IS » (version SCI) avec ses variables, ou confirmer qu'il est
identique à un modèle déjà existant pour un autre type de société ?
```

---

## Genre / pluriel *(transverse — appliquer après confirmation Albane pour le pluriel)*

### 11 — [NotebookLM] Variations de GENRE dans les documents SCI (paires de chaînes exactes)

```
Dans les documents d'une SCI (statuts SCI/SCI IRIS, PV de nomination du gérant), quelles formulations
varient selon le GENRE de l'associé ou du gérant — par exemple « le gérant »/« la gérante »,
« associé »/« associée », « né le »/« née le », « soussigné »/« soussignée » ? Donne les PAIRES de
chaînes EXACTES à substituer, document par document, et précise pour chaque accord QUELLE personne le
détermine (le gérant ? un associé donné ? le signataire ?) plutôt qu'un genre global du dossier.
N'utilise PAS de règle de terminaison automatique (-é/-ée) : uniquement des paires réellement
attestées dans les modèles. Cite la source.
```

### 12 — [NotebookLM] Passages à mettre au PLURIEL selon le nombre d'associés

```
Pour une SCI, quelles parties EXACTES des documents passent du singulier au pluriel quand il y a
plusieurs associés (comparution, apports, répartition des parts, gouvernance/administration,
signatures) ? Précise les endroits exacts à pluraliser et indique si la gouvernance est déjà rédigée
au pluriel dans les modèles ou s'il faut la pluraliser. Cette pluralisation doit-elle être validée par
Albane avant mise en œuvre ? Cite la source.
```

---

## Multi *(nombre d'associés / de sociétés à modéliser)*

### 13 — [NotebookLM] Nombre d'associés d'une SCI : minimum, maximum, et associé société

```
Combien d'associés une SCI compte-t-elle dans des dossiers types, et quel est le minimum légal (une
SCI doit-elle avoir au moins deux associés ?) ? Nos modèles exposent 3 personnes physiques, et la
variante « IRIS » ajoute une société associée. Quelle est la borne haute réaliste à modéliser pour une
SCI ? Et une SCI standard (non IRIS) peut-elle compter un associé personne morale, ou est-ce réservé à
la variante IRIS ? Cite la source.
```

---

## Note de passation (pour le message Rafael — pas un prompt NLM)

Après NotebookLM, regrouper dans un message **Rafael** (jamais une question au PM) tout ce qui reste
**non attesté** — typiquement : version du canon qui fait foi + maintien de la SCI au périmètre
(prompt 1), liste des cas hors création (2), critère SCI vs SCI IRIS (4), durée société + figement du
capital variable (8), **modèle manquant « Lettre d'option IS »** (10). Être **CERTAIN** que la réponse
n'est pas déjà dans les sources avant de faire relayer.