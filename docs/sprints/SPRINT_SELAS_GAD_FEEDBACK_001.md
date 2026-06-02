# SELAS Gad feedback 001

Date : 2026-06-01

Ticket : `SELAS-GAD-FEEDBACK-001`

Statut : `DONE - retour Gad analyse`

Decision sprint : `NO-GO dev maintenu`

## Retour Gad

> tu es sur de faire cas par cas ? Tu veux pas faire tous les cas d'un coup ?
> Et aussi il me semble que la SELAS et la SELARL sont relativement similaire,
> tu es conscient que tu as un agent qui est censé etre spécialisé pour savoir
> quoi réutiliser ?

## Lecture Codex

Ce retour ne vaut pas `GO dev`. Il demande une justification de strategie et une
meilleure utilisation explicite de la reutilisation SELARL / globale.

Gad pose deux questions distinctes :

1. faut-il developper tous les cas SELAS d'un coup plutot que cas par cas ?
2. l'audit de reutilisation SELARL / SELAS est-il bien pris en compte ?

## Reponse courte

Oui, la SELAS et la SELARL sont proches sur la structure de saisie, les roles
globaux, les adresses, la signature, l'Ordre, le capital et plusieurs documents
courts.

Non, il ne faut pas generer tous les cas SELAS d'un coup, car certains cas
changent le risque juridique :

- president au lieu de gerant ;
- actions au lieu de parts sociales ;
- actionnaire au lieu d'associe selon les zones ;
- statuts SELAS propres ;
- multi-actionnaires ;
- directeur general non source ;
- actions de preference ;
- micro-holding ;
- cession / SCM / derogations ;
- regime communautaire encore a arbitrer pour SELAS.

La bonne strategie est donc :

```text
mutualiser massivement les briques techniques et front,
mais activer la generation documentaire cas par cas.
```

## Clarification sur le role de l'audit reuse

L'audit de reutilisation a deja ete fait dans :

- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`.

Il conclut que le socle SELARL / global est reutilisable pour :

- methode de sprint ;
- roles et personnes ;
- adresses ;
- signature ;
- capital et titres, avec adaptation `actions` ;
- Ordre professionnel ;
- documents courts en `reuse-check` ;
- tests et structure front.

Mais il interdit la copie directe du wording SELARL :

- pas de remplacement aveugle `gerant -> president` ;
- pas de remplacement aveugle `parts -> actions` ;
- pas de statuts SELARL transformes automatiquement en statuts SELAS ;
- pas de multi-actionnaires ou actions de preference sans spec propre.

## Proposition ajustee apres retour Gad

Au lieu de presenter `SELAS-FRONT-SCHEMA-001` comme un mini-cas isole, le
presenter comme un socle reutilisable SELAS :

```text
SELAS-FRONT-SCHEMA-001 = socle commun SELAS reutilisable,
avec activation prudente du premier parcours generable.
```

Ce ticket pourrait preparer tous les cas au niveau front / structure :

- type dossier SELAS ;
- blocs communs ;
- roles president/actionnaire/signataire/mandataire/conjoint ;
- capital en actions ;
- documents candidats/reserves ;
- blocages visibles ;
- hooks futurs pour dentiste, multi-actionnaires, cession, SCM, derogation.

Mais il ne genererait toujours qu'un parcours autorise plus tard, apres specs
documentaires.

## Recommandation revisee

Demander a Gad un arbitrage reformule :

```text
GO dev SELAS-FRONT-SCHEMA-001 comme socle commun SELAS reutilisable,
sans generation documentaire, avec premier parcours activable limite a
SELAS medecin actionnaire unique president unique.
```

Ce compromis repond aux deux demandes :

- on ne refait pas tout cas par cas au niveau architecture ;
- on ne prend pas le risque juridique de generer tous les documents/cas d'un
  coup.

## Message pret a envoyer a Gad

```text
Oui, tu as raison sur le principe : la SELAS et la SELARL sont proches, et on
doit reutiliser au maximum le socle deja construit.

Ce que je propose, ce n'est pas de refaire chaque cas depuis zero.
La logique serait :

1. construire un socle commun SELAS reutilisable cote front/data :
   - type SELAS ;
   - roles president / actionnaire / signataire / mandataire ;
   - capital en actions ;
   - blocs Ordre, regime communautaire, signature ;
   - documents candidats et cas bloques ;
   - hooks pour les futurs cas dentiste, multi-actionnaires, SCM, cession, etc.

2. activer la generation documentaire progressivement, car le risque n'est pas
   le meme :
   - president vs gerant ;
   - actions vs parts ;
   - statuts SELAS propres ;
   - DG non source ;
   - actions de preference / micro-holding / multi-actionnaires ;
   - cession et SCM plus complexes.

Donc la demande de GO dev revisee serait :

GO dev SELAS-FRONT-SCHEMA-001 comme socle commun SELAS reutilisable,
sans generation DOCX/PDF/ZIP, et avec premier parcours activable limite a
SELAS medecin actionnaire unique president unique.

L'agent de reutilisation a bien ete utilise : son audit existe dans
SPRINT_SELAS_REUSE_AUDIT_001.md. Il conclut qu'on peut reutiliser beaucoup de
structure, mais pas copier le wording juridique SELARL tel quel.
```

## Decision de sortie

Le sprint reste en `NO-GO dev`.

La prochaine action est d'envoyer a Gad la reponse reformulee ci-dessus et
d'attendre une decision explicite.
