# Carnet de reproches à Rafael

> **PRIVÉ — pour Gad uniquement.** Ne JAMAIS le remonter à Rafael ni le mentionner dans un message qui
> lui est destiné pendant le projet (cf. mémoire `rafael-collaboration-grievances.md`, confidentialité
> dure). Matériel de pilotage + débrief éventuel, pas une arme à dégainer maintenant. Gad décide.
>
> **Règle d'or** : on ne reproche QUE ce qui est **prouvé** (faux alors qu'il était à jour, OU faute
> de méthode documentée sur le vécu de Gad). Sinon = vrai retour (on le traite) ou notre gap.
>
> **Source riche** : `rafael-collaboration-grievances.md` (griefs G1-G4 + éval honnête 75-85% + leviers).
> Ce carnet = la version **vérifiée** (gate adversarial 2026-06-24, « avocat de la défense » par point).

## ✅ Reproches qui TIENNENT (par gravité)

| # | Date | Ce que Rafael a fait | Réalité / preuve | Verdict |
|---|---|---|---|---|
| **G3** sources de vérité | 06-22 (incident antérieur) | T'a juré **plusieurs fois** que « Documents générés par cas » était la **SEULE** source de vérité — tu lui as explicitement demandé « pas de règles genre/pluriel ailleurs ? » → « non, tout est dedans » | **FAUX, et le plus coûteux.** Il y avait **aussi tout le NotebookLM** (règles genre/pluriel/durée/légal). Résultat : **ton premier travail entièrement refait.** La complétude des inputs = **son** job (tu fais le technique, tu ne connais rien au droit des sociétés), pas le tien. | 🟥🟥 **CAPITAL.** Fausse assertion sur les sources → **rework total**. C'est ce qui a donné `SOURCES_DE_VERITE.md` (NotebookLM en source #1). |
| **RR-04** (=G2) validation aveugle | plusieurs **semaines**, révélé un **vendredi ~9h30** avant son RDV de 10h | A validé « **c'est bon, c'est bon** » pendant des semaines **sans générer ni tester** les documents | **CAPITAL.** Le reproche n'est PAS « il a vu 4/7 docs » — c'est l'**inverse** : ne le découvrir qu'à 9h30 avant son RDV **prouve** qu'il ne générait même pas les docs (sinon le 4/7 saute aux yeux d'emblée). | 🟥🟥 Process/workflows/règles bâtis sur ses **fausses validations** → **avancé dans le vide** → **reconstruction sur plusieurs jours.** Le 4/7 = la **preuve** du non-test, pas le reproche. |
| **RR-03** (=G4) fait tester le BOSS en live | 06-22 | A fait tester la SCM à **David (le boss/décideur) + Albane**, en **live**, pendant qu'on travaillait encore | **Grave.** Conséquence concrète : Gad **ne peut plus rebooter pour déployer** les fixes — si l'interface redémarre pendant que David teste, **le boss croit que ça ne marche pas**. Rafael a **paralysé le déploiement** + mis la **perception du décideur** en otage, sans coordination dev. | 🟥 **Sabotage opérationnel (con ou calculé, même effet).** Pas un bug fantôme (le fix SCM était poussé `c2d3498`) : c'est l'**exposition du boss à du non-déployé** + le **piège du reboot**. Aggrave G2 : au lieu de tester lui-même, il mobilise les clients. |
| **RR-01** SCM valeur de part | 06-24 | « ça ne s'est pas appliqué à la **SCM** pour la **valeur de la part** » | **FAUX, et il était à jour.** Valeur auto-calculée (champ grisé « (calculée) »), test vert. Push **05:14**, reboot **05:18**, son retour **09:58** → version corrigée + rebootée **~4 h avant**. | 🟥 **Connerie.** Marchait sous ses yeux, aucune excuse de version. |
| **G1** réouverture du « 100% validé » | 06-22 | Rouvre une remarque sur la **SELARL** déclarée « **100% validée** » il y a longtemps (le *gold* sur lequel tout le reste est bâti) | Nouvelle remarque confirmée (pas une régression) — mais sur un socle annoncé top. | 🟧 **Légitime mais le plus mou** (ton éval) : la validation humaine par sondage est faillible par nature ; le vrai remède = vérification systématique (ce qu'on construit). Entame quand même la confiance dans le socle. |

## ⛔ NE PAS lui ressortir — il avait RAISON ou c'était NOTRE bug

Ces points **paraissaient** des conneries mais la défense les a **réfutés**. Les brandir te ferait
**passer pour un con**.

| Point | Ce qui s'est vraiment passé |
|---|---|
| **RR-02 — « il manque le compromis cabinet médical »** (06-22) | ✅ **Rafael avait RAISON.** En SELAS‑acte le compromis (DOC‑010) n'était **réellement pas généré** ; on a livré le fix **O24‑14 8 h après** son retour (`10f3e9f`). **Notre bug.** |
| **R6/R9 — re-signal de R1/R3** (06-23) | Fixes codés (`ae234e9`) mais **pas déployés** → il ne pouvait pas les voir. **Notre gap.** |
| **« 10 euro sans s » au PV de nomination** (06-08) | ✅ Il avait raison : « euro » singulier hardcodé dans ~7 générateurs, jamais de vraie logique pluriel. |
| **« calculateur valeur de parts pas dupliqué SELAS »** (06-18) | Excusé (pas de reboot confirmé) + partiellement légitime (raison sur SAS/SPFPL en saisie libre). |
| **« vendeur cession pas sélectionnable »** (06-24) | Le selectbox existait mais « peu découvrable » — verbatim de **notre** commit de fix (`d8393f8`). UX réelle. |

## 🔎 Verdict de complétude (gate adversarial)

> **« Pas de mine cachée. »** Croisé les dates de commit git contre chaque re-signal + tracé tous les
> reboots confirmés (2 seulement). Tout autre candidat tombe dans « excuse » (pas déployé/rebooté) ou
> « Rafael avait raison ».

## Le bilan, sans fard

Tu pensais « énormément de conneries ». Vérifié un par un :

- **🟥🟥 CAPITAL — G3 (sources)** : t'a caché le NotebookLM comme source → **1er travail entièrement refait.**
- **🟥🟥 CAPITAL — RR-04 (validation aveugle)** : « c'est bon » des semaines sans tester → **avancé dans le vide** → reconstruction sur plusieurs jours.
- **🟥 GRAVE — RR-03 (boss en live)** : a piégé ton déploiement (tu ne peux plus rebooter sans que David croie que c'est cassé).
- **🟥 RR-01** : connerie béton (SCM, à jour, sous ses yeux).
- **🟧 G1** : réouverture du socle « 100% validé » — le plus mou.
- **⛔ RR-02** : là **il avait raison** (compromis = notre bug). Idem d'autres re-signals.

⚠️ **Le 4/7 a deux faces** : (a) SELAS vraiment incomplète = **notre bug** (corrigé) ; (b) ne l'avoir vu
qu'à la fin après des semaines de « c'est bon » = **sa faute** (RR-04). Les deux à la fois.

**Le vrai fond est lourd** : sa discipline de test + sa gestion des sources/clients ont coûté des
semaines. Mais garde la rigueur sur les **bugs précis** (RR-02 = il avait raison).

## Les leviers (convertir les griefs en garde-fous — côté Gad)

1. **Contrat d'inputs écrit** en amont : liste exhaustive signée de TOUTES les sources/règles (docs,
   NotebookLM, genre/pluriel). « Je construis UNIQUEMENT là-dessus ; hors liste = inexistant. » → tue G3.
2. **Definition of done de test** : checklist que Rafael remplit par tour (télécharger les N docs, ouvrir
   chacun, vérifier chacun). Pas de retour accepté sans. → tue G2/RR-04.
3. **Vérification automatisée de notre côté** (audits + protocole gold) — ne pas **dépendre** que son
   test manuel soit complet. La vraie assurance.
4. **Environnements séparés** : le client teste une **URL stable figée** ; le dev/les fixes vont sur un
   **staging séparé**. → on n'est plus jamais **paralysé** par un client qui teste en live (le piège RR-03).
