# ADR-0004 — Génération DOCX propre à partir d'un gabarit reconstruit

- Statut : ACCEPTÉ
- Date : 2026-05-12

## Contexte

Les sources du Lot 1 contiennent des artefacts de transformation : commentaires, révisions, placeholders colorés.

## Proposition

Pour le Lot 1, préférer une génération DOCX propre depuis un gabarit reconstruit ou from-scratch plutôt qu'un nettoyage des sources transformées à l'exécution.

## Règle de fidélité

Le générateur consomme exclusivement les tokens du modèle source tokenisé (remplissage de template via `rendering/docx_template_fill.py`). Toute formulation absente du modèle déclenche une escalade `sachant-juridique`, JAMAIS une paraphrase ou une invention de wording juridique. Toute ambiguïté juridique (ex. durée, accord de genre, unité) est escaladée, jamais tranchée en douce dans le code.

## Point à valider

Validation humaine finale avant implémentation effective.
