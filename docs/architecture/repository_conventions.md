# Conventions de dépôt

## Branching

- `main` protégée
- PR obligatoire
- CI obligatoire
- revue humaine obligatoire

## Granularité des PR

- une PR par helper transverse ;
- une PR par document implémenté ;
- une PR séparée pour les changements de registre ;
- une PR séparée pour les changements d'architecture.

## Dossiers source

- `project/source_truth/` : référentiel métier maître
- `project/source_documents/lot_xx/` : sources par lot
- `docs/delivery/` : analyses et specs figées

## Règle de nommage des tickets

- `[BOOT]` bootstrap dépôt / infra
- `[ANALYSE]` analyse documentaire
- `[GEN]` générateur documentaire
- `[TEST]` recette / cas d'essai
- `[ADR]` décision d'architecture
