# SCS — Réponses NotebookLM (synthèse exploitable)

> **Ordre de passage :** 5 / 6 · **Prompts :** 13 — **passe PARTIELLE : 1 à 10 obtenus**, **11/12/13
> NON posés** (limite NotebookLM journalière). À redemander à la réinitialisation.
> **Verbatim brut :** `NOTEBOOKLM_ANSWERS_RAW_V1.txt`. Ce fichier-ci = lecture du Second.

---

## VERDICT (Second)

**SCS = société civile (parts / Gérant), capital VARIABLE, à DEUX catégories d'associés** :
**commandité** (gestionnaire, le praticien PP, responsabilité indéfinie et solidaire, gère seul) et
**commanditaire** (investisseur, souvent la **SPFPL**, responsabilité limitée à l'apport, ne gère pas).
Montage **patrimonial/immobilier** « plan personnel » : faire basculer l'argent de la SPFPL vers un
projet immobilier perso tout en laissant la gestion au praticien. NotebookLM donne **rôles +
responsabilités + structure + genre/nombre**, mais **pas le wording statutaire intégral** (→ modèle
source + Rafael). Les prompts multi (11-13) manquent mais **ne sont pas bloquants** (cf. plus bas).

→ **Conséquence build :** réutilise le socle civil (parts/Gérant, capital variable, multi, PM associée,
genre/nombre) + une **couche « rôle statutaire » commandité/commanditaire** et la **décorrélation droits
de vote / droits financiers** (déjà nécessaire pour SCI IRIS). **Audit du moteur Codex `statuts_scs.py`**
contre ce montage + le modèle source `lot_04/Statuts_SCS_modele.docx`.

---

## ACQUIS — utilisable tout de suite

### Périmètre / nature
- SCS **maintenue** (bouton « SCS » catégorie « Autres »), **plan personnel/patrimonial**, **pas
  d'inscription Ordre** (« l'ordre s'en fiche »). ~15 docs (allégé).
- **Forme à part entière**, mais usage quasi systématique = **outil de restructuration** reliant pro
  (SPFPL commanditaire) et perso (praticien commandité) pour de l'**immobilier**.

### Deux catégories d'associés (cœur SCS)
| Rôle | Qui | Responsabilité | Gestion |
| :--- | :--- | :--- | :--- |
| **Commandité** (gestionnaire) | praticien (PP) | **indéfinie et solidaire** (biens propres) | **gère seul** |
| **Commanditaire** (investisseur) | souvent la **SPFPL** (PM) | **limitée à l'apport** | ne s'immisce pas |
- Wording : « Monsieur [NOM Prénom], associé commandité » / « La société [Dénomination], associée
  commanditaire ».
- **Montages à couvrir** : (a) commandité PP + commanditaire PP (familial) ; (b) commandité PP +
  commanditaire **SPFPL** (cœur de métier) ; (c) mixte plusieurs commanditaires PP+PM. **Min 2**
  (≥1 commandité + ≥1 commanditaire), **borne haute 6**.

### Capital + répartition
- **Capital VARIABLE systématique** (comme SCI ; un seul bouton, pas de variante). Mise à jour auto.
- **Décorrélation droits de vote / droits financiers** : « 1 % des parts ≠ 1 % du résultat » ;
  **numérotation des parts par lots** « numérotées de [X] à [Y] inclus ».
- **Clause de protection de l'associé exerçant** (canon SELARL) : « En aucun cas la répartition du
  capital ne pourra être modifiée dans des conditions qui retireraient la majorité des droits de vote
  aux associés exerçant dans la société. »

### Documents création
| Document | Statut |
| :--- | :--- |
| Fiche de création | **Collecte interne — à IMPORTER, pas un livrable** |
| Statuts SCS | Systématique |
| Procuration / DNC / Autorisation domiciliation | Systématiques (tronc commun) |
| Attestation sur le capital | Systématique (preuve de dépôt/apport) |
| PV nomination gérant | Conditionnel : si pas nommé dans les statuts |
| Lettre d'option IS | Conditionnel : si IS |
| Lettre renonciation + conjoint | Conditionnel : si associé marié sous communauté |
| Contrat d'apport | Conditionnel : si SCS créée par apport de titres (vs numéraire) |
- **Liste des souscripteurs = NON** pour la SCS (réservée aux sociétés par actions) ; identité +
  répartition portées par les **Statuts + l'Attestation de capital**.
- **Rapport de mission / « compte rendu » = HORS périmètre génération** : document de **conseil rédigé
  à la main** (PowerPoint adapté ~1h, ou mail 1-3h), « source de vérité » validée par le client avant
  rédaction des actes. **Ne pas l'automatiser.** S'il décrit la structure créée, le wording correct est
  « Société en Commandite Simple » (peut citer la SCI en comparaison, jamais comme la forme créée).

### Couche GENRE / NOMBRE (prompt 10)
associé/associée · gérant/gérante (jamais président) · **commandité/commanditée** · commanditaire
(invariant ; article/participe s'accordent : « l'associée commanditaire ») · Monsieur/Madame ·
né/née · marié/mariée · divorcé/divorcée · inscrit/inscrite · soussigné/soussignée. Pluriel : Les
Soussignés · Les Associés · Les Gérants · **Les Commanditaires** · a décidé/ont décidé · apporte/
apportent · part sociale/parts sociales · numérotée/numérotées. PM commanditaire → « La société
[Dénomination] » + genre du **représentant**.

---

## NON OBTENU / NON TROUVÉ

- **Prompts SCS 11, 12, 13 NON posés** (limite NotebookLM) — à redemander :
  - **11** : wording statuts selon commanditaire **PP vs société (holding)**.
  - **12** : **plusieurs commanditaires** — énumération, apports, plage de parts.
  - **13** : **répartition apports & parts** entre commandités et commanditaires (règles spécifiques :
    le commandité reçoit-il des parts / d'un type particulier ?).
  - **Pas bloquants** : NotebookLM est de toute façon insuffisant pour le wording multi exact
    (« ultra personnalisé ») ; la source autoritaire = le **modèle tokenisé** `Statuts_SCS_modele.docx`
    + **Rafael**. Les reposer serait de la corroboration, pas un débloquant.
- **Wording statutaire intégral SCS** (objet, articles responsabilité, apports, répartition) : NON
  TROUVÉ verbatim → tokeniser `lot_04/Statuts_SCS_modele.docx` + Rafael.
- ⚠️ **Point à trancher (audit + Rafael)** : la source NotebookLM décrit une SCS **civile/immobilière
  patrimoniale** (commandité praticien + commanditaire SPFPL). Le moteur Codex `statuts_scs.py`
  correspond-il à ce montage, ou a-t-il inventé une **SCS d'exercice** non sourcée ? → audit de fidélité.

---

## CONSÉQUENCES BUILD (à porter dans la spec SCS)

- **SCS = société civile parts/Gérant, capital variable, 2 catégories (commandité/commanditaire),
  min 2 max 6, commanditaire PM (SPFPL) central, montage immobilier perso.**
- **MVP = bloc de création** (statuts + tronc commun + attestation capital + conditionnels). **Hors
  périmètre** : rapport de mission (conseil manuel), liste des souscripteurs (NON).
- **Socle réutilisé** : substitution parts/Gérant, capital variable (SCI), couche multi, **PM associée**,
  genre/nombre, **décorrélation droits de vote/financiers + numérotation par lots** (SCI IRIS) +
  nouvelle **couche rôle statutaire commandité/commanditaire**.
- **Audit Codex `statuts_scs.py`** vs modèle source + cette synthèse AVANT câblage ; reposer 11-13 à
  NotebookLM seulement si l'audit/Rafael ne suffit pas.

---

## Réponses brutes

Verbatim (prompts 1-10) dans `NOTEBOOKLM_ANSWERS_RAW_V1.txt`. Ne pas reformuler : le brut fait foi.
