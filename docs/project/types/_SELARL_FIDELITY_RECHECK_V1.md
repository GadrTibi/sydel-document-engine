# SELARL — Re-check de fidélité FOND + FORME (V1)

> Audit read-only daté **2026-06-07**. Aucun `.py` modifié. Objectif : la SELARL — seul type
> validé par Rafael — souffre-t-elle de la même cause racine que les 5 autres types audités
> (générateurs « from-scratch » qui reconstruisent le doc et perdent logo / footers / mise en
> forme / réinjectent des blocs qui inventent) ?
>
> Périmètre code : `generators/lot_04/statuts_selarl_medecin.py`, `statuts_selarl_dentiste.py`,
> `statuts_sel_exercice_common.py`, `statuts_sel_exercice_templates.py`,
> `rendering/docx_builder.py`. Modèles source : `project/source_documents/lot_04/Modèle statuts
> SELARL médecins.docx` et `Modele statuts SELARL chirurgien dentiste sans communaute.docx`.
> Échantillon généré : via `_context()` du test `tests/unit/test_lot_04_statuts_sel_exercice.py`
> (médecin + dentiste). Suite ciblée `pytest -k selarl` : **41 passed, 295 deselected** (sans DB).

---

## 1. Verdict global

**La SELARL est bâtie sur la MÊME architecture « from-scratch » que les 5 autres types** — elle
n'ouvre PAS le `.docx` source, elle reconstruit le corps paragraphe par paragraphe via
`docx_builder` à partir de tuples de texte (`*_BLOCKS`). La cause racine d'architecture est donc
**identique**. MAIS, contrairement aux 5 autres, la SELARL n'est **pas réellement abîmée** par
cette cause, pour deux raisons concrètes :

1. **FOND blindé** : le texte des `*_BLOCKS` est transcrit **verbatim** du modèle source, et un
   test (`test_statuts_selarl_medecin_matches_source_docx_line_by_line`) **épingle** le corps
   généré au modèle source ligne par ligne (à partir d'ARTICLE 1). Aucun bloc ne paraphrase ni
   n'invente.
2. **Les modèles source SELARL ne portent PAS de logo** : pas de logo à perdre. Le piège « logo
   perdu » qui a frappé la SCM ne s'applique tout simplement pas ici.

- **Verdict FOND : FIDÈLE (keep).** Verbatim, 0 invention, épinglé par test.
- **Verdict FORME : MAJORITAIREMENT FIDÈLE, avec UN écart réel (footer médecin) + 2 angles morts non testés.**

| Axe | SELARL médecin | SELARL dentiste |
|---|---|---|
| Logo / image d'en-tête | ✅ n/a (aucun logo dans le source) | ✅ n/a (aucun logo dans le source) |
| Footer | ❌ **PERDU** (source = pagination + « Statuts [denomination] ») | ✅ n/a (footers source vides) |
| Titre encadré « STATUTS » | ✅ sans bordure (= source) | ✅ avec bordure (= source) |
| Police | ✅ Roboto (profil moteur = source) | ✅ Roboto |
| Marges | ✅ 2,5 cm (= source) | ✅ 2,5 cm (= source) |
| Gras / souligné des titres ARTICLE | ✅ gras+souligné (cohérent) | ✅ gras+souligné (cohérent) |
| Tirets / listes à puce | ✅ tirets pendants rendus | ✅ idem |
| Alignement du corps | ⚠️ uniformisé en justifié par le moteur (source médecin = justifié, OK) | ⚠️ source mixte (paragraphes sans alignement explicite) — non strictement répliqué |

---

## 2. FORME (le point clé)

### 2.1 Logo / en-tête — AUCUN logo dans les modèles SELARL → rien à perdre

Inspection des deux `.docx` source (python-docx + lecture du zip) :

- `inline_shapes` (images dans le corps) = **0** dans les deux modèles.
- `word/media/` = **vide** dans les deux (aucune ressource image embarquée).
- En-têtes : médecin = **aucune** partie header ; dentiste = 3 headers **vides** (0 image, 0 texte).
- Le moteur ne pose pas de logo non plus (`render_statuts_sel_docx` part de `new_document()`,
  jamais `add_header_logo`). **Cohérent** : il n'y a pas de logo à reproduire.

**Conséquence** : `add_header_logo` existe et est appelé sur d'autres docs (lot_03
`appel_fond_sel.py`, lot_05 `courrier_sde_cession_scm.py`) — mais **PAS** dans les statuts SELARL,
et c'est **correct** ici car les modèles statuts SELARL n'ont jamais porté de logo. Le drame SCM
(« LOGO SYDEL perdu », cf. board) n'a **pas** d'équivalent SELARL.

### 2.2 Footers — UN écart réel, côté MÉDECIN

- **Modèle médecin** : `word/footer1.xml` et `footer3.xml` portent un footer **non vide** :
  un champ `PAGE` (numérotation, aligné à droite, Roboto 8 pt) **et** une ligne
  « **Statuts [denomination_societe]** » (Roboto 8 pt, à gauche).
- **Doc généré médecin** : footer **vide**, **aucun champ PAGE**. → **footer source PERDU** :
  plus de pagination, plus de mention « Statuts <dénomination> » en pied de page.
- **Modèle dentiste** : footers **vides** (0 texte, 0 champ PAGE) → le moteur produit aussi un
  footer vide → **conforme** (rien à reproduire).

C'est le **seul écart de forme strictement avéré** vs source. Il touche uniquement le médecin.
À noter : les autres générateurs lot_04 (SCI/SAS/SCM via `statuts_civils_common.py`, `statuts_sas.py`,
`statuts_scm.py`) **réinjectent** explicitement un texte de footer (`sections[0].footer.paragraphs[0].text = ...`) ;
les générateurs SELARL, eux, **n'en posent aucun** → c'est un oubli de patch par-document, pas une
décision documentée.

### 2.3 Titre encadré « STATUTS » — FIDÈLE (bordure différenciée par overlay)

- Médecin source : table 1×1 « STATUTS » **sans bordure** (style None). Moteur :
  `title_box_bordered=False` → table 1×1 sans bordure (`Normal Table`). ✅
- Dentiste source : table 1×1 « STATUTS » **bordée** (`Table Grid`). Moteur : défaut
  `title_box_bordered=True` → `Table Grid`. ✅
- Le « titre encadré perdu » subi par la SCS n'a **pas** d'équivalent SELARL : le moteur restitue
  bien l'encadré, et même la nuance bordé/non-bordé selon le métier.

### 2.4 Police, marges, gras/souligné, tirets

- Police : modèles source en **Roboto** ; profil moteur (`DEFAULT_STYLE_PROFILE`) = **Roboto 10 pt**.
  ✅ Aligné. (médecin source : runs explicitement à 10 pt ; dentiste : hérité du style Normal.)
- Marges : source = 2,5 cm sur les 4 côtés ; moteur = 2,5 cm. ✅
- Titres ARTICLE : générés en **gras + souligné** (`add_statuts_article_heading`). Le source met
  gras+souligné sur la plupart des ARTICLE (quelques-uns du source médecin sont gras seul, ex.
  ARTICLE 1 « FORME » apparaît gras+souligné dans le rendu généré alors que le run source est
  parfois gras seul) → **harmonisation cosmétique mineure**, non bloquante, plutôt plus propre.
- Tirets / listes : `add_statuts_hanging_list_item` rend les items « - … » en retrait pendant. ✅

### 2.5 Alignement du corps — divergence cosmétique mineure

`add_statuts_body_paragraph` force `JUSTIFY` sur tout le corps. Le source médecin est **déjà
justifié** → conforme. Le source dentiste a beaucoup de paragraphes **sans alignement explicite**
(hérité Normal) ; le moteur les met en justifié → **uniformisation**, pas une perte d'info portée
par le source. Impact visuel faible. Non testé formellement (le test FOND ne compare que le texte).

---

## 3. FOND — FIDÈLE (verbatim, épinglé par test)

- Les `STATUTS_SELARL_MEDECIN_BLOCKS` / `STATUTS_SELARL_DENTISTE_BLOCKS` sont une transcription
  **mot pour mot** des paragraphes du modèle source (vérifié par recoupement
  paragraphe-source ↔ bloc-template : libellés, ponctuation, numéros d'ordonnance, mojibake-safe).
- Le test `test_statuts_selarl_medecin_matches_source_docx_line_by_line` **compare le corps généré
  au `.docx` source ligne par ligne** (de ARTICLE 1 à la fin, après normalisation des espaces et
  application des mêmes substitutions). Il **passe**. C'est une garantie anti-dérive forte que les
  5 autres types n'ont pas au même niveau.
- Garde-fou « pas de placeholder résiduel » : `render_statuts_sel_docx` lève si `[` ou `]`
  subsiste dans le rendu → impossible de livrer un token non remplacé.
- Accords de genre (« LE SOUSSIGNÉ » → « LA SOUSSIGNÉE », « né le » → « née le ») pilotés par
  `apply_gender_pairs` sur des chaînes **littérales ancrées** (pas de regex de terminaison) →
  pas de désaccentuation/invention.
- **Réserve de périmètre** : le test ligne-par-ligne ne couvre que le médecin **et** ne pince que
  la partie **ARTICLE 1 → fin**. Le **bloc de page de titre** (dénomination, forme, capital, siège,
  ligne « LE SOUSSIGNÉ », ligne d'identification) et **tout le dentiste** ne sont pas épinglés par
  un test ligne-par-ligne équivalent — ils restent fidèles par lecture manuelle, mais sans filet
  automatisé. Angle mort de **couverture de test**, pas une divergence constatée.

---

## 4. Comparaison aux 5 autres types

| Type | Architecture | FOND | FORME | Logo |
|---|---|---|---|---|
| **SELARL** | from-scratch (`*_BLOCKS`) | **keep** (verbatim, **test ligne-par-ligne**) | quasi-fidèle, **1 écart : footer médecin** | n/a (pas de logo source) |
| SELAS | from-scratch | keep | FORME fix (footers/gras/centrage), incomplet | — |
| SPFPL | from-scratch | keep | FORME fix | — |
| SCM | from-scratch | keep +2 fix | FORME fix **+ LOGO SYDEL perdu** | logo source → perdu |
| SCI | from-scratch (ouvre le source en partie) | **FOND fix** (blocs réinjectés inventent) | FORME fix | — |
| SCS | from-scratch | **FOND fix** (blocs inventent/suppriment) | FORME fix (**titre encadré perdu**) | — |

**Conclusion comparative** : la SELARL est **nettement plus propre** que les 5 autres, et c'est
**directement attribuable au travail UAT Rafael** :

- son FOND est **épinglé par test** (les autres ont dû être corrigés : SCI/SCS inventaient) ;
- ses pièges de forme spécifiques **ne s'appliquent pas** (pas de logo source → pas de « logo
  perdu » ; titre encadré correctement restitué, y compris la nuance bordé/non-bordé) ;
- il ne lui reste qu'**un** écart de forme réel (footer médecin) et **deux angles morts non testés**
  (alignement dentiste, couverture test page-de-titre + dentiste).

La cause racine d'**architecture** (rebuild from-scratch) est **partagée** ; mais l'**impact** sur
la SELARL est résiduel parce que les patchs par-document UAT + le test de fidélité ont colmaté ce
qui comptait.

---

## 5. Conclusion actionnable

La SELARL est **réellement « fidèle FOND »** (verbatim, testé) et **« fidèle FORME » à une exception
près**. Le « c'est bon pour la SELARL » de Rafael **tient** sur le fond et sur l'essentiel de la
forme, mais **un détail de pied de page médecin** est passé sous le radar (peu visible à l'écran,
visible à l'impression / sur le PDF paginé).

Quand on fera le **fix systémique de rendu** (préservation du modèle source plutôt que rebuild
from-scratch), il faudra **inclure la SELARL** dans le périmètre — non pas pour réparer une casse
grave, mais pour :

1. **Restaurer le footer médecin** : pagination (`PAGE`) + ligne « Statuts <dénomination> » (le
   modèle source la porte ; le moteur ne la pose pas). C'est le **seul correctif de forme dû**.
   *(Patch léger possible sans attendre le fix systémique : poser le footer dans le générateur
   médecin, comme le font déjà SCI/SAS/SCM — décision technique, pas un arbitrage métier.)*
2. **Étendre la garantie de test** : ajouter un équivalent ligne-par-ligne **dentiste** et étendre
   le test médecin au **bloc de page de titre** (actuellement seul ARTICLE 1→fin est épinglé).
3. **Décider de l'alignement dentiste** (uniformisation justifié vs respect du source mixte) —
   cosmétique, à confirmer côté métier si on veut le strict respect du source.

Aucun de ces points n'invalide la validation Rafael ; ce sont des **durcissements**, pas des
régressions. La SELARL peut rester la **référence**, à condition de traiter le footer médecin lors
du fix systémique (ou plus tôt, en patch léger).

---

### Annexe — éléments non vérifiables / hors périmètre

- Le **PDF** final (post-LibreOffice) n'a pas été rendu ; l'audit porte sur le `.docx` généré. La
  perte de footer/pagination se confirmera visuellement au PDF mais la cause (footer vide dans le
  `.docx`) est établie.
- L'audit n'a pas rejoué la suite **globale** (295 tests désélectionnés) : seul le **périmètre
  `-k selarl` (41 verts)** a tourné cette session, sans DB. Suite globale **non relancée**.
