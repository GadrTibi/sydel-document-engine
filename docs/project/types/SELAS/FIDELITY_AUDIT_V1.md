# SELAS — Audit de fidélité V1 (générateur Codex vs modèle source vs NotebookLM)

Date : 2026-06-07
Auteur : auditeur de fidélité (FOND + FORME). Lecture seule du code ; seul ce rapport est écrit ; aucun `.py` modifié ; aucun commit.

## Périmètre audité
- Générateur : `src/sydel_doc_engine/generators/lot_04/statuts_selas_medecin.py`
- Helpers : `generators/lot_04/statuts_sel_exercice_common.py`, `generators/lot_04/statuts_sel_exercice_templates.py`
  (bloc `STATUTS_SELAS_MEDECIN_BLOCKS`, l. 589-845)
- Modèle source (= vérité) : `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
  (558 paragraphes bruts → 255 non vides, 1 table « STATUTS », 0 image, 3 footers)
- Vérité métier : `docs/project/types/SELAS/NOTEBOOKLM_ANSWERS.md` (+ RAW_V1, BUILD_READINESS_V1)
- Échantillons générés : `artifacts/_audit_tmp/selas_M/…docx` (masculin), `…/selas_F/…docx` (féminin)
- Tests ciblés : `pytest tests/unit/test_lot_04_statuts_sel_exercice.py -k selas` → **7 passés** *(périmètre SELAS du fichier lot_04 uniquement ; suite globale NON relancée)*.

## PIÈGE D'ENVIRONNEMENT (à retenir)
Le clone par défaut (`...\sydel-document-engine`, branche `main`) est installé comme package `sydel_doc_engine`.
Tout `python -c "import sydel_doc_engine..."` lancé sans précaution résout vers `main`, PAS vers le clone
audité `...\sydel-document-engine-claude` (branche `sprint/engine-completion`). Sur `main`, le bloc art. 8
est encore figé en `associé unique` (masculin) ; sur le clone audité il est dynamique
(`[qualite_associe_article_8]`). **Les chiffres de ce rapport sont pris sur le clone audité** (sys.path forcé
sur `…-claude/src`, et pytest dont le `rootdir` est bien `…-claude`).

---

## VERDICT GLOBAL : **KEEP** (unipersonnel V1) — fidélité fond ET forme élevée, avec correctifs de forme à appliquer (FIX)

Le générateur SELAS n'est **PAS** une invention « from-scratch » au sens dangereux. Le modèle source SELAS
**existe dans le repo** et est **déjà tokenisé**, et le bloc de texte Codex `STATUTS_SELAS_MEDECIN_BLOCKS`
en est une **transcription verbatim** : 254 / 255 paragraphes **identiques au token près**, l'unique écart
(art. 8) étant une **amélioration d'accord en genre**, pas une dérive. La forme est **majoritairement
fidèle** (police Roboto 10 pt, justification du corps, gras+souligné des articles, encadré « STATUTS »,
italique de la mention finale, ANNEXE) avec quelques pertes de mise en forme **réparables** (centrage du
bloc-titre, gras du nom, footers, alignement signature).

- **Verdict FOND : KEEP** (transcription verbatim du modèle source ; cohérent NotebookLM).
- **Verdict FORME : FIX** (fidèle sur l'essentiel ; pertes ciblées à corriger).

> Nuance de gouvernance (cadre, pas le périmètre audité) : `NOTEBOOKLM_ANSWERS.md` + `BUILD_READINESS_V1.md`
> posent que la **cible produit SELAS** est **multi-associés 2-5 + personne morale + DG** (cela *supersede*
> le périmètre « unipersonnel »). Le générateur audité **ne couvre QUE l'unipersonnel** (multi explicitement
> bloqué : `validate_sel_context`). Donc : ce qui est codé est **fidèle et à GARDER**, mais **incomplet**
> par rapport à la cible. Ce n'est pas un défaut de fidélité — c'est un périmètre V1 réduit, à compléter
> plus tard (REBUILD/extension multi), décision Rafael (déjà tracée, pas un bloquant du présent audit).

---

## VOLET 1 — FIDÉLITÉ DU FOND

### Méthode
Diff token-à-token des 255 paragraphes non vides du modèle source contre les 255 blocs
`STATUTS_SELAS_MEDECIN_BLOCKS`, les deux étant encore tokenisés (placeholders `[…]` identiques de part
et d'autre). Puis rendu d'un échantillon (contexte de test) et relecture du texte produit.

### Résultat brut
**254 / 255 paragraphes strictement identiques.** Un seul écart, intentionnel et conforme :

| Élément | Verdict | Note |
|---|---|---|
| Art. 8 — ligne d'attribution du capital | keep | Source : `…attribuées en totalité à l'associé unique, [civilite] [prenom] [nom].` Code : `…à l'[qualite_associe_article_8], …`. Le token rend « associé unique » (H) / « associée unique » (F). **Amélioration d'accord en genre**, pas une invention. Vérifié : échantillon F → « associée unique ». |
| Bloc-titre (dénomination / forme / capital / siège) | keep | Verbatim source. |
| Identification du soussigné (art. liminaire) | keep | Verbatim ; profession/qualification/RPPS/régime via tokens conformes NotebookLM. |
| Art. 1 FORME (renvois R.4113-1, ord. 2023-77, déonto R.4127-1) | keep | Verbatim. |
| Art. 2 OBJET / Art. 3 DÉNOMINATION / Art. 4 SIÈGE / Art. 5 LIEU / Art. 6 DURÉE | keep | Verbatim. Art. 5 gère le 2e lieu (`render_selas_second_lieu`) — fidèle au paragraphe source conditionnel. |
| Art. 7 APPORTS + dépôt fonds | keep | Verbatim. Le wording dépôt (« déposée sur un compte ouvert au nom de la société en formation… ne pourra être retirée que sur présentation d'un certificat du greffier… ») = exactement le verbatim confirmé NotebookLM (bloc dépôt capital). |
| Art. 8 CAPITAL — clause majorité de contrôle | keep | « En aucun cas la répartition du capital ne pourra être modifiée… retireraient la majorité des droits de vote aux associés exerçant dans la société. » = **verbatim NotebookLM confirmé** (fin art. 8 à conserver). Présent et exact. |
| Art. 9 QUALITÉ D'ASSOCIÉ (composition capital, interdictions, délais) | keep | Verbatim. |
| Art. 10 FORME DES ACTIONS (nominatives, actions de préférence) | keep | Verbatim. Cohérent NotebookLM (actions de préférence pour non-exerçants). |
| Art. 11 TRANSMISSION DES ACTIONS (agrément 2/3, libre entre associés) | keep | Verbatim. « parts » → « actions » : conforme à la règle de substitution NotebookLM. |
| Art. 12 à 14 (droits/obligations, démembrement, exclusion) | keep | Verbatim. |
| Art. 15 PRÉSIDENCE (+ nomination dirigeant via tokens) | keep | Verbatim. « Gérant » → « Président » : conforme NotebookLM. Bloc de nomination (`[qualite_associe] … est nommé [fonction_dirigeant] … pour [duree_mandat_dirigeant]`) suit le paragraphe source équivalent. |
| Art. 16 DIRECTEURS GÉNÉRAUX | keep | Verbatim. (Présent dans le modèle source ; DG « optionnel » côté NotebookLM — ici le texte statutaire est présent en dur, conforme au modèle.) |
| Art. 17 à 39 (décisions sociales, conventions, cessation, CAC, capital, hors-convention, comptes courants, exercice, comptes, résultats, capitaux propres, déonto, dissolution, liquidation, disciplinaire, communication Ordre, reprise actes, condition suspensive, conciliation, frais, pouvoirs, élection domicile, signature électronique) | keep | Verbatim, ordre identique. |
| Bloc signature (`Fait à … le …`, `[PRENOM] [NOM]`, mention « bon pour acceptation des fonctions de [fonction_dirigeant] ») | keep | Verbatim source (fond). |
| ANNEXE (liste actes — ouverture compte bancaire) | keep | Verbatim. |

### Wording / règle INVENTÉ (présent dans le code, absent du modèle ET de NotebookLM)
**Aucun.** Aucun article, clause ou phrase contractuelle n'a été trouvé dans les blocs Codex sans correspondance
exacte dans le modèle source. Le seul écart (token art. 8) est une mécanique d'accord, pas du contenu inventé.

### Conformité aux règles de substitution NotebookLM (SELARL → SELAS)
| Règle NotebookLM | Respectée dans le code ? |
|---|---|
| « parts » → **actions** | OUI (toutes les occurrences du modèle SELAS sont déjà en « actions »). |
| « Gérant » → **Président** / **Présidente** | OUI (art. 15 PRÉSIDENCE ; couche genre Président/Présidente disponible). |
| « SELARL » → **SELAS / par actions simplifiée** | OUI (`[forme_sociale]`, `[forme_sociale_abregee]`, `[forme_sociale_complete]`). |
| « Associés » conservé (pas « actionnaires ») | OUI (« associés » partout ; pas de substitution forcée vers « actionnaires »). |
| Accord en genre (Né/Née, Soussigné/Soussignée, associé/associée) | OUI — vérifié sur échantillon F : « LA SOUSSIGNÉE », « née le », « associée unique ». |

---

## VOLET 2 — FIDÉLITÉ DE LA FORME

### Méthode
Génération d'un échantillon (`StatutsSelasMedecinGenerator`, contexte de test, clone audité) puis inspection
python-docx comparée au modèle source, aspect par aspect.

### Constat structurel
- **Logo / en-tête** : le modèle source **n'a AUCUN logo ni image** (0 image dans le corps, 0 image en en-tête,
  3 headers vides). L'échantillon généré n'en a pas non plus (le seul « image part » détecté est
  `docProps/thumbnail.jpeg`, vignette Office, pas un logo de corps). **Donc la leçon UAT SELARL « le moteur
  perd le logo » ne s'applique PAS ici : il n'y a pas de logo à perdre.** → fidèle.
- **Encadré « STATUTS »** : présent des deux côtés (table 1×1, centrée, gras Roboto 10 pt, bordurée). Le moteur
  l'insère après le bloc-titre. → fidèle (réserve : épaisseur de bordure, ci-dessous).
- **Footers** : le modèle source porte **3 footers** (numérotation « - Page … - » ; mention légale « VERSO DE
  LA PRESENTE FEUILLE ANNULE ARTICLE 905 DU C.G.I. - ARRETE DU 20 MARS 1958 » ; « Statuts [denomination] »).
  L'échantillon généré **n'a AUCUN footer**. → **perdu**.

### Tableau par aspect

| Aspect | Verdict | Moteur produit / modèle porte |
|---|---|---|
| logo / en-tête | fidèle | Aucun logo ni dans le modèle ni dans la sortie (rien à perdre). |
| police (corps) | fidèle | Modèle : Roboto 10 pt posé au **run** ; sortie : Roboto 10 pt posé au **style Normal** (héritage). Rendu visuel identique. |
| alignement — corps des articles | fidèle | Modèle JUSTIFY / sortie JUSTIFY. |
| alignement — bloc-titre (dénom/forme/capital/siège) | perdu | Modèle **CENTER** ; sortie **JUSTIFY** (gauche). Le bloc-titre n'est plus centré. |
| gras — dénomination (bloc-titre) | perdu | Modèle : dénomination **en gras** ; sortie : non gras. |
| gras — identification (Civilité Prénom Nom du soussigné) | perdu | Modèle : 1er run (nom) **en gras** ; sortie : non gras. |
| gras + souligné — titres d'articles « ARTICLE N - … » | fidèle | Présents dans la sortie (B+U). |
| alignement — titres d'articles | divergent (mineur) | Modèle JUSTIFY ; sortie alignement par défaut (None ≈ gauche). Effet visuel quasi nul (titre court), mais non strictement identique. |
| italique — mention finale « Faire précéder… / bon pour acceptation… » | fidèle | Italique préservé. |
| centrage + gras — « ANNEXE » | fidèle | CENTER + gras des deux côtés. |
| alignement — bloc signature (« Fait à … », « [Prénom] [Nom] ») | divergent | Modèle **gauche** (None) ; sortie **CENTER**. Le moteur centre le bloc signature alors que le modèle l'aligne à gauche. |
| gras — nom du signataire « [PRENOM] [NOM] » | perdu | Modèle : signataire **en gras** ; sortie : non gras. |
| encadré « STATUTS » — présence + centrage + gras | fidèle | Présent, centré, gras. |
| encadré « STATUTS » — épaisseur de bordure | divergent (mineur) | Modèle `w:sz=24` (≈ 3 pt, bordure épaisse) ; sortie `w:sz=4` (≈ 0,5 pt, bordure fine). Même style/couleur (single/noir). |
| footers (pagination + mention légale C.G.I. + « Statuts <dénom> ») | perdu | 3 footers dans le modèle, **0** dans la sortie. |
| tableaux | fidèle | Seule table = encadré « STATUTS », traité ci-dessus. Pas d'autre tableau dans le modèle. |
| numérotation des articles / sous-parties | fidèle | Numérotation en dur dans le texte (« ARTICLE 1 », « 15.1- », « 16-1 - », « 1-Modifications… »), reproduite verbatim. |
| tirets / puces (exclusions, DG, ANNEXE) | fidèle | Items « -\t… » rendus en liste à retrait pendant ; contenu verbatim. |

---

## SYNTHÈSE « INVENTÉ / DIVERGENT »

### Inventé (danger maximal) — FOND
- **Néant.** Aucun wording ni règle inventés.

### Divergent / perdu — FORME (à corriger, sans toucher au fond)
1. **Footers perdus** — pagination + mention légale « VERSO DE LA PRESENTE FEUILLE… ART. 905 C.G.I.… » +
   footer « Statuts <dénomination> » absents de la sortie.
2. **Bloc-titre non centré** — modèle CENTER, sortie justifiée/gauche ; **dénomination non mise en gras**.
3. **Gras perdu** sur l'identification du soussigné (Civilité Prénom Nom) et sur le **nom du signataire**.
4. **Bloc signature centré** alors que le modèle l'aligne à **gauche**.
5. **Bordure de l'encadré « STATUTS »** plus fine que le modèle (sz 4 vs 24) — mineur.
6. **Alignement des titres d'articles** par défaut vs JUSTIFY du modèle — mineur.

---

## BLOQUANTS BUILD

- **Aucun bloquant de FOND** : la transcription est verbatim, zéro invention, conforme NotebookLM → le contenu
  unipersonnel V1 est **constructible et fiable**.
- **Bloquants de FORME (non bloquants de génération, bloquants de fidélité visuelle)** : footers + centrage
  bloc-titre + gras titre/identité/signataire + alignement signature. À traiter avant de présenter une sortie
  « fidèle au modèle » à Rafael.
- **Hors fidélité, à la décision Rafael (déjà tracé)** : la cible produit SELAS est **multi-associés + personne
  morale + DG** ; le générateur audité est **unipersonnel uniquement**. Complétude ≠ fidélité : ce qui est codé
  est fidèle ; l'extension multi est un chantier distinct (cf. `BUILD_READINESS_V1.md`, modèle Reynaud à
  tokeniser). Ce point ne dégrade pas le verdict de fidélité du périmètre codé.

---

## NOTE MÉTHODE / NotebookLM
La synthèse `NOTEBOOKLM_ANSWERS.md` affirme (point « NON TROUVÉ » n°9) que « les sources ne contiennent que
les 2 premières pages d'un modèle SELARL ». **Ce constat est dépassé pour le périmètre audité** : le modèle
source SELAS médecin (`lot_04/Statuts_SELAS_medecin.docx`, 39 articles complets) **est bien présent et complet
dans le repo**, et le générateur en est la transcription. La note NotebookLM visait l'état antérieur / le cas
multi (Reynaud). À ne pas confondre : pour l'**unipersonnel**, la matière source existe et est fidèlement reprise.
