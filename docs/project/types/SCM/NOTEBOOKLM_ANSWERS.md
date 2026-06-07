# SCM — Réponses NotebookLM (synthèse exploitable)

> **Ordre de passage :** 3 / 6 · **Prompts :** 18 (16 NotebookLM + 2 Rafael : 7, 14)
> **Verbatim brut intégral :** `NOTEBOOKLM_ANSWERS_RAW_V1.txt` (réponses NotebookLM dans l'ordre de
> collage). Ce fichier-ci = **lecture du Second** : ACQUIS / NON TROUVÉ / conséquences build.

---

## VERDICT (Second)

**Pas de carte « cas → documents » canon pour la SCM** (confirmé absent — c'est le territoire Rafael),
**mais récolte opérationnelle riche** : liste de création (~15 docs « allégés »), statuts **wording
verbatim** (comparution PP + PM, apports, capital), gérant, deux durées, tables genre + pluriel, multi,
et surtout des **décisions de périmètre** : la fiche de création n'est **pas un livrable** (collecte
interne), l'avenant bail est **rattaché à la cession** (pas à la création pure), et pacte / règlement
intérieur / contrat de frais communs sont des **opérations distinctes** (hors bloc création).

→ **Conséquence build :** SCM = société civile **parts / Gérant** (jamais Président/actions), **min 2
associés** (PP + souvent une SEL associée). MVP = **bloc de constitution** uniquement. Tokeniser les
**11 modèles SCM** pour le wording NON TROUVÉ (contrat de frais, RI, PV gérant), puis Rafael pour la
carte des cas + la clé de répartition des dépenses + (Albane) le pluriel.

---

## ACQUIS — utilisable tout de suite

### Décisions de périmètre (importantes)
- **Création SCM = bloc de constitution seul** (~15 docs allégés). Liste + statut :
  | Document | Statut |
  | :--- | :--- |
  | Fiche de création | **Collecte interne — À IMPORTER, PAS un livrable généré** |
  | Procuration | Systématique (tronc commun) |
  | Statuts SCM | Systématique |
  | Déclaration de non-condamnation (DNC) | Systématique |
  | Autorisation de domiciliation | Systématique (souvent fusionnée) |
  | PV de nomination du gérant | **Conditionnel** : si le gérant n'est pas nommé dans les statuts |
  | Lettre renonciation + avertissement conjoint | **Conditionnel** : si associé marié sous communauté (« cas n°2 ») |
- **Pacte d'associés / Règlement intérieur / Contrat de frais communs / Liste des dépenses communes =
  opérations juridiques DISTINCTES**, hors bloc création. À modéliser comme cas séparés plus tard,
  **pas dans le MVP création**.
- **Avenant au bail = déclenché par la CESSION** (transfert d'activité), pas par la création pure.
  Parties : bailleur + ancien locataire (praticien BNC) + SCM nouvelle locataire.
- **Demande d'inscription à l'Ordre** : NotebookLM répond « fait partie (systématique), l'Ordre doit
  être informé même s'il s'en fiche ». ⚠️ **Confirmable Rafael** (contredit l'hypothèse « la SCM n'est
  pas une structure d'exercice donc pas d'Ordre »).

### Statuts SCM — wording EXACT confirmé (verbatim)
- **Comparution** (titre pluriel « LES SOUSSIGNÉS ») :
  - PP : « [Monsieur/Madame] [Prénom NOM], [Profession], né(e) le [Date] à [Lieu], de nationalité
    [Nationalité], demeurant [Adresse], [Situation matrimoniale]. »
  - PM (SEL) : « La société [Dénomination], [SELARL/SELAS] au capital de [Montant] euros, dont le siège
    social est à [Adresse], immatriculée au RCS de [Ville] sous le numéro [SIREN], représentée par
    [Civilité NOM Prénom] en sa qualité de [Gérant/Président]. »
  - Liaison : « …ont établi ainsi qu'il suit les statuts de la Société [Dénomination SCM] qu'ils ont
    décidé d'instituer : »
- **Article 7 — Apports** : « Le Docteur [Nom], apporte à la société la somme de [Montant] euros. » /
  « La société [Dénomination SEL], apporte … la somme de [Montant] euros. » + dépôt « Cette somme a été
  déposée par les associés sur un compte … banque [Nom/adresse]. » · apport en industrie/nature =
  « néant » par défaut.
- **Article 8 — Capital (parts)** : « Le capital social est fixé à la somme de [Total] euros. Il est
  divisé en [Nombre] parts sociales de [Valeur] chacune, intégralement libérées, souscrites et
  attribuées de la façon suivante : - [Civilité Nom] : [N] parts · - La société [Dénom SEL] : [N] parts.
  Soit au total : [Total] parts. » + numérotation « parts n°1 à X ».

### Gérant
- Nommé par les associés (AG si plusieurs ; décision associé unique si 1). **Dans les statuts OU PV
  séparé**. **Co-gérance possible** (« Les Gérants », bloc identité + signature par gérant). Durée du
  mandat / liste des pouvoirs exacts = **NON TROUVÉ**.

### Deux durées
- **Société** : figée dans les statuts + clause de **prorogation** (« au moins un an avant la date
  d'expiration … l'AG décide de la prorogation »). 99 ans = pratique, **non cité verbatim** (confirmable).
- **Domiciliation** : **indéterminée** (comme la SEL).

### Couche GENRE (paires exactes, bloc 15)
LE SOUSSIGNE/LA SOUSSIGNEE · Monsieur/Madame · né le/née le · inscrit/inscrite au tableau ·
divorcé/divorcée · marié/mariée · associé/associée · associé unique/associée unique · **gérant/gérante**
· **co-gérant/co-gérante** · apporteur/apporteuse · « il a décidé »/« elle a décidé » · signature
« L'Associé »/« L'Associée ». « Le Docteur » fém. = NON TROUVÉ. médecin / chirurgien-dentiste = épicène.
**Vocabulaire SCM = gérance + parts** (jamais Président/actions). « le Docteur/la Docteure » se gère
**par associé** (cas par cas), pas par règle universelle (bloc 17).

### Couche NOMBRE / multi (blocs 16, 18)
LES SOUSSIGNÉS · « qu'ils ont décidé » · apports par associé + « les associés » · « Les parts sociales
sont réparties entre les associés comme suit » + numérotation · clause majorité-contrôle au pluriel ·
gouvernance **NON pré-rédigée au pluriel** (modèles = associé unique, 60 % des cas) → pluraliser
dynamiquement : « Délibérations des associés » / « Assemblée Générale », « Les Gérants », signatures
multipliées. **Min 2 associés** (par définition SCM) ; borne haute à modéliser **6 PP + ~3-4 SEL
associées**. Droits de vote ≠ droits financiers (1 % parts ≠ 1 % résultat).

---

## NON TROUVÉ — à lever via les 11 modèles SCM tokenisés PUIS Rafael

1. **Carte officielle « cas → documents » SCM** (n'existe pas dans le canon → Rafael, prompt 1/7).
2. **PV nomination gérant** : durée du mandat + liste des pouvoirs (texte exact).
3. **Avenant au bail** : wording exact (parties / objet / date d'effet).
4. **Contrat de frais communs / Règlement intérieur / Liste des dépenses communes** : texte intégral +
   **clé de répartition** (seuil de dépense commune, année de référence des charges) — NON TROUVÉ.
5. **Cession de parts à un tiers** : clauses spécifiques (garantie de passif) ; PV d'agrément SCM
   entre personnes physiques.
6. **Inscription à l'Ordre pour la SCM** : confirmer (réponse NotebookLM ambiguë).
7. **Pluriel** : validation **Albane** (via Rafael).
8. Référence « Liste des dépenses communes » .doc vs .docx (prompt 14, Rafael).

---

## CONSÉQUENCES BUILD (à porter dans la spec SCM)

- **SCM = société civile, parts / Gérant**, min 2 associés, **PP + PM (SEL) associées dès le départ**.
- **MVP = bloc de constitution** (Statuts + tronc commun + PV gérant conditionnel + conjoint
  conditionnel). **Hors MVP** : pacte, règlement intérieur, contrat de frais communs (cas distincts),
  avenant bail (rattaché cession).
- **Fiche de création = import**, jamais un document généré.
- **Tokeniser les 11 modèles SCM** pour le wording NON TROUVÉ, puis **un message Rafael** : carte des
  cas, clé de répartition des dépenses, inscription Ordre SCM, .doc/.docx dépenses + (Albane) pluriel.
- **Réutilise la couche commune** (DNC / domiciliation / procuration) et la couche multi (LES
  SOUSSIGNÉS, répartition numérotée, gouvernance pluralisée).

---

## Réponses brutes

Capturées **verbatim** dans `NOTEBOOKLM_ANSWERS_RAW_V1.txt`. Ne pas reformuler : le brut fait foi.
