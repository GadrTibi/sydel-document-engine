# INDEX des types d'entreprise — état de fondation

> **Date :** 2026-06-05. **Nature :** index de navigation des dossiers de fondation réellement créés
> sous `docs/project/types/*/`. Construit **uniquement** à partir des fichiers présents
> (`STATUT.md`, `INVENTAIRE_MODELES.md`, `CARTOGRAPHIE_TENTATIVE.md`, `NOTEBOOKLM_PROMPTS.md` de
> chaque type) — **rien deviné**. Le canon validé du projet ne couvre que la **SELARL** ; la SELARL
> n'a **pas** de dossier ici (c'est l'implémentation de référence, vit ailleurs dans `docs/project/`).
>
> **Fait transverse n°1 :** la **carte officielle « cas → documents » est MANQUANTE pour TOUS** les
> types ci-dessous. Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est **100 %
> SELARL** (SELARL ×23 ; aucun de ces 6 types n'y figure, sauf la SCM en seule « cession de parts vers
> SELARL »). **Génération NO-GO** pour tous tant que la carte + le wording ne sont pas validés
> (NotebookLM → Rafael/Albane).

## 1. Tableau maître

| Type | Modèles dispo | Cas tentatives | Carte canon officielle ? | Manques clés | Prochaine étape |
|---|---|---|---|---|---|
| **EURL** | **0** — aucun modèle sur le Drive (scan 125 docx, nom + contenu) ; type **vierge** | Création (assumption) ; régime matrimonial / apport-cession / option IR-IS / gérance / ordre = `open` | **NON** (canon = SELARL ; EURL ×0). En plus : **aucun modèle** | Modèles `.docx` tokenisés **inexistants** ; périmètre EURL non confirmé (santé vs commercial ?) ; pas dans `CaseType` ; rien dans `src/` | Envoyer `NOTEBOOKLM_PROMPTS.md` **Bloc 1** (existence + liste cas + carte) **puis Bloc 2** (modèles + variables) ; sans modèles, fondation **non démarrable** |
| **SAS** | **7** copiés (`source_documents/sas/`) ; 1 seul statuts = **SAS/SPFPL médecins** (capital en **actions**) | A Création (socle) ; B Statuts ; C Capital/souscription ; D Président ; E SASU (?) | **NON** (canon = SELARL ; 0 SAS/SASU/SPFPL) | Carte cas absente (bloquant n°1) ; périmètre profession non confirmé (médecin only ?) ; modèle « attestation capital » **introuvable** ; 2 variantes « liste souscripteurs » à arbitrer ; générateurs Codex **from-scratch** (drift fidélité) ; pas de `scenarios/sas.py` ni slice UI | Envoyer `NOTEBOOKLM_PROMPTS.md` **bloc A** (liste cas + carte) ; trancher SASU Holding + variantes ; re-vérifier le code Codex (zéro confiance) |
| **SCI** | **7** dans `source_documents/sci/` dont **2 vraiment SCI** (`statuts SCI`, `statuts SCI IRIS`) ; 5 transverses (3 « tous cas » + PV gérant + lettre option IS) | Création (carte **codée par Codex sans canon**) : statuts / statuts IRIS / option IS / 3 docs communs / PV gérant | **NON** (canon = SELARL ; 23 SELARL / 0 SCI). Carte présente seulement **dans le code**, non ratifiée | Carte cas non sourcée (hypothèse Codex) ; statuts SCI **générés from-scratch** (drift fidélité — wording dans le code) ; sens d'« IRIS » inconnu ; condition option IS / durée / objet / borne associés (>3 ?) ; `SCI_SIMPLE_PROFILE` legacy à aligner ; pas de journal `SCI-…` | Envoyer `NOTEBOOKLM_PROMPTS.md` **BLOC A** (carte officielle) ; trancher template-fill vs from-scratch ; re-tester les générateurs |
| **SCM** | **11** dans `source_documents/scm/` (10 docx + 1 `.doc` legacy) + `variables_source_scm.csv` | 1.a SCM autonome (statuts/pacte/contrat frais communs/règlement/liste dépenses) ; 1.b SCM **satellite cession** côté SELARL (déjà au canon) | **NON** pour « créer une SCM » (canon = SELARL ; SCM seulement en « cession parts vers SELARL ») | Carte « créer une SCM » absente (bloquant) ; carte Codex `case_catalog.py:701-713` extrapolée (liste `demande_inscription_ordre` **absente du Drive** = invention probable) ; `.doc` legacy `Liste depenses communes` à convertir ; pas d'UI SCM autonome ni fixture « création » | Envoyer `NOTEBOOKLM_PROMPTS.md` **Bloc 1** (carte officielle) ; réconcilier `case_catalog.py` ; re-tester DOC-025/026/027/028/030 |
| **SCP** | **5 `.docx`** dans `source_documents/scp/` + `variables_source_scp.csv` ; **2 non récupérés** (1 `.doc` PV gérant, 1 `.pdf` note IR) ; **`src/` = RIEN** (page blanche) | Création (statuts 2 associés / fiche jusqu'à 5 / 3 docs communs) — sous réserve de la nature du type | **NON** (canon = SELARL ; SCP **jamais** mentionnée V1/V2/V3) | **Ambiguïté n°1 : « SCP » ≠ société civile professionnelle** — l'objet social des statuts est une société civile de **portefeuille/participations** → nature du type à trancher AVANT tout ; borne associés incohérente (statuts 2 / fiche 5) ; `.doc` PV (avec emprunt/bien ?) + PDF IR à statuer ; `forme_sociale` et `duree_societe` variables | Envoyer `NOTEBOOKLM_PROMPTS.md` **Bloc 1.0 EN PREMIER** (nature réelle du type) puis carte des cas |
| **SPFPL** | **33 distincts** dans `source_documents/spfpl/` (44 docx Drive dédupliqués) ; **3 `.doc` legacy non récupérés** ; nombreuses **variantes de contenu** | `SPFPL_CESSION` + `SPFPL_APPORT` déjà dans `CaseType` ; carte « mappe de près la carte **V1** » (Codex a vraisemblablement suivi V1, pas inventé) | **PARTIELLE / disparue** : la carte SPFPL **existait en V1** mais a été **retirée en V2/V3** — c'est la question n°1 (quelle version fait foi ?) | Version canon à confirmer ; 3 `.doc` legacy (actes cession parts/actions, PV autorisation emprunt) à reconvertir ; PV nomination gérant SPFPL tokenisé introuvable ; variantes canoniques à arbitrer (note info ×3, attestations, contrat apport simple vs commissaires) ; pas de `scenarios/spfpl.py` ni slice UI | Envoyer `NOTEBOOKLM_PROMPTS.md` **Bloc A** (version du canon + liste cas) ; vérifier la fidélité de `case_catalog.py` à V1 ; reconvertir les `.doc` |

**Légende fidélité (rappel) :** plusieurs types ont du code Codex qui **construit le document en Python**
(`new_document()` / from-scratch : SAS, SCI) au lieu de **remplir le modèle `.docx` tokenisé**. Le
wording vit alors dans le code, **non validé humainement** → drift de fidélité à trancher au build.
Tous les constats sur `src/` sont à **RE-VÉRIFIER soi-même** (zéro confiance dans l'auto-rapport ;
`workflow_status=TESTE` ≠ validé juridiquement).

## 2. CE QU'ON DOIT OBTENIR DE NOTEBOOKLM / RAFAEL EN PRIORITÉ

### Priorité absolue — la carte officielle « cas → documents » MANQUE pour TOUS ces types

Le canon `Documents_a_generer_par_cas_V3.docx` ne couvre que la **SELARL**. Pour **EURL, SAS, SCI, SCM,
SCP, SPFPL**, il n'existe **aucune carte ratifiée** disant *quels documents se génèrent dans quel cas*.
Tout regroupement par cas présent ici (ou codé par Codex) est une **hypothèse non ratifiée**. C'est **le
bloquant n°1** : sans cette carte, la Phase 2 (cartographie) du workflow reste bloquée et aucun backlog
n'est ratifiable. À obtenir via le **Bloc 1 / Bloc A** des `NOTEBOOKLM_PROMPTS.md` de chaque type, puis
Rafael si NotebookLM ne suffit pas.

Cas particuliers de la carte :
- **SPFPL** : la carte **existait en V1** mais a **disparu en V2/V3** → trancher **quelle version fait foi**.
- **SCM** : le canon ne connaît que la SCM **en cession vers SELARL** ; la carte « **créer une SCM** » est totalement absente.
- **SCP** : avant même la carte, trancher **la nature du type** (l'objet des statuts est une société civile de **portefeuille**, pas une SCP d'exercice).

### Types SANS aucun modèle (fondation non démarrable côté moteur)

- **EURL** : **0 modèle** tokenisé sur le Drive (aucun dossier « Création EURL » ; scan de 125 docx, nom **et** contenu) et **0 carte**. Il faut faire **fournir les modèles `.docx` tokenisés EURL** avant toute chose ; le périmètre (EURL santé vs commercial) est lui-même inconnu.

### Modèles partiellement manquants / à reconvertir (legacy non tokenisables)

- **SPFPL** : 3 `.doc` legacy (`Acte_cession_parts_Dr_SPFPL`, `Acte_cession_SPFPL_tiers`, `PV SPFPL autorisation emprunt`) + PV nomination gérant SPFPL tokenisé introuvable.
- **SCP** : 1 `.doc` legacy (`PV nomination gérant`) + 1 `.pdf` (`note IR`) à statuer.
- **SCM** : 1 `.doc` legacy (`Liste depenses communes SCM`) à convertir.

### Arbitrages de variantes / périmètre (après la carte)

- **SAS** : modèle « attestation capital » introuvable ; 2 variantes « liste souscripteurs » ; SASU Holding dans/hors type ; périmètre profession (médecin only ?).
- **SPFPL** : variantes canoniques (note d'info ×3, attestations capital, contrat d'apport simple vs commissaires aux apports).
- **SCI** : sens d'« IRIS » ; condition d'option IS ; borne d'associés (au-delà de 3 ?).
- **SCP** : borne associés (statuts 2 vs fiche 5) ; `forme_sociale`/`duree_societe` variables ou figées.

## 3. Mode d'emploi (1 ligne)

Au retour, **Gad envoie les `NOTEBOOKLM_PROMPTS.md` de chaque type à NotebookLM** ; les réponses
débloquent la **cartographie** (carte officielle cas → documents) puis la **fondation** (cf.
`/type-entreprise` et `docs/project/WORKFLOW_TYPE_ENTREPRISE_V1.md`).
