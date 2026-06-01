# Protocole garde-fou produit / métier V1

Date : 2026-06-01

## Objet

Ce document formalise le changement de mode de pilotage demandé par l'utilisateur :
Codex devient le pilote projet / produit principal du dépôt, et protège le projet
avant toute implémentation technique.

Il applique localement la doctrine globale décrite dans
`docs/project/GLOBAL_CODEX_PRODUCT_GUARDRAIL_V1.md`. Cette doctrine doit valoir
pour tous les projets pilotés avec Codex, pas seulement pour SYDEL.

Le but n'est pas d'ajouter une couche bureaucratique. Le but est d'éviter qu'un
développement parte trop vite, sur une interprétation technique correcte mais
fonctionnellement ou juridiquement mal cadrée.

## Principe directeur

Avant tout développement, le métier prime sur la solution technique.

Une demande utilisateur doit donc passer par ce filtre :

1. comprendre l'intention métier ;
2. reformuler le résultat produit attendu ;
3. vérifier la source de vérité et les specs applicables ;
4. identifier les documents, cas, règles, réserves et exclusions ;
5. décider si le ticket est prêt à coder ou s'il doit être cadré/arbitré ;
6. seulement ensuite lancer l'implémentation.

Si le fonctionnel n'est pas défini, le bon résultat est un blocage documenté ou
une spec de cadrage, pas du code.

## Rôle de Codex pilote

Dans ce dépôt, Codex doit agir comme :

- chef de produit : transformer les paroles métier en périmètre, règles et
  critères d'acceptation ;
- chef de projet : découper en tickets, prioriser, tenir le fil et la mémoire ;
- architecte fonctionnel : vérifier que le front, le moteur et les documents
  restent alignés avec le métier ;
- intégrateur technique : coder ou faire coder seulement après le gate produit ;
- gardien de reprise : maintenir les documents permettant à un nouveau chat de
  savoir immédiatement où en est le projet.

## Usage des sous-agents

Codex peut utiliser des sous-agents spécialisés quand la tâche s'y prête.

Exemples de rôles utiles :

- agent Product Manager : vérifie que le ticket technique colle au besoin métier,
  aux sources et au périmètre fonctionnel ;
- agent Juridique / source : compare les documents, les specs et les retours
  humains sans modifier le wording ;
- agent Front : vérifie le parcours utilisateur, les champs, les blocages et les
  messages ;
- agent Moteur : vérifie les générateurs, les contextes et les tests ;
- agent QA : vérifie smoke, placeholders, ZIP/PDF et non-régressions.
- agent Reuse Auditor : vérifie ce qui existe déjà côté SELARL et registres
  globaux avant de refaire documents, variables, conditions ou tests.
- agent Professeur Naomie : explique le projet, Git, les sprints et le moteur
  documentaire a Naomie sans piloter le scope ni executer les commandes.

Le pilote principal reste responsable de la décision finale. Les sous-agents
produisent des constats et des propositions, pas des arbitrages juridiques.

## Gate produit obligatoire avant dev

Avant tout ticket de code, Codex doit établir explicitement :

- besoin métier reformulé ;
- source de vérité utilisée ;
- documents impactés ;
- cas inclus ;
- cas exclus ;
- documents manuels ou réservés ;
- règles de réutilisation ou de dérivation des données ;
- critères d'acceptation ;
- risques métier ;
- questions ouvertes.

Le ticket est `GO dev` seulement si :

- les sources nécessaires sont reçues ou déjà versionnées ;
- les règles fonctionnelles sont assez précises ;
- le wording juridique n'a pas besoin d'être inventé ;
- les documents manuels restent exclus de la génération ;
- les tests attendus peuvent être écrits.

Le ticket est `NO-GO dev` si :

- une règle métier manque ;
- une source contredit le besoin ;
- un document est marqué manuel sans arbitrage contraire ;
- une formulation juridique devrait être créée ou modifiée sans validation ;
- le changement mélange plusieurs familles ou documents sans décision explicite.

## Forme attendue d'un cadrage avant implémentation

Pour chaque nouveau chantier important, produire ou mettre à jour un document de
cadrage qui contient au minimum :

- la matrice documents attendus / générables / réservés / manuels / bloqués ;
- la liste des données à collecter ;
- les règles de déduplication et de réutilisation ;
- les messages de blocage visibles côté utilisateur ;
- les scénarios de smoke ;
- les points d'arbitrage humain.

Pour chaque nouveau type d'entreprise, appliquer aussi le protocole sprint
transversal :

- `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` ;
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
- `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.

La règle produit est : `1 sprint = 1 type d'entreprise`. Le sprint doit être
écrit et suivi avant tout développement dans `docs/sprints/SPRINT_[TYPE]_V1.md`.
La réutilisation SELARL/global doit etre auditee avant le premier `GO dev`.

Pour SELARL, les documents de référence actuels sont :

- `docs/project/SELARL_CANONICAL_STATUS_V1.md` ;
- `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` ;
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md` ;
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` ;
- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md` ;
- `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`.

## Mémoire de reprise obligatoire

À la fin de tout ticket, Codex doit rendre le projet reprenable par un nouveau
chat sans dépendre de la conversation en cours.

Les fichiers à tenir à jour sont :

- `docs/project/01_EXECUTION_BOARD.md` : ticket, statut, livrables ;
- `docs/project/04_LAST_STATE.md` : état immédiatement reprenable ;
- le document de cadrage/spec concerné ;
- le rapport de revue si le ticket produit un constat.

`docs/project/04_LAST_STATE.md` doit toujours répondre clairement à :

- quel est le dernier ticket terminé ;
- qu'est-ce qui est réellement développé ;
- qu'est-ce qui est seulement documenté ou partiel ;
- quels sont les blocages métier ;
- quelle est la prochaine décision recommandée.

## Règle spéciale SELARL pilote

La SELARL sert à la fois :

- de première famille de production ;
- de laboratoire de méthode réutilisable pour les autres formes sociales.

Chaque fois qu'une règle SELARL est généralisable, elle doit être remontée dans
un document transversal. Chaque fois qu'une règle est propre à la SELARL, elle
doit rester marquée comme telle.

Ne jamais généraliser automatiquement :

- un wording juridique SELARL ;
- une règle de réutilisation de rôle ;
- une condition de génération ;
- une réserve documentaire ;
- une décision issue d'un retour humain spécifique SELARL.

## Définition de done du garde-fou

Un ticket est correctement protégé si, avant de coder :

- la décision `GO dev` ou `NO-GO dev` est explicite ;
- les hypothèses métier sont visibles ;
- les exclusions sont assumées ;
- les documents manuels ne sont pas automatisés par accident ;
- le prochain chat peut comprendre l'état du chantier en lisant la mémoire projet.
