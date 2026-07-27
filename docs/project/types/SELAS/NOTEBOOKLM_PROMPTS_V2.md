# Prompts NotebookLM DÉFINITIFS — type SELAS (V2)

**But.** Obtenir, depuis NotebookLM, la **totalité de l'info métier manquante** pour bâtir la SELAS
(moteur + UI) avec la recette `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`. Ces prompts sont
**prêts à coller un par un** dans NotebookLM (chacun dans son bloc de code).

**Méthode de relais.** Coller **un seul prompt à la fois**, attendre la réponse, structurer la réponse
dans le journal NotebookLM, puis passer au suivant. Priorité **P-A → P-D** (le bloc « Multi /
personne morale / DG » est le cœur du nouveau besoin et débloque le plus).

---

## CE QUI EST DÉJÀ RÉPONDU — NE PAS RE-DEMANDER

La SELAS a déjà bouclé NotebookLM (9 réponses, 2026-06-01/02) + un cas réel reçu le 2026-06-05.
Les points ci-dessous sont **acquis** (matière exploratoire NotebookLM, non opposable tant que Rafael
n'a pas tranché, mais **suffisamment cernés pour ne PAS reposer la question telle quelle**) :

- **Squelette cas → documents** (déjà modélisé dans `case_catalog.py`) : création (statuts SELAS,
  DNC, autorisation domiciliation, procuration, PV/décision président, demande inscription Ordre) ;
  régime communautaire (renonciation conjoint) ; cession fonds (avenant bail) ; SCM (PV AGE + courrier
  SDE + acte cession parts) ; dérogation / site distinct.
- **Lexique de base** : `président` (jamais `gérant`), `actions` (jamais `parts sociales`) pour le
  capital ; `associé` toléré pour désigner les personnes. *(La carte article-par-article reste à faire
  → voir P-B.)*
- **Féminin** : `Présidente` si la dirigeante est une femme (accord piloté par le genre). *(Le wording
  féminin exact des autres rôles reste à confirmer → P-C.)*
- **Numérotation des actions** : `1 à N` validé pour V1 (démembrement / droits dérogatoires = hors V1).
- **Plans des locaux + devis matériel (Ordre)** : **bloquants** — mais ce sont des **pièces fournies
  par le client** (checklist de complétude), **pas des DOCX générés**.
- **Attestation de dépôt de capital + liste des souscripteurs** : **obligatoires** (source
  « Besoins Sydel (juridique).pdf »).
- **Questionnaire Ordre** : OUI médecin / NON dentiste (pièce conditionnelle par profession).
- **Pièces de cession de fonds / origine de propriété** : **rédaction manuelle / revue humaine**
  (hors automatisation V1) — ne pas redemander si c'est automatisable.

**Points NotebookLM restés MUETS** (donc à creuser ici, pas acquis) : DG (était « non trouvé » mais le
cas réel en contient → P-A4), filiation de la DNC président, titre exact de la lettre de renonciation
conjoint, nomination du président dans les statuts vs acte séparé, wording multi-associés et personne
morale associée.

**Convention de tag dans les prompts** : chaque prompt vise une réponse **avec citation de source**.
Si une info manque, la réponse doit écrire `non trouvé` et donner la **source ou l'indice source**.

---

## P-A — Multi 2-5 associés + personne morale + DG (NOUVEAU BESOIN — PRIORITÉ MAX)

> Contexte produit (2026-06-05) : la SELAS doit gérer **2 à 5 associés** (jamais 1, jamais > 5),
> peut compter une **personne morale associée** (ex. une Société Civile) et des **Directeurs Généraux**.
> Cela remplace/complète le périmètre V1 « actionnaire unique ». Un cas réel de référence existe
> (statuts SELAS du Dr Reynaud, 38 articles, non tokenisé). Ces prompts cherchent le **wording exact**
> du passage de 1 à plusieurs associés, faute de quoi le moteur multi serait inventé.

1.
```text
Contexte : moteur documentaire déterministe pour des statuts de SELAS (société d'exercice libéral par actions simplifiée). Réponds uniquement d'après les sources de ce NotebookLM ; si une information manque, écris "non trouvé" et donne la source ou l'indice source.

Pour des statuts de SELAS à PLUSIEURS associés (de 2 à 5), donne le wording EXACT de la clause de COMPARUTION (le bloc "LES SOUSSIGNÉS ... ont décidé d'instituer une société ..."), et la façon dont l'identité de chaque associé est répétée (un bloc identité par associé : civilité, nom, naissance, adresse, profession). Cite l'article/passage source.
```

2.
```text
Contexte : statuts de SELAS à plusieurs associés (2 à 5), moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne le wording EXACT, en présence de PLUSIEURS associés, de : (a) l'article APPORTS (une ligne d'apport en numéraire par associé + total des apports), et (b) l'article CAPITAL / RÉPARTITION des actions ("le capital est divisé en N actions réparties entre les associés comme suit ..."), avec la forme du tableau ou de la liste de répartition. Indique la phrase qui remplace, en associé unique, "actions attribuées en totalité à l'associé unique". Cite la source.
```

3.
```text
Contexte : statuts de SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Une SELAS peut-elle avoir une PERSONNE MORALE (ex. une Société Civile / holding) comme associée ? Si oui, donne le wording EXACT de sa COMPARUTION dans les statuts ("La société X, [forme sociale], au capital de ..., dont le siège est ..., immatriculée au RCS de ... sous le numéro ..., représentée par ... en sa qualité de ..."), de sa LIGNE de répartition du capital, et de sa SIGNATURE ("Pour la société X, [représentant], [fonction]"). Cite la source. Si aucun wording n'existe dans les sources, écris "non trouvé".
```

4.
```text
Contexte : gouvernance d'une SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

La SELAS peut nommer un ou plusieurs DIRECTEURS GÉNÉRAUX en plus du président. Donne le wording EXACT de l'article des statuts qui institue le ou les directeurs généraux, leurs pouvoirs, leur nomination et la durée de leur mandat ; et le wording de l'acte/PV de nomination du directeur général s'il existe. Précise si le DG est obligatoire ou optionnel. Cite la source. Si non trouvé, écris "non trouvé".
```

5.
```text
Contexte : décisions des associés d'une SELAS à plusieurs associés (2 à 5), moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Quand la SELAS a PLUSIEURS associés, quelle forme prend l'acte de décision : un PV d'assemblée générale (avec convocation, quorum, ordre du jour, résolutions) au lieu d'une "décision de l'associé unique" ? Donne le wording EXACT du PV d'assemblée et la liste des résolutions de constitution (nomination du président, éventuel DG, etc.). Cite la source. Indique ce qui n'est pas trouvé.
```

6.
```text
Contexte : statuts de SELAS à 2-5 associés, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne le wording EXACT du BLOC DE SIGNATURES des statuts en présence de plusieurs associés : mention manuscrite éventuelle ("Lu et approuvé"), une signature par associé, ordre des signataires, et la forme de signature d'une personne morale associée ("Pour la société X ..."). Cite la source.
```

7.
```text
Contexte : statuts de SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Existe-t-il, à plusieurs associés, des clauses de statuts ABSENTES du modèle à associé unique : agrément des cessions d'actions entre associés/à des tiers, droit de préemption, organisation des décisions collectives, clauses d'exclusion ? Pour chacune présente dans les sources, donne le wording EXACT et la condition de déclenchement. Si une clause n'existe pas dans les sources, écris "non trouvé".
```

---

## P-B — Cas → documents (compléter le squelette déjà connu)

> Le squelette est déjà modélisé. Ces prompts ferment les **trous précis** restants sur la carte
> cas → documents, sans reposer l'inventaire global déjà obtenu.

8.
```text
Contexte : moteur documentaire déterministe pour la CRÉATION d'une SELAS (médecin ou dentiste). Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Pour la nomination du PRÉSIDENT de SELAS à la création : est-elle faite DANS les statuts (clause de désignation du premier président), ou par un ACTE / PV SÉPARÉ de nomination ? Si les deux existent, dans quel cas chacun s'applique ? Donne le wording EXACT de la clause ou de l'acte concerné. Cite la source. Indique ce qui n'est pas trouvé.
```

9.
```text
Contexte : déclaration de non-condamnation (DNC) du président d'une SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

La DNC du président doit-elle mentionner la FILIATION complète du déclarant (noms et prénoms des parents) ? Donne le wording EXACT de la DNC SELAS, en précisant les champs obligatoires. Cite la source. Si la filiation n'est pas exigée dans les sources, écris "non trouvé".
```

10.
```text
Contexte : régime communautaire d'un associé de SELAS marié sous communauté, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Quel est le TITRE EXACT et le wording de l'acte par lequel le conjoint d'un associé de SELAS renonce à revendiquer la qualité d'associé (ou d'actionnaire) ? L'effet juridique en SELAS (capital en actions) diffère-t-il de la SELARL (parts sociales) ? Cite la source. Indique ce qui n'est pas trouvé.
```

---

## P-C — Wording exact par document (fidélité)

> But : verrouiller le wording document par document, sans paraphrase. Ces prompts ciblent les
> documents où le passage SELARL → SELAS change réellement le texte.

11.
```text
Contexte : statuts de SELAS médecin, moteur documentaire déterministe (fidélité au modèle, pas de paraphrase). Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne le wording EXACT, article par article, des clauses des statuts SELAS qui DIFFÈRENT d'une SELARL : forme sociale ("Société d'exercice libéral par actions simplifiée"), article CAPITAL exprimé en actions, article DIRECTION (président, éventuel directeur général), article DÉCISIONS. Pour chaque clause, donne le texte source et sa référence d'article. Indique ce qui n'est pas trouvé.
```

12.
```text
Contexte : moteur documentaire déterministe, SELAS. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne le wording EXACT de la PROCURATION et de la DEMANDE D'INSCRIPTION À L'ORDRE pour une SELAS : quelles mentions changent par rapport à une SELARL (rôle "président" au lieu de "gérant", forme sociale "SELAS", mandataire) ? Cite chaque passage et sa source. Indique ce qui n'est pas trouvé.
```

13.
```text
Contexte : attestation de dépôt de capital et liste des souscripteurs d'une SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne le wording EXACT de l'attestation de dépôt de capital et de la liste des souscripteurs pour une SELAS : champs requis (banque, montant, division en actions, identité des souscripteurs et nombre d'actions souscrites par chacun). Précise comment ces deux pièces s'articulent (document unique ou deux pièces distinctes). Cite la source. Indique ce qui n'est pas trouvé.
```

14.
```text
Contexte : moteur documentaire déterministe, SELAS. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Liste les termes qui NE DOIVENT PAS apparaître dans des documents SELAS (ex. "gérant", "parts sociales", "gérance", "cession de parts") et le terme SELAS correct à leur place, document par document. Donne, pour chaque substitution, la source qui justifie le terme SELAS. Indique ce qui n'est pas trouvé.
```

---

## P-D — Genre / pluriel (couche transverse)

> But : table d'accords pilotée par le genre et par le nombre, sans regex de terminaison.

15.
```text
Contexte : accords grammaticaux dans des statuts et actes de SELAS, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Donne la table d'accord de GENRE (piloté par la civilité de la personne) pour les termes SELAS : président / présidente, directeur général / directrice générale, associé / associée, soussigné / soussignée, né / née, le Docteur / la Docteur(e). Pour "Docteur" au féminin (statuts médecin/dentiste), indique la forme correcte d'après les sources ("la Docteur", "la Docteure", "Doctoresse", ou reformulation). Cite la source. Indique ce qui n'est pas trouvé.
```

16.
```text
Contexte : statuts de SELAS à plusieurs associés (2 à 5), accords de NOMBRE, moteur documentaire déterministe. Réponds uniquement d'après les sources ; si l'info manque, écris "non trouvé" + source.

Quels passages des statuts et des actes SELAS passent au PLURIEL quand il y a plusieurs associés (ex. "le soussigné" → "les soussignés", "l'associé unique" → "les associés", "il a décidé" → "ils ont décidé") ? Donne, pour chaque passage, le singulier source et le pluriel exact attendu, avec la référence d'article. Indique ce qui n'est pas trouvé.
```

---

## Schéma de sortie

- **Chemin** : `docs/project/types/SELAS/NOTEBOOKLM_PROMPTS_V2.md`
- **Nombre de prompts finaux** : **16** (P-A : 7 · P-B : 3 · P-C : 4 · P-D : 2)
- **Déjà répondu (non reposé)** : squelette cas→documents, lexique de base président/actions, féminin
  « Présidente », numérotation actions 1→N, plans/devis Ordre bloquants, attestation capital + liste
  souscripteurs obligatoires, questionnaire Ordre médecin/dentiste, cession fonds manuelle.
- **Question bloquante (arbitrage Gad, hors NotebookLM)** : le nouveau besoin « 2 à 5 associés +
  personne morale + DG » **contredit** le périmètre V1 « actionnaire unique » déjà ratifié. À trancher
  AVANT de tokeniser/coder : (a) la V1 uni est-elle remplacée ou complétée par le multi ? (b) la
  personne morale associée est-elle dans le périmètre V1 ? (c) le DG entre-t-il en V1 ? (d) le cas
  Reynaud est-il LE modèle de référence ou un exemple parmi d'autres ? Ces prompts préparent la matière
  métier ; ils ne tranchent pas le périmètre produit.
