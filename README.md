# SYDEL Document Engine

Moteur documentaire déterministe pour DAAT x SYDEL.

## Objectif

Construire un moteur de génération documentaire **par document canonique** à partir du référentiel métier **par cas**. Le moteur doit produire :

- des **DOCX** modifiables par les juristes ;
- des **PDF** ;
- un **ZIP** contenant le dossier complet.

Le cœur du moteur reste **déterministe** : aucune IA générative n'est utilisée dans la logique de production documentaire.

## Statut actuel (mis à jour 2026-06-24)

Le moteur déterministe est **livré et fonctionnel**, bien au-delà d'une V1 stub :

- **plusieurs types de dossiers câblés** (SELARL création + cession, SELAS pluripersonnelle médecin/dentiste, SCI / SCI IRIS / SCS / SCM, SPFPL…), avec des **générateurs réels par document** ;
- **front Streamlit opérationnel** : saisie, validation, génération **DOCX + ZIP** déterministe ;
- **630 tests verts**, `ruff` propre, tests gold de fidélité ;
- **retours client** (Albane / Rafael) traités en continu, avec un gate adversarial (règle 66) avant tout « traité ».

> ⚠️ **Ne pas se fier à ce README pour l'état détaillé du jour.** LA photo vivante :
> [`docs/returns/DASHBOARD.md`](docs/returns/DASHBOARD.md) (état du jour, retours).
> [`docs/project/04_LAST_STATE.md`](docs/project/04_LAST_STATE.md) est une **archive 2026-06-03** (ne pas s'y fier).
> Carte complète de la doc : [`docs/INDEX.md`](docs/INDEX.md). Reprise à froid :
> commencer par [`docs/project/05_NEW_CHAT_PROMPT.md`](docs/project/05_NEW_CHAT_PROMPT.md).

## Décisions structurantes déjà actées

1. **Source de vérité** : `Documents à générer par cas.docx`
2. **Architecture** : moteur **par document**, pas par branche d'arbre
3. **Méthode** : avancement **par lots documentaires**
4. **Pipeline** : `Inventorié → Validé → Source reçue → Analysé → Spécifié → Codé → Testé → Validé`
5. **Hors périmètre initial** : documents marqués « à remplir à la main »

## Périmètre du dépôt

### Inclus dès maintenant

- pilotage projet ;
- conventions d'architecture ;
- cadrage GitHub / Codex ;
- base de code Python ;
- seeds de registre pour le Lot 1 ;
- tests unitaires sur les helpers transverses.

### Encore partiel / en cours (2026-06-24)

- **conversion PDF** : back-end disponible (`src/sydel_doc_engine/rendering/pdf_export.py`) mais **non câblé dans le front** (le front produit DOCX + ZIP ; `pdf_results=[]`) ;
- **périmètre produit V1** (quels types exposés au juriste) non encore formellement ratifié ;
- **fidélité juridique ligne-à-ligne** verrouillée sur un sous-ensemble des générateurs (chantier en cours — cf. Bilan de Santé).

> Génération DOCX réelle, packaging ZIP et écran Streamlit métier : **faits** (n'étaient « non implémentés » qu'au tout début du dépôt).

## Structure du dépôt

```text
.
├── AGENTS.md
├── docs/
├── examples/
├── project/
├── src/
└── tests/
```

### Repères utiles

- `project/pilotage/` : suivi projet et registre vivant
- `project/source_truth/` : document de référence métier
- `project/source_documents/` : modèles source par lot
- `docs/adr/` : décisions d'architecture
- `docs/architecture/` : conventions et mode opératoire
- `src/sydel_doc_engine/` : base du moteur
- `tests/` : tests unitaires

## Démarrage local

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest
ruff check .
streamlit run src/sydel_doc_engine/front_app/app.py
```

## Ordre de travail recommandé à partir de ce dépôt

1. créer le dépôt GitHub privé ;
2. pousser cette base V1 ;
3. connecter GitHub à Codex ;
4. activer `AGENTS.md` comme contrat de travail repo ;
5. ouvrir les tickets GitHub à partir du pilotage ;
6. faire coder par Codex les briques transverses puis les documents **un par un** ;
7. imposer revue humaine juridique sur toute évolution de texte.

## Prochaine séquence recommandée

- arbitrer `DOC-002` sur la règle d'adresse de domiciliation ;
- valider définitivement l'approche `DOCX from-scratch` pour le Lot 1 ;
- créer les tickets d'implémentation `DOC-001` et `DOC-003` ;
- garder `DOC-002` derrière son ticket d'arbitrage si nécessaire.
