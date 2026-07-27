# Prompts NotebookLM DEFINITIFS — Type SPFPL (V2)

> **But.** Obtenir de NotebookLM **toute l'info métier** nécessaire pour bâtir le type **SPFPL**
> (moteur + UI Streamlit) selon la recette `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`.
> Chaque bloc de code ci-dessous est **autonome** et **prêt à coller individuellement** dans NotebookLM.
> Cible NotebookLM = règle / wording **juridique** avec citations. Les arbitrages purement **projet**
> (modélisation, scope V1) ne sont PAS posés à NotebookLM : ils sont tranchés dans les specs.

> **Méthode.** Relayer **par vagues de priorité**. Le **Prompt 1 est bloquant** : il fixe le périmètre
> réel du type (canon V1 vs V2/V3) et lève l'ambiguïté **parts vs actions**. Ne pas coder avant sa réponse.

---

## Acquis — NE PAS reposer à NotebookLM

Établi par lecture du canon V1 et des modèles tokenisés (`lot_04`, `lot_05`) + specs
`lot_04_statuts_spfpl_*`, `lot_05_spfpl_*`. À traiter comme **connu** :

- **Deux parcours SPFPL** existent au canon V1 : **SPFPL cession** et **SPFPL apport**.
- **La SPFPL elle-même est une SAS** : modèles intitulés « Société de Participations Financières de
  Profession Libérale … **par actions simplifiée** » → elle émet des **actions** (tokens `nb_actions`,
  `valeur_nominale_action`, dirigeant = **président**).
- **Carte cas → documents (canon V1)** : voir Prompt 1 ; documents universels (déclaration non
  condamnation, autorisation domiciliation, procuration, demande d'inscription à l'ordre, PV nomination
  gérant) et batch **régime communautaire** (renonciation, avertissement conjoint) sont **déjà cadrés
  ailleurs** (transverses), pas à re-spécifier ici.
- **Commissaire** : le rôle métier est **commissaire aux apports** (le libellé canon « comm. aux
  comptes » est une coquille du tableau ; les DOCX portent bien « commissaire aux apports »). — Reste à
  faire **confirmer** par NotebookLM (Prompt « Wording » dédié), pas à redécouvrir.
- **Tokens connus par document** : inventoriés (statuts cession/apport, contrat d'apport, actes de
  cession parts/actions, attestation capital, désignation CAA, PV agrément 1/plusieurs associés).
- **Société cible** = la SEL dont les titres sont cédés/apportés à la SPFPL ; rôle `societe_cible`.
- **Personne principale** = `cedant` (parcours cession) ou `apporteur` (parcours apport).

---

## Cas → documents (PRIORITÉ 1 — bloquant)

### Prompt 1 — Canon SPFPL faisant foi + parts vs actions (BLOQUANT)

```
Contexte : je construis un générateur de documents juridiques pour une SPFPL (Société de Participations Financières de Profession Libérale) de professionnels de santé (médecins, chirurgiens-dentistes). Une première version du tableau « Documents à générer par cas » contenait une section SPFPL complète, mais des versions ultérieures du même tableau ont SUPPRIMÉ toute la section SPFPL. Je dois savoir si la section SPFPL fait toujours foi.

Cette section SPFPL distinguait deux parcours :
- SPFPL « cession » : documents communs (déclaration sur l'honneur de non condamnation, autorisation de domiciliation, procuration), statuts SPFPL « cession », PV nomination gérant, demande d'inscription à l'ordre, note d'information ; si régime communautaire (lettre de renonciation, lettre d'avertissement au conjoint) ; PV d'agrément de cession (variante « associé unique » et variante « plusieurs associés ») ; acte de cession DE PARTS ; et une ligne « acte de cession D'ACTIONS » laissée sans modèle.
- SPFPL « apport » : mêmes documents communs et statuts SPFPL « apport », note d'information, régime communautaire ; puis contrat d'apport, attestation sur le capital / liste des souscripteurs, attestation de nomination du commissaire aux apports.

Questions :
1. Cette cartographie de cas et de documents SPFPL est-elle correcte et complète, ou manque-t-il / y a-t-il en trop des cas ou des documents ?
2. Une SPFPL est-elle juridiquement une société PAR ACTIONS (SAS, donc « actions », « président ») ou une société à responsabilité limitée (SARL, donc « parts sociales », « gérant ») ? Peut-elle être l'une OU l'autre selon le dossier, et qu'est-ce qui détermine la forme ?
3. Indépendamment de la forme de la SPFPL : l'opération porte sur des titres de la société sous-jacente (la SEL détenue). Ces titres sous-jacents sont-ils des « parts sociales » ou des « actions » selon que la SEL est une SELARL ou une SELAS ? C'est ce qui distingue « acte de cession de parts » et « acte de cession d'actions ».
Réponds avec les citations des sources.
```

### Prompt 2 — Existence de l'acte de cession d'actions SPFPL

```
Contexte : pour une SPFPL (Société de Participations Financières de Profession Libérale), je dispose d'un modèle « acte de cession de PARTS » de la société détenue, mais la cartographie des documents mentionne aussi un « acte de cession D'ACTIONS » sans modèle associé.

Question : existe-t-il un modèle de référence ou un wording-type pour un « acte de cession d'ACTIONS » dans le contexte d'une opération SPFPL (quand la société dont les titres sont cédés est une société par actions, ex. SELAS) ? Si oui, en quoi diffère-t-il de l'acte de cession de parts (vocabulaire « actions » vs « parts sociales », mentions de registre de mouvements de titres, ordre de mouvement, absence d'agrément des statuts, etc.) ? Si non, l'acte de cession de parts peut-il être adapté, et lesquelles de ses clauses doivent changer ?
Cite les sources.
```

### Prompt 3 — Variante PV d'agrément selon la forme de la société cible

```
Contexte : dans une opération SPFPL, la SPFPL devient associée d'une société d'exercice (SEL) déjà existante. Cette SEL doit agréer la SPFPL comme nouvelle associée. J'ai deux modèles de PV d'agrément, tous deux quand la SEL est une SELARL : un « SELARL à associé unique » (procès-verbal de l'associé unique) et un « SELARL à plusieurs associés » (procès-verbal d'AGE).

Questions :
1. Existe-t-il une variante de ce PV d'agrément lorsque la société cible est une SELAS (société par actions) au lieu d'une SELARL ? Le vocabulaire et l'organe compétent changent-ils (assemblée d'actionnaires, agrément du conseil/président, clause d'agrément des statuts d'une SAS) ?
2. Le PV d'agrément n'est-il requis que pour les cessions, ou aussi pour un apport de titres à la SPFPL ?
Réponds avec les citations.
```

---

## Wording exact par document (PRIORITÉ 2)

### Prompt 4 — Note d'information : wording cession vs apport (lever la double formule)

```
Contexte : la « note d'information » d'une SPFPL existe en deux parcours, cession et apport, mais le modèle source contient une double formulation non tranchée du type « la SPFPL a pour objet d'ACQUÉRIR / de RECEVOIR EN APPORT EN NATURE les titres de la société ». Je dois rendre une seule formulation par parcours.

Question : donne le wording EXACT de la note d'information de la SPFPL :
- variante « cession » (la SPFPL acquiert les titres de la société d'exercice) ;
- variante « apport » (les titres sont apportés en nature à la SPFPL).
Précise notamment : la phrase d'objet, la présentation de la SPFPL, la présentation de la société cible, et la phrase décrivant la décomposition du capital APRÈS opération (parts/actions restant au cédant/apporteur + part détenue par la SPFPL). Cite les sources.
```

### Prompt 5 — PV d'agrément : « cession » vs vocabulaire « apport » (incohérence source)

```
Contexte : deux modèles de PV s'appellent « PV SELARL agrément cession SPFPL » (variantes 1 associé et plusieurs associés) et sont classés comme documents de CESSION. Or leur texte interne emploie le vocabulaire de l'APPORT (« contrat d'apport », « parts apportées »).

Question : pour ce PV par lequel la SELARL agrée la SPFPL comme nouvelle associée, quel est le wording JURIDIQUEMENT correct selon le type d'opération ?
- Si l'opération réelle est une CESSION de parts à la SPFPL : faut-il dire « cession de parts » et « cessionnaire » plutôt que « apport » et « apportées » ? Donne les résolutions correctes (ordre du jour, résolutions, article 7 bis de répartition du capital).
- Si l'opération est un APPORT en nature : le vocabulaire d'apport est-il alors correct ?
Autrement dit : ce vocabulaire d'apport dans un PV nommé « cession » est-il une erreur à corriger, ou le même PV sert-il aux deux opérations avec un vocabulaire à adapter ? Cite les sources.
```

### Prompt 6 — Acte de cession de parts : origine de propriété, répartition, prix, coquille « cession d'action »

```
Contexte : modèle « acte de cession de parts » d'une SPFPL, par lequel un cédant (personne physique) cède à une SPFPL cessionnaire des parts de la société d'exercice (la SEL). Le modèle fige une répartition du capital sur trois personnes et contient, dans le bloc « frais », une mention isolée « cession d'action » alors que c'est un acte de cession de PARTS.

Questions :
1. Comment doit s'écrire l'« origine de propriété » des parts cédées (décrit-elle le CÉDANT — acquéreur/apporteur initial — et non l'acquéreur) ? Donne le wording type.
2. Le bloc « répartition actuelle du capital » doit être dynamique (1 à N associés). Donne la structure de phrase pour : un associé personne physique, un associé personne morale (autre société), et le total.
3. Quel est le wording correct du bloc « prix et modalités de paiement » (prix unitaire par part, prix total, en chiffres + en lettres) ?
4. La mention « cession d'action » dans le bloc frais est-elle une coquille à remplacer par « cession de parts » ?
Cite les sources.
```

### Prompt 7 — Contrat d'apport SEL → SPFPL : biens apportés, évaluation, rémunération, report d'imposition

```
Contexte : modèle « contrat d'apport » par lequel un apporteur apporte à la SPFPL bénéficiaire des titres d'une société d'exercice (SEL). Le modèle contient un jeton « parts sociales OU actions » et « président OU gérant », et il fige certaines entités pour l'évaluateur et le commissaire aux apports.

Question : donne le wording EXACT, par section, du contrat d'apport :
1. « Biens apportés » : description des titres apportés (nombre, plage de numéros, nature « parts sociales » ou « actions » selon la forme de la SEL).
2. « Évaluation de l'apport » : phrase d'évaluation et renvoi au rapport du commissaire aux apports.
3. « Rémunération de l'apport » : nombre et valeur des actions de la SPFPL remises en contrepartie.
4. « Option pour le report d'imposition » : wording de l'option (article 150-0 B ter ou équivalent).
5. « Conditions suspensives » : ordre professionnel, immatriculation.
Cite les sources.
```

### Prompt 8 — Statuts SPFPL : article Forme, article Objet, article Apports, article Capital

```
Contexte : statuts d'une SPFPL de professionnels de santé, forme « société par actions simplifiée ». Deux modèles existent : un parcours « cession » (constitution par apport en NUMÉRAIRE, capital exprimé en euros) et un parcours « apport » (constitution par apport en NATURE de titres d'une SELARL, capital calculé depuis la valeur des titres apportés). Le modèle « cession » fige la forme « SAS » ; le modèle « apport » paramètre la forme et ajoute les bases légales.

Question : donne le wording EXACT des articles structurants des statuts SPFPL, en distinguant cession et apport quand c'est nécessaire :
1. Article 1 — Forme (mention SAS + bases légales de la SPFPL d'exercice de profession de santé).
2. Article 2 — Objet (prise de participation et gestion de participations dans des SEL de la même profession).
3. Article 6 — Apports (numéraire pour cession ; apport en nature de titres pour apport, avec renvoi commissaire aux apports).
4. Article 8 — Capital social (cession : montant + nombre d'actions + valeur nominale ; apport : capital depuis le montant des apports en nature).
Cite les sources.
```

### Prompt 9 — Attestation capital / liste des souscripteurs + désignation du commissaire aux apports

```
Contexte : deux documents du parcours « apport » d'une SPFPL :
- « Attestation sur le capital / liste des souscripteurs » signée par le président : capital, nombre d'actions et valeur nominale, répartition, apports en nature, total des apports, apports en numéraire.
- « Acte de désignation d'un commissaire aux apports » : le modèle hard-code deux options de commissaire séparées par « OU ».

Questions :
1. Donne le wording EXACT de l'attestation sur le capital (en-tête SPFPL, corps de l'attestation par le président, lignes apports en nature / numéraire / total, certification finale).
2. Donne le wording EXACT de l'acte de désignation du commissaire aux apports (identification du soussigné, rappel de la constitution de la SPFPL, description de l'apport en nature, nomination, mission). Le rôle correct est-il bien « commissaire aux apports » (et non « commissaire aux comptes ») ?
Cite les sources.
```

---

## Genre / pluriel (PRIORITÉ 3 — transverse)

### Prompt 10 — Accords de genre pilotés par la civilité (SPFPL)

```
Contexte : dans les documents d'une SPFPL, la personne principale (cédant, apporteur, associé unique, président, souscripteur) et le conjoint peuvent être homme ou femme. Je veux une table d'accord de genre pilotée par la civilité, pour ne jamais laisser de forme « (e) » dans le document final.

Question : donne la forme masculine ET féminine correcte de chacun de ces termes tels qu'ils apparaissent dans des statuts / actes / PV / attestations :
soussigné(e), né(e) le, associé(e), associé(e) unique, président(e), apporteur / apporteuse, cédant(e), cessionnaire, souscripteur / souscriptrice, représentant(e). Précise aussi la forme correcte au féminin pour un médecin (« Docteur » / « Docteure ») et la formule devant la civilité dans une comparution (« Monsieur » / « Madame », avec ou sans article). Cite les sources.
```

---

## Multi (nombre d'associés) (PRIORITÉ 4)

### Prompt 11 — SPFPL multi-associés : statuts (comparution, apports, répartition, signatures)

```
Contexte : les modèles de statuts SPFPL dont je dispose sont à associé UNIQUE, mais une SPFPL peut compter de 1 à 6 associés. Je dois pouvoir générer des statuts à plusieurs associés à partir du même tronc.

Question : donne le wording EXACT des blocs qui changent quand la SPFPL a PLUSIEURS associés au lieu d'un seul :
1. Comparution (« LES SOUSSIGNÉS … ont décidé d'instituer » + un bloc d'identité par associé).
2. Article Apports (une ligne d'apport par associé + total des apports).
3. Article Capital / répartition des actions (« les actions sont réparties entre les associés comme suit » + tableau, en remplacement de l'attribution totale à l'associé unique).
4. Bloc de signatures (une signature par associé, mention manuscrite, ordre).
La pluralisation est-elle dérivable du modèle singulier, ou existe-t-il un modèle « SPFPL plusieurs associés » distinct avec des clauses propres (agrément entre associés, décisions collectives) ? Cite les sources.
```

### Prompt 12 — PV d'agrément « plusieurs associés » : présents/représentés, quorum, signatures

```
Contexte : PV d'agrément par lequel une SELARL « à plusieurs associés » (société d'exercice cible) agrée une SPFPL comme nouvelle associée, sous forme de procès-verbal d'AGE. La liste des associés présents ou représentés est dynamique (de 2 à 6 associés, personnes physiques et éventuellement personnes morales).

Question : donne le wording EXACT pour :
1. La liste des associés présents ou représentés (un bloc par associé, avec son nombre de parts), pour une personne physique ET pour une personne morale associée.
2. La phrase de quorum / totalité (« les associés présents ou représentés possèdent la totalité des parts… »).
3. Le bloc de signatures de tous les associés présents ou représentés.
Précise les accords singulier/pluriel à appliquer (l'associé / les associés, présent / présents). Cite les sources.
```
