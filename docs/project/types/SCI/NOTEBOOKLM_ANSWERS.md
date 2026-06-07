# SCI — Réponses NotebookLM (synthèse exploitable)

> **Ordre de passage :** 4 / 6 · **Prompts :** 13 (11 NotebookLM + 2 Rafael : 5, 10)
> **Verbatim brut intégral :** `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (réponses dans l'ordre de collage).
> Ce fichier-ci = **lecture du Second** : ACQUIS / NON TROUVÉ / conséquences build.

---

## VERDICT (Second)

**Très bonne récolte, canon TRANCHÉ.** NotebookLM confirme que **la SCI reste au périmètre Sydel**
(« Besoins Sydel (juridique).pdf » fait foi ; boutons « sci » et « sci iris » présents) ; le bloc a
juste été déplacé en catégorie **« Autres »** par segmentation **pro vs personnel** (la SCI est
**patrimoniale**, « n'a rien à voir avec la profession », « l'Ordre s'en fiche »). La distinction
**SCI vs SCI IRIS** est clarifiée, et la table genre/pluriel est riche (paires exactes, accord **par
personne**). NON TROUVÉ ciblé : wording exact des actes hors statuts + modèle « Lettre d'option IS ».

→ **Conséquence build :** SCI = société civile **parts / Gérant**, **capital variable**, **min 2
associés**, **personne morale associée autorisée dans les DEUX variantes**. SCI IRIS ≠ « a une PM
associée » → IRIS = **répartition dérogatoire du résultat par groupes de parts numérotés**. MVP =
bloc de création. Tokeniser les modèles SCI/SCI IRIS ; Rafael uniquement pour la « Lettre d'option IS ».

---

## ACQUIS — utilisable tout de suite

### Périmètre / canon (tranché)
- **SCI maintenue** au périmètre, catégorie **« Autres »** (vs le cœur SEL/SPFPL = « 90 % des cas »).
  Canon de référence = « Besoins Sydel (juridique).pdf ». **Pas d'inscription à l'Ordre** (sauf via
  une SEL associée) — la SCI est patrimoniale, pas une structure d'exercice. Profession du client
  **sans impact** sur le document (médecin = dentiste, même statuts).
- **2 variantes** : `SCI` (immobilier patrimonial classique) et `SCI IRIS` (montage d'optimisation).

### SCI vs SCI IRIS — critère tranché
- **Le déclencheur de IRIS n'est PAS la présence d'une personne morale associée** (les deux variantes
  peuvent avoir une PM associée). **IRIS = répartition DÉROGATOIRE du résultat** : « 1 % des parts ne
  donne pas forcément droit à 1 % du résultat » → droits financiers ≠ droits de vote, pilotés par
  **groupes de parts numérotés**. Usage : faire circuler l'argent SEL/SPFPL/Micro-holding → projet
  immobilier perso, ou investissement de la holding dans l'immobilier du praticien.

### Création SCI — documents + statut
| Document | Statut |
| :--- | :--- |
| Fiche de création | **Collecte interne — à IMPORTER, pas un livrable** |
| Statuts (SCI ou SCI IRIS) | Systématique (choix piloté par stratégie patrimoniale / IS-IR) |
| PV de nomination du gérant | **Conditionnel** : si gérant pas nommé dans les statuts |
| Procuration | Systématique (tronc commun) |
| Déclaration de non-condamnation | Systématique |
| Autorisation de domiciliation | Systématique (souvent fusionnée) |
| Attestation sur le capital | Systématique (preuve de dépôt) |
| Lettre d'option IS | **Conditionnel** : si option IS choisie (variable IS/IR) |
| Lettre renonciation + avertissement conjoint | **Conditionnel** : si associé marié sous communauté |

### Spécificités SCI des trames communes (substitutions)
- « **Gérant** » (jamais Président) · « **parts sociales** » (jamais actions) · forme « **Société
  Civile** » (pas « société d'exercice libéral ») · objet « **immobilier / patrimonial** ».
- Procuration : identique au tronc commun. DNC / domiciliation : structure identique + ces substitutions.
- **Domiciliation = durée indéterminée** ; **société = durée figée** (99 ans, constante du modèle, pas
  saisie libre) + clause de **prorogation** (AG ≥ 1 an avant expiration).

### Capital
- **Variable** : capital initial **libre** (saisi par le client), divisé en parts ; la fiche société se
  **met à jour automatiquement** aux opérations (augmentation/réduction). Pas de formule de plafond
  citée ; **numérotation précise des parts** (n°1 à X) essentielle, surtout en IRIS.

### SCI IRIS — wording confirmé
- Associé PM dans la comparution : « La société [Dénomination], [SELARL/SELAS/SPFPL] au capital de
  [Montant] euros, dont le siège social est à [Adresse], immatriculée au RCS de [Ville] sous le numéro
  [SIREN], représentée par [Civilité NOM Prénom] en sa qualité de [Gérant/Président]. »
- Répartition (Art. 8) : « La société [Dénomination] : [Nombre] parts, numérotées de [X] à [Y] inclus. »
- Quote-part résultat exceptionnel (mécanique, texte intégral NON TROUVÉ) : « Les parts numérotées de
  [1 à 10 …] donnent droit à [X] % des droits aux résultats [exceptionnels]. »

### Gérant
- Nommé par les associés (AG si plusieurs ; décision associé unique si 1). Pas obligatoirement associé.
  **Dans les statuts OU PV séparé**. **Co-gérance possible** (« Les Gérants »). Durée / pouvoirs exacts
  NON TROUVÉ.

### Couche GENRE (paires exactes, accord PAR PERSONNE — bloc 11)
LE SOUSSIGNE/LA SOUSSIGNEE · Monsieur/Madame · né le/née le · inscrit/inscrite au tableau ·
divorcé/divorcée · marié/mariée · « qu'il a décidé »/« qu'elle a décidé » · **Le Docteur/La Docteure**
· associé/associée · L'Associé/L'Associée · gérant/gérante · co-gérant/co-gérante · nommé/nommée.
⚠️ Accord **par personne** (chaque bloc d'identité), **jamais un genre global du dossier**. PM associée
→ « La société […] » (neutre), mais son **représentant** déclenche un accord (« représentée par
Madame… »).
**Note :** ici NotebookLM donne « **La Docteure** » au féminin (paire attestée) — diverge des SELAS/
SPFPL/SCM où « Le Docteur » fém. était NON TROUVÉ. À confirmer comme règle transverse (Rafael/Albane).

### Couche NOMBRE / multi (blocs 12, 13)
LES SOUSSIGNÉS · « qu'ils ont décidé » · dépôt « par les associés » · « réparties entre les associés »
+ numérotation · gouvernance NON pré-rédigée au pluriel (60 % unipersonnel) → « Délibérations des
associés »/« Assemblée Générale », « Les Gérants », signatures multipliées. **Min 2 associés** (forme
civile), borne haute **6** ; PM associée OK dans les deux variantes. ⚠️ **Pluralisation à valider
Albane** (NotebookLM l'indique explicitement — mail de validation systématique à Albane).

---

## NON TROUVÉ — tokenisation modèles SCI PUIS Rafael

1. **Modèle « Lettre d'option IS »** (absent du corpus → Rafael, prompt 10).
2. Wording exact des **actes hors statuts** : acte de cession de parts SCI (clauses spécifiques),
   PV de nomination gérant (durée/pouvoirs), transfert de siège, augmentation de capital, dissolution.
3. **Article quote-part de résultat exceptionnel** (IRIS) : texte intégral (mécanique connue, wording
   non reproduit) → tokeniser le modèle SCI IRIS.
4. Conventions de trésorerie SCI (bouton existe, lien SCI non explicité).
5. Pluriel : **validation Albane** (via Rafael).

---

## CONSÉQUENCES BUILD (à porter dans la spec SCI)

- **SCI = société civile, parts / Gérant, capital VARIABLE, min 2 associés**, PM associée autorisée
  dans les **deux** variantes. **IRIS = couche « répartition dérogatoire par groupes de parts
  numérotés »** par-dessus la SCI standard (droits financiers ≠ droits de vote), pas une structure
  d'associés différente.
- **MVP = bloc de création** (statuts SCI/SCI IRIS + tronc commun + attestation capital + PV gérant
  conditionnel + lettre IS conditionnelle + conjoint conditionnel). Cession/transfert/augmentation/
  dissolution = cas ultérieurs.
- **Fiche de création = import** (pas un livrable). **Pas d'inscription à l'Ordre.**
- **Tokeniser** les modèles SCI + SCI IRIS (déjà au repo `project/source_documents/sci`) ; **Rafael**
  uniquement pour la « Lettre d'option IS » + (Albane) le pluriel.
- Réutilise la couche commune + la couche multi + le support **personne morale associée** (mutualisé
  avec SCM/SPFPL/SELAS).

---

## Réponses brutes

Capturées **verbatim** dans `NOTEBOOKLM_ANSWERS_RAW_V1.txt`. Ne pas reformuler : le brut fait foi.
