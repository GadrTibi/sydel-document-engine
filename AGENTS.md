# AGENTS.md

Ce dépôt sert à construire un moteur documentaire juridique **déterministe** pour DAAT x SYDEL.

## Mission de l'agent

Tu interviens comme agent de développement dans un cadre très contraint.

Tu peux :

- structurer le dépôt ;
- écrire du code Python ;
- écrire des tests ;
- améliorer la documentation technique ;
- proposer des refactors sûrs ;
- préparer des PR propres et limitées.

Tu ne dois pas :

- réinventer l'architecture métier ;
- modifier la source de vérité sans décision explicite ;
- coder un document sans respecter le pipeline documentaire ;
- introduire de logique d'IA générative dans le moteur de production ;
- modifier des formulations juridiques sans les signaler explicitement.

## Source de vérité métier

Le document de référence est :

- `project/source_truth/Documents_a_generer_par_cas.docx`

L'arbre théorique abandonné n'est pas une source valide.
Il n'existe pas de fichier séparé « Documents avec variables ».

## Principes d'architecture non négociables

1. Le moteur se construit **par document canonique**.
2. Le référentiel de départ est **par cas métier**.
3. L'orchestrateur appelle les bons générateurs selon le contexte dossier.
4. Les documents marqués « à remplir à la main » restent hors automatisation initiale.
5. Toute génération doit pouvoir sortir un DOCX propre, puis PDF, puis ZIP dossier.

## Pipeline documentaire obligatoire

Aucun document ne doit passer en implémentation sans ce cycle :

`Inventorié → Validé → Source reçue → Analysé → Spécifié → Codé → Testé → Validé`

Concrètement :

- pas de code documentaire sans source reçue ;
- pas de code documentaire sans spec écrite ;
- pas de merge sans test ;
- pas de changement de wording sans note de validation.

## Mode de travail attendu

### Pour toute tâche Codex

1. lire la doc liée dans `docs/` ;
2. repérer l'ADR applicable ;
3. limiter le changement au périmètre du ticket ;
4. ajouter ou mettre à jour les tests ;
5. documenter les hypothèses ;
6. ne pas toucher à plusieurs documents métier dans la même PR sauf ticket explicite.

### Pour toute PR

- rester petite et traçable ;
- annoncer les risques ;
- lister les fichiers touchés ;
- signaler toute hypothèse métier ;
- vérifier que le wording juridique n'a pas dérivé.

## Commandes utiles

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest
ruff check .
streamlit run src/sydel_doc_engine/app/streamlit_app.py
```

## Conventions de code

- Python 3.11+
- typage explicite
- fonctions courtes
- logique métier séparée des couches UI / I/O
- pas de constantes magiques en dur dans les générateurs
- helpers transverses mutualisés dès que deux documents en dépendent

## Conventions de projet

- `DOC-xxx` = document canonique
- `LOT-x` = lot documentaire
- `ADR-xxxx` = décision d'architecture
- `EPIC-x` = chantier transversal GitHub

## Priorités actuelles

1. finaliser le bootstrap GitHub / Codex
2. verrouiller le registre moteur initial
3. implémenter les helpers transverses sûrs
4. coder le Lot 1 document par document après arbitrages

## Garde-fous juridiques

- ne jamais « améliorer » le texte juridique sans ticket explicite ;
- préférer l'identité stricte avec la source ;
- si une ambiguïté existe, bloquer la génération et documenter la décision requise.
