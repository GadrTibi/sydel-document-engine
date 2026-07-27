# Cadrage du lot post-réunion 2026-06-09 (Albane × David × Rafael)

> Auteur : Nico Robin (product-manager). Cadrage AVANT implémentation. Aucun code modifié.
> Source réunion : `_REUNION_2026-06-09_ALBANE_DAVID.md`. Canon : `JOURNAL_DECISIONS_SELARL_V1.md`,
> `_MEGASPRINT_BOARD.md`, `_RAFAEL_PACKET_V1.md`. V1 = CRÉATION uniquement. Moteur FIDÈLE
> (aucune formulation juridique inventée ; toute ambiguïté → Rafael).

## 1. Intention métier du lot (langage simple)

Albane et David ont vu le moteur tourner et validé le **fonctionnel** (docs, logos, variables,
féminisation, pluralisation, ZIP). Ils demandent trois évolutions produit et signalent des erreurs
juridiques (vagues, sans cas concret).

Les trois évolutions :
1. **Plusieurs associés (2, 3, 5+)** : la saisie et tous les documents (statuts, procurations, PV,
   annexes) doivent s'adapter au nombre réel d'associés, pas rester bloqués à 2.
2. **Un associé n'est pas forcément un dirigeant** : pouvoir cocher qui dirige (Président / DG / DG
   délégué) ; les champs lourds (filiation parents, déclaration de non-condamnation) ne sont demandés
   que pour les dirigeants, pas pour un simple associé.
3. **Base de personnes** : ne plus ressaisir une identité déjà entrée ailleurs (personnes physiques
   ET morales).

Le juridique signalé (intérêts de retard, clauses de cession, désignation dirigeants, infos
parentales, variables mal injectées) est **inactionnable** tant que Rafael n'a pas fourni les cas
concrets — c'est explicitement son action item de réunion.

## 2. Deux colonnes : constructible vs en attente Rafael

### A. CONSTRUCTIBLE MAINTENANT (aucune dépendance juridique externe)

| Item | Surfaces / types | Existe déjà | Manque |
| :-- | :-- | :-- | :-- |
| A1 — Multi-associés N générique (saisie) | `associe_repeater.py`, slices civils (SCI/SCI IRIS/SCS/SCM), SELAS multi | Repeater 1→N opérationnel (`nb_max=6`, boutons ajouter/retirer) ; SELAS multi 2→5 | Borne par type non harmonisée ; pas de garde UX sur la cohérence somme parts/actions au-delà de 2 (le moteur la fait déjà côté validation) |
| A2 — Génération multi-N câblée bout-en-bout | générateurs civils + SELAS multi | Les générateurs **itèrent vraiment** `for associe in data.associes` (apports, capital, répartition, signatures) ; bornes `MAX_ASSOCIES=6` (civils) / `5` (SELAS) | À **prouver par test** sur 3 et 5 associés (aujourd'hui les fixtures de test sont surtout à 2) ; satellites SCM verrouillés à exactement 2 (modèles bâtis pour 2 — voir B) |
| A3 — Sélecteur de dirigeant (qui dirige) | SELAS multi, SAS, et tout type à dirigeant nommé | Modèle de données déjà prêt : `ReunionPresident.ref_associe_index` permet de pointer un associé précis ; aujourd'hui défaut = `physiques[0]` | UI pour **choisir** le dirigeant parmi les associés (au lieu du 1er physique imposé) ; case « dirigeant » par associé |
| A4 — Champs dirigeant conditionnels | SELAS multi (DNC), SAS | DNC/filiation collectés aujourd'hui **uniquement pour le signataire/président** (selas_multi_slice `_render_common_docs_form`) | Rendre la collecte conditionnelle **par associé coché dirigeant** plutôt que sur un signataire unique implicite — structure du formulaire à généraliser |
| A5 — Base de personnes (réutilisation) | couche front transverse (`front_data/`, shell) | **Rien** : aucun store de personnes n'existe (les occurrences trouvées sont des champs d'adresse/représentant, pas un annuaire) | Tout : modèle de stockage (session ou persistant ?), UI « réutiliser une personne », PP + PM. **À scoper en ticket dédié** — non trivial |

### B. EN ATTENTE RAFAEL (juridique non précisé — ne pas coder à l'aveugle)

| Sujet | Ce qui manque exactement |
| :-- | :-- |
| Wording **désignation des dirigeants** (Président / DG / DG délégué) | La formulation EXACTE des clauses de nomination DG / DG délégué dans les statuts. Les modèles source tokenisés ne contiennent à ce jour qu'un **Président** (SAS, SELAS multi). Pas de modèle observé avec DG / DG délégué. Le moteur ne peut pas inventer ces clauses. → Rafael : modèle ou wording de référence. (`_RAFAEL_PACKET_V1.md` §6) |
| **Intérêts de retard** | Où (quel document/clause), quelle formule exacte. (`_RAFAEL_PACKET_V1.md` §4) |
| **Clauses de cession** | Lesquelles revoir — et cession **hors V1** : confirmer qu'il ne s'agit pas de rouvrir le périmètre. (`_RAFAEL_PACKET_V1.md` §5) |
| **Infos parentales / DNC** : qui et quand | Requises pour le **seul dirigeant** ou pour **tout associé** ? Détermine la condition exacte de A4. C'est une règle métier, pas un choix technique. (`_RAFAEL_PACKET_V1.md` §7) |
| **Variables mal injectées** | Lesquelles précisément (doc généré / capture à l'appui). (`_RAFAEL_PACKET_V1.md` §8) |
| Clauses « parts sociales » / « gérant » dans modèles **en actions / Président** (SAS, SELAS) | Déjà flaggé : le moteur est fidèle (wording identique source↔généré), mais le modèle SOURCE contient ces termes incohérents. Adapter le `.docx` source = décision juridique Rafael, jamais en douce. (`_RAFAEL_PACKET_V1.md` §3) |
| Satellites SCM **>2 ou <2 associés** | Pacte + liste dépenses bâtis pour **exactement 2** ; généraliser exige confirmation Rafael (une SCM peut-elle avoir 1 ou 3+ membres ?). (`_RAFAEL_PACKET_V1.md` §1) |

## 3. Ordre de bataille (constructible) + pièges de fidélité

Ordre recommandé (par dépendance) :
1. **A2 d'abord — prouver le multi-N existant par test (3 et 5 associés).** C'est de la
   vérification, pas de l'invention : valide que le socle déjà câblé tient avant d'empiler du neuf.
2. **A1 — harmoniser bornes/UX multi-associés** sur les types civils + SELAS (cohérence des libellés,
   bornes par type).
3. **A3 puis A4 — dirigeant : sélecteur + champs conditionnels.** A3 (choisir le dirigeant) débloque
   A4 (champs conditionnels par dirigeant). **A4 dépend d'une règle Rafael** (DNC = dirigeant seul ou
   tout associé, §7) : on peut construire la **mécanique conditionnelle** (case dirigeant → champs)
   sans attendre, mais la **condition exacte de déclenchement** de la DNC reste à confirmer.
   → constructible en mécanique, paramètre métier à verrouiller.
4. **A5 — base de personnes : ticket dédié séparé.** Ne pas l'embarquer dans le même lot ;
   c'est une feature transverse à part entière (modèle de stockage, PP+PM, UI de réutilisation).

Pièges de fidélité connus (ne PAS « corriger » en passant) :
- Clauses « parts sociales » / « gérant » présentes mot pour mot dans les modèles SOURCE SAS/SELAS
  (en actions / Président) : le moteur les reproduit fidèlement ; toute correction = `.docx` source
  + GO Rafael (B).
- Désignation DG / DG délégué : **aucun wording source** → ne rien rédiger ; A3 ne fait que
  pointer/structurer, le texte de clause attend Rafael.
- Satellites SCM verrouillés à 2 associés : ne pas les forcer à N sans confirmation modèle (B).

## 4. État réel de l'existant multi-associés (vérifié dans le code)

- `associe_repeater.py` gère **déjà 1→N** : `RepeaterConfig.nb_max=6` par défaut, bouton
  « Ajouter / Retirer un associe », état dans `st.session_state`. Personne physique ET morale,
  vocabulaire parts/actions paramétrable, rôle statutaire optionnel (commandité/commanditaire SCS).
  (`associe_repeater.py:36-90`)
- Côté **générateurs civils** (`statuts_civils_common.py`) : itération réelle `for associe in
  data.associes` pour apports, capital, répartition numérotée et signatures ; borne `MAX_ASSOCIES=6`
  (`:32`, `:618-619`, `:320`, `:403`, `:468`, `:496`). → le multi-N est **vrai**, pas un placeholder.
- Côté **SELAS multi** (`statuts_selas_multi.py`) : `MIN..MAX = ..5`, itérations N réelles
  (`:213`, `:278`, `:305`, `:339`), président choisi via `ref_associe_index` sinon `physiques[0]`
  (`:377-403`). Le modèle de données **sait déjà** désigner n'importe quel associé comme président.
- **Ce qui casse / manque au-delà de 2 :**
  - Rien ne « casse » dans les statuts civils ni SELAS au-delà de 2 (itération générique) — mais les
    **tests** couvrent surtout 2 associés → A2 = prouver 3 et 5.
  - **Satellites SCM** (pacte, liste dépenses) : verrouillés à **exactement 2 associés** (modèles
    bâtis pour 2) — généralisation = attente Rafael (`_RAFAEL_PACKET_V1.md:50-52`).
  - **Dirigeant** : aujourd'hui le président est **imposé = 1er associé physique**
    (`selas_multi_slice.py:264,539-543` ; SAS = actionnaire unique `sas_slice.py:61,105`).
    Pas de case « dirigeant », pas de rôle DG / DG délégué. → c'est exactement la feature A3/A4 à
    construire.
  - **DNC / filiation** : collectée pour un **signataire unique implicite**
    (`selas_multi_slice.py:171-204`, `_render_common_docs_form`), pas par associé-dirigeant.

## 5. Verdict

Le lot CONSTRUCTIBLE **n'est PAS entièrement prêt à partir sans arbitrage** :
- **A1, A2, A3 + base de personnes (A5)** : prêts, aucune dépendance juridique → GO build.
- **A4 (champs dirigeant conditionnels)** : la **mécanique** est constructible, mais la **règle de
  déclenchement de la DNC** (dirigeant seul vs tout associé) est une question Rafael (§7) → construire
  la mécanique avec un défaut documenté, verrouiller la condition au retour Rafael.
- Tout le **wording dirigeant DG / DG délégué et les corrections juridiques** restent **hors build**
  jusqu'aux cas concrets de Rafael.
