# SPFPL — Prompts NotebookLM (prêts à envoyer)

> Ordre d'escalade : **sources tokenisées → NotebookLM → message Rafael** (NotebookLM TOUJOURS avant
> Rafael ; ne jamais poser de question métier au PM). Copier-coller chaque prompt **tel quel** dans
> NotebookLM (corpus : transcripts Albane + docs sources tokenisés). Une question = un bloc.
> Numérotation stable : `SPFPL-NLM-xx`. Les réponses retournent dans `STATUT.md` puis le journal de décisions.

---

## BLOC A — Liste des cas + carte cas → documents (QUESTION N°1, BLOQUANTE)

**SPFPL-NLM-01**
> Pour le type de société **SPFPL** (Société de Participations Financières de Professions Libérales) chez
> Sydel : quelle est la **liste exhaustive et officielle des CAS** (opérations) que l'on traite ? Le
> document de référence « Documents à générer par cas » liste, dans sa version la plus ancienne, deux cas :
> « SPFPL cession » et « SPFPL apport ». Confirme : est-ce bien la liste complète, ou existe-t-il d'autres
> cas (par ex. une création « pure », ou une opération mixte « cession + apport ») ?

**SPFPL-NLM-02**
> Les versions récentes du tableau « Documents à générer par cas » (V2, V3) ne contiennent **plus** de
> section SPFPL, alors que la version d'origine en avait une. Est-ce **volontaire** (la SPFPL a-t-elle
> été retirée du périmètre Sydel ?) ou est-ce un oubli ? Quelle version fait **autorité** aujourd'hui
> pour la SPFPL ?

**SPFPL-NLM-03**
> Pour CHAQUE cas SPFPL confirmé, donne la **liste exacte des documents à générer**, dans l'ordre, en
> distinguant : (a) les documents générés dans **tous les cas**, (b) les documents conditionnels et leur
> **condition** (ex. « si régime communautaire », « si associé unique » vs « si plusieurs associés »,
> « si cession de parts » vs « si cession d'actions »). Indique pour chacun le **nom du modèle** Word
> correspondant.

---

## BLOC B — Forme sociale & nature des titres (structurant)

**SPFPL-NLM-04**
> La SPFPL chez Sydel est-elle constituée sous forme de **SARL** (titres = parts sociales), de **SAS**
> (titres = actions), ou **les deux selon le dossier** ? Nos modèles mélangent les deux : un « acte de
> cession de **parts** » et des « statuts SAS SPFPL » avec un champ « nombre d'**actions** ». Quelle est
> la règle ?

**SPFPL-NLM-05**
> Existe-t-il des modèles de statuts SPFPL **par profession** (nous avons : dentistes en « SPFPL-AS »,
> médecins en « SAS SPFPL », pharmaciens en « SAS SPFPL ») ? La profession est-elle une simple
> **variable** dans un modèle unique, ou faut-il un **modèle distinct par profession** ? Quelles
> professions sont dans le périmètre SPFPL ?

---

## BLOC C — Documents « hors carte » à rattacher ou exclure

**SPFPL-NLM-06**
> Les documents suivants existent dans le dossier SPFPL mais ne figurent PAS dans la carte cas→documents :
> « **Liste des souscripteurs** », « **Appel des fonds** », « **RM Sydel** » (fiche patrimoniale :
> revenus, IFI, objectifs client), « **PV d'autorisation d'emprunt** ». Pour chacun : doit-il être
> **généré** par le moteur, dans **quel cas**, et sous **quelle condition** ? Le « RM Sydel » est-il un
> document de conseil interne (hors chaîne d'actes) ?

**SPFPL-NLM-07**
> La carte d'origine cite un « **Acte de cession d'actions** » pour la SPFPL **sans** nommer de modèle.
> Le modèle `Acte_cession_SPFPL_tiers_modele.doc` correspond-il à cet acte de cession d'actions (par
> opposition à l'acte de cession de **parts** `..._tiers_part_modele`) ? Confirme le bon appariement
> document ↔ condition (cession de parts vs cession d'actions).

**SPFPL-NLM-08**
> Y a-t-il bien un **PV de nomination du gérant** propre à la SPFPL ? La carte le réclame, mais nous
> n'avons pas trouvé de modèle SPFPL tokenisé dédié. Faut-il **réutiliser** un PV de nomination générique,
> ou existe-t-il un modèle SPFPL spécifique à fournir ?

---

## BLOC D — Variantes de contenu (quel modèle est canonique)

**SPFPL-NLM-09**
> Plusieurs documents SPFPL existent en **plusieurs variantes de contenu** très proches. Pour chaque
> couple, lequel est le **modèle officiel à utiliser** ?
> - « Note d'information » : 3 variantes.
> - « Attestation sur le capital - apport » : 3 variantes ; « ... - cession » : 2 variantes.
> - « Contrat d'apport SEL SPFPL » : version simple vs version avec commissaires aux apports + évaluateur.
> - « Attestation nomination commissaire aux apports » : 1 commissaire vs 2.
> - « Autorisation de domiciliation » : version courte vs détaillée.

**SPFPL-NLM-10**
> Pour le **commissaire aux apports** dans l'apport SPFPL : est-il **obligatoire** dans tous les apports,
> ou seulement au-dessus d'un seuil ? Le contrat d'apport doit-il prévoir 0, 1 ou plusieurs commissaires
> de façon paramétrable ?

---

## BLOC E — Genre / pluriel / nombre d'associés

**SPFPL-NLM-11**
> Pour les documents SPFPL, quelles formulations varient selon le **genre** de la personne (ex. « le
> Docteur » / « la Docteure », accords masculin/féminin) ? Donne les **paires de chaînes exactes** à
> substituer, et précise si la préférence est **par personne** (et non universelle).

**SPFPL-NLM-12**
> La SPFPL peut compter de **1 à 6 associés**. Quels passages des **statuts** (et autres documents)
> changent selon le nombre d'associés (en-tête « le soussigné »/« les soussignés », apports, répartition,
> signatures) ? Le pluriel doit-il être traité maintenant, ou attendre une validation dédiée ?

---

## BLOC F — Points ambigus / pièges (vérification anti-coquille)

**SPFPL-NLM-13**
> Y a-t-il des **coquilles inter-profession** connues dans les modèles SPFPL (ex. une mention « cabinet
> dentaire » qui apparaîtrait dans un document destiné aux médecins, ou inversement) ? Lesquelles purger ?

**SPFPL-NLM-14**
> Quelle est la **durée** correcte (a) de la **société SPFPL** dans les statuts, et (b) de la
> **domiciliation** ? (Sur la SELARL, durée société = 99 ans figée, durée domiciliation = « indéterminée » —
> confirme les valeurs pour la SPFPL pour ne pas les confondre.)

**SPFPL-NLM-15**
> Dans l'**acte de cession SPFPL** et le **compromis de cession de cabinet**, l'« origine de propriété »
> doit-elle décrire le **vendeur/cédant** (et non l'acquéreur) ? Confirme la règle, comme pour la SELARL.
