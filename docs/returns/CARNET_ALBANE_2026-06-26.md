# CARNET DE TRIAGE — Retours Albane LALLEMAND (Direction Juridique SYDEL)

- **Source** : mail Albane 2026-06-26 — `docs/review/albane_returns_2026-06-26/email_body_clean.txt`
- **Contexte** : SELAS pluripersonnelle, TOUTES options cochées, 15 documents générés (doc_01..doc_15) et annotés.
- **Loi fondamentale** : le verbatim du mail = la SPEC. Les .docx générés ne sont que du contexte.
- **Clone** : `sydel-document-engine-claude` · branche `sprint/engine-completion` · HEAD `0f612ca`.
- **État** : `À VÉRIFIER` partout (le gate-chercher technique se fait après, hors de Vivi).

Classifications : **PRESENTATION** · **FIDELITE-MODELE** · **BUG** · **METIER-DONNE** · **NOUVEAUTE-PRODUIT** · **QUESTION-METIER-OUVERTE**

---

## Section 1 — Formulaire

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-01 | Formulaire | « en cas de cession sur la partie financement le destinataire n'est pas utile (si c'est pour l'appel de fonds […]) il faut que seule le nom de la société et […] le nom du client soient préremplis » | METIER-DONNE | tous docs cession (volet financement) | À VÉRIFIER |
| A26-02 | Formulaire | « montant de déblocage mini si c'est pour l'appel de fonds il faut aussi que cela reste vierge » | METIER-DONNE | tous docs cession (volet financement) | À VÉRIFIER |
| A26-03 | Formulaire | « montant du prêt (compromis) = prix de cession » | METIER-DONNE | tous docs cession | À VÉRIFIER |
| A26-04 | Formulaire | « taux du prêt : toujours mettre 5,5 % » | METIER-DONNE | tous docs cession | À VÉRIFIER |
| A26-05 | Formulaire | « durée du prêt : toujours mettre 10 ans » | METIER-DONNE | tous docs cession | À VÉRIFIER |
| A26-06 | Formulaire | « crédit vendeur - majoration intérêts de retard : […] c'est fixe, il n'y a pas de variable […] il faut reprendre ce qu'il y avait dans le modèle » | FIDELITE-MODELE | tous docs cession | À VÉRIFIER |
| A26-07 | Formulaire | « date limite de la réalisation : c'est possible d'avoir par défaut à + 6 mois de la date des actes ? » | METIER-DONNE | tous docs cession | À VÉRIFIER |
| A26-08 | Formulaire (Avenant bail) | « bailleur : tout est pour une personne physique, mais il arrive que le bailleur soit une personne morale, il faudrait donc mettre la forme sociale, le nom, le siège social, le numéro SIREN avec le lieu d'immatriculation et le représentant » | NOUVEAUTE-PRODUIT | avenant bail (tous types ayant un bail) | À VÉRIFIER |
| A26-09 | Formulaire (SCM) | « SCM / Parts cédées & prix : en mettant le prix global est ce qu'il peut se mettre d'office en lettre ? » | METIER-DONNE | tous docs cession parts SCM | À VÉRIFIER |
| A26-10 | Formulaire (SCM) | « pour les plages cédées est ce qu'on peut prendre la main ? […] le mec détienne 10 parts, numérotées de 1 à 5 et 21 à 25 par ex. » | NOUVEAUTE-PRODUIT | cession parts SCM (plages non contiguës) | À VÉRIFIER |
| A26-11 | Formulaire (SCM) | « SCM/ Associés présents à l'ass : les plages de parts pour les associés présents je pense qu'il n'est pas nécessaire de le mettre […] et […] le premier peut être le cédant aussi » | METIER-DONNE | PV AGE cession SCM | À VÉRIFIER |
| A26-12 | Formulaire | « J'ai vu qu'il y avait des champs sur le côté pour copier le texte, est ce qu'il serait possible de les retirer ? […] le tab passe dessus, ca rend la saisie moins fluide » | PRESENTATION | UI formulaire (tous types) | À VÉRIFIER |
| A26-13 | Formulaire | « pas mal d'infos requises avant de pouvoir générer […] faire une liste des choses non complétées, mais il ne faudrait pas que ca bloque la génération des docs pour aucune info » | NOUVEAUTE-PRODUIT | UI formulaire (tous types) | À VÉRIFIER |

> Note : A26 « relever les incohérences sur la somme des actions c'est topissime » = compliment, pas un item de défaut (non numéroté).

---

## Section 2 — Intitulé du document statuts

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-14 | Statuts | « tu pourrais stp remettre le nom de la société dans l'intitulé du doc des statuts pour avoir "Status nom" ? » | PRESENTATION | tous types (nommage fichier statuts) | À VÉRIFIER |

---

## Section 3 — Statuts

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-15 | Statuts | « centrer l'entête, même le nom en gras, de l'espace avant et après le cadre des statuts, de l'espace entre chaque soussigné au début » | PRESENTATION | tous types (statuts) | À VÉRIFIER |
| A26-16 | Statuts | « j'ai "Monsieur Jean Durant, Docteur Médecin généraliste", je pense qu'il y a un "Docteur" en trop dans le modèle car je n'ai rien ajouté dans le formulaire » | BUG | tous types ayant profession médicale | À VÉRIFIER |
| A26-17 | Statuts | « pour la date de naissance, si le chiffre est de 1 à 9 […] au lieu de 1 janvier il peut y avoir un 0 devant pour mettre 01 ? » | PRESENTATION | tous types (format date) | À VÉRIFIER |
| A26-18 | Statuts | « associé marié sous un régime spécifique et dans les statuts il n'apparait que "marié" sans plus de précision, ni le nom de l'époux […] ajouter le régime et le nom du conjoint » | BUG | tous types (mention régime matrimonial) | À VÉRIFIER |
| A26-19 | Statuts (art. 2) | « le nom est à moitié en majuscule et minuscule […] harmoniser pour mettre en majuscule partout ? » | PRESENTATION | tous types (statuts art. 2) | À VÉRIFIER |
| A26-20 | Statuts (art. 3 & 4) | « le nom peut il être au milieu en gras ? (arti 3), idem pour le siège social (art 4) ? » | PRESENTATION | tous types (statuts art. 3-4) | À VÉRIFIER |
| A26-21 | Statuts (art. 14.1) | « le nom du dirigeant et son adresse peut-il aussi être en gras ? Et là j'ai mis un homme mais c'est écrit "est nommée présidente", c'est possible de genrer aussi ? » | BUG | tous types (genre dirigeant) + PRESENTATION | À VÉRIFIER |
| A26-22 | Statuts (art. 16, 17, 22) | « pareil le titre n'est pas en majuscule partout » | PRESENTATION | tous types (titres articles) | À VÉRIFIER |
| A26-23 | Statuts | « les mentions de signature à la fin décalent pas mal les noms […] peut être refaire des cases […] assez grandes pour que l'encadré de signature passe (je dirais environ 5 cm) » | PRESENTATION | tous types (bloc signatures) | À VÉRIFIER |

---

## Section 4 — PV de nomination de gérant

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-24 | PV nomination gérant | « est qu'on peut changer l'intitulé en dirigeant (car ici ce ne sont justement pas des gérants) » | FIDELITE-MODELE | SELAS / structures à président (pas gérant) | À VÉRIFIER |
| A26-25 | PV nomination gérant | « dans l'entête il y a Société d'exercice libéral par actions simplifiées de "Docteur" or il faudrait mettre la profession soit de chirurgien dentiste soit de médecin » | BUG | tous types ayant profession (entête) | À VÉRIFIER |
| A26-26 | PV nomination gérant | « mettre de l'espace entre les paragraphes » | PRESENTATION | PV nomination | À VÉRIFIER |
| A26-27 | PV nomination gérant | « mettre des tirets pour les points de l'ordre du jour » | PRESENTATION | PV nomination | À VÉRIFIER |
| A26-28 | PV nomination gérant | « on a déjà nommé le président dans les statuts et […] une nouvelle décision qui le nomme président […] retirer la partie des statuts […] ou juste nommer les autres dirigeants […] pas de doublon — et […] supprimer dans les statuts le paragraphe suivant sur sa rémunération » | BUG | SELAS multi (doublon statuts↔PV) | À VÉRIFIER |
| A26-29 | PV nomination gérant | « dans les dirigeants nommés, dans les résolutions il faudrait après le nom de l'associé, ajouter sa profession et à la fin mettre son régime matrimonial » | FIDELITE-MODELE | PV nomination | À VÉRIFIER |
| A26-30 | PV nomination gérant | « "en quatre exemplaires" après la ville peut être supprimé » | FIDELITE-MODELE | PV nomination | À VÉRIFIER |
| A26-31 | PV nomination gérant | « pareil les mentions à la fins ne s'intercalent pas bien » | PRESENTATION | PV nomination (bloc signatures) | À VÉRIFIER |

---

## Section 5 — Procuration

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-32 | Procuration | « C'est juste de la présentation pour descendre le cadre, l'agrandir, mettre de l'espace après et que "fait à le" soit à gauche » | PRESENTATION | procuration (tous types) | À VÉRIFIER |

---

## Section 6 — Lettre de renonciation associé

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-33 | Lettre renonciation | « c'est sensé être un courrier, en haut à droite au dessus de "à ville" il faut mettre le destinataire et son adresse et que le texte avec objet soit bien plus bas » | PRESENTATION | lettre renonciation (format courrier) | À VÉRIFIER |
| A26-34 | Lettre renonciation | « on peut retirer le "en quatre exemplaires" qui n'a pas de sens pour un courrier » | FIDELITE-MODELE | lettre renonciation | À VÉRIFIER |
| A26-35 | Lettre renonciation | « le montant de l'apport dans la phrase "en apportant X euros" correspond au montant du capital et non au montant de l'apport fait par l'associé » | BUG | tous docs mentionnant apport associé | À VÉRIFIER |

---

## Section 7 — Lettre d'avertissement

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-36 | Lettre avertissement | « dans l'entête et au milieu, sous le nom, il y a société d'exercice libérale de "Docteur", alors qu'il faudrait […] de chirurgien dentiste ou médecin » | BUG | tous types ayant profession (entête) | À VÉRIFIER |
| A26-37 | Lettre avertissement | « l'adresse est scindée en 2 il faudrait que tout soit sur la même ligne, on pourrait même écrire "siège social" devant. Exactement comme dans le PV en retirant en cours d'immatriculation » | PRESENTATION | tous docs ayant entête siège | À VÉRIFIER |
| A26-38 | Lettre avertissement | « dans le nom du destinataire c'est civilité et nom mais il manque le prénom (c'est dans le destinataire, dans le début de courrier et à la fin) » | BUG | lettre avertissement (destinataire) | À VÉRIFIER |
| A26-39 | Lettre avertissement | « pouvoir féminisé le "j'atteste avoir été informé(e)" » | BUG | tous docs avec accord en genre | À VÉRIFIER |
| A26-40 | Lettre avertissement | « le montant de l'apport correspond au montant du capital et non au montant de l'apport […] (dans l'ex la personne a fait un apport de 500 €, non de 1020 €) » | BUG | tous docs mentionnant apport associé | À VÉRIFIER |

---

## Section 8 — Demande d'inscription à l'Ordre

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| — | Demande inscription Ordre | « C'est juste parfait :) » | (VALIDÉ — aucun item) | n/a | VALIDÉ |

---

## Section 9 — Déclaration de non condamnation

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| — | Déclaration non condamnation | « Tout est nickel ! » | (VALIDÉ — aucun item) | n/a | VALIDÉ |

---

## Section 10 — Compromis de cession de cabinet médical

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-41 | Compromis cession cabinet | « sur l'identité du vendeur, seul son nom doit être en gras, pas tout le reste » | PRESENTATION | tous docs cession (identité parties) | À VÉRIFIER |
| A26-42 | Compromis cession cabinet | « après sa ville de naissance, il y a entre parenthèse "France" alors qu'il faudrait le département "75" par ex. » | BUG | tous docs mentionnant lieu de naissance | À VÉRIFIER |
| A26-43 | Compromis cession cabinet | « sur l'origine de propriété tout à disparu, le paragraphe est totalement vide, j'avais noté créé et j'ai mis une date » | BUG | compromis + acte cession cabinet | À VÉRIFIER |
| A26-44 | Compromis cession cabinet | « 4. chiffre d'affaires : il faudrait pour les exercices mettre 01/01/2023 au 31/12/2023 […] comme dans le modèle et non que 2023 et ajouter le sigle € après les montants mis en résultat » | FIDELITE-MODELE | compromis + acte cession cabinet | À VÉRIFIER |
| A26-45 | Compromis cession cabinet | « III promesse : lorsqu'il y a "docteur" il faudrait ajouter aux 2 endroits "le" pour mettre "le docteur" » | FIDELITE-MODELE | tous docs cession cabinet (mention "docteur") | À VÉRIFIER |
| A26-46 | Compromis cession cabinet | « Date prévue de réalisation : la date est mise avec une barre en plus "01/01//2027" […] cette date est à 4 endroits dans l'acte » | BUG | tous docs cession (format date réalisation) | À VÉRIFIER |
| A26-47 | Compromis cession cabinet | « pour le nombre de page tout à la fin […] que ca s'adapte automatiquement […] Sinon […] par défaut de mettre sept plutot que huit ? » | BUG | compromis cession cabinet (numérotation pages) | À VÉRIFIER |

---

## Section 11 — Avenant au bail

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-48 | Avenant bail | « l'identité du Locataire devrait être en non gras (sauf son nom), peut être que c'est pareil pour le bailleur […]. Et pour la date de naissance également que le chiffre ne soit pas 1 janvier mais 01 janvier » | PRESENTATION | avenant bail | À VÉRIFIER |
| A26-49 | Avenant bail | « Art 1 : devant Docteur, mettre "le docteur" (pareil à l'art 2 sur la seconde phrase) » | FIDELITE-MODELE | avenant bail (mention "docteur") | À VÉRIFIER |
| A26-50 | Avenant bail | « d'ajouter un espace entre chaque article » | PRESENTATION | avenant bail | À VÉRIFIER |
| A26-51 | Avenant bail | « on peut retirer "en quatre exemplaires" » | FIDELITE-MODELE | avenant bail | À VÉRIFIER |

---

## Section 12 — Acte de cession de cabinet médical

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-52 | Acte cession cabinet | « j'ai les mêmes remarques sur le compromis pour les mentions communes » | (RENVOI A26-41..A26-46) | acte cession cabinet | À VÉRIFIER |
| A26-53 | Acte cession cabinet | « paiement du prix : j'ai coché "crédit vendeur", si on le coche il faut que dans le texte soit retiré 'ajouter en cas de CV' […] soit 100% CV (enlever "au moyen d'un prêt bancaire") soit les 2 (crédit bancaire à hauteur de XX € et pour partie crédit vendeur) » | METIER-DONNE | acte cession cabinet (clause paiement CV) | À VÉRIFIER |
| A26-54 | Acte cession cabinet | « Autrement est ce que le texte peut être surligné de couleur pour que l'on oublie pas d'adapter » | NOUVEAUTE-PRODUIT | acte cession cabinet (surlignage à compléter) | À VÉRIFIER |
| A26-55 | Acte cession cabinet | « page 6 3. sur les contrats de travail : c'est possible que ce soit surligné pour penser à le compléter si nécessaire ? » | NOUVEAUTE-PRODUIT | acte cession cabinet (surlignage contrats travail) | À VÉRIFIER |
| A26-56 | Acte cession cabinet | « il y a des espaces en trop entre les paragraphes affirmation de sincérité et le suivant » | PRESENTATION | acte cession cabinet | À VÉRIFIER |
| A26-57 | Acte cession cabinet | « en page 6 au point 8 ce n'est pas ce texte dans le modèle, c'est un texte concernant la SCM […] s'il y a une SCM […] "De céder l'intégralité des parts qu'il détient de la SCM" […] Il faut retirer le texte "maintenir le cabinet médical dans son état actuel..." » | FIDELITE-MODELE | acte cession cabinet (clause SCM, cas avec SCM) | À VÉRIFIER |

---

## Section 13 — Acte de cession de parts SCM

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-58 | Acte cession parts SCM | « Mettre des espaces dans le cadre au début, avant et après » | PRESENTATION | acte cession parts SCM | À VÉRIFIER |
| A26-59 | Acte cession parts SCM | « mettre dans le cadre sur une 3e ligne le nom de la SCM qui fait l'objet de la cession » | FIDELITE-MODELE | acte cession parts SCM | À VÉRIFIER |
| A26-60 | Acte cession parts SCM | « espacer les soussignés, mettre les phrases soussignés de première part et soussigné de seconde part à droite en gras, idem pour "ci après dénommé 'La Société'" » | PRESENTATION | acte cession parts SCM | À VÉRIFIER |
| A26-61 | Acte cession parts SCM | « pour le soussigné 1 que monsieur soit avec un majuscule au début, pareil sur la date de naissance (01 non 1) » | PRESENTATION | acte cession parts SCM | À VÉRIFIER |
| A26-62 | Acte cession parts SCM | « le soussigné 2 : la SELAS il y a écrit sur la 2e ligne SELARL au lieu de SELAS et représentée par son gérance au lieu de son président » | BUG | acte cession parts SCM (forme + représentant SELAS) | À VÉRIFIER |
| A26-63 | Acte cession parts SCM | « Mettre des espaces après chaque titre » | PRESENTATION | acte cession parts SCM | À VÉRIFIER |
| A26-64 | Acte cession parts SCM | « "il est préalable exposé ce qui suit" : il y a une adresse […] pas demandée dans le formulaire, souvent la même que le siège de la SEL, il faudrait que ce soit proposé par défaut ou en cochant une case » | NOUVEAUTE-PRODUIT | acte cession parts SCM (adresse SCM par défaut) | À VÉRIFIER |
| A26-65 | Acte cession parts SCM | « le nom des cogérants qui suit est mis aussi aux hasard, il faudrait que dans la liste des associés sur le formulaire on puisse cocher si la personne est gérante pour que ces noms là apparaissent » | NOUVEAUTE-PRODUIT | formulaire associés (case "gérant") + actes SCM | À VÉRIFIER |
| A26-66 | Acte cession parts SCM | « Origine de propriété : après liste des associés, la civilité il faudrait une majuscule en début de phrase » | PRESENTATION | acte cession parts SCM | À VÉRIFIER |
| A26-67 | Acte cession parts SCM | « propriétaire des parts pour les avoir souscrites à la constitution, mais ce n'est pas toujours le cas, comme pour le compromis […] il faudrait pouvoir adapter » | NOUVEAUTE-PRODUIT | acte cession parts SCM (origine propriété adaptable) | À VÉRIFIER |
| A26-68 | Acte cession parts SCM | « cession les numéros de parts ne correspondent pas à la somme de mes parts (ici 20 parts cédées, numérotées de 151 à 200) » | BUG | acte cession parts SCM (numérotation parts) | À VÉRIFIER |
| A26-69 | Acte cession parts SCM | « j'ai mis un prix global (ici 20 €) mais le prix moyen par part n'est pas ajusté […] 20 parts pour 20 € […] la part cédée vaut un (1) euro et non 100 € » | BUG | acte cession parts SCM (prix unitaire calculé) | À VÉRIFIER |
| A26-70 | Acte cession parts SCM | « le nombre d'exemplaires c'est quatre et non trois pour cet acte » | FIDELITE-MODELE | acte cession parts SCM | À VÉRIFIER |
| A26-71 | Acte cession parts SCM | « pour les signatures il faudrait soit les mettre cote à cote soit avec plus d'espace […] on peut retirer les mots cédants et cessionnaires ca ne me dérange pas » | PRESENTATION | acte cession parts SCM (bloc signatures) | À VÉRIFIER |

---

## Section 14 — Courrier SDE

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-72 | Courrier SDE | « les 5 premières lignes doivent être sur la droite, formalisme obligatoire de la poste […] aligné à gauche mais qu'il démarre vers le cm 12 de la règle » | PRESENTATION | courrier SDE | À VÉRIFIER |
| A26-73 | Courrier SDE | « répétition de la SCM peut être que l'on peut mettre de la Société "variable dénomination" pour éviter de faire doublon si la forme est dans la dénomination » | BUG | courrier SDE (doublon forme/dénomination) | À VÉRIFIER |
| A26-74 | Courrier SDE | « on peut mettre de l'espace pour que l'objet et le début du courrier commence plus bas » | PRESENTATION | courrier SDE | À VÉRIFIER |

---

## Section 15 — PV AGE cession SCM

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-75 | PV AGE cession SCM | « l'adresse du siège devrait correspondre à une adresse d'un formulaire » | BUG | PV AGE cession SCM (adresse siège) | À VÉRIFIER |
| A26-76 | PV AGE cession SCM | « mettre de l'espace entre les paragraphes et entre les résolutions » | PRESENTATION | PV AGE cession SCM | À VÉRIFIER |
| A26-77 | PV AGE cession SCM | « Mme XX présente la séance en qualité de "gérant associé', il faudrait pouvoir le féminiser pour que ce soit gérante associée et par défaut […] mettre comme associé celui qui vend les parts de la SCM » | BUG | PV AGE cession SCM (genre + associé présentateur par défaut) | À VÉRIFIER |
| A26-78 | PV AGE cession SCM | « dans la première résolution […] ajouter : " et par conséquent, autorise la cession de XX parts sociales de Monsieur XXX à la SEL XX" […] remplacer "dans un délai de 3 mois […] soit jusqu'au" par "à compter de ce jour" » | METIER-DONNE | PV AGE cession SCM (1re résolution) | À VÉRIFIER |
| A26-79 | PV AGE cession SCM | « la résolution suivante […] "L'ag, compte tenu de la résolution qui précède [supprimer et sous réserve de la réalisation], décide […] de modifier l'article [chiffre en surlignage] des statuts qui sera rédigé ainsi [ajouter : à compter de ce jour]" » | METIER-DONNE | PV AGE cession SCM (résolution suivante) | À VÉRIFIER |
| A26-80 | PV AGE cession SCM | « dans la liste de la 2e résolution retirer la mise à la ligne de à associé 1, "à concurrence de" ne soit pas mis sur la ligne du dessous, mais à la suite de l'associé » | PRESENTATION | PV AGE cession SCM (2e résolution) | À VÉRIFIER |
| A26-81 | PV AGE cession SCM | « A la fin mettre que c'est signé par tous les associés (enlever la gérance), ca évite des erreurs et c'est correct » | FIDELITE-MODELE | PV AGE cession SCM (bloc signatures) | À VÉRIFIER |

---

## Section 16 — Autres points

| ID | Document | Verbatim exact (citation courte) | Classification | Périmètre propagation | État |
|---|---|---|---|---|---|
| A26-82 | Transverse / Statuts | « capital social variable […] ajouter partout où le capital est suggéré, une case pour cocher s'il est variable et […] le montant minimum […] dans les statuts le montant du capital maximum apparaît […] max = 10 fois le capital minimum […] "capital : 1 000 € (minimum : 1 000 € et max : 10 000 €)" » | NOUVEAUTE-PRODUIT | sociétés civiles / micro holding (capital variable) | À VÉRIFIER |
| A26-83 | Transverse | « Pour éviter d'ajouter des variables dans tous les actes, il n'y a que dans la société micro holding qu'il faut en mettre […] quand on choisit un associé personne morale, il faut qu'on puisse indiquer que le capital est variable » | NOUVEAUTE-PRODUIT | micro holding / associé personne morale uniquement | À VÉRIFIER |
| A26-84 | Liste des sociétés | « il n'y avait pas la micro holding dans la liste des sociétés, si tu peux l'ajouter » | NOUVEAUTE-PRODUIT | catalogue types (nouvelle structure micro holding) | À VÉRIFIER |

---

# SYNTHÈSE

## 1. COMPTE par classification

| Classification | Nombre | IDs |
|---|---|---|
| **PRESENTATION** | 27 | A26-12, 14, 15, 17, 19, 20, 22, 23, 26, 27, 31, 32, 33, 37, 41, 48, 50, 56, 58, 60, 61, 63, 66, 71, 72, 74, 76, 80 |
| **FIDELITE-MODELE** | 13 | A26-06, 24, 29, 30, 34, 44, 45, 49, 51, 57, 59, 70, 81 |
| **BUG** | 21 | A26-16, 18, 21, 25, 28, 35, 36, 38, 39, 40, 42, 43, 46, 47, 62, 68, 69, 73, 75, 77 |
| **METIER-DONNE** | 11 | A26-01, 02, 03, 04, 05, 07, 09, 11, 53, 78, 79 |
| **NOUVEAUTE-PRODUIT** | 10 | A26-08, 10, 13, 54, 55, 64, 65, 67, 82, 83, 84 |
| **QUESTION-METIER-OUVERTE** | 0 | — |

> Note de comptage : A26-21 (genre + gras) et A26-39 sont rangés en BUG (le défaut genre prime, le gras est secondaire) ; A26-80 figure aussi dans la colonne PRESENTATION ci-dessus. Le total d'items numérotés est **84** (A26-01 → A26-84) ; A26-52 est un RENVOI (mentions communes acte/compromis), non recompté en classification. 2 sections (Ordre, non condamnation) sont VALIDÉES sans item.

## 2. LES NOUVEAUTÉS PRODUIT (à cadrer séparément)

- **A26-08** — Bailleur personne morale dans l'avenant au bail (forme sociale, nom, siège, SIREN + lieu, représentant).
- **A26-10** — Plages de parts SCM non contiguës saisies à la main (ex. 1-5 et 21-25).
- **A26-13** — Liste des champs non complétés SANS bloquer la génération (génération tolérante au vide).
- **A26-54** — Surlignage couleur des passages à adapter (clause crédit vendeur).
- **A26-55** — Surlignage des contrats de travail à compléter.
- **A26-64** — Adresse SCM proposée par défaut (= siège SEL) ou via case à cocher.
- **A26-65** — Case "gérant" dans la liste des associés du formulaire (pilote les cogérants affichés).
- **A26-67** — Origine de propriété adaptable (pas systématiquement "souscrites à la constitution").
- **A26-82** — Capital social variable PARTOUT où le capital est suggéré (min/max, max = 10× min).
- **A26-83** — Capital variable restreint à la micro holding / associé personne morale.
- **A26-84** — Ajouter la micro holding au catalogue des types de sociétés.

## 3. LES QUESTIONS MÉTIER OUVERTES (candidates à UN message Rafael unique)

**Aucune QUESTION-METIER-OUVERTE.** Tout le métier est soit fourni explicitement par Albane
(METIER-DONNE : taux 5,5 %, durée 10 ans, +6 mois, crédit vendeur fixe, formulations PV SCM…),
soit dérivable d'un modèle source (FIDELITE-MODELE), soit un bug/présentation. Albane EST le sachant
métier et a livré une spec complète dans ce mail.

> Points à surveiller au gate technique (pas des questions métier, des vérifs de faisabilité/source) :
> - A26-46/A26-43 (date "01/01//2027" et origine propriété vide) : Albane n'avait plus accès à son
>   formulaire — confirmer si erreur de saisie ou bug générateur lors du gate-chercher.
> - A26-47 (sept vs huit pages) : la valeur par défaut « sept » est une donnée d'Albane ; l'auto-
>   adaptation du nombre de pages est une faisabilité technique à trancher en interne (pas Rafael).
