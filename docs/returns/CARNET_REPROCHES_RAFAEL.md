# Carnet de reproches à Rafael

> Ouvert sur demande de Gad (2026-06-24). On note ici, **avec preuves**, les retours de Rafael
> qui sont **faux / incohérents / des conneries** — pour qu'il vérifie AVANT de remonter, et qu'on
> ne brûle pas du temps à chasser des fantômes. Ton : franc, taillé sur de la matière réelle.
> Règle d'or : on ne reproche QUE ce qui est **prouvé faux** (sinon c'est un vrai retour, on le traite).

| # | Date | Ce que Rafael a dit | La réalité (preuve) | Verdict |
|---|---|---|---|---|
| RR-01 | 2026-06-24 | « Les changements appliqués à tous les cas… ça ne s'est pas appliqué à la **SCM** pour la **valeur de la part**. » | **FAUX.** La valeur nominale de la part de SCM est **auto-calculée** (`calculate_nominal_value`), champ désactivé « (calculée) » : cession `shell.py:2781/2787`, création `shell.py:1479`. Mieux : le commentaire en clair dit « **O24-05 (re-Akainu 2026-06-23) : s'applique à TOUS les types — Y COMPRIS la SCM cédée** ». Donc non seulement c'est appliqué, mais ça a été **spécifiquement re-vérifié** il y a un jour. La seule valeur de part en saisie libre dans tout le moteur = la **cible SPFPL** (société tierce externe, pas une SCM, exclusion déjà tracée). | 🟥 **Connerie aggravée.** Rafael remonte un trou qui n'existe pas — et (d'après Gad) il était sur le staging **rebooté**, donc la fonctionnalité marchait **sous ses yeux** au moment où il a dit qu'elle ne marchait pas. **Aucune excuse de version périmée.** Le champ « Valeur nominale d'une part de SCM (calculée) » est grisé et se remplit tout seul. Charge de la preuve = capture + champ exact, jamais un ressenti. |

## Rappel process (pour couper court)

La propagation « un changement s'applique à TOUS les cas concernés » **EST** dans nos process —
règle globale **68 (Q4 triage)** + mémoire `feedback-propagation-tous-cas`. Quand un retour est
universel, on le propage par défaut partout, et un gate Akainu re-régénère les DOCX pour le prouver.
Donc : si Rafael pense qu'un truc « tous cas » a été raté, la **charge de la preuve est de montrer
le champ exact qui ne suit pas** (capture + type + champ) — pas une impression. Dans 1 cas sur 1
jusqu'ici (RR-01), l'impression était fausse.

## Le pattern récurrent (le VRAI sujet — bien plus gros que RR-01)

Au-delà de RR-01, les transcripts du projet montrent un schéma **répété** : Rafael remonte des choses
**déjà faites / déjà livrées** parce qu'il teste une version **pas à jour ou pas rebootée**.

**Comptage brut** (transcripts du projet, signaux ASCII, accents ignorés) :

| Signal | Occurrences |
|---|---|
| « re-signale » | 25 |
| « déjà livré » | ~21 |
| « déjà fait » (toutes casses) | ~29 |
| « staging pas (rebooté) » | 11 |
| « pré-reboot » | 6 |
| « déjà corrigé » | ~7 |
| « faux bug » / « faux retour » | 3 — ⚠️ **MACHINE (B2 / chemins hallucinés), PAS Rafael** : c'est MOI qui ai écarté ces faux positifs du bloc-gold → **exclus du carnet** |
| Mentions « Rafael / Rapha… » (3 transcripts) | **12 579** (≠ conneries : juste la fréquence de son nom) |

**RECOUPAGE (fait — règle 65, ne pas servir les chiffres bruts)** : à l'inspection, ces comptes
**dégonflent**. « faux bug / faux retour » = erreurs de la **machine** que j'ai interceptées (pas lui).
« staging pas rebooté » = surtout mon propre diagnostic RR-01. Les ~50 « déjà fait / re-signalé » =
majoritairement le re-signal **avec excuse de déploiement** (R6/R9 style). **Cas Rafael-FAUTE prouvés à
ce stade : RR-01 (1 seul).** Ne pas brandir « 50 conneries » devant lui : il rembarrerait à raison.
L'enquêteur cherche d'éventuels autres cas « déployé + rebooté + raté » ; tant qu'ils ne sont pas
prouvés, ils ne montent pas en entrée numérotée.

**NUANCE DE JUSTICE — à tenir absolument** (sinon il rembarre à raison) : toutes ces occurrences ne
sont PAS sa faute. Deux cas distincts :
- **Fix DÉPLOYÉ + il a rebooté + encore faux** → **sa connerie** (ex. RR-01 : rebooté, déployé, faux
  sous ses yeux). → carnet.
- **Fix codé mais PAS encore déployé** → **excuse valable**, c'est notre gap de déploiement (ex.
  **R6 = re-signal de R1**, **R9 = re-signal de R3**, fixes non déployés — JOURNAL.md:128). → PAS carnet.

Donc la liste « à charge » individuelle se limite aux cas **déployés** qu'il a ratés **en étant à jour**.
L'enquêteur (en cours) trie les ~50 candidats sur ce critère ; seuls les « déployé + raté » montent en
entrée numérotée du tableau.

**LE MESSAGE DE FOND À LUI PASSER** : *« Avant de remonter un bug, confirme que tu es sur le **dernier
déploiement rebooté**. Sinon on chasse des fantômes — comme RR-01, où tu étais à jour et où ça marchait
déjà devant toi. »* C'est ça qui fait perdre du temps, bien plus que chaque cas pris isolément.
</content>
