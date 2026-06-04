# Sprint SELAS - prompts NotebookLM V1

Date : 2026-06-01

## Objet

Ce fichier contient les prompts courts que Codex doit donner a Naomi pour
interroger NotebookLM pendant le sprint SELAS.

Regles :

- un seul prompt a la fois ;
- ne pas envoyer tout le questionnaire d'un coup ;
- attendre la reponse NotebookLM ;
- structurer la reponse dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
- choisir le prompt suivant selon les manques ;
- rester en `NO-GO dev`.

Le Prompt 01 doit etre donne meme si Naomi dit seulement `bonjour`, des lors
que Naomi est l'interlocutrice active deja identifiee. Si Gad parle de Naomi,
Codex applique l'orchestrateur de suivi et ne declenche pas NotebookLM par
reflexe. Voir `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` et
`docs/project/NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md`.

## Prompt 01 - Inventaire documentaire SELAS

```text
Contexte : nous construisons un moteur documentaire deterministe pour les dossiers SELAS. Reponds uniquement avec les informations presentes dans les sources de ce NotebookLM. Si une information manque, ecris "non trouve".

Pour une creation de SELAS, liste tous les documents a produire ou a traiter.
Pour chaque document, donne :
1. nom du document ;
2. condition d'apparition ;
3. statut : toujours / conditionnel / manuel / reserve / inconnu ;
4. source ou indice source ;
5. incertitudes.

Termine par les 5 questions les plus importantes a poser ensuite.
```

## Prompt 02 - Differences SELARL / SELAS

```text
Compare SELARL et SELAS uniquement d'apres les sources du NotebookLM.

Liste les differences qui changent les documents, les roles ou les variables :
1. gerant / president / directeur general ;
2. parts sociales / actions ;
3. associe / actionnaire ;
4. statuts ;
5. PV ou decisions ;
6. ordre professionnel ;
7. regime communautaire.

Pour chaque difference, indique la source, l'impact documentaire et ce qui reste non trouve.
```

## Prompt 03 - Gouvernance et statuts SELAS

```text
Analyse seulement la gouvernance et les statuts SELAS.

Reponds en tableau :
1. sujet ;
2. regle trouvee ;
3. document impacte ;
4. variables necessaires ;
5. cas simple V1 possible ;
6. cas a bloquer ;
7. source.

Inclure president, directeur general, associes/actionnaires, decisions collectives, capital, actions, signature et annexes.
```

## Prompt 04 - Variables et donnees a demander

```text
Pour une creation de SELAS, liste les donnees utilisateur a demander.

Classe-les par blocs :
1. client / praticien ;
2. societe ;
3. gouvernance ;
4. capital / actions ;
5. siege / exercice ;
6. ordre professionnel ;
7. conjoint / regime communautaire ;
8. signature.

Pour chaque donnee : obligatoire ou conditionnelle, document concerne, source, et si elle semble reutilisable depuis SELARL.
```

## Prompt 05 - Documents deja proches de SELARL

```text
Identifie les documents SELAS qui semblent identiques ou proches de documents deja traites pour SELARL.

Pour chaque document :
1. document SELAS ;
2. document SELARL proche ;
3. elements identiques ;
4. elements a verifier ;
5. elements differents ;
6. risque de copier-coller ;
7. source.

Classe chaque ligne : identique / reuse-check / adapter / no-go.
```

## Prompt 06 - Cas conditionnels et blocages

```text
Liste les cas SELAS conditionnels ou dangereux a automatiser.

Inclure si present dans les sources :
1. regime communautaire ;
2. cession cabinet ;
3. SCM ;
4. derogation ;
5. site distinct ;
6. multi-associes/actionnaires ;
7. directeur general ;
8. documents a remplir a la main.

Pour chaque cas : declencheur, documents, donnees requises, source, statut recommande et raison.
```

## Prompt 07 - Recette et validation humaine

```text
Pour valider un sprint SELAS, quels scenarios de test et quelles revues humaines faut-il prevoir ?

Donne :
1. scenario simple minimal ;
2. scenarios conditionnels ;
3. documents a comparer ligne par ligne ;
4. documents a faire relire par l'associe ;
5. points de wording juridique sensibles ;
6. criteres pour dire "sprint SELAS complet".

Reponds uniquement selon les sources disponibles et signale ce qui est non trouve.
```

## Prompt de suivi libre

Codex peut ensuite produire un prompt de suivi court, cible sur les manques du
journal. Format obligatoire :

```text
Dans ta reponse precedente, il manque [sujet].
D'apres les sources du NotebookLM, precise uniquement [question ciblee].
Si l'information n'existe pas, ecris "non trouve".
Donne la source ou l'indice source pour chaque point.
```
