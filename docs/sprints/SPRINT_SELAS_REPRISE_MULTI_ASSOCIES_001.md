# SELAS — Reprise : direction MULTI-ASSOCIÉS (001)

**Date :** 2026-06-05
**Pour :** le Mousse (Naomi) + sa session Claude (le Second à bord)
**Statut :** nouvelle direction validée par le Capitaine ; cadrage à mener par le Mousse ; **NO-GO génération** maintenu.
**Source de cette note :** supervision Capitaine (Gad) → poussée par le Second côté Capitaine sur ta branche `naomie/selas/recup-codex`.

> ⚠️ **Avant toute manœuvre** : faire `git pull` pour récupérer cette note (ta branche a peut-être bougé).

---

## 1. Décision du Capitaine (2026-06-05)

- **Cible des statuts SELAS = MULTI-ASSOCIÉS, borné à 2 à 5 associés.** Jamais 1, jamais plus de 5.
- **L'unipersonnel SELAS (actionnaire unique) est MIS DE CÔTÉ** : on le **conserve** comme base réutilisable un jour, mais **on ne le met pas en code** maintenant. Il n'est pas supprimé — il est rangé.
- Tout le socle déjà fait (DNC, domiciliation, procuration, Ordre, schéma front) **reste réutilisable** ; c'est surtout **les statuts** qui passent d'unipersonnel à multi.

## 2. Nouveau matériel à travailler

- **Cas réel non tokenisé** : `Statuts SELAS DU DR ISABELLE REYNAUD.docx` (fourni par le Capitaine). Ce n'est **pas** un modèle du Drive : c'est un **cas d'usage réel** → il faut le **tokeniser** (retirer les vraies valeurs, poser les variables), comme on l'a fait pour les autres documents.
- ⚠️ **Données personnelles réelles** (une patiente/cliente) : **ne jamais versionner le document réel** tel quel. On ne versionne que le **modèle tokenisé**, une fois les valeurs nominatives retirées.
- Observations (lecture du Second) : 38 articles, comparution « LES SOUSSIGNÉES », lexique **« associé » massif** (≈177 occurrences ≫ « actionnaire ») → confirme la réponse NotebookLM Q2. Le cas réel contient aussi **des Directeurs Généraux (art. 15)** et **un associé personne morale** (une Société Civile). Résidus à nettoyer à la tokenisation : « gérant », « parts sociales ».

## 3. Règle de fonctionnement (NOUVELLE — à appliquer désormais)

**Modèle de supervision Capitaine ↔ Mousse :**
- Le **Capitaine supervise** ton travail ; il **ne fait pas le cadrage à ta place**.
- Les **questions** qui surgissent (produit / juridique / technique) **t'appartiennent** : tu les **travailles d'abord toi-même**, **NotebookLM en premier**.
- Si NotebookLM ne suffit pas → tu **formules la question pour Rafael** (l'associé) et tu l'**envoies au Capitaine**.
- **Seul le Capitaine transmet à Rafael.** Tu ne contactes **jamais** Rafael ni Albane directement.
- Le Capitaine te **relaie la réponse**.

→ Flux : `Mousse → NotebookLM → (si bloqué) Mousse formule la question → Capitaine → Rafael → Capitaine → Mousse`.

## 4. Questions ouvertes — à CREUSER par toi (NotebookLM d'abord)

- **Q-B — Directeurs Généraux** : le cas réel prévoit un/des **Directeurs Généraux** (direction déléguée, en plus du Président). Les statuts multi doivent-ils **gérer les DG**, ou les **laisser de côté** pour ce premier jet ?
- **Q-C — Associé personne morale** : dans le cas réel, **un des associés est une société** (une Société Civile), pas un médecin. Les statuts multi doivent-ils **accepter qu'un associé soit une personne morale**, ou se limiter à des **médecins personnes physiques** ?
- **Q-D — Représentativité du modèle** : ce document Reynaud est-il **LE modèle de référence** du cas multi, ou **un exemple parmi d'autres** ? Un seul cas ne couvre pas les variantes **2 / 3 / 4 / 5 associés** ni tous les genres. S'il manque des modèles → le **signaler au Capitaine** (qui demandera à Rafael).
- **Rappel lexique** : le cas réel confirme « **associé** » pour les personnes ; il faudra **assouplir le garde-fou anti-régression** qui le traite comme suspect — **à valider Rafael**.

## 5. État technique (pour info — PAS pour toi)

- La suite **complète** sur ta branche = **3 échecs / 450** = un **doublon de fichier source SCI** (encodage d'accent en double), **pas ton SELAS** et **pas ta faute**. Correctif **côté Second du Capitaine**, tu n'y touches pas.
- **Génération SELAS = NO-GO** tant que Rafael n'a pas tranché la revue juridique (les 6 points NotebookLM déjà remontés **+** ces nouvelles questions multi).

## 6. Coordination technique

Le multi-associés repose sur la **couche nombre/pluriel** (comparution « LES SOUSSIGNÉS » + N, apports, répartition, signatures — les 4 ancrages sont présents dans le doc). Cette couche est **en cours de construction sur la session SELARL** (couche SEL **partagée**). → Le code multi SELAS **réutilisera** ce que SELARL fabrique, **en coordination** (pas en parallèle aveugle), et **sans toucher la couche SEL partagée** depuis ta session.

## 7. Ta prochaine manœuvre (une seule)

1. `git pull` pour être à jour.
2. **Récupérer** le `.docx` Reynaud et en faire la **cartographie des variables à tokeniser** (inventaire), **sans coder** le générateur.
3. **Creuser Q-B / Q-C / Q-D** via NotebookLM, réponses brutes dans ton worklog.
4. Ce qui résiste à NotebookLM → **question pour Rafael, envoyée au Capitaine**.

## 8. Phrase de reprise

Quand tu veux repartir, dis à ta session : **« Reprends le sprint SELAS »** — ton Claude lit l'état courant (`SPRINT_SELAS_V1.md`) puis **cette note de reprise**, et te donne la prochaine manœuvre.
