# SPFPL — AUDIT DE FIDELITE V1 (FOND + FORME) — statuts cession + apport

> Date : 2026-06-07 · Auteur : auditeur de fidelite (lecture seule, aucun .py modifie, aucun commit, aucun git)
> Perimetre : les deux generateurs de **statuts** SPFPL ecrits par Codex (mai 2026) AVANT NotebookLM.
> Methode : (FOND) comparaison ligne a ligne generateur Codex vs modele source .docx vs synthese NotebookLM ;
> (FORME) generation d'un echantillon reel via les generateurs, puis comparaison de la mise en forme
> python-docx echantillon vs modele source.
> Cette version V1 **remplace** une version anterieure qui n'auditait que le FOND ; le volet FORME
> (logo / alignement / gras / police / tableaux) est ajoute ici, c'etait le trou de l'audit precedent.

## Fichiers audites (generateurs Codex)

- `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_cession.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_apport.py`
- `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_common.py` (renderer from-scratch `render_statuts_docx`)
- `src/sydel_doc_engine/generators/lot_04/statuts_spfpl_templates.py` (blocs verbatim)
- helper de rendu : `src/sydel_doc_engine/rendering/docx_builder.py`

## Modeles source de reference (verite juridique + mise en forme)

- `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx` (cession, numeraire, associe unique)
- `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx` (apport en nature de titres SEL)

## Verite metier croisee

- `docs/project/types/SPFPL/NOTEBOOKLM_ANSWERS.md` + `NOTEBOOKLM_ANSWERS_RAW_V1.txt`
- `docs/project/types/SPFPL/BUILD_READINESS_V1.md`

## Echantillon de sortie genere (volet FORME)

Generateurs invoques directement avec le contexte de `tests/unit/test_lot_04_statuts_spfpl.py` :
- `artifacts/_audit_tmp/spfpl_sample/statuts_spfpl_cession.docx`
- `artifacts/_audit_tmp/spfpl_sample/statuts_spfpl_apport.docx`

Tests cibles (**perimetre SPFPL uniquement, suite globale NON relancee**) :
`python -m pytest tests/ -k "spfpl"` -> **29 passed, 307 deselected**. Confirme le comportement code par
Codex, PAS la fidelite juridique NI la fidelite de mise en forme (cf. cadrage de la mission).

---

## VERDICT GLOBAL : **FIX** (FOND = KEEP avec FIX herites de la source ; FORME = FIX — 4 ecarts de mise en forme)

- **FOND : KEEP** (avec 4 FIX = coquilles de la source recopiees fidelement). Codex n'a **rien invente
  juridiquement** dans ces deux fichiers de statuts : il a **reconstruit verbatim** les deux DOCX source
  de `lot_04`, defauts compris. Aucune clause / duree / montant / regle metier fabriquee.
- **FORME : FIX**. Le rendu from-scratch perd plusieurs attributs de mise en forme presents dans le modele
  source : **centrage du bloc de titre** (denomination/capital/siege), **soulignement de "Le soussigne :"**,
  **gras de la ligne d'identite** et **gras des lignes de capital/total** (Art. 6 et 8). Aucun n'est
  bloquant juridiquement, mais ce sont de vraies divergences visuelles vs le modele Sydel.
- **Point logo (lecon UAT SELARL) : NON APPLICABLE ici.** Les deux DOCX source SPFPL **ne portent aucun
  logo reel** : la seule image est un **PNG 1x1 transparent (70 octets)** ancre en corps de page (et un
  footer vide). Le renderer SPFPL n'appelle pas `add_header_logo` — c'est **fidele** au modele (rien a
  perdre), contrairement a la SELARL ou le logo vivait dans l'en-tete. A surveiller si Rafael veut un
  en-tete de marque sur les statuts SPFPL (ce serait alors une evolution, pas une fidelite).

---

# VOLET 1 — FIDELITE DU FOND

## 1. STATUTS SPFPL CESSION (`statuts_spfpl_cession.py` + `STATUTS_SPFPL_CESSION_BLOCKS`)

**Modele source = `Statuts_SPFPLAS_dentistes_cession.docx`. Verdict article par article = KEEP integral.**

Reconstruction Codex **identique au DOCX source** sur en-tete + 40 articles + ANNEXE 1.

| Element | Source DOCX | Bloc Codex | Verdict |
|---|---|---|---|
| En-tete | "Societe de Participations Financieres de Profession Liberale de Chirurgiens-Dentistes par actions simplifiee" | identique | KEEP |
| Art. 1 Forme | "Il est forme, entre les proprietaires des actions ci-apres creees... ord. 2023-77... art. L227-20 c. com." | identique | KEEP |
| Art. 2 Objet | art. 110 ord. 2023-77, SEL chirurgiens-dentistes | identique | KEEP |
| Art. 3 Denomination | art. 111, mention "S.P.F.P.L.A.S." | identique | KEEP |
| Art. 5 Duree | 99 ans | identique | KEEP |
| Art. 6 APPORTS | apport associe unique + depot banque + retrait sur certificat greffe | identique | KEEP |
| Art. 8 Capital | "[capital] ([lettres]) euros, divise en [nb] actions de [vn]... attribue a l'associe unique" | identique | KEEP |
| Art. 9 Qualite d'associe | art. 114 ord. 2023-77 (moitie capital, 10 ans / 5 ans deces / R.4113-14) | identique | KEEP |
| Art. 10-18 | augmentation/reduction capital, liberation, indivisibilite, cession, agrement, exclusion | identiques | KEEP |
| Art. 19-22 President/DG/CAC/conventions | identiques | identiques | KEEP |
| Art. 23-31 decisions collectives / resultats / dividendes | identiques | identiques | KEEP |
| Art. 32-40 transfo / dissolution / contestations (R.4127-259 CSP) / constitution / nomination President | identiques | identiques | KEEP |
| ANNEXE 1 | "Ouverture compte / Lettre de mission Sydel / Acompte honoraires Sydel" | identique | KEEP |

**vs NotebookLM** : confirme l'orientation (SPFPLAS, President, actions ; commissaire aux apports ; ord.
2023-77). Aucun ACQUIS NotebookLM contredit par le generateur cession.

**Placeholders branches** : toutes les variables exigees (raise si absent) correspondent a un placeholder
reellement present dans le DOCX source. Pas de variable orpheline ni inventee.

## 2. STATUTS SPFPL APPORT (`statuts_spfpl_apport.py` + `STATUTS_SPFPL_APPORT_BLOCKS`)

**Modele source = `Statuts SPFPLAS dentistes - apport.docx`. Verdict = KEEP, avec coquilles source heritees.**

| Element | Source DOCX apport | Bloc Codex | Verdict |
|---|---|---|---|
| En-tete | "Societe par actions simplifiees au capital de [capital] euros / Societe de Participations Financieres de Profession Liberale de dentistes" | identique | KEEP |
| Art. 1 Forme | "Societe [forme_sociale]" + liste a puces (ord. 2023-77, c. com., CSP, deontologie R.4127-1) | identique | KEEP |
| Art. 6 APPORTS (nature) | "Apports en nature / [identite] fait apport de [nb] parts numerotees de [plage] de la SELARL [..] pour une valeur de [montant] / rapport commissaire aux apports annexe / Apports en numeraire : Neant" | identique | KEEP (cf. FIX-3) |
| Art. 8 Capital | "fixe a la somme de [montant] € [montant]euros, divise en [nb] actions..." | identique (incl. doublon) | KEEP (cf. FIX-1) |
| Art. 38 nomination President | identique | identique | KEEP |
| ANNEXE 1 | "Nomination d'un commissaire aux apports" | identique | KEEP |

**vs NotebookLM** : NotebookLM marque le parcours apport comme largement "NON TROUVE" (objet, Art. 6/8
apport, contrat d'apport, report 150-0 B ter, conditions suspensives). **Mais** pour les **statuts** apport,
le wording EST dans le DOCX source lot_04 (Codex l'a recopie) ; le "NON TROUVE" portait sur des **documents
satellites** (contrat d'apport lot_05, designation commissaire) et des points fiscaux **absents des statuts**.
=> Statuts apport = sources ; parcours apport complet (satellites lot_05) = a valider hors de ce fichier.

**Placeholders branches** : tous correspondent au DOCX source. Pas de variable inventee. Patch sain :
`_apport_blocks_with_contextual_siege` remplace `[adresse_siege]` par `[adresse_siege_societe_cible]` dans
la clause d'apport (sinon le siege de la cible afficherait celui de la SPFPL).

## 3. COMMON / RENDERER (`statuts_spfpl_common.py`)

Aucune **regle metier** ecrite. Deux comportements a connaitre (KEEP) :
- **Garde multi-associes** : leve une erreur si `len(associes) > 1` ou > 1 souscripteur ("statuts SPFPL
  multi-associes bloques en V1") — coherent (les deux DOCX sont mono-associe, multi non source).
- **`required_actionnaire_unique`** : retombe sur `cedant`/`apporteur` si `actionnaire_unique` absent
  (mapping, pas une regle juridique).

---

# VOLET 2 — FIDELITE DE LA FORME (echantillon genere vs modele source)

Methode : inspection python-docx de l'echantillon genere **et** du modele source, attribut par attribut.

## Tableau comparatif par aspect

| Aspect | Modele source (.docx) | Sortie moteur (echantillon) | Verdict |
|---|---|---|---|
| **Logo / en-tete** | AUCUN logo reel : seule image = **PNG 1x1 transparent 70 o** ancre en corps (para 61 inline + une image flottante mid-doc) ; en-tete vide ; footer vide | aucun logo, aucune image (`inline_shapes=0`, 0 pic en corps/en-tete/footer) | **fidele** (rien a perdre ; voir note logo) |
| **Police** | Roboto 10 pt (runs) | Roboto 10 pt (style Normal) | **fidele** |
| **Bloc de titre (denomination / capital / siege)** | **CENTER** | **JUSTIFY** (left-justified) | **divergent** |
| **"STATUTS"** | style `Heading 3`, **taille 12**, centre par le style | CENTER + **bold**, taille **10** (defaut) | **divergent** (taille 12->10 ; gras ajoute) |
| **"Le soussigne :"** | JUSTIFY + **souligne** | JUSTIFY, **non souligne** | **divergent** (soulignement perdu) |
| **Ligne d'identite "- [civilite] [prenom] [nom]"** | JUSTIFY + **gras** | rendu en item de liste, **non gras**, sans alignement | **divergent** (gras perdu) |
| **Titres d'ARTICLE** | **LEFT** + **gras**, non souligne | LEFT (defaut) + **gras**, non souligne | **fidele** |
| **Lignes de capital / total (Art. 6 "Total des apports" ; Art. 8 "- Le Docteur ... N actions" ; "Total des actions composant...")** | **gras** | **non gras** (JUSTIFY) | **divergent** (gras perdu) |
| **Tableaux encadres des grandes sections** (DECISIONS DES ACTIONNAIRES, RESULTATS SOCIAUX, TRANSFORMATION, DISSOLUTION-LIQUIDATION, CONTESTATIONS, CONSTITUTION) | 6 tableaux 1 cellule **bordures simples**, centre | reproduits en boxed tables **bordures simples**, centre | **fidele** (rendu) |
| **ANNEXE 1 / sous-titres annexe** | source : ANNEXE non boxee de la meme facon | moteur : **3 boxes separees** (ANNEXE 1 / ETAT DES ENGAGEMENTS / LA CONSTITUTION) | **divergent mineur** (sur-encadrement de l'annexe) |
| **Bloc signature** ("Fait a / Le / nom / Bon pour acceptation") | bas de page, mention italique | nom CENTER + mention **italique** preservee | **fidele** (mention italique OK) |
| **Tirets / puces / numerotation d'articles** | tirets "- " et numerotation "I./II./1°" du texte | preserves (items hanging-list) | **fidele** |
| **Marges** | T 2.82 / B 0 / L 0.74 / R 1.24 cm (apport L 0.74 / R 0) | T/B/L/R **2.5 / 2.5 / 2.5 / 2.5** (DEFAULT_STYLE_PROFILE) | **divergent mineur** (profil compact SPFPL non applique) |

### Cause technique des divergences de forme (lecture seule, pour info build)

- Le renderer `render_statuts_docx` (common) route chaque bloc par heuristique de texte : `STATUTS` ->
  centre+gras ; `_is_major_heading` -> box bordee ; `ARTICLE ` -> `add_statuts_article_heading(underline=False)` ;
  `- ` -> hanging list item ; sinon `add_statuts_body_paragraph` (**JUSTIFY**).
- Consequences directes : le bloc de titre (denomination/capital/siege) tombe en "body" donc **JUSTIFY**
  (source = CENTER) ; "Le soussigne :" tombe en "body" donc **sans soulignement** (source = souligne) ;
  la ligne d'identite et les lignes de capital tombent en list-item/body **sans gras** (source = gras).
- `render_statuts_docx` appelle `new_document()` **sans profil de style** -> `DEFAULT_STYLE_PROFILE`
  (marges 2.5) au lieu de `STATUTS_SPFPL_COMPACT_STYLE_PROFILE` qui existe dans `docx_builder.py` mais
  n'est jamais cable pour SPFPL -> marges divergentes.
- `add_header_logo` existe dans `docx_builder.py` mais n'est **jamais** appele par le renderer SPFPL.
  Ici ce n'est PAS un defaut (source sans logo) ; a garder en tete pour les types dont le modele porte un logo.

---

## INVENTE / DIVERGENT

### FOND — invente par Codex
**Aucune invention juridique Codex** dans les deux fichiers de statuts. Les "ecarts" signales par NotebookLM
sont des **divergences ENTRE SOURCES** (modeles SPFPLAS differents), pas des inventions :

- **DIV-A — Wording Art. 1.** DOCX dentistes (cession+apport) ouvre "Il est forme, entre les proprietaires
  des actions...". NotebookLM cite un autre verbatim ("La Societe est une Societe de Participations
  Financiere de Profession Liberale par Actions Simplifiee (SPFPLAS)..."). Deux modeles distincts ; Codex a
  suivi le DOCX dentistes. **A trancher Rafael : quel Art. 1 fait foi.**
- **DIV-B — Place des apports (Art. 6 vs 7).** NotebookLM : "en SAS les apports sont a l'Article 6". Le DOCX
  dentistes met APPORTS=Art.6 -> Codex **conforme au DOCX**. Pas un defaut.
- **DIV-C — "commissaire aux apports" vs "aux comptes".** Statuts apport disent "commissaire aux apports"
  (Art. 6, evaluation) ET conservent "ARTICLE 21 - COMMISSAIRES AUX COMPTES" (controle legal) : deux
  fonctions distinctes, pas de contradiction. Coherent avec l'arbitrage NotebookLM. KEEP.

### FORME — divergent vs modele source (mise en forme perdue/modifiee)
- **STYLE-1** Bloc de titre centre -> rendu JUSTIFY.
- **STYLE-2** "Le soussigne :" souligne -> rendu non souligne.
- **STYLE-3** Ligne d'identite en gras -> rendu non gras.
- **STYLE-4** Lignes de capital/total (Art. 6 & 8) en gras -> rendu non gras.
- **STYLE-5 (mineur)** "STATUTS" taille 12 -> rendu taille 10 (+ gras ajoute).
- **STYLE-6 (mineur)** marges compactes source -> rendu marges 2.5 par defaut.
- **STYLE-7 (mineur)** sur-encadrement de l'ANNEXE en 3 boxes.

Aucun wording de forme **invente** : le moteur n'ajoute pas de gras/souligne la ou la source n'en a pas
(sauf "STATUTS" passe en gras, et les box d'annexe). Les divergences sont des **pertes** d'attributs, pas
des ajouts trompeurs.

---

## FIX (FOND — coquilles HERITEES DE LA SOURCE, recopiees fidelement par Codex)

Defauts du **modele Sydel lui-meme**, pas des bugs Codex. A corriger dans la source/bloc sous validation
Rafael (modification de wording juridique).

- **FIX-1 (apport, Art. 8) — doublon de montant.** Source ET bloc :
  `"...fixe a la somme de [montant_apports_nature] € [montant_apports_nature]euros, divise en..."`.
  La valeur du capital apparait deux fois ("X € Xeuros") et le placeholder reutilise `[montant_apports_nature]`
  (valeur de l'apport) sans separation "euros". Defaut present dans le DOCX source. Rendu bancal. **A nettoyer.**
- **FIX-2 (apport, Art. 6) — collision de placeholder `[adresse_siege]`.** Dans le DOCX source apport, la
  clause d'apport reutilise le MEME token que le siege SPFPL. **Codex a deja patche** via
  `_apport_blocks_with_contextual_siege` -> `[adresse_siege_societe_cible]`. Correction saine ; **a confirmer
  correcte par Rafael.**
- **FIX-3 (apport, Art. 6) — "SELARL" fige en dur.** La clause d'apport ecrit "societe d'exercice liberal a
  responsabilite limitee... opposable a la SELARL... statuts modifies des SELARL". Fidele a la source mais
  **fige la cible en SELARL** ; pour un apport de titres d'une SELAS (titres = actions) ce wording serait
  faux. **A arbitrer Rafael** (parametrer forme cible / titres). Deja signale B5/B8 du BUILD_READINESS.
- **FIX-4 (cession, signature) — "Le" sans date.** Bloc cession : `'Fait a [lieu_signature]'` puis `'Le'`
  (sans placeholder de date), conforme au DOCX cession. La version apport a `'Le [date_signature]'`.
  Incoherence entre parcours **heritee des deux DOCX**. A uniformiser. Mineur, non bloquant.

Coquilles OCR source inoffensives recopiees : `c_m` au lieu de `et`, `1cr`/`2078 alinea 1cr`, `<lesdites`
(apport). A nettoyer au passage Rafael ; aucune incidence sur une regle metier.

## FIX (FORME — a porter si Rafael veut une fidelite visuelle stricte au modele)

- **FIX-F1** Centrer le bloc de titre (denomination / capital / siege) [STYLE-1].
- **FIX-F2** Souligner "Le soussigne :" [STYLE-2].
- **FIX-F3** Mettre en gras la ligne d'identite et les lignes de capital/total Art. 6 & 8 [STYLE-3, STYLE-4].
- **FIX-F4 (mineur)** Aligner "STATUTS" sur la taille 12 du modele [STYLE-5] ; cabler
  `STATUTS_SPFPL_COMPACT_STYLE_PROFILE` pour les marges [STYLE-6] ; revoir l'encadrement de l'ANNEXE [STYLE-7].

Ces FIX-F sont **techniques** (re-routage de blocs dans `render_statuts_docx` / `docx_builder`), sans impact
metier — mais touchent la couche de rendu partagee, donc a faire sous controle (ne pas casser les autres types).

---

## BLOQUANT POUR LE BUILD (a trancher avant de garder/livrer le type)

**FOND** — rien ne bloque la conservation du code (KEEP). Bloquants = validation metier / perimetre, deja
recenses dans `BUILD_READINESS_V1.md` (B1-B8) :
1. **Convergence Art. 1 (DIV-A)** + choix du modele de statuts faisant foi -> Rafael.
2. **FIX-1 a FIX-3** = corrections de wording juridique du modele -> Rafael (FIX-3 cible SELARL figee = le
   plus impactant pour un apport vers une SELAS).
3. **Parcours apport complet** (contrat d'apport, designation commissaire, report 150-0 B ter, conditions
   suspensives) -> NON couvert par les statuts ; a valider sur les satellites lot_05.
4. **Multi-associes statuts** : bloque V1 (non source). Aligne.
5. **SPFPL medecins** : statuts audites = dentistes uniquement ; route medecins sous SAS (B4).

**FORME** — non bloquant juridiquement. Les FIX-F sont des ameliorations de fidelite visuelle a confirmer
avec Rafael (le modele Sydel actuel est-il la reference visuelle a egaler exactement ?). Le **point logo**
n'est pas bloquant ici (source sans logo).

---

## Synthese pour le PM (1 ligne)

FOND **fidele** (Codex n'a rien invente juridiquement, il a recopie les deux DOCX dentistes ; restent 4 FIX
= coquilles du modele a faire valider Rafael, dont la cible figee "SELARL") ; FORME = **FIX** : le rendu
from-scratch **perd le centrage du titre, le soulignement de "Le soussigne", et le gras de l'identite et des
lignes de capital** vs le modele ; **pas de logo a perdre** ici (le modele SPFPL n'en a pas).
