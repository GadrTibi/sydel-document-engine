# Workstream trace agent protocol V1

Date : 2026-06-02

## Objet

Ce protocole definit l'`Agent de tracabilite de flux`.

Il est generique : il s'applique a Naomi, a un autre pilote accompagne, a un
autre type d'entreprise, ou a un autre projet.

Son role est simple :

```text
Tracer l'avancement du flux de travail, sans demander au pilote humain de tenir
le journal lui-meme.
```

Dans SYDEL, le premier flux concerne Naomi sur SELAS. Si Codex, un sous-agent,
NotebookLM, GitHub ou un outil avance dans le perimetre de ce flux, cela compte
comme avancement du flux Naomi pour le rapport Gad.

## Regle centrale

```text
Le pilote humain ne porte pas la charge de tracabilite.
L'agent de tracabilite enregistre le flux.
```

Naomi peut donner des reponses, poser des questions, choisir une option ou
transmettre de la matiere. Mais elle ne doit pas etre responsable de maintenir
le worklog, les curseurs, les preuves, les rapports ou les historiques.

## Vocabulaire

| Terme | Definition |
| --- | --- |
| Flux | Perimetre de travail suivi : sprint, mission, branche ou type d'entreprise |
| Pilote accompagne | Personne associee au flux, par exemple Naomi |
| Avancement du flux | Tout fait utile produit dans ce perimetre, par humain, Codex, sous-agent ou outil |
| Preuve interne | Fichier, thread, commit, source, rapport ou artefact qui justifie le statut |
| Rapport boss | Synthese courte et decisionnelle pour Gad |
| Rattrapage retroactif | Reconstruction des traces passees quand le suivi n'a pas ete tenu |

Le mot anglais `backfill` peut apparaitre dans certains fichiers techniques. Il
signifie uniquement `rattrapage retroactif`.

## Responsabilites

L'Agent de tracabilite de flux doit :

- identifier le flux actif ;
- identifier le pilote accompagne ;
- identifier la branche ou le perimetre attendu ;
- lire et tenir le worklog ;
- enregistrer les avances du flux apres chaque action significative ;
- enregistrer les blocages et gates ;
- enregistrer les rapports demandes par Gad ;
- tenir un curseur pour les rapports differentiels ;
- conserver les preuves internes sans alourdir le rapport boss ;
- declencher un rattrapage retroactif si le suivi est stale ;
- declencher le protocole de synchronisation si une avancee est annoncee mais
  absente des traces publiees ;
- produire un rapport court par defaut quand Gad demande le statut.

Il ne doit pas :

- attendre que le pilote accompagne fasse lui-meme le suivi ;
- reduire l'avancement du flux aux seules actions humaines ;
- travestir une preuve absente en certitude ;
- transformer un rapport boss en audit detaille sauf demande explicite ;
- lancer du dev sans gate `GO dev`.

## Sources a lire

Pour un rapport de statut, l'agent lit selon le besoin :

1. tour de controle projet ;
2. dernier etat projet ;
3. fichier du sprint ou de la mission ;
4. worklog du flux ;
5. journal specialise, par exemple NotebookLM ;
6. branche locale ou distante ;
7. derniers commits ou fichiers modifies ;
8. threads Codex accessibles ;
9. rapports `docs/review/` ;
10. Sync packet, s'il existe ;
11. sources, specs, code, tests et artefacts lies au flux.

Ces preuves servent a l'agent. Elles ne doivent pas toutes etre deversees dans
le rapport Gad.

## Rapport boss par defaut

Quand Gad demande `ou en est [pilote] ?`, la reponse par defaut doit etre courte
et decisionnelle :

```text
Statut flux [pilote] : [projet / sprint / phase / GO-NO-GO]
Avancement depuis le dernier point : [1-3 faits utiles du flux]
Prochaine etape : [une action concrete]
Blocage / risque : [aucun ou blocage principal]
Fiabilite : [OK / suivi a rattraper / source manquante]
```

Le rapport ne doit pas separer en surface `Naomi personnelle`, `Codex`, `repo`
et `projet`, sauf si Gad demande un audit. Cette separation reste en preuve
interne pour eviter les fausses affirmations.

## Rapport audit sur demande

Si Gad demande un audit detaille, l'agent peut sortir :

- sources lues ;
- branches ;
- commits ;
- journal ;
- worklog ;
- ecarts ;
- attribution fine ;
- rattrapage retroactif ;
- fiabilite ligne par ligne.

## Rattrapage retroactif

Le rattrapage retroactif s'active quand :

- le worklog est absent ;
- le worklog existe mais ne couvre pas l'etat reel du flux ;
- un thread, une branche ou un rapport contient une avance non reportee ;
- Gad signale qu'un rapport est faux ou stale.

Sortie attendue :

```text
docs/review/[flux]_trace_recovery_001_report_v1.md
```

ou, si le nom existant est deja cree :

```text
docs/review/[flux]_naomie_backfill_001_report_v1.md
```

Le rapport de rattrapage est une preuve interne. Le rapport boss suivant doit
redevenir court.

## Synchronisation inter-threads

Si Gad annonce que le flux a avance, mais que ni la branche, ni le worklog, ni
les rapports ne montrent cette avancee, l'agent ne doit pas conclure que le
travail n'existe pas.

Il doit conclure :

```text
avancee annoncee, synchronisation manquante
```

Puis appliquer :

```text
docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md
```

Le but est de recuperer soit un commit pousse, soit un `Sync packet` produit par
le thread qui contient le travail.

## Application a SYDEL / SELAS

Pour SELAS, le flux suivi est :

```text
Flux Naomi SELAS
```

Donc, pour Gad, les travaux faits par Codex et les sous-agents dans le perimetre
`codex/naomie-selas-sprint` remontent comme avancement du flux Naomi.

La question n'est pas :

```text
Qu'a fait Naomi personnellement ?
```

La question par defaut est :

```text
Ou en est le flux Naomi SELAS, quelle est la prochaine etape, et qu'est-ce qui bloque ?
```

La distinction fine reste disponible en audit, mais elle n'est pas le rapport
boss par defaut.
