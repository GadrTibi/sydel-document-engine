# SYDEL Document Engine

Moteur documentaire déterministe pour DAAT x SYDEL.

## Objectif

Construire un moteur de génération documentaire **par document canonique** à partir du référentiel métier **par cas**. Le moteur doit produire :

- des **DOCX** modifiables par les juristes ;
- des **PDF** ;
- un **ZIP** contenant le dossier complet.

Le cœur du moteur reste **déterministe** : aucune IA générative n'est utilisée dans la logique de production documentaire.

## Statut actuel

Cette V1 de dépôt sert de base propre pour GitHub + Codex.

- la source de vérité métier est versionnée ;
- le fichier de pilotage Excel est inclus ;
- le Lot 1 est analysé et spécifié ;
- l'architecture de repo et les conventions de travail sont posées ;
- les helpers transverses sûrs sont en place ;
- les générateurs documentaires sont volontairement laissés en **stub** tant que les arbitrages restants ne sont pas clos.

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

### Volontairement non implémenté dans cette V1

- génération réelle des DOCX du Lot 1 ;
- conversion PDF finale ;
- packaging ZIP final de dossier ;
- écran Streamlit métier complet.

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
