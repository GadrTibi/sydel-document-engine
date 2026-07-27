# SAS — Prompts NotebookLM DÉFINITIFS (V2)

> **Date :** 2026-06-07 · **Branche :** `sprint/engine-completion` · **Remplace** : `NOTEBOOKLM_PROMPTS.md` (V1, 16 prompts).
> **Objet :** obtenir la TOTALITÉ de l'info métier nécessaire pour bâtir le type **SAS** (moteur + UI)
> selon `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. Set **dédoublonné, priorisé, prêt à coller**.
>
> **Pourquoi c'est critique :** le canon `Documents_a_generer_par_cas_V3.docx` est **100 % SELARL**
> (0 occurrence SAS / SASU / SPFPL). Il n'existe **aucune carte officielle cas → documents pour la SAS**.
> Toute cartographie actuelle (V1 `CARTOGRAPHIE_TENTATIVE.md` ET le code Codex) est **inférée, non ratifiée**.
>
> **Mode d'emploi :** copier-coller chaque bloc **tel quel**, **un prompt à la fois**, dans le NotebookLM
> Sydel (corpus tokenisé + transcripts Albane). **NotebookLM TOUJOURS avant Rafael.** Si NLM répond
> « non présent dans les sources » → ne pas combler : c'est exactement ce qui partira dans le message Rafael.
>
> **Garde-fou :** ne rien reformuler, ne pas inventer de cas ni de wording.

---

## Déjà connu / NE PAS redemander (établi par lecture des modèles + du code moteur)

Ces points sont **factuels** (lus dans les `.docx` et le code `sydel_doc_engine`). Ils n'ont **pas besoin
d'être demandés à NLM** — ils servent de contexte aux prompts. (Le **wording** reste à valider par Rafael,
mais la **structure** est connue.)

- **7 modèles** dans le corpus `Création SAS` : statuts SAS/SPFPL médecins, PV rémunération président,
  liste des souscripteurs (2 variantes), déclaration non-condamnation, autorisation domiciliation, procuration.
- **Capital en ACTIONS** (`[nb_actions]`, `[valeur_nominale_action]`), pas en parts. Dirigeant = **président**.
- **Statuts SAS** = 30 tokens, profession **médecin** (mentions ordinales `[numero_ordre] [numero_rpps] [ordre_departemental]`), bloc conjoint/régime matrimonial présent.
- Le moteur modélise déjà : `forme_sociale`, `ville_rcs`, `qualite_associe` (« actionnaire unique »),
  président à **mandat illimité**, rémunération président = **absence de rémunération jusqu'à clôture du 1er exercice**.
- **À demander quand même** (parce qu'inféré, pas ratifié) : que ces valeurs soient **figées** ou **variables**
  (durée société, durée mandat, absence de rémunération) → couvert par les prompts 4 et 8 ci-dessous.

---

## Cas → documents  *(priorité 1 — LE point bloquant)*

### Prompt 1 — Existe-t-il une carte cas → documents SAS ? + périmètre du type
```
Dans le corpus Sydel, le document « Documents à générer par cas » décrit les cas et les documents pour la SELARL. Existe-t-il, dans les sources, une description équivalente pour la SAS (Société par Actions Simplifiée) ou la SASU ? Si oui, cite la source exacte ; si non, dis-le explicitement. Précise aussi le périmètre réel du type SAS chez Sydel : pour quels usages le cabinet crée-t-il une SAS plutôt qu'une SELARL ? Est-ce limité aux médecins, ou couvre-t-il aussi pharmaciens / chirurgiens-dentistes ? Distingue-t-on une SAS « d'exercice » (SELAS) d'une SAS « holding » (SPFPL) ? Réponds uniquement à partir des sources, sans rien inventer.
```

### Prompt 2 — Liste exhaustive des cas SAS + carte cas → documents
```
Pour une création en SAS chez Sydel, donne la liste EXHAUSTIVE des cas / situations qui déclenchent des documents différents (par analogie avec la SELARL : « dans tous les cas », statuts par profession, régime matrimonial/communauté, cession, SCM, dérogation, site distinct…). Pour CHAQUE cas applicable à la SAS, liste les documents à générer avec le nom exact du fichier modèle .docx quand il existe dans les sources, et précise si le document est systématique (« dans tous les cas ») ou conditionnel (à quelle condition). Si un cas SELARL n'a PAS d'équivalent SAS, dis-le. Si un document est attendu sans modèle source, signale « modèle manquant ». N'invente aucun cas, aucun document.
```

### Prompt 3 — La SAS a-t-elle un cas cession (d'actions) et un cas régime communautaire ?
```
Le modèle de statuts SAS du corpus contient un bloc conjoint / régime matrimonial. La SAS chez Sydel donne-t-elle lieu, comme la SELARL : (a) à un cas de CESSION (d'actions, et/ou de cabinet médical ou dentaire) — si oui, avec quels documents et quels modèles ? (b) à un cas de RÉGIME COMMUNAUTAIRE — renonciation du conjoint à la qualité d'actionnaire et/ou avertissement au conjoint en cas d'apport d'un bien commun — si oui, avec quels modèles ? Existe-t-il pour la SAS une « demande d'inscription à l'ordre » comme en SELARL ? Pour chaque cas absent en SAS, confirme-le explicitement. Réponds à partir des sources uniquement.
```

### Prompt 4 — Actionnaire unique (SASU) vs plusieurs actionnaires
```
La SAS traitée par Sydel est-elle, en pratique, unipersonnelle (SASU, actionnaire unique) ou pluripersonnelle (plusieurs actionnaires) ? Si elle peut avoir plusieurs actionnaires : quel est le nombre minimum et maximum traité, et quels documents ou quelles sections changent (comparution, répartition du capital en actions, gouvernance, président, signatures) ? Le document « statuts SASU Holding » présent dans le corpus fait-il partie du type SAS, ou relève-t-il d'un montage holding distinct ? La durée du mandat du président est-elle figée (illimitée ?) ou à saisir au cas par cas ? Réponds à partir des sources, sans rien inventer.
```

---

## Wording par document  *(priorité 2)*

### Prompt 5 — Statuts SAS / SPFPL médecins : durée, profession, points juridiques
```
Pour le modèle « STATUTS SAS SPFPL médecins », réponds précisément : (1) la DURÉE de la société est-elle figée dans ces statuts, et à quelle valeur (ex. 99 ans), ou est-elle variable ? (2) Y a-t-il des mentions propres à une profession (médecin) qui ne devraient PAS apparaître pour une autre profession, donc à neutraliser si la SAS s'élargit (anti-coquille inter-profession) ? (3) Le capital y est-il exprimé en ACTIONS (nombre + valeur nominale), et est-ce la seule forme admise ? (4) Le bloc conjoint / régime matrimonial est-il systématique ou conditionnel au régime de l'actionnaire ? Réponds uniquement à partir des sources.
```

### Prompt 6 — PV rémunération du président (+ existe-t-il un PV de nomination distinct ?)
```
Pour le modèle « PV rémunération président » d'une SAS : (1) ce PV acte-t-il SYSTÉMATIQUEMENT une ABSENCE de rémunération du président jusqu'à la clôture du premier exercice, ou la rémunération est-elle variable (montant à saisir) ? (2) L'en-tête de ce PV reprend l'identité complète de la société (forme sociale, capital, siège, ville du RCS) en plus de l'identité du président : confirme que c'est bien la société émettrice qui est désignée, pas un tiers. (3) Existe-t-il, en plus de ce PV de rémunération, un PV de NOMINATION du président distinct (analogue au « PV nomination gérant » de la SELARL) ? Si oui, quel est son modèle ? Réponds à partir des sources.
```

### Prompt 7 — Capital : « liste des souscripteurs » (2 variantes) + « attestation sur le capital »
```
Le corpus SAS contient DEUX modèles « Liste des souscripteurs » : une version A (état par souscripteur : civilité, nom, prénom, adresse personnelle détaillée, nombre d'actions, montant souscrit) et une version B « enrichie SPFPL » (qui ajoute la forme sociale, le capital social, l'adresse du siège et la mention « Société de Participations Financières de Profession Libérale de [profession] »). (1) Laquelle est la version de RÉFÉRENCE à générer, et dans quel cas ? Sont-ce deux documents distincts ou deux états d'un même document ? (2) Par ailleurs, un document « Attestation sur le capital - apport - liste des souscripteurs » est-il un document SAS À PART ENTIÈRE, distinct de ces listes, ou est-ce un autre nom pour l'une d'elles ? Si distinct, où est son modèle ? Réponds à partir des sources, sans reconstituer aucun document absent.
```

### Prompt 8 — Documents « dans tous les cas » (DNC, domiciliation, procuration) : spécificités SAS
```
Pour la SAS, les modèles « Déclaration sur l'honneur de non-condamnation », « Autorisation de domiciliation » et « Procuration » sont-ils identiques à ceux de la SELARL, ou comportent-ils des spécificités SAS — notamment la mention « président » au lieu de « gérant », et la forme « par actions » ? Confirme que ces trois documents sont bien « dans tous les cas » pour une création SAS. Dans l'autorisation de domiciliation, la durée de la domiciliation est-elle bien « indéterminée » (à ne pas confondre avec la durée de la société) ? Réponds à partir des sources.
```

---

## Genre / pluriel  *(priorité 3)*

### Prompt 9 — Accord de genre : paires de chaînes exactes (président/présidente…)
```
Dans les documents SAS, quelles formulations exactes changent selon le genre du dirigeant et des actionnaires ? Donne les PAIRES de chaînes exactes à substituer, document par document — par exemple « le Président » / « la Présidente », « né le » / « née le », « soussigné » / « soussignée », « l'actionnaire unique » / « l'actionnaire unique » (ou « associé unique » / « associée unique » si ce wording est utilisé). Précise aussi, pour chaque accord, QUELLE personne le détermine (le président ? un actionnaire donné ? le signataire ?) plutôt qu'un genre global du dossier. N'utilise PAS de règle de terminaison automatique (-é/-ée) : uniquement des paires de chaînes réellement attestées dans les modèles. Réponds à partir des sources.
```

---

## Multi (nombre d'actionnaires)  *(priorité 4)*

### Prompt 10 — Pluriel : passages qui changent avec plusieurs actionnaires
```
Pour la SAS, quelles parties EXACTES des documents passent du singulier au pluriel quand il y a plusieurs actionnaires au lieu d'un actionnaire unique : comparution, apports, répartition du capital en actions, signatures, et vocabulaire (« l'actionnaire unique » devient « les actionnaires » ; « il » / « ils ») ? Donne les passages concernés, document par document. Cette pluralisation doit-elle être validée par Albane avant mise en œuvre ? Réponds à partir des sources, sans inventer de passage.
```

### Prompt 11 — Vocabulaire d'interface SAS attendu par les juristes
```
Pour l'interface logicielle de la SAS, confirme les libellés exacts attendus par les juristes : faut-il employer « actionnaire » plutôt qu'« associé », « actions » plutôt que « parts », « président » plutôt que « gérant », « actionnaire unique » plutôt qu'« associé unique » ? Signale tout terme à éviter ou toute exception où le wording d'un document précis diffère du libellé d'interface. Réponds à partir des sources.
```

---

## Note de passation (pour le message Rafael — pas un prompt NLM)

Après NotebookLM, regrouper dans un message **Rafael** (jamais une question au PM) tout ce qui reste
**non attesté** — typiquement : existence d'une carte cas → documents SAS (prompts 1-2), périmètre
profession/forme (1, 4), cas cession/communauté (3), variante de référence « liste souscripteurs » +
« attestation capital » (7), durée de la société (5), figement de l'absence de rémunération (6).
Être **CERTAIN** que la réponse n'est pas déjà dans les sources avant de faire relayer.
