# Bootstrap GitHub + Codex

## But

Disposer d'un dépôt GitHub privé propre, puis brancher Codex dans un cadre strictement contrôlé.

## Ordre recommandé

1. Créer un dépôt GitHub privé `sydel-document-engine`
2. Pousser cette V1
3. Protéger `main`
4. Activer les issues et les PR templates
5. Connecter le dépôt à Codex
6. Vérifier que `AGENTS.md` est bien présent à la racine
7. Activer les revues Codex sur PR
8. Utiliser Codex sur tickets petits et tracés

## Ce que Codex doit faire en premier

- harmoniser les helpers transverses ;
- compléter les tests ;
- implémenter les briques de registre ;
- préparer l'infra DOCX ;
- implémenter les générateurs document par document.

## Ce que Codex ne doit pas faire en premier

- réécrire le wording juridique ;
- restructurer le dépôt sans ADR ;
- lancer des implémentations multi-documents non spécifiées ;
- changer la source de vérité.

## Usage conseillé en PR

- utiliser `@codex review` sur les PR sensibles ;
- garder les commentaires de review centrés sur les risques majeurs ;
- faire corriger par Codex des sujets ciblés et bornés.

## Passage ultérieur en CI

Quand l'équipe sera prête, reprendre `examples/github-actions/codex-pr-review.yml` et l'activer dans `.github/workflows/` avec le secret adapté.
