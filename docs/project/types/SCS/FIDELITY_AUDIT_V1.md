# SCS — Audit de fidélité V1 (FOND + FORME)

Date : 2026-06-07
Auteur : auditeur de fidélité (lecture seule du code ; aucune modif `.py` ; aucune action Git)
Gouvernance : le générateur SCS a été écrit par **Codex (mai 2026)** depuis le seul « Documents à
générer par cas », **avant** NotebookLM → **suspect jusqu'à validation**. « Les tests passent » ne
prouve QUE le comportement codé, pas la fidélité juridique ni la mise en forme.

## Périmètre audité
- Générateur : `src/sydel_doc_engine/generators/lot_04/statuts_scs.py` (wrapper) →
  `src/sydel_doc_engine/generators/lot_04/statuts_civils_common.py` (`SCS_TEMPLATE` +
  `generate_statuts_civil_docx`) → helpers `src/sydel_doc_engine/rendering/docx_builder.py`.
- Modèle source (= LA vérité wording) : `project/source_documents/lot_04/Statuts_SCS_modele.docx`
  (289 paragraphes, **2 tables** : titre « STATUTS » + grille de signature).
- Synthèse NotebookLM : `docs/project/types/SCS/NOTEBOOKLM_ANSWERS.md` (+ RAW V1).
- Échantillon de sortie généré : `artifacts/_audit_tmp/scs_sample/statuts_scs.docx`
  (via le constructeur de contexte de `tests/unit/test_lot_04_statuts_civils.py`, 2 associés :
  commandité Jean Durand + commanditaire Alice Martin).

---

## VERDICT GLOBAL : **FIX** (mécanique template-fill saine, mais plusieurs blocs codés divergent /
inventent / suppriment du wording source, et la forme dérive sur plusieurs aspects)

- **Fond : FIX.** ~90 % du texte est repris **verbatim de la source** (le moteur recopie les
  paragraphes source et ne substitue que des variables ; contrôle anti-placeholder en sortie). MAIS
  les 3 blocs réinjectés en code (apports, capital, signature) **inventent du wording absent de la
  source ET de NotebookLM** (« SOIT AU TOTAL… »), **suppriment des clauses source** (phrase
  capital-effectif + valeur nominale + numérotation des parts ; lignes « Total des apports »,
  « Total des parts sociales composant le capital »), et **dupliquent** l'intro des apports. Aucun de
  ces écarts n'est un faux montage : c'est une SCS **civile/immobilière, capital variable, commandité
  / commanditaire** — fidèle au montage NotebookLM. La dérive est dans la **fidélité de reprise**, pas
  dans la nature.
- **Forme : FIX (mixte).** Le titre encadré « STATUTS » est **totalement perdu** (le moteur n'itère
  que `paragraphs`, jamais `tables` de la source). En-tête (dénomination/forme/capital/siège/RCS) en
  **JUSTIFY au lieu de CENTER**, dénomination **non grasse** (source : grasse). Titres TITRE **CENTER
  au lieu de JUSTIFY**. ARTICLES **soulignés** (source : **non soulignés**). ARTICLE 21 & 22 perdent
  tout style de titre (espace insécable). Accentuation **mixte** (source accentuée / blocs codés
  désaccentués). Pas de perte de logo (le modèle SCS n'en a pas).

---

## VOLET 1 — FIDÉLITÉ DU FOND (wording / cas / règles)

### Triangulation montage (NotebookLM ↔ source ↔ moteur)
| Critère NotebookLM | Source `Statuts_SCS_modele.docx` | Moteur Codex | Verdict |
|---|---|---|---|
| SCS = société civile, parts / Gérant | objet civil immobilier (art. 2), parts sociales, gérance (art. 16-19) | parts + gérant (socle civils, PV gérant) | KEEP |
| Capital VARIABLE systématique | art. 7-8 « Le capital social est variable » + min/max | recopié verbatim de la source | KEEP |
| 2 catégories commandité / commanditaire | art. 6, 13 ; rôles explicites | `role_statutaire` obligatoire ; refuse si rôle manque (`_validate_scs`) ; jamais déduit du rang | KEEP |
| Min 2 (≥1 commandité + ≥1 commanditaire), max 6 | montage 2 associés | `_validate_scs` exige les 2 rôles ; `MAX_ASSOCIES=6` | KEEP |
| Commanditaire PM (SPFPL) possible | ligne `[denomination_societe_associe_1]` | `_is_morale` / `_add_morale_identity` | KEEP |
| Genre / nombre (commandité/commanditée, né/née) | source porte « épousе/née » en dur (remplacé) | `Ne/Nee` via `Gender` ; **rôle rendu « commandite » sans accent** | FIX (accent) |
| Pas de liste des souscripteurs | absente | absente | KEEP |

→ **Pas de SCS « d'exercice » inventée.** Le moteur respecte le montage civil/immobilier. Le point B5
de `BUILD_READINESS_V1` (civile vs exercice pro) reste un arbitrage Rafael, mais le code **ne dérive
pas** : il suit la source civile.

### Divergences de reprise (bloc par bloc)
| Élément | Source | Moteur Codex | Verdict |
|---|---|---|---|
| Corps des statuts (art. 1-5, 9-30, titres, objet, gérance, décisions, dissolution, annexe) | wording intégral | **recopié verbatim** (substitution de variables uniquement) | KEEP |
| Bloc comparution « LES SOUSSIGNÉS » (`associate_slice 14-18`) | 2 personnes en dur | bloc dynamique 1-6 associés, identité PP/PM | KEEP |
| **Intro apports** « Le capital social est constitué par les apports… Associés commandités : » | 1 fois (para source 41) | **DUPLIQUÉ** : rendu en source (para 41) PUIS ré-émis par le code → 2 occurrences | FIX |
| **« SOIT AU TOTAL [montant] euros »** (apports) | **ABSENT** | **INVENTÉ** par le code | FIX (inventé) |
| Ligne « **Total des apports en numéraires : [capital_social]** » | présente (para 57) | **SUPPRIMÉE** | FIX |
| Phrase dépôt banque « **Cette somme de … a été intégralement versée dès avant ce jour…** » | wording source (para 57) | **remplacée** par « Les associés déclarent et reconnaissent que la somme libérée… a été déposée intégralement… » (wording **inventé**, hors source) | FIX (inventé) |
| « Associé commanditaire : » | **singulier** (para 51) | « Associes commanditaires : » (**pluriel**) | FIX |
| Ligne « **Le montant total versé par le commanditaire est de …** » | présente (para 56) | **SUPPRIMÉE** | FIX |
| **Phrase capital-effectif** « Le capital social effectif est fixé à … divisé en [nb_parts] parts de [valeur_nominale] euro de valeur nominale, numérotées de [plage], lesquelles sont attribuées aux associés comme suit : » | présente (para 63, clause de fond) | **SUPPRIMÉE** (le `capital_slice 63-76` écrase ce paragraphe sans le réémettre) | FIX (perte de clause) |
| **« SOIT AU TOTAL [n] parts »** (capital) | **ABSENT** | **INVENTÉ** par le code | FIX (inventé) |
| Ligne « **Total des parts sociales composant le capital : [nb_parts_total] parts sociales** » | présente (para 75) | **SUPPRIMÉE** (remplacée par « SOIT AU TOTAL … parts ») | FIX |
| Répartition par associé (`Propriétaire de … parts sociales`, `Numérotées de …`, `[qualite_associe]`) | présent | rendu dynamique fidèle (sauf intro perdue ci-dessus) | KEEP |
| Bloc apport commandité (total commandité) | présent | présent, fidèle | KEEP |
| Clôture « Fait à …, le … / En … exemplaires » + ANNEXE (actes, mandataire) | présent | recopié verbatim | KEEP |

### Wording **inventé / divergent** (présent dans le code, ABSENT du modèle ET de NotebookLM = danger max)
1. **« SOIT AU TOTAL [montant] euros »** (`_add_apport_block`) — inventé.
2. **« SOIT AU TOTAL [n] parts »** (`_add_capital_block`) — inventé.
3. **« Les associés déclarent et reconnaissent que la somme libérée, d'un montant de … a été déposée
   intégralement et avant ce jour, au crédit d'un compte ouvert, au nom de la société en formation, à
   la banque … »** (`_add_apport_block`) — remplace le wording source « Cette somme de … a été
   intégralement versée dès avant ce jour à un compte ouvert au nom de la Société en formation, à la
   Banque … » ; reformulation non sourcée.
4. **« Associes commanditaires : » (pluriel)** vs source **« Associé commanditaire : » (singulier)**.
5. **« Lu et approuve »** seul (grille de signature) vs source **« (Faire précéder de la mention
   « Lu et approuvé ») »** en italique — wording amputé.

NotebookLM RAW V1 confirme : 0 occurrence de « SOIT AU TOTAL », « Lu et approuv », « capital variable »,
« Total des » → **aucun appui NotebookLM** pour ces formulations ; le RAW porte les rôles
(commandité ×31) mais **pas le wording statutaire** (« insuffisant pour le wording multi exact » dit la
synthèse). Donc ces 5 points sont des **inventions/reformulations Codex non corroborées**.

### Clauses de fond **perdues** (source → absentes de la sortie)
- Phrase **capital-effectif + valeur nominale + numérotation globale des parts** (« … divisé en N parts
  de X euro de valeur nominale, numérotées de [plage], lesquelles sont attribuées aux associés comme
  suit : »). C'est une clause **substantielle** (assise juridique de la répartition) — sa perte est le
  point de fond le plus grave.
- Lignes de **totaux** : « Total des apports en numéraires », « Total des parts sociales composant le
  capital », « Le montant total versé par le commanditaire ».

**Cause technique commune** (non bloquante en soi mais à l'origine des écarts) : `SCS_TEMPLATE` repère
les blocs par **index de paragraphes en dur** (`apport_slice=(43,58)`, `capital_slice=(63,76)`). Les
bornes sont **désalignées** d'un paragraphe par rapport au contenu réel de la source (l'intro apports
vit au para 41, hors slice → dupliquée ; la phrase capital-effectif vit au para 63, dans le slice →
écrasée sans réémission). Cf. dette B7 de `BUILD_READINESS_V1`.

---

## VOLET 2 — FIDÉLITÉ DE LA FORME (mise en forme)

Échantillon : `artifacts/_audit_tmp/scs_sample/statuts_scs.docx` (202 paragraphes, 1 table) vs modèle
source (289 paragraphes, 2 tables).

| Aspect | Source | Moteur (échantillon) | Verdict |
|---|---|---|---|
| **Logo / en-tête image** | **aucun logo** (0 inline_shape, pas de `header1.xml`, pas de `media/`, le « drawing » du XML = simple namespace) | aucun logo (header vide) | **fidèle** (rien à perdre — contrairement à SELARL) |
| **Titre encadré « STATUTS »** | table 1×1 bordée (sz=24), « STATUTS » gras centré ~18pt | **PERDU** : le moteur n'itère que `source_doc.paragraphs`, jamais les **tables** de la source → le titre n'apparaît nulle part | **perdu** |
| **En-tête (dénomination/forme/capital/siège/RCS)** | **CENTER**, Roboto 10pt, **dénomination grasse** | **JUSTIFY**, dénomination **non grasse** | **divergent** |
| **Titres TITRE I…VII** | bold, **JUSTIFY** | bold, **CENTER** | **divergent** (alignement) |
| **Titres ARTICLE 1…30** | bold, **NON soulignés** | bold, **soulignés** (`add_statuts_article_heading` underline défaut True) | **divergent** (souligné en trop) |
| **ARTICLE 21 & 22** | bold (espace insécable `ARTICLE\xa021`) | rendus en **corps justifié non gras** (le `startswith("ARTICLE ")` rate à cause du `\xa0`) → **perdent le style titre** | **divergent** |
| **Bloc identité associés** | JUSTIFY | alignement **None** (défaut gauche) | divergent (mineur) |
| **Grille de signature** | table 2×2 bordée (sz=4), centrée, mention italique « (Faire précéder de la mention « Lu et approuvé ») » + nom | table bordée centrée, « Lu et approuve » (italique) + nom **gras** ; mention **amputée** | **divergent** (wording mention + nom gras non source) |
| **Bordures de table** | présentes (titre sz=24, grille sz=4) | présentes (toutes sz=4) — épaisseur titre non répliquée car titre perdu | partiellement fidèle |
| **Police / taille** | Roboto 10pt (corps) ; 18pt (STATUTS) | Roboto 10pt (profil `DEFAULT_STYLE_PROFILE`) | **fidèle** (corps) |
| **Accentuation** | accentuée (é, è, à…) partout | **mixte** : paragraphes recopiés de la source **accentués**, blocs codés (apports/capital/signature) **désaccentués** (« constitue », « numeraire », « commandite », « Lu et approuve ») | **divergent** (incohérence visible) |
| **Marges** | (modèle) | L/R/T/B = 2,5 cm (`DEFAULT_STYLE_PROFILE`) — `STATUTS_CIVIL_COMPACT` existe mais **non appliqué** par ce chemin | non-vérifiable (marges source non comparées ici) ; à noter : profil compact disponible mais inutilisé |
| **Pied de page** | 2 paragraphes vides (source) | « SCS EXEMPLE - Statuts constitutifs » | divergent (ajout moteur, hors source) |
| **Numérotation articles/parts** | ARTICLE 1…30, parts numérotées par lots | identique côté articles ; parts numérotées dynamiquement (« Numérotées de 1 a 60 ») | **fidèle** |

---

## BLOQUANTS DE BUILD (avant de déclarer SCS « fidèle livrable »)
1. **Perte du titre « STATUTS »** : le moteur n'injecte jamais le titre encadré (jamais lu depuis les
   tables source). À corriger (réémettre un `add_statuts_title_box("STATUTS")` en tête).
2. **Wording inventé non sourcé** : « SOIT AU TOTAL … » (×2) + phrase dépôt banque reformulée +
   « Associés commanditaires » pluriel + mention « Lu et approuvé » amputée. À aligner sur la source
   verbatim, ou faire valider par Rafael (jamais inventer).
3. **Clause de fond perdue** : phrase capital-effectif + valeur nominale + numérotation globale +
   lignes de totaux. Réémettre ce wording source (assise juridique de la répartition).
4. **Désalignement des slices en dur** (`apport_slice`, `capital_slice`) : cause racine des
   duplications/suppressions. Sans garde de structure, toute réédition du DOCX source casse plus encore.
   Cf. dette B7 de `BUILD_READINESS_V1`.
5. **Dérives de forme** : en-tête CENTER + dénomination grasse, TITRE en JUSTIFY, ARTICLES **non
   soulignés**, ARTICLE 21/22 stylés comme titres, accentuation cohérente. À reprendre.

### Non bloquant / fidèle
- Nature SCS (civile/immobilière, capital variable, commandité/commanditaire, min 2 max 6, PM
  commanditaire) : **fidèle au montage NotebookLM** — aucune SCS d'exercice inventée.
- Logo : aucune perte (le modèle SCS n'en porte pas — contrairement à SELARL).
- ~90 % du corps : recopié verbatim de la source (contrôle anti-placeholder en sortie).

## Vérification effectuée (périmètre nommé)
- `pytest tests/unit/test_lot_04_statuts_civils.py -k "scs or SCS or commandit" --basetemp=artifacts/_audit_tmp/pt_scs`
  → **2 passed, 3 deselected** (périmètre SCS uniquement ; suite globale **non relancée**). Les 2 tests
  ne vérifient que la présence de « Associes commandites/commanditaires » et « Lu et approuve » — ils
  **ne détectent ni les inventions, ni les clauses perdues, ni la forme**.
- Échantillon généré et inspecté via python-docx ; modèle source inspecté en parallèle (paragraphes,
  tables, runs, alignements, bordures, en-tête, accents).
- Aucun fichier `.py` modifié. Aucune action Git.

## Sources lues (preuve)
- `project/source_documents/lot_04/Statuts_SCS_modele.docx`
- `src/sydel_doc_engine/generators/lot_04/statuts_scs.py`,
  `src/sydel_doc_engine/generators/lot_04/statuts_civils_common.py`,
  `src/sydel_doc_engine/rendering/docx_builder.py`
- `docs/project/types/SCS/NOTEBOOKLM_ANSWERS.md`, `NOTEBOOKLM_ANSWERS_RAW_V1.txt`,
  `BUILD_READINESS_V1.md`
- `tests/unit/test_lot_04_statuts_civils.py`
- Échantillon : `artifacts/_audit_tmp/scs_sample/statuts_scs.docx`
