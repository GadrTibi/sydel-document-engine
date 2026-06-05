# SAS — Prompts NotebookLM prêts à envoyer (V1)

> **Date :** 2026-06-05 · **Objet :** obtenir, pour le type **SAS**, ce que le canon ne fournit PAS :
> la **liste des cas** et la **carte cas → documents**, puis confirmer variables / wording / genre / pluriel.
> **Pourquoi c'est critique :** `Documents_a_generer_par_cas_V3.docx` est **100 % SELARL** (0 occurrence
> SAS / SASU / SPFPL). Il n'existe **aucune carte officielle cas → documents pour la SAS**. Tout
> regroupement actuel (y compris dans le code Codex) est **inféré, non ratifié**.
>
> **Mode d'emploi :** copier-coller chaque prompt **tel quel** dans le NotebookLM Sydel (corpus tokenisé
> + transcripts Albane). Un prompt = une question précise. **NotebookLM TOUJOURS avant Rafael.** Ce qui
> reste sans réponse après NotebookLM part dans un message Rafael (cf. bloc D et STATUT.md).
>
> **Garde-fou :** ne rien reformuler, ne pas inventer de cas ni de wording. Si NotebookLM répond « non
> présent dans les sources », ne pas combler — c'est précisément ce qu'il faut faire confirmer à Rafael.

---

## BLOC A — Liste des cas SAS + carte cas → documents (LE point n°1)

**A1 — Existence et périmètre du type SAS**
```
Dans le corpus Sydel, le document « Documents à générer par cas » décrit les cas et les documents pour la SELARL. Existe-t-il, dans les sources, une description équivalente pour la SAS (Société par Actions Simplifiée) ou la SASU ? Si oui, cite la source exacte. Si non, dis-le explicitement. Pour quels usages concrets le cabinet utilise-t-il une SAS plutôt qu'une SELARL (par exemple SPFPL holding, autre) ? Réponds uniquement à partir des sources, sans rien inventer.
```

**A2 — Liste exhaustive des cas SAS**
```
Pour une création en SAS chez Sydel, quelle est la liste EXHAUSTIVE des cas / situations qui déclenchent des documents différents (par analogie avec la SELARL : « dans tous les cas », statuts par profession, régime matrimonial/communauté, cession, SCM, dérogation, site distinct, etc.) ? Pour chaque cas, indique s'il s'applique à la SAS, et s'il est attesté par une source. Si un cas SELARL n'a pas d'équivalent en SAS, dis-le. N'invente aucun cas.
```

**A3 — Carte cas → documents pour la SAS**
```
Construis la carte « cas → documents » pour la SAS, sur le même modèle que « Documents à générer par cas » de la SELARL : pour chaque cas, liste les documents à générer avec le nom exact du fichier modèle (.docx) quand il existe dans les sources. Pour chaque document, précise s'il est systématique (« dans tous les cas ») ou conditionnel (et à quelle condition). Si un document est attendu mais n'a pas de modèle source, signale-le comme « modèle manquant ». Ne génère aucun wording ; uniquement la cartographie.
```

**A4 — Périmètre profession et forme (médecin uniquement ?)**
```
Le seul modèle de statuts SAS du corpus est « STATUTS SAS SPFPL médecins ». Le type SAS chez Sydel est-il limité aux médecins, ou existe-t-il aussi des SAS pour pharmaciens, chirurgiens-dentistes, ou d'autres professions ? Existe-t-il une SAS « d'exercice » (SELAS) distincte de la SAS « holding » (SPFPL) ? Précise, source à l'appui, quelles formes/professions le cabinet traite réellement en SAS.
```

**A5 — Cas actionnaire unique (SASU) vs pluripersonnel**
```
La SAS traitée par Sydel est-elle majoritairement unipersonnelle (SASU, actionnaire unique) ou pluripersonnelle ? Le document « statuts SASU Holding » du corpus fait-il partie du type SAS, ou d'un montage holding distinct ? Si la SAS peut avoir plusieurs actionnaires, quels documents/sections changent (gouvernance, président, répartition du capital en actions) ? Réponds à partir des sources uniquement.
```

---

## BLOC B — Confirmation des variables et du wording par modèle

> Pour chaque modèle, NotebookLM doit confirmer le rôle exact des tokens et signaler tout token
> ambigu, manquant ou en doublon. Liste des tokens établie par lecture du contenu des `.docx`.

**B1 — Statuts SAS / SPFPL médecins**
```
Pour le modèle « STATUTS SAS SPFPL médecins », confirme le rôle de chacune de ces variables et signale toute ambiguïté ou mention spécifique à une profession qui ne devrait pas y figurer : [denomination_societe], [capital_social], [capital_lettres], [adresse_siege], [civilite], [prenom], [nom], [date_naissance], [ville_naissance], [departement_naissance], [nationalite], [adresse_personnelle], [qualification_principale], [numero_ordre], [numero_rpps], [ordre_departemental], [nb_actions], [nb_actions_lettres], [valeur_nominale_action], [valeur_nominale_action_lettres], [nom_banque], [debut_exercice], [fin_exercice], [date_cloture_exercice_1], [situation_maritale], [regime_matrimonial], [civilite_conjoint], [prenom_conjoint], [nom_conjoint], [lieu_signature]. La durée de la société dans ces statuts SAS est-elle figée (et à quelle valeur) ou variable ? Réponds à partir des sources.
```

**B2 — PV rémunération du président**
```
Pour le modèle « PV rémunération président » d'une SAS, confirme le rôle de : [civilite], [prenom], [nom], [num_voie_perso], [voie_perso], [ville_perso], [cp_perso], [qualite_associe], [fonction_dirigeant], [denomination_societe], [date_cloture_exercice_1], [lieu_signature], [date_signature]. Ce PV acte-t-il systématiquement une ABSENCE de rémunération du président jusqu'à la clôture du premier exercice, ou la rémunération est-elle variable ? Y a-t-il aussi un PV de NOMINATION du président distinct de ce PV de rémunération ?
```

**B3 — Liste des souscripteurs : deux variantes**
```
Le corpus SAS contient deux versions de « Liste des souscripteurs » : une version courte (tokens [denomination_societe], [nb_actions], [montant_sous], [nom], [prenom], [lieu_signature], [date_signature]) et une version enrichie SPFPL (ajoutant [forme_sociale], [profession_reglementee], [capital_social], [adresse_siege], [adresse_personnelle], [civilite], [signature]). Laquelle est la version de référence ? Sont-ce deux documents distincts ou deux états d'un même document ? Lequel faut-il générer, et dans quel cas ?
```

**B4 — Attestation sur le capital (modèle introuvable)**
```
Le code Sydel référence un document « Attestation sur le capital - apport - liste des souscripteurs » pour la SAS, mais aucun fichier .docx de ce nom n'existe dans le dossier « Création SAS » du corpus. Ce document existe-t-il bien pour la SAS ? Est-il distinct de la « Liste des souscripteurs », ou s'agit-il du même document sous un autre nom ? Si distinct, où se trouve son modèle ? Réponds à partir des sources, sans le reconstituer.
```

**B5 — Documents « dans tous les cas » (DNC, domiciliation, procuration)**
```
Pour la SAS, les modèles « Déclaration sur l'honneur de non condamnation », « Autorisation de domiciliation » et « Procuration » sont-ils identiques à ceux de la SELARL, ou comportent-ils des spécificités SAS (mention « président » au lieu de « gérant », forme par actions) ? Confirme que ces trois documents sont bien « dans tous les cas » pour une création SAS. Dans l'autorisation de domiciliation, la durée est-elle bien « indéterminée » ?
```

---

## BLOC C — Genre et pluriel (couches transverses)

**C1 — Accord de genre (président / présidente)**
```
Dans les documents SAS, quelles formulations exactes changent selon le genre du dirigeant et des associés ? Donne les PAIRES de chaînes exactes à substituer (par exemple « le Président » / « la Présidente », « né le » / « née le », « soussigné » / « soussignée », « l'associé unique » / « l'associée unique »), document par document. Ne propose pas de règle de terminaison automatique (-é/-ée) : uniquement des paires de chaînes attestées dans les modèles.
```

**C2 — Genre par personne**
```
Dans une SAS, certaines mentions de civilité ou de titre dépendent-elles du genre d'une personne précise (le président, un actionnaire donné) plutôt que d'un genre global du dossier ? Précise, document par document, quelle personne détermine chaque accord de genre.
```

**C3 — Pluriel / nombre (actionnaire unique vs plusieurs)**
```
Pour la SAS, quelles parties exactes des documents passent du singulier au pluriel quand il y a plusieurs actionnaires au lieu d'un actionnaire unique (comparution, apports, répartition du capital en actions, signatures) ? Donne les passages concernés. Cette pluralisation doit-elle être validée par Albane avant mise en œuvre ?
```

---

## BLOC D — Points ambigus à lever (sinon → message Rafael)

**D1 — Synthèse des manques**
```
Pour la SAS, récapitule tout ce qui n'est PAS attesté par les sources et qui resterait à clarifier : cas sans documents, documents sans modèle, variables ambiguës, choix entre variantes. Présente-le comme une liste de questions ouvertes hiérarchisées (bloquant / important / confort), pour transmission au juriste référent.
```

**D2 — Cas cession / régime communautaire en SAS**
```
La SAS chez Sydel donne-t-elle lieu à un cas de cession (d'actions) et/ou à un cas de régime communautaire (renonciation du conjoint à la qualité d'associé / actionnaire), comme la SELARL ? Si oui, quels documents et quels modèles ? Si ces cas n'existent pas pour la SAS, confirme-le explicitement.
```

**D3 — Vocabulaire d'interface SAS**
```
Pour l'interface logicielle, quels termes employer pour la SAS : « actionnaire » plutôt qu'« associé », « actions » plutôt que « parts », « président » plutôt que « gérant », « actionnaire unique » plutôt qu'« associé unique » ? Confirme les libellés attendus par les juristes pour la SAS, en signalant tout terme à éviter.
```

---

## Si NotebookLM ne sait pas → message Rafael (à préparer, ne pas envoyer sans Gad)

Les questions restées sans réponse côté NotebookLM (typiquement A1/A3/A4, B4, et tout le bloc D) sont à
regrouper dans un message destiné à **Rafael** (jamais une question métier au PM). Être **certain** que
la réponse n'est pas déjà dans les sources avant de faire relayer. Voir `STATUT.md` § Pack de passation.
