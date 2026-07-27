# SCM — FIDELITY AUDIT V1 (audit de fidélité du générateur Codex — FOND + FORME)

Date : 2026-06-07 (rév. 2 — ajout du volet FORME / mise en forme)
Auditeur : auditeur de fidélité (lecture seule du code, écriture du seul présent rapport, aucune action Git)
Périmètre audité : `src/sydel_doc_engine/generators/lot_04/statuts_scm.py` (générateur Codex,
écrit en mai 2026 AVANT la passe NotebookLM) — document **Statuts SCM (DOC-025)** + son helper unique
`src/sydel_doc_engine/rendering/docx_builder.py`.
Méthode : extraction python-docx du modèle source + génération d'un échantillon réel (2 associés :
1 PM SELARL + 1 PP) + comparaison paragraphe par paragraphe ET attribut de mise en forme par attribut
(source ↔ rendu) + confrontation à la synthèse et au verbatim NotebookLM.

Sources de vérité utilisées :
- Modèle source tokenisé : `project/source_documents/lot_04/Statuts SCM.docx`
  (**269 paragraphes, 0 table, header AVEC logo SYDEL** ; police Roboto, corps 10 pt, titre STATUTS 20 pt).
- Synthèse métier : `docs/project/types/SCM/NOTEBOOKLM_ANSWERS.md` + verbatim `NOTEBOOKLM_ANSWERS_RAW_V1.txt`
  + `BUILD_READINESS_V1.md`.
- Pièces audit générées cette session :
  `artifacts/_audit_tmp/scm_source_paras.txt` (269 paragraphes source),
  `artifacts/_audit_tmp/scm_source_fmt.txt` (mise en forme source),
  `artifacts/_audit_tmp/scm_source_meta.txt` (header/footer/logo/police source),
  `artifacts/_audit_tmp/scm_sample/statuts_scm.docx` + `scm_sample_dump.txt` (échantillon généré, mise en forme).

---

## 0. VERDICT GLOBAL : **MIXED**
- **FOND : KEEP majoritaire + 2 FIX ciblés** (sur-spécification « représentée par … » dans apport + parts).
- **FORME : FIX (plusieurs divergences réelles, dont 1 GRAVE : LOGO PERDU).**

Le générateur Codex `statuts_scm.py` **n'invente PAS de structure ni de règle juridique**. Il rouvre le
DOCX source, itère ses 269 paragraphes et **ne reconstruit en code que 4 zones dynamiques** (comparution,
apports, répartition des parts, signatures) ; tout le reste (30 articles, 7 TITRES) est une **reprise
fidèle du texte source** avec remplacement des placeholders → **FOND = KEEP massif**.

MAIS le mode de reconstruction passe par les helpers `docx_builder` qui **ré-appliquent une mise en forme
« maison »** au lieu de conserver celle du source. Conséquence : la **mise en forme dérive sur plusieurs
points**, dont le plus grave est la **perte du logo SYDEL** de l'en-tête (exactement le piège UAT SELARL :
un générateur from-scratch qui ne recopie jamais le header du modèle). **FORME = FIX.**

Réserve de gouvernance : **36 tests `-k scm` verts cette session** (`--basetemp=artifacts/_audit_tmp/pt_scm`,
**périmètre SCM uniquement — suite globale NON relancée**). Ces tests ne contrôlent QUE du texte (présence
de chaînes, `[`/`]` absents, italique de la mention) : **aucun n'assert le logo, l'alignement, le gras/
souligné des titres, la police ou la taille**. Ils ne prouvent donc NI la fidélité juridique NI la fidélité
de mise en forme — et l'un d'eux **fige même la divergence de fond D2** (`"SELARL DURAND, représentée par
Monsieur Jean Durand 70 parts"`).

---

## 1. Architecture du générateur (constat technique)

`StatutsScmGenerator.generate()` :
1. `new_document()` → document VIERGE (style Roboto 10 pt). **`add_header_logo` n'est JAMAIS appelé** (vérifié
   par recherche : 0 occurrence dans `statuts_scm.py`, alors que `lot_03/appel_fond_sel.py` et
   `lot_05/courrier_sde_cession_scm.py`, eux, l'appellent). Le footer est posé en texte (« … - Statuts
   constitutifs »).
2. charge le DOCX source, itère ses 269 paragraphes ;
3. sur 4 index DE DÉBUT codés en dur, **saute** une tranche source et **injecte** un bloc dynamique :
   - `ASSOCIATE_SLICE = (25, 42)` → comparution multi-associés (PP/PM) ;
   - `APPORT_SLICE = (81, 90)` → Article 6 Apports (montants + dépôt banque) ;
   - `CAPITAL_SLICE = (95, 100)` → Article 7 répartition des parts ;
   - `SIGNATURE_SLICE = (262, 269)` → bloc de signatures.
4. pour tout autre paragraphe : `text = paragraph.text.strip()` → on ne lit QUE le TEXTE du source, **jamais
   son alignement, son gras, sa taille, son style Word** ; puis remplacement des placeholders, puis
   re-rendu via `_add_rendered_paragraph` qui **ré-attribue une mise en forme reconstruite** (titre encadré,
   article bold+souligné, etc.).
5. garde-fou : lève une erreur si un `[` ou `]` survit (anti-fuite de placeholder).

**Point clé pour la FORME** : comme l'étape 4 ne conserve que `paragraph.text`, **toute la mise en forme du
modèle source est jetée puis reconstruite à la main**. C'est la racine technique des divergences de forme.

---

## 2. VOLET FOND — Audit par bloc (KEEP / FIX / REBUILD)

### 2.1 En-tête / page de garde (source 2-15) — **KEEP (fond)**
Dénomination, forme sociale, capital, siège, « STATUTS », forme + dénomination courte : texte fidèle
(placeholders remplacés). NotebookLM ne contredit pas. (Réserves de FORME : voir §3.)

### 2.2 Comparution « ENTRE LES SOUSSIGNÉS » (slice ASSOCIATE) — **KEEP (fond)**
- Titre pluriel « ENTRE LES SOUSSIGNÉS : » conservé → conforme couche multi NotebookLM.
- PM : dénomination / « [forme] de [profession] » / capital / siège / RCS / « Représentée par … en sa
  qualité de … ». Conforme source (25-30) ET verbatim NotebookLM PM.
- PP : civilité+prénom+nom / « [profession] de profession » / « Né(e) le … à … » (genre dérivé) /
  « Demeurant … » / « De nationalité … » / situation maritale. Conforme source (36-41) ET NotebookLM PP.
- Séparateur « ET » (centré, gras) conforme source (33). Généralisation propre à N associés sans invention
  de wording = la « couche multi » demandée. **KEEP.**

### 2.3 TITRE I — Articles 1 à 5 — **KEEP (fond)**
- Art. 1 : références « art. 36 loi n°66-879 du 29 nov. 1966 », « art. 1832 à 1870-1 code civil » **reprises
  du source, non inventées**.
- Art. 5 Durée : « 99 ans » **écrit en dur dans le source (para 73)** → repris, pas inventé. NotebookLM :
  « 99 ans = pratique, non cité verbatim (confirmable) » → le source le cite, donc KEEP, reste un point
  Rafael (§5).

### 2.4 TITRE II — Article 6 Apports (slice APPORT) — **FIX (divergence de fond D1)**
- **Codex produit** : « SELARL DURAND, **représentée par Monsieur Jean Durand** apporte à la Société la somme
  de sept cents euros / ci- 700. » puis « Madame Alice Martin apporte … cinq cents euros / ci- 500. »
- **Source (81-85)** : « **La** [dénomination] apporte à la Société la somme de [montant lettres] ci- [montant]. »
- **NotebookLM** : PM « **La société** [Dénom SEL], apporte à la société la somme de [Montant] euros. » ;
  PP « Le Docteur [Nom Prénom], apporte… ».
- **Divergences (PM)** : (1) Codex **AJOUTE « , représentée par [civilité prénom nom] »** — absent du source ET
  de NotebookLM dans la ligne d'apport ; (2) Codex **perd le préfixe « La / La société »**.
- **Verdict FIX** : ligne d'apport PM = « La société [dénomination], apporte à la Société la somme de … »
  SANS représentant. Ligne PP = source-fidèle (KEEP) ; « Le Docteur [Nom] » + « Le Docteur » féminin =
  confirmable Rafael (NON TROUVÉ).
- KEEP du même bloc : remplacement correct du résidu source « ci- 510 € » par le montant réel ; « Total des
  apports … » fidèle (87) ; clause de dépôt banque fidèle source (89, plus étoffée que la variante NotebookLM
  → on garde le source).

### 2.5 TITRE II — Article 7 Capital / répartition des parts (slice CAPITAL) — **FIX (divergence de fond D2)**
- **Codex produit** : « … / SELARL DURAND, **représentée par Monsieur Jean Durand** 70 parts / Madame Alice
  Martin 50 parts / Total … : 120 parts ».
- **Source (92-99)** : « … [dénomination][nb] parts / [civilité prénom nom][nb] parts / Total … : [nb] parts ».
- **NotebookLM (Art. 8)** : « … attribuées de la façon suivante : * [Civilité Nom Prénom] : [N] parts *
  **La société [Dénom SEL] : [N] parts**. Soit au total : [Total] parts. » + numérotation « parts n°1 à X ».
- **Divergences** : (1) même sur-spécification « , représentée par … » sur la ligne PM (absente source +
  NotebookLM) → **FIX** ; (2) séparateur entité↔nombre : NotebookLM met « : », source colle les placeholders,
  Codex met un espace → confirmable mineur.
- KEEP / confirmables : « divisé en N parts de [valeur] chacune » fidèle source (terse) — le membre
  « parts SOCIALES … intégralement libérées, souscrites et attribuées » + la **numérotation « parts n°1 à X »**
  décrits par NotebookLM sont **ABSENTS du source ET du rendu** → Codex ne les a PAS inventés ; enrichissement
  à trancher Rafael. Contrôle somme-parts == nb_parts_total et somme-apports == capital = validation interne
  saine (pas du wording) → KEEP.

### 2.6 Articles 8 à 13 (Augmentation, Droits, Cessions, Retrait, Décès) — **KEEP (fond)**
Copie fidèle source (101-156). Agrément à l'unanimité, délais 2/6 mois, expertise art. 1843-4, continuation
après décès « un an » : reprises du source, non inventées. Renvois inter-articles cohérents.

### 2.7 TITRES III à VII — Articles 14 à 30 — **KEEP (fond)**
- Art. 14 Gérance : vocabulaire **GÉRANT** (jamais Président) → conforme consigne SCM NotebookLM.
- Art. 15-18 (assemblées, PV, quorum 3/4, majorités détaillées), Art. 19-22 (exercice 1er janv.–31 déc.,
  comptes, ressources, contribution art. 1857), Art. 23-26 (prorogation/transformation/dissolution/
  liquidation), Art. 27-30 (conciliation Conseil départemental, contre-lettre, élection domicile,
  communication art. L. 4113-9 CSP) : **tous repris verbatim du source, non inventés.** KEEP.

### 2.8 Bloc signatures (slice SIGNATURE) — **KEEP (fond), réserve mineure**
Texte conforme source (262-268) ET NotebookLM (une ligne par associé + mention « Lu et approuvé »).
Réserve : le source laisse « Le » VIDE (date manuelle) ; Codex **remplit** la date (« Le 15/05/2026 ») →
choix produit cohérent à confirmer (NotebookLM ne tranche pas). `_validate_signatures` exige que TOUS les
associés soient signataires.

---

## 3. VOLET FORME — Audit par aspect (fidèle / divergent / perdu / non-vérifiable)

Comparaison de l'échantillon généré (`scm_sample/statuts_scm.docx`) au modèle source.

### 3.1 Logo / en-tête de marque — **PERDU (GRAVE)**
- **Source** : header NON lié au précédent, **2 `w:drawing` dont 1 image** = le **logo SYDEL** vit dans
  l'en-tête de page (body = 0 drawing). Vérifié sur `scm_source_meta.txt`.
- **Rendu** : header `is_linked_to_previous = True`, **0 drawing** → **AUCUN logo**. Le générateur n'appelle
  jamais `add_header_logo` (helper pourtant disponible, `assets/logo_sydel.png` présent, et utilisé par
  d'autres générateurs).
- **Verdict : PERDU.** C'est EXACTEMENT le défaut UAT SELARL. **Correctif trivial** : appeler
  `add_header_logo(output_doc)` après `new_document()`. → **bloquant qualité de livraison.**

### 3.2 Page de garde (denomination / forme / capital / siège) — **DIVERGENT**
- **Source** (para 2-5) : **alignement CENTER** ; denomination en **gras** ; les 4 lignes en **20 pt** (les runs
  de la couverture et de STATUTS sont à 254000 EMU = 20 pt).
- **Rendu** (para 0-3) : **alignement JUSTIFY**, denomination **non gras**, **tout en 10 pt**.
- **Verdict : DIVERGENT** sur alignement (centre→justifié), gras (perdu) et taille (20→10 pt). La couverture
  ne ressemble plus à la page de garde du modèle.

### 3.3 Titre « STATUTS » — **DIVERGENT (encadré inventé)**
- **Source** : « STATUTS » = **texte centré, gras, 20 pt, SANS bordure** (le DOCX source a **0 table**).
- **Rendu** : « STATUTS » placé dans une **table 1×1 bordée** (`add_statuts_title_box` → `Table Grid` +
  bordures) à 10 pt.
- **Verdict : DIVERGENT.** Codex **ajoute un encadré qui n'existe pas dans le modèle** et perd la taille 20 pt.
  (C'est aussi la seule table du rendu — voir 3.8.)

### 3.4 Titres d'articles (« Article N – … ») — **DIVERGENT (souligné inventé)**
- **Source** : titres d'articles **gras, NON soulignés** (`run.underline = None`), souvent style Word
  « Heading 1 ».
- **Rendu** : `add_statuts_article_heading(..., underline=True)` → **gras + SOULIGNÉ** (vérifié sur tous les
  Articles 1-30 du dump : `b=True,u=True`).
- **Verdict : DIVERGENT.** Le souligné des titres d'articles est **ajouté par Codex**, absent du modèle.

### 3.5 Titres de parties (« TITRE I … VII ») et sous-titres — **DIVERGENT (sous-titre)**
- **TITRE I…VII** : source = gras, centré, non souligné ; rendu = gras, centré, non souligné → **fidèle.**
- **Sous-titre de TITRE I** (« FORME ‐ DENOMINATION ‐ SIEGE ‐ OBJET – DURÉE », source para 53) : source =
  **CENTER, gras** ; rendu (para 23) = **JUSTIFY, non gras** → **DIVERGENT** (et idem pour
  « APPORTS ‐ CAPITAL SOCIAL ‐ PARTS SOCIALES »). Cause : ces sous-titres ne commencent ni par « TITRE » ni
  par « Article », donc Codex les traite en corps justifié.

### 3.6 Police / taille — **MIXTE**
- **Corps** : source Roboto 10 pt ; rendu Roboto 10 pt → **fidèle.**
- **Titres** (couverture, STATUTS) : source 20 pt ; rendu 10 pt → **DIVERGENT / perdu** (cf. 3.2 / 3.3).

### 3.7 Gras / souligné / italique sur les bons runs — **MIXTE**
- Italique de la mention « Lu et approuvé » : **fidèle** (test l'asserte).
- « ET » séparateur centré gras : **fidèle.**
- Gras des titres d'articles : présent mais **+ souligné parasite** (3.4) → divergent.
- Gras de la denomination de couverture : **perdu** (3.2).

### 3.8 Tableaux — **DIVERGENT (table inventée)**
- **Source** : **0 table.**
- **Rendu** : **1 table** = l'encadré « STATUTS » (`Table Grid`, bordures présentes). → **DIVERGENT**
  (la table n'existe pas dans le modèle).

### 3.9 Alignement / indentation des blocs comparution-apports-parts — **DIVERGENT (mineur)**
- **Source** : comparution PM/PP en **JUSTIFY** avec **retrait gauche** (≈ 0,5-0,7 cm) ; apports/parts idem
  avec léger retrait et tabulations.
- **Rendu** : blocs injectés en **alignement par défaut (None ≈ gauche), sans retrait** ; tabulations source
  remplacées par un simple espace.
- **Verdict : DIVERGENT mineur** (lisible, pas de faux juridique, mais mise en page différente du modèle).

### 3.10 Espacement / numérotation — **MIXTE**
- Numérotation des articles (1→30) et des TITRES (I→VII) : **fidèle** (texte repris du source).
- Numérotation « parts n°1 à X » (NotebookLM) : **absente** du source ET du rendu (non-vérifiable côté forme ;
  confirmable Rafael côté fond, §5).
- Espacement : `space_after` uniforme (≈ 6 pt) vs source variable ; non bloquant.

### 3.11 Bloc de signatures (mise en page) — **DIVERGENT (mineur)**
- **Source** (266-268) : deux colonnes côte à côte séparées par des tabulations (signataire 1 | signataire 2),
  mention italique « Lu et approuvé » entre parenthèses.
- **Rendu** : signataires **empilés verticalement, centrés**, mention italique « « Lu et approuvé » ».
- **Verdict : DIVERGENT mineur** (le contenu est fidèle ; la disposition 2 colonnes du modèle n'est pas
  reproduite — choix de généralisation à N signataires, acceptable).

---

## 4. Inventé / divergent (présent dans le code, ABSENT du source ET de NotebookLM)

Recherche ciblée du « danger maximal ».
- **FOND** : **aucune règle métier, durée, montant ou clause inventée.** Le seul écart de fond est la
  **sur-spécification « représentée par [civilité prénom nom] »** dans les lignes d'APPORT (D1) et de
  RÉPARTITION DES PARTS (D2) d'une personne morale — wording **hors place** (le représentant n'existe, dans le
  modèle, qu'en comparution et en signature). Gravité moyenne → FIX, pas rebuild.
- **FORME** (éléments de mise en forme ajoutés par Codex, absents du modèle) :
  - **Encadré bordé autour de « STATUTS »** (table 1×1 `Table Grid`) → le modèle n'a aucune table.
  - **Souligné des titres d'articles** → le modèle a des titres gras NON soulignés.
  Ces deux-là sont du « décor inventé » côté forme (pas du fond juridique), mais ils **éloignent visuellement
  le rendu du modèle Rafael**.

---

## 5. Bloquant pour le build (à trancher avant de garder/livrer SCM)

Métier/juridique → **Rafael via Gad** (jamais à inventer) ; technique → équipe.

1. **[FORME — bloquant qualité, technique] LOGO PERDU.** Rétablir le logo SYDEL en en-tête
   (`add_header_logo(output_doc)`). Correctif trivial, aucun arbitrage métier requis. **À builder dès GO.**
2. **[FORME — technique] Page de garde + STATUTS** : restaurer alignement CENTER, gras et taille 20 pt de la
   couverture ; **retirer l'encadré table** autour de STATUTS (le modèle = texte centré nu).
3. **[FORME — technique] Souligné des titres d'articles** : aligner sur le modèle (gras seul, **sans
   souligné**) — sauf si Rafael préfère explicitement le souligné (cosmétique, défaut = suivre le modèle).
4. **[FORME — technique] Sous-titres de TITRE** : rendre « FORME ‐ DENOMINATION … » / « APPORTS ‐ CAPITAL … »
   en CENTER gras (comme le source) au lieu de JUSTIFY.
5. **[FIX FOND — confirmable Rafael] D1/D2** : retirer « , représentée par … » des lignes d'apport et de
   répartition des parts d'une SEL associée (revenir à « La société [dénomination] … »). Source + NotebookLM
   concordent. **Met à jour le test** qui fige `"SELARL DURAND, représentée par Monsieur Jean Durand 70 parts"`.
6. **[Confirmable Rafael] « Le Docteur [Nom] »** ligne d'apport PP : NotebookLM le suggère, le source ne
   l'écrit pas, féminin « Le Docteur » = NON TROUVÉ → garder la version source tant que non tranché.
7. **[Confirmable Rafael] Wording Art. 7/8 capital** : source terse vs NotebookLM (« parts sociales …
   intégralement libérées, souscrites et attribuées » + numérotation « parts n°1 à X »). Décider statu quo
   source vs enrichissement NotebookLM.
8. **[Métier — Rafael] Borne associés** : statuts scalent 1→6 (`MAX_ASSOCIES = 6`), mais SCM = **min 2**
   (NotebookLM) ; les 4 satellites exigent exactement 2 (B2 BUILD_READINESS). Bloquer < 2 au niveau statuts ?
9. **[Confirmable] Date de signature** pré-remplie (Codex) vs manuelle (source « Le » vide).
10. **[Technique, équipe] Dette index en dur** : les 4 slices sont des **entiers** dans le DOCX source —
    toute réédition du modèle (ajout/suppression d'un paragraphe vide) **décale silencieusement** les
    tranches → injection au mauvais endroit / fuite de placeholders source. Le garde-fou anti-`[` n'attrape
    qu'une partie. Ancrer les slices sur des marqueurs textuels (« Article 6 », « Total des apports »,
    « Fait à »). (B5 BUILD_READINESS.)
11. **[Mise en forme mineure] Capital affiché brut** : `capital_social="1200"` → « Au capital de 1200euros »
    (sans espace) et « … fixé à la somme de 1200 » (sans « euros » ni séparateur de milliers). Le champ
    attend une chaîne déjà formatée (« 1 200 euros ») mais rien ne le contraint. Hérité du source.

**Rappel de gouvernance** : aucune passe NotebookLM SCM n'avait validé ce générateur à sa création (Codex
avant NLM). Le FOND est globalement fidèle ; la FORME doit être corrigée (logo + couverture + titres) ; les
confirmables 5-9 restent à Rafael avant de déclarer SCM « livrable ». Conforme au registre canonique qui
interdit de dire « SCM terminée » sans retour humain.

---

## 6. Vérification effectuée (périmètre nommé)

- Modèle source `Statuts SCM.docx` extrait intégralement (269 paragraphes, 0 table) + métadonnées header/
  footer/logo/police via python-docx → `artifacts/_audit_tmp/scm_source_paras.txt`, `scm_source_fmt.txt`,
  `scm_source_meta.txt`.
- Échantillon réel généré (1 PM SELARL + 1 PP) via `StatutsScmGenerator` →
  `artifacts/_audit_tmp/scm_sample/statuts_scm.docx` + `scm_sample_dump.txt` (comparaison attribut par
  attribut : alignement, gras, souligné, italique, police, taille, tables, header).
- Verbatim NotebookLM (`NOTEBOOKLM_ANSWERS_RAW_V1.txt`) + synthèse + `BUILD_READINESS_V1.md` confrontés sur
  apports, capital/parts, comparution, signatures, genre, gérance, périmètre.
- **36 tests `-k scm` lancés cette session** (`--basetemp=artifacts/_audit_tmp/pt_scm`) → **36 verts, sur le
  seul périmètre SCM** (suite globale NON relancée). Constat : ces tests ne contrôlent aucun attribut de mise
  en forme (logo, alignement, souligné, taille) et un test fige la divergence de fond D2.
- AUCUN fichier `.py` modifié. AUCUNE action Git. Seul fichier écrit : le présent rapport.
