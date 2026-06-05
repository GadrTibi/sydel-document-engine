# EURL — Prompts NotebookLM (prêts à envoyer)

> **Mode d'emploi.** Prompts à coller **tels quels** dans NotebookLM (corpus tokenisé + transcripts
> Albane). Une question précise par bloc. Ordre conseillé : Bloc 1 d'abord (il débloque tout le
> reste). **NotebookLM TOUJOURS avant Rafael** ; Claude ne contacte jamais Albane directement
> (cf. principe 2 du `WORKFLOW_TYPE_ENTREPRISE_V1.md`).
>
> **Question n°1 du dossier EURL :** il n'existe AUCUN modèle EURL sur le Drive et AUCUNE carte
> officielle cas→documents pour l'EURL (le canon est entièrement SELARL). C'est l'objet du Bloc 1.

---

## BLOC 1 — Existence du périmètre EURL, liste des cas, carte cas→documents (PRIORITÉ ABSOLUE)

**Prompt 1.1 — L'EURL fait-elle partie du périmètre Sydel ?**
> Dans le périmètre des dossiers traités par le cabinet, traitez-vous des dossiers de type **EURL**
> (Entreprise Unipersonnelle à Responsabilité Limitée) ? Si oui, pour quel public (professions de
> santé comme pour la SELARL, ou activité commerciale classique) et pour quelles opérations
> (création seule, apport/cession de fonds, transformation, autre) ? Répondez en distinguant
> clairement ce qui est effectivement pratiqué de ce qui ne l'est pas.

**Prompt 1.2 — Liste exhaustive des cas EURL.**
> Donnez la **liste exhaustive et nommée des cas** (sous-dossiers / situations) que vous gérez pour
> une EURL, comme il en existe pour la SELARL (création, régime communautaire, cession/apport de
> fonds, cession de parts de SCM, dérogation de site, etc.). Pour chaque cas EURL, indiquez s'il
> s'applique **toujours** ou **seulement sous condition** (laquelle).

**Prompt 1.3 — Carte officielle cas → documents (le livrable central).**
> Pour **chaque cas EURL** identifié, listez **tous les documents à générer**, dans l'ordre, avec
> leur **intitulé exact**. Indiquez pour chaque document : est-il **généré automatiquement** ou
> **rempli à la main** ? est-il **commun à tous les cas** ou **conditionnel** (à quelle condition) ?
> Format souhaité : un tableau `Cas | Document (intitulé exact) | Toujours/Conditionnel | Condition`.

**Prompt 1.4 — Différences EURL vs SELARL.**
> En quoi le dossier **EURL** diffère-t-il du dossier **SELARL** sur le plan des documents produits ?
> Quels documents SELARL **n'existent pas** pour l'EURL, et quels documents sont **spécifiques** à
> l'EURL (ex. option fiscale IR/IS, décision de l'associé unique) ?

---

## BLOC 2 — Modèles et variables par document

**Prompt 2.1 — Fourniture des modèles EURL.**
> Pour chaque document du dossier EURL, disposez-vous d'un **modèle Word tokenisé** (avec variables
> entre crochets `[...]`) équivalent aux modèles SELARL ? Si oui, lesquels et où les trouver ? Si non,
> quels documents existent seulement en version « à compléter à la main » ?

**Prompt 2.2 — Variables par document.**
> Pour chaque modèle EURL, listez les **variables** à renseigner (identité de l'associé unique,
> identité de la société, capital, gérance, fonds apporté/cédé, etc.) avec leur **libellé exact** tel
> qu'il doit apparaître dans le document. Signalez toute variable **spécifique à l'EURL** absente de
> la SELARL.

**Prompt 2.3 — Wording figé vs variable.**
> Pour chaque document EURL, quels passages sont **figés** (texte juridique invariable) et quels
> passages sont **variables** (dépendant des données du dossier) ? En particulier : durée de la
> société, objet social, clause de gérance, clause d'option fiscale.

---

## BLOC 3 — Genre et nombre (couches transverses)

**Prompt 3.1 — Genre de l'associé unique / gérant.**
> Dans les documents EURL, les formulations doivent-elles s'accorder au **genre** de l'associé unique
> et du gérant (« l'associé unique » / « l'associée unique », « le gérant » / « la gérante »,
> « le Docteur » / « la Docteure ») ? Donnez les **paires de formulations exactes** (masculin /
> féminin) à utiliser, document par document.

**Prompt 3.2 — Unipersonnel = singulier.**
> L'EURL étant **unipersonnelle** (un seul associé), confirmez que toutes les formulations doivent
> rester au **singulier** (« l'associé unique décide », et non « les associés décident »). Existe-t-il
> des passages où un pluriel subsiste malgré tout (ex. modèle dérivé d'une structure pluripersonnelle) ?

---

## BLOC 4 — Points ambigus à trancher

**Prompt 4.1 — Profession de santé ou commercial.**
> L'EURL traitée par le cabinet concerne-t-elle des **professions de santé** (et donc inscription à
> l'Ordre, dérogations de site, etc.) ou une **activité commerciale** ordinaire ? Cette réponse
> conditionne toute la liste de documents.

**Prompt 4.2 — Option fiscale IR / IS.**
> Pour une EURL, le choix entre **IR (par défaut)** et **option IS** déclenche-t-il un document
> spécifique (lettre d'option à l'IS) ? Est-ce un cas systématique, optionnel, ou hors périmètre ?

**Prompt 4.3 — Gérance.**
> Dans une EURL Sydel, le gérant est-il **toujours l'associé unique** ou peut-il être un **tiers** ?
> Cela change-t-il les documents (PV/décision de nomination, acceptation des fonctions) ?

**Prompt 4.4 — Durée de la société.**
> Quelle est la **durée** inscrite dans les statuts d'une EURL (99 ans comme pour la SELARL, ou
> autre) ? Ne pas confondre avec la durée de la **domiciliation** (« indéterminée »). Confirmez la
> valeur exacte.

---

## Pack de passation Rafael (à n'envoyer qu'après NotebookLM)

À remplir **après** avoir épuisé NotebookLM. Ne transmettre à Rafael (via Gad) que les points
**restés sans réponse ou contradictoires** dans NotebookLM. Le tout premier point à faire trancher
si NotebookLM ne suffit pas : **« Sydel traite-t-elle réellement des EURL, et si oui, fournir les
modèles + la carte cas→documents »** (sans cela, la fondation EURL ne peut pas démarrer).
