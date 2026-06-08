# Prompts NotebookLM — REDESIGN V3 (tous types V1)

> **Date :** 2026-06-08 · **Remplace** les `NOTEBOOKLM_PROMPTS_V2.md` par type, **jugés mauvais par
> Rafael** (« pas de bonnes questions / c'est dans les docs / trop technique »).
>
> **Pourquoi V3 est différent.** Les V2 demandaient à NotebookLM (a) **le wording des modèles**
> (durée figée ? bloc conjoint ? liste souscripteurs A/B ?) → c'est dans les `.docx`, on l'extrait ;
> (b) **la carte cas→documents** → elle est dans le canon « Documents à générer par cas » V1 ;
> (c) des **décisions de périmètre produit** → ça revient au PM, pas à NotebookLM. D'où le rejet.
>
> **Doctrine V3 — on ne demande à NotebookLM QUE ce qu'Albane (la juriste) sait et qu'aucun modèle
> ni le canon ne porte** : l'**usage/montage réel**, les **règles légales/ordinales non écrites**, la
> **logique de décision** (pourquoi tel choix, pièges), les **conditions concrètes des cas**
> conditionnels (le *quand/pourquoi*, pas le *quoi écrire*), et le **genre/nombre comme règle métier**.
>
> **Mode d'emploi.** Coller **un prompt à la fois** dans le NotebookLM Sydel (ou relayer à Rafael).
> Chaque prompt finit par « si ce n'est pas dans les sources, dis-le » : **ce que NotebookLM ne porte
> pas = ce qui partira, groupé, à Rafael** (jamais une question au PM). Ne rien reformuler au retour :
> capture brute, puis je range dans le canon.
>
> **Périmètre :** CRÉATION uniquement. **SCP exclue** (parquée hors V1, décision Rafael) — on ne pose
> rien pour elle ; à rouvrir seulement si tu décides de la réintégrer.

---

## SELAS

**1. Quand une SELAS plutôt qu'une SELARL ?** · [usage]
```
Dans quelles situations concrètes le cabinet oriente-t-il un praticien vers une SELAS plutôt que vers une SELARL ? Quels signaux client (nombre d'associés visé, entrée d'investisseurs, projet de holding, sortie future) déclenchent ce choix ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Montage type SELAS + holding/SCI/SCM** · [usage]
```
Comment s'articule en pratique une SELAS avec une SPFPL, une SCM ou une SCI dans un montage réel de cabinet ? Qui détient quoi, dans quel ordre crée-t-on les structures, et à quoi sert chaque étage ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Détention du capital par des extérieurs — contraintes ordinales réelles** · [règle légale]
```
Au-delà du texte des statuts, quelles contraintes l'Ordre fait-il réellement respecter sur la détention du capital d'une SELAS par des personnes ou sociétés non exerçantes ? Y a-t-il des refus, des seuils surveillés ou des montages que l'Ordre rejette en pratique ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Conséquences du choix « Président » de SELAS** · [logique]
```
Quelles conséquences concrètes (statut social, fiscalité, responsabilité, gouvernance) le cabinet explique-t-il au client du fait que la SELAS est dirigée par un Président plutôt que par un gérant ? Quels arbitrages cela ouvre-t-il pour le praticien ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Pièges fréquents signalés par le cabinet sur la SELAS** · [logique]
```
Quelles erreurs ou difficultés récurrentes Albane signale-t-elle lors de la constitution d'une SELAS (répartition capital/droits de vote, actions de préférence, associé non exerçant) ? Que faut-il vérifier avant de constituer ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Quand nomme-t-on un Directeur Général** · [condition cas]
```
Dans quelles situations concrètes une SELAS se dote-t-elle d'un Directeur Général en plus du Président ? Qu'est-ce qui, côté client, justifie ce choix, et y a-t-il des contraintes ordinales sur qui peut être DG ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Quand le régime communautaire déclenche les lettres au conjoint** · [condition cas]
```
Concrètement, dans quels cas le régime matrimonial d'un associé de SELAS impose-t-il la renonciation ou l'avertissement du conjoint ? Comment identifie-t-on que le cas s'applique, et le conjoint peut-il revendiquer la qualité d'associé ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**8. Quand un associé personne morale entre au capital** · [condition cas]
```
Dans quelles situations réelles un associé personne morale (holding, micro-holding civile) entre-t-il au capital d'une SELAS à la création, et quelles vérifications ou pièces le cabinet demande-t-il alors en plus par rapport à un associé personne physique ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**9. Règle de genre du dirigeant et du titre professionnel** · [genre-nombre]
```
Comment féminise-t-on le titre du dirigeant (Directeur Général / Directrice Générale) et le titre professionnel (« le Docteur ») dans les actes d'une SELAS, et qui — quelle donnée — détermine la variante retenue ? Existe-t-il des termes qui ne se féminisent pas par convention du cabinet ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## SPFPL

**1. Pourquoi un praticien monte une SPFPL holding — déclencheur réel** · [usage]
```
Dans quelles situations concrètes un chirurgien-dentiste ou médecin décide-t-il de créer une SPFPL pour détenir les titres de sa SEL plutôt que de les détenir en direct ? Quel problème patrimonial, fiscal ou de transmission cela résout-il en pratique ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Cession de titres vs apport de titres — comment Albane choisit** · [logique]
```
Pour constituer une SPFPL, comment un praticien arbitre-t-il en pratique entre faire CÉDER ses titres de SEL à la holding (contre numéraire) et les APPORTER (apport en nature) ? Quels critères de la situation du client font pencher pour l'un ou l'autre, et quelles conséquences concrètes en découlent ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Report d'imposition 150-0 B ter — règle et conditions de déclenchement** · [règle légale]
```
Dans quels cas le report (ou sursis) d'imposition de l'article 150-0 B ter s'applique-t-il lors de la création d'une SPFPL par apport, et à quelles conditions concrètes le praticien en bénéficie-t-il ou le perd-il (durée de conservation, réinvestissement, etc.) ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Qui peut détenir le capital d'une SPFPL — règle ordinale en pratique** · [règle légale]
```
Au-delà du texte, comment se vérifie concrètement la détention du capital d'une SPFPL (la majorité aux professionnels en exercice, le complément possible) : qui l'Ordre accepte comme associé non-exerçant, et quels seuils ou délais l'Ordre contrôle-t-il réellement à l'inscription ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Commissaire aux apports — quand il est réellement exigé** · [condition cas]
```
Pour la création d'une SPFPL par apport de titres de SEL, le commissaire aux apports est-il toujours obligatoire, ou existe-t-il des seuils/dispenses qui le rendent facultatif ? Qui le désigne et à quel moment du montage intervient-il ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Agrément de la SEL : pourquoi associé unique vs plusieurs** · [condition cas]
```
Pour la création d'une SPFPL, qu'est-ce qui, dans la situation réelle de la SEL cible, déclenche le cas « associé unique » plutôt que « plusieurs associés » au niveau du PV d'agrément de la SEL ? Pourquoi cette distinction existe-t-elle (et non comment l'écrire) ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Articulation SPFPL → SEL (et le cas SCI/SCM) — montage réel** · [usage]
```
Comment s'articule en pratique une SPFPL avec la ou les SEL qu'elle détient, et la holding peut-elle aussi détenir des parts de SCI ou de SCM dans le même montage ? Qu'est-ce qui est usuel ou au contraire à éviter selon Albane ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**8. Régime communautaire — quand la renonciation du conjoint est nécessaire** · [condition cas]
```
Lors de la création d'une SPFPL, dans quelles situations le régime matrimonial du praticien déclenche-t-il l'avertissement et/ou la renonciation du conjoint, et le déclencheur diffère-t-il entre le parcours cession (numéraire) et le parcours apport (titres) ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**9. Pièges signalés par Albane sur la création d'une SPFPL** · [logique]
```
Quels sont les pièges ou erreurs récurrentes qu'Albane signale spécifiquement sur la création d'une SPFPL (confusion vocabulaire cession/apport, valorisation des titres apportés, délais ordinaux, détention du capital) et comment les éviter ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## SCM

**1. À quoi sert une SCM et ce qu'elle met (ou non) en commun** · [usage]
```
Concrètement, à quoi sert une société civile de moyens dans la pratique d'Albane, qu'est-ce qu'elle met en commun et qu'est-ce qu'elle ne met PAS en commun (honoraires, patientèle, exercice) ? Comment s'articule-t-elle avec les sociétés d'exercice (SEL) des praticiens membres ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Qui sont les associés d'une SCM dans le montage type** · [usage]
```
Dans le montage habituel d'Albane, qui devient associé de la SCM : les praticiens en personne physique, ou leurs sociétés d'exercice (SELARL/SELAS) ? Y a-t-il un cas où l'on mélange personnes physiques et SEL associées, et pourquoi ce choix ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Inscription / information de l'Ordre pour une SCM** · [règle légale]
```
Une SCM (qui n'est pas une structure d'exercice) doit-elle être inscrite à l'Ordre, ou seulement l'en informer, et à quel moment ? Quelle est l'obligation réelle vis-à-vis du conseil de l'Ordre à la constitution ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Moment de production des satellites (pacte, frais communs, RI, liste des dépenses)** · [condition cas]
```
Le pacte d'associés, le contrat de frais communs, le règlement intérieur et la liste des dépenses communes se signent-ils EN MÊME TEMPS que la constitution de la SCM (avec les statuts), ou APRÈS l'immatriculation comme opérations séparées ? Quelle est la pratique d'Albane sur leur enchaînement ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Entre qui se signent le contrat de frais communs et le règlement intérieur** · [condition cas]
```
Le contrat d'exercice à frais communs et le règlement intérieur de la SCM se concluent-ils entre les SOCIÉTÉS d'exercice (les SEL des praticiens) ou entre les PERSONNES PHYSIQUES (les praticiens eux-mêmes) ? Si la réponse diffère selon le document, précise pour chacun. Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Quelle clé de répartition des dépenses communes Albane recommande** · [logique]
```
Entre une répartition au prorata du temps d'occupation des salles, au prorata des parts de SCM, ou au prorata du nombre de patients, laquelle Albane recommande-t-elle en pratique, et dans quels cas l'une plutôt que l'autre ? Quels sont les pièges d'une mauvaise clé ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Logique du seuil de dépense commune et des décisions à l'unanimité** · [logique]
```
Comment fixe-t-on en pratique le seuil au-delà duquel une dépense commune exige l'accord de tous les associés, et que conseille Albane sur le niveau de ce seuil et sur les décisions soumises à l'unanimité ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**8. Statut juridique des locaux et du bail dans une SCM** · [règle légale]
```
Dans le montage d'Albane, le bail des locaux est-il établi au nom de la SCM, au nom des praticiens, ou de leurs SEL ? Quelles sont les obligations qui en découlent entre associés quant à l'usage et au partage des locaux ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**9. Genre et nombre comme règle métier pour la SCM** · [genre-nombre]
```
Pour une SCM, comment doit-on accorder en genre et en nombre selon le profil des associés : « gérant/gérante », « co-gérants », « associé/associée », « Le Docteur/La Docteure », et le passage au pluriel quand il y a plusieurs associés ou plusieurs gérants ? Y a-t-il une règle d'accord propre que vous appliquez systématiquement ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## SCI / SCI IRIS

**1. À quoi sert une SCI dans les montages des praticiens** · [usage]
```
Dans les montages que vous voyez, à quoi sert concrètement une SCI pour un praticien de santé : détention des murs du cabinet, patrimoine privé, autre ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Ce qui fait une « SCI IRIS » plutôt qu'une SCI classique** · [IRIS]
```
Du point de vue du montage, qu'est-ce qui caractérise une SCI IRIS par rapport à une SCI standard, et dans quelle situation un praticien choisit l'une plutôt que l'autre ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Décorrélation droits de vote / droits financiers — pourquoi** · [logique]
```
Pourquoi, dans une SCI IRIS, dissocie-t-on les droits financiers des droits de vote (« 1 % des parts ≠ 1 % du résultat ») : quel objectif patrimonial ou fiscal cela sert-il pour le praticien ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Option IS vs IR pour une SCI — quand et pourquoi** · [règle légale]
```
Quand un praticien a-t-il intérêt à opter pour l'IS plutôt que de rester à l'IR sur sa SCI, et quelles conséquences cette option entraîne-t-elle pour lui ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Cas réel d'une personne morale associée d'une SCI** · [condition cas]
```
Dans quels cas concrets une société (SEL, SPFPL, micro-holding) devient-elle associée d'une SCI, et qu'est-ce que ce montage permet d'atteindre ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Articulation SCI → micro-holding → SPFPL** · [montage]
```
Comment s'articulent une SCI, une micro-holding et une SPFPL dans un même montage : qui détient qui, et dans quel sens circule l'argent vers le projet immobilier du praticien ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Pourquoi un capital variable en SCI** · [logique]
```
Pourquoi retient-on un capital variable plutôt que fixe pour ces SCI, et qu'est-ce que ça change en pratique quand un associé entre ou sort ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**8. Pièges qu'Albane signale sur les SCI** · [logique]
```
Quels pièges ou erreurs Albane signale-t-elle à éviter lors de la création d'une SCI (notamment IRIS) pour un praticien ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**9. Numérotation des parts en IRIS — à quoi elle sert** · [IRIS]
```
À quoi sert concrètement la numérotation précise des parts par groupes dans une SCI IRIS, et que permet-elle de piloter dans la répartition du résultat ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## SCS

**1. Usage réel et variantes du montage SCS** · [usage]
```
Au-delà du montage type (commandité = praticien gestionnaire, commanditaire = SPFPL investisseuse, pour de l'immobilier patrimonial), quelles autres situations réelles conduisent Sydel à créer une SCS plutôt qu'une autre société civile ? Décris les variantes de montage rencontrées en pratique et à quoi elles servent. Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Logique de choix SCS vs SCI et pièges à éviter** · [logique]
```
Pour un projet patrimonial / immobilier, sur quels critères de décision Sydel oriente-t-il un client vers une SCS plutôt que vers une SCI ? Quels sont les pièges ou les erreurs à éviter qui justifient de préférer l'une à l'autre ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Règle de répartition des apports et des parts entre commandité et commanditaire** · [condition-multi]
```
Dans une SCS, la répartition des apports et du nombre de parts entre l'associé commandité et l'associé commanditaire suit-elle une règle (par exemple un plancher ou un type de parts réservé au commandité), ou est-ce un choix libre fixé au cas par cas selon le dossier ? Je ne demande pas la formulation des statuts, mais la règle métier qui gouverne ce partage. Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Règle de décorrélation droits de vote / droits financiers** · [règle légale]
```
Dans une SCS, la décorrélation entre droits de vote et droits financiers (« 1 % des parts ne donne pas forcément droit à 1 % du résultat ») est-elle une liberté contractuelle laissée au choix des associés, ou répond-elle à une règle ou une contrainte (par exemple le commandité gestionnaire doit conserver la majorité des droits de vote) ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Règle en présence de plusieurs commanditaires** · [condition-multi]
```
Une SCS créée par Sydel comporte-t-elle, en pratique, plusieurs associés commanditaires (et/ou plusieurs commandités), ou reste-t-elle quasi toujours sur un commandité + un commanditaire ? S'il y a plusieurs commanditaires, quelles règles métier s'appliquent à eux (apports, parts, droits) par rapport au cas à un seul commanditaire ? Je cherche la règle, pas la rédaction. Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Règle quand le commanditaire est une personne morale (SPFPL)** · [règle légale]
```
Quand l'associé commanditaire d'une SCS est une personne morale (souvent la SPFPL), cela change-t-il les règles applicables par rapport à un commanditaire personne physique : une personne morale peut-elle aussi être commanditée, sachant que le commandité a la qualité de commerçant et une responsabilité indéfinie et solidaire ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Accord en genre et en nombre du rôle statutaire** · [genre-nombre]
```
Pour les rôles statutaires d'une SCS, confirme les règles d'accord en genre et en nombre : « commandité » devient-il « commanditée » au féminin et « commandités » au pluriel, et « commanditaire » reste-t-il invariant en genre (seuls l'article et le participe s'accordant) y compris au pluriel « les commanditaires » ? Précise aussi le rôle attribué à une personne morale associée. Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## SAS (holding SPFPL par actions)

**1. Pourquoi une SAS-holding plutôt qu'une autre forme** · [usage]
```
Chez Sydel, dans quel cas concret le cabinet monte-t-il une holding SPFPL sous forme de SAS (société par actions simplifiée) plutôt que sous une autre forme de SPFPL ou plutôt qu'une SEL d'exercice ? Quel est l'intérêt pratique recherché par le médecin (détention de titres de SEL, montage patrimonial, transmission) ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**2. Articulation SAS-holding → SEL d'exercice** · [usage]
```
Comment s'articule, en pratique chez Sydel, la SPFPL constituée en SAS avec la ou les SEL d'exercice dont elle détient les titres ? La SAS-holding est-elle créée avant, après ou en même temps que la SEL ? Existe-t-il un ordre ou une dépendance entre les deux opérations ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**3. Profession éligible à la SPFPL par actions** · [règle légale]
```
La SPFPL constituée en SAS est-elle réservée aux médecins, ou la même forme par actions est-elle ouverte aux autres professions de santé suivies par Sydel (chirurgiens-dentistes, pharmaciens, infirmiers...) ? Existe-t-il une règle légale ou ordinale qui restreint la forme par actions à certaines professions ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**4. Détention du capital d'une SPFPL par actions — règles de l'Ordre** · [règle légale]
```
Pour une SPFPL constituée en SAS, quelles sont les règles légales et ordinales de détention du capital et des droits de vote : qui peut être actionnaire (professionnels en exercice, anciens professionnels, tiers...), quelles proportions sont imposées, et quel rôle joue l'inscription au tableau de l'Ordre dans la validité de la société ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**5. Durée de la société : règle constante ou choix du dossier** · [logique]
```
Pour une SPFPL en SAS chez Sydel, la durée de la société est-elle systématiquement fixée à la même valeur pour tous les dossiers (pratique constante du cabinet), ou est-ce une donnée arbitrée dossier par dossier avec le client ? Existe-t-il une raison métier ou juridique derrière la durée retenue ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**6. Rémunération du président : absence systématique ou choix** · [logique]
```
Pour la SPFPL en SAS, le principe selon lequel le président ne perçoit aucune rémunération jusqu'à la clôture du premier exercice est-il une pratique constante du cabinet appliquée à tous les dossiers, ou un choix arbitré au cas par cas ? Dans quels cas le président serait-il au contraire rémunéré dès le départ, et qu'est-ce qui déclencherait ce choix ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**7. Durée du mandat du président et points de vigilance** · [logique]
```
Pour le président d'une SPFPL en SAS, comment se décide la durée de son mandat (durée déterminée, illimitée, alignée sur un événement) ? Quels sont les pièges ou points de vigilance que le cabinet signale habituellement sur le mandat du président d'une telle société ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**8. Actionnaire unique vs plusieurs en pratique** · [condition cas]
```
En pratique chez Sydel, une SPFPL en SAS se crée-t-elle le plus souvent avec un actionnaire unique (qui est aussi le président), ou rencontre-t-on couramment des créations à plusieurs actionnaires ? Y a-t-il des situations métier typiques qui amènent plusieurs actionnaires dès la création ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**9. Apport de titres de SEL et commissaire aux apports** · [condition cas]
```
Quand la SPFPL en SAS est constituée par apport de titres d'une SEL (et non uniquement en numéraire), quelles conditions ou obligations s'appliquent : faut-il l'intervention d'un commissaire aux apports ou une évaluation par un tiers, dans quels cas est-ce obligatoire, et qui le désigne ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**10. Régime communautaire de l'actionnaire** · [condition cas]
```
Lorsque l'actionnaire d'une SPFPL en SAS est marié sous un régime de communauté et que les actions sont souscrites avec des biens communs, le cabinet applique-t-il la même logique de protection du conjoint qu'en SELARL (information / renonciation du conjoint à la qualité d'actionnaire, avertissement) ? Cette étape est-elle un cas conditionnel propre à la création SAS ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

**11. Genre du président et de l'actionnaire comme règle métier** · [genre-nombre]
```
Pour les documents d'une SPFPL en SAS, comment doit s'accorder le genre lorsque le président ou l'actionnaire est une femme (présidente, actionnaire, civilité, qualité professionnelle de médecin) ? Le cabinet a-t-il une règle métier sur ces accords, et le genre du président et celui de l'actionnaire peuvent-ils différer dans un même dossier ? Réponds uniquement à partir des sources ; si ce n'est pas dans les sources, dis-le explicitement.
```

---

## Au retour de NotebookLM
- Coller les réponses brutes (par type, par numéro de prompt) — je range ensuite dans le canon
  (synthèses `NOTEBOOKLM_ANSWERS.md`, journal de décisions, specs), sans reformuler le verbatim.
- Tout prompt où NotebookLM répond « pas dans les sources » → liste groupée pour **Rafael** (jamais une
  question au PM), une fois certain que ce n'est ni dans les modèles ni dans le canon.
