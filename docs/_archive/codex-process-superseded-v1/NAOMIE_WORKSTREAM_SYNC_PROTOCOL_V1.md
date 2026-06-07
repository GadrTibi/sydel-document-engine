# Naomi workstream sync protocol V1

Date : 2026-06-02

## Objet

Ce protocole definit le checkpoint de synchronisation entre :

- le thread Gad ;
- le thread Naomi ;
- l'Agent Git/Branch ;
- l'Agent de tracabilite de flux ;
- la branche de sprint.

Il est generique. SELAS est seulement le premier cas.

## Regle centrale

```text
Un travail termine dans un thread mais non pousse ou non documente est invisible
pour le rapport boss.
```

Donc, quand Naomi ou son agent termine une phase importante, le flux doit
produire au moins une de ces deux preuves :

1. un commit pousse sur la branche de sprint ;
2. un `Sync packet` brut colle dans le thread, si le push est impossible.

Sans l'une de ces preuves, Codex ne doit pas conclure que le flux est termine.
Il doit dire : `avancee annoncee, synchronisation manquante`.

## Declencheurs

Appliquer ce protocole quand :

- Gad dit que Naomi a avance mais que le rapport ne le voit pas ;
- Naomi dit qu'une phase est terminee ;
- un agent Codex termine un travail dans le perimetre Naomi ;
- un rapport Gad contredit ce que Gad sait du travail reel ;
- une branche distante ne montre pas le travail attendu ;
- un agent a ajoute des protocoles que l'autre thread doit recuperer.

## Roles

### Agent Git/Branch

Responsable de :

- verifier le dossier courant ;
- verifier le remote ;
- verifier la branche locale ;
- comparer le HEAD local et le HEAD distant ;
- proteger les changements non pousses ;
- commit/push si le travail est coherent et autorise ;
- produire un `Sync packet` si le push bloque.

### Agent de tracabilite de flux

Responsable de :

- noter le checkpoint dans le worklog ;
- relier le commit ou le `Sync packet` au flux ;
- mettre a jour le dernier curseur Gad ;
- signaler les trous de sync.

### Orchestrateur Naomi

Responsable de :

- lire le checkpoint avant tout rapport Gad ;
- ne pas confondre `branche sans nouveau commit` et `Naomi n'a rien fait` ;
- conclure `sync manquante` quand le travail est annonce mais absent des traces.

## Checkpoint obligatoire cote thread Naomi

Quand le flux Naomi avance fortement ou se dit termine, Codex dans le thread
Naomi doit :

1. lire `docs/project/PROJECT_CONTROL_TOWER_V1.md` ;
2. lire `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` ;
3. lire `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md` ;
4. lire le fichier de sprint actif ;
5. lire le worklog du flux ;
6. verifier :
   - dossier courant ;
   - remote ;
   - branche ;
   - HEAD local ;
   - HEAD distant ;
   - `git status --short --branch` ;
   - fichiers modifies ou crees ;
   - derniers commits ;
   - tests ou smokes faits.

Si des changements locaux existent, Codex ne doit pas faire un pull aveugle.
Il doit d'abord consigner l'etat local, puis choisir :

- commit/push si coherent et autorise ;
- ou `Sync packet` si le push est bloque ;
- ou blocage explicite si conflit, branche incorrecte ou source manquante.

## Sync packet

Si le push est impossible, le thread Naomi doit produire ce bloc brut :

```text
SYNC PACKET - FLUX NAOMIE
Projet :
Sprint / type :
Thread :
Dossier courant :
Remote :
Branche locale :
Branche attendue :
HEAD local :
HEAD distant :
Statut git :
Fichiers modifies :
Fichiers crees :
Dernier commit local :
Dernier commit pousse :
Travail realise :
Livrables / packs :
Rapports crees :
Tests / smokes :
Statut metier :
Ce qui bloque le push :
Action demandee a Gad/Codex :
```

Ce paquet permet au thread Gad de savoir si le probleme est :

- travail non pousse ;
- mauvaise branche ;
- mauvais depot ;
- conflit avec les nouveaux protocoles ;
- travail seulement oral/chat ;
- livrables crees mais non relies au worklog.

## Recuperation des mises a jour Gad

Quand le thread Gad pousse de nouveaux protocoles, le thread Naomi doit les
recuperer avant de continuer, sauf si des changements locaux non sauvegardes
rendent le pull risqué.

Ordre sur un thread Naomi propre :

```powershell
git fetch origin
git switch codex/naomie-selas-sprint
git pull --ff-only origin codex/naomie-selas-sprint
```

Si le thread Naomi est sale, Codex doit d'abord faire un checkpoint local ou un
`Sync packet`. Il ne doit pas ecraser les changements.

## Prompt de sync a donner a Naomi

Si Gad sait que Naomi a avance mais que le thread Gad ne voit rien, Gad peut
demander a Naomi de coller ce prompt dans sa discussion :

```text
Je suis Naomi.
Sync checkpoint obligatoire pour le flux Naomi SELAS.

Gad indique que mon travail SELAS est avance jusqu'a attente du retour humain,
mais le thread Gad ne voit pas cette avancee sur la branche.

Ne developpe rien de nouveau.
Applique un checkpoint de synchronisation :
1. verifie le dossier courant, le remote et la branche ;
2. verifie que la branche attendue est codex/naomie-selas-sprint ;
3. verifie le HEAD local, le HEAD distant et git status --short --branch ;
4. liste les fichiers modifies, crees, les rapports, packs et tests ;
5. dis si le travail est committe et pousse ;
6. si possible, recupere les dernieres modifications de Gad sans ecraser les changements locaux ;
7. si le travail est coherent et non pousse, commit/push sur codex/naomie-selas-sprint ;
8. si tu ne peux pas push, donne un SYNC PACKET complet.

Format obligatoire :
Statut sync :
Branche :
HEAD local :
HEAD distant :
Fichiers changes :
Livrables SELAS :
Tests/smokes :
Statut SELAS :
Push :
Blocage :
Prochaine action :

Reste en NO-GO dev sauf GO Gad deja trace.
```

## Rapport Gad quand la sync manque

Format court :

```text
Statut flux Naomi : [projet / sprint / phase annoncee ou inconnue / GO-NO-GO]
Avancement depuis le dernier point : avancee annoncee par Gad, mais absente des traces publiees.
Prochaine etape : demander a Naomi un Sync checkpoint ou lire le thread source si accessible.
Blocage / risque : sync Git/thread manquante ; le rapport boss ne peut pas verifier les livrables.
Fiabilite : non verifiee tant que commit pousse ou Sync packet absent.
```
