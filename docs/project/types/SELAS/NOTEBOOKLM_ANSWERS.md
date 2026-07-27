# SELAS — Réponses NotebookLM (synthèse exploitable)

> **Ordre de passage :** 1 / 6 · **Prompts :** 16 (voir `NOTEBOOKLM_PROMPTS_V2.md`)
> **Verbatim brut intégral :** `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (37 430 car., 16 blocs dans l'ordre
> de collage du PM). Ce fichier-ci est la **lecture du Second** : ce qui est ACQUIS, ce qui est
> NON TROUVÉ, et ce que ça implique pour le build. La synthèse n'invente rien — chaque point renvoie
> au brut.

---

## VERDICT (Second)

**NotebookLM confirme le CADRE et les RÈGLES DE SUBSTITUTION, mais PAS le wording exact** des cas
multi-associés / personne morale / DG. Le cabinet qualifie lui-même ces rédactions d'« **ultra
personnalisées** », « **impossible de faire autant de modèles qu'il faut** », faites « **à la main** »
sur Word. **NotebookLM est donc INSUFFISANT à lui seul pour générer une SELAS multi fidèle.**

→ **Conséquence build (décidée) :** la SELAS se construit comme **tronc SELARL + couche de
substitution + couche multi**, et il faut **tokeniser le modèle SELAS de référence (« Reynaud »,
dans `C:\Users\Gad\Downloads`)** pour récupérer le wording exact que les sources n'ont pas. Les
NON TROUVÉ résiduels après lecture du modèle Reynaud → **message Rafael** (jamais avant d'avoir
épuisé Reynaud).

---

## ACQUIS — utilisable tout de suite (aucune escalade nécessaire)

### Règles de substitution SELARL → SELAS (transverses, TOUS documents)
| NE PAS écrire | TERME CORRECT |
| :--- | :--- |
| « parts sociales » / « parts » | **actions** (« le mot qui revient le plus dans tous les documents ») |
| « Gérant » | **Président** (fém. **Présidente**) |
| « à responsabilité limitée » / « SELARL » | **par actions simplifiée** / **SELAS** |
| « Cession de parts » | **Cession d'actions** (déduit de la règle parts→actions) |
| « associé unique » (répartition) | liste de répartition par associé |

- **« Associés » est CONSERVÉ** (le cabinet **n'impose pas** « actionnaires ») — bloc 14.
- **« Gérance »** : pas de substantif de remplacement explicite cité (rôle = Président) → NON TROUVÉ.

### Wording EXACT confirmé (verbatim source)
- **Clause majorité de contrôle** (fin Article 8, à conserver) :
  > « En aucun cas la répartition du capital ne pourra être modifiée dans des conditions qui
  > retireraient la majorité des droits de vote aux associés exerçant dans la société. »
- **Dépôt du capital** (repris mot pour mot dans l'Article 7 Apports, sert l'attestation capital) :
  > « Cette somme a été déposée par l'associé [unique / les associés] sur un compte ouvert au nom de
  > la société dans les livres de la banque [NOM DE LA BANQUE], [ADRESSE DE LA BANQUE]. Elle ne pourra
  > être retirée que sur présentation d'un certificat du greffier attestant l'immatriculation de la
  > société au registre du commerce et des sociétés. »
- **Article 8 — structure de répartition** (« parts » → « actions ») :
  > « Il est divisé en [Nombre] ([NOMBRE EN LETTRES]) actions de [Valeur] ([VALEUR EN LETTRES])
  > chacune, intégralement libérées, souscrites et attribuées de la façon suivante :
  > - [Civilité Nom Prénom] : [Nombre] actions
  > Soit au total : [Total] actions »
  > Multi-associés : numérotation précise type « **actions n°1 à 10 inclus** ».

### Structure / scope confirmés
- **Personne morale associée : OUI** (cas « 25 % d'une société médicale » ; soit **SPFPL** holding,
  soit **société civile micro-holding**). Données à collecter : **dénomination + SIREN**. (bloc 3)
- **DG : optionnel**, structure centrée sur un **Président majoritaire** ; le dirigeant peut être
  nommé **dans les statuts OU par PV séparé** (« dépend des statuts sélectionnés »). Données mini
  dirigeant : **nom, prénom, téléphone**. (blocs 4, 8)
- **Forme des décisions selon le nombre** : associé unique = « décision de l'associé unique »
  (court) ; **plusieurs associés = PV d'AGE** (long : « les associés présents… forment le capital »,
  « les associés discutent entre eux »). (blocs 5, 11)
- **Décorrélation capital / résultat** : gérer séparément **droits de vote** et **droits financiers**
  (1 % des actions ≠ 1 % du résultat) ; **actions de préférence** pour associés non-exerçants. (bloc 7)

### Couche GENRE (table pilotée par la civilité) — bloc 15
| Masculin | Féminin |
| :--- | :--- |
| Président | Présidente |
| Associé | Associée |
| Soussigné | Soussignée |
| Né | Née |
| Directeur Général | **NON TROUVÉ** |
| Le Docteur | **NON TROUVÉ** (sources ne donnent que « Le Docteur ») |

### Couche NOMBRE (singulier → pluriel) — bloc 16
- « LE SOUSSIGNÉ » → « **LES SOUSSIGNÉS** » ; « qu'il a décidé d'instituer » → « qu'**ils ont** décidé
  d'instituer ».
- « déposée par l'associé unique » → « déposée par **les associés** ».
- « attribuées en totalité à l'associé unique » → « **réparties entre les associés** de la façon
  suivante » + numérotation.
- Accords : Associé(e)s, Soussigné(e)s, Né(e)s — le système doit savoir « deux messieurs / deux dames /
  mélange ».

---

## NON TROUVÉ — à lever via le modèle Reynaud PUIS Rafael

1. Bloc **comparution multi** « LES SOUSSIGNÉS … » complet (texte contractuel).
2. **Personne morale** : wording exact comparution, ligne de répartition, **bloc signature**
   « Pour la société X, représentée par… ».
3. **Article DG** + **PV de nomination** (Président ou DG) — texte intégral.
4. **PV d'assemblée multi** : convocation, quorum, liste des résolutions de constitution.
5. **Bloc signatures multi** + mention manuscrite + ordre des signataires.
6. **Clauses SELAS multi** : agrément, droit de préemption, exclusion (texte statutaire).
7. **DNC** (déclaration sur l'honneur de non-condamnation) : texte intégral + question filiation
   (parents) non tranchée.
8. **Renonciation conjoint** (régime communautaire) : titre contractuel + texte (« pas du tout fait »
   dans les trames actuelles).
9. **Statuts SELAS complets** : les sources ne contiennent que **les 2 premières pages d'un modèle
   SELARL** — articles 1/7/8 SELAS définitifs absents.
10. **Procuration** texte intégral + désignation du **mandataire**.
11. **Demande d'inscription à l'Ordre** : formulaire complet (médecin = questionnaire en plus vs
    dentiste).

---

## CONSÉQUENCES BUILD (à porter dans la spec SELAS)

- **Architecture** : SELAS = tronc SELARL **rejoué** via couche substitution (`parts→actions`,
  `gérant→président`) + couche **multi** (déjà prévue pour la SELARL) + support **personne morale
  associée** (dénomination/SIREN) + **DG optionnel**.
- **Pré-requis bloquant matière** : **tokeniser le modèle Reynaud** (Downloads) AVANT de coder le
  wording SELAS exact ; sans lui, on n'a que la substitution (insuffisant pour le multi).
- **Escalade Rafael** : un seul message groupé sur les NON TROUVÉ résiduels **après** Reynaud
  (ne jamais relayer avant d'avoir épuisé le modèle).
- **Scope à confirmer (décision produit Gad)** : SELAS **multi 2-5 + personne morale + DG** —
  cela **supersede** le périmètre V1 « actionnaire unique » ratifié pour la SELARL. À acter au
  journal de décisions avant build SELAS.

---

## Réponses brutes

Capturées **verbatim** dans `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (16 blocs, ordre de collage =
ordre des prompts). Ne pas reformuler le brut : il fait foi pour toute relecture juridique.
