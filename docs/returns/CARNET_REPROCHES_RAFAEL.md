# Carnet de reproches à Rafael

> Ouvert sur demande de Gad (2026-06-24). On note ici, **avec preuves**, les retours de Rafael
> qui sont **faux / incohérents / des conneries** — pour qu'il vérifie AVANT de remonter, et qu'on
> ne brûle pas du temps à chasser des fantômes. Ton : franc, taillé sur de la matière réelle.
> Règle d'or : on ne reproche QUE ce qui est **prouvé faux** (sinon c'est un vrai retour, on le traite).

| # | Date | Ce que Rafael a dit | La réalité (preuve) | Verdict |
|---|---|---|---|---|
| RR-01 | 2026-06-24 | « Les changements appliqués à tous les cas… ça ne s'est pas appliqué à la **SCM** pour la **valeur de la part**. » | **FAUX.** La valeur nominale de la part de SCM est **auto-calculée** (`calculate_nominal_value`), champ désactivé « (calculée) » : cession `shell.py:2781/2787`, création `shell.py:1479`. Mieux : le commentaire en clair dit « **O24-05 (re-Akainu 2026-06-23) : s'applique à TOUS les types — Y COMPRIS la SCM cédée** ». Donc non seulement c'est appliqué, mais ça a été **spécifiquement re-vérifié** il y a un jour. La seule valeur de part en saisie libre dans tout le moteur = la **cible SPFPL** (société tierce externe, pas une SCM, exclusion déjà tracée). | 🟥 **Connerie.** Rafael remonte un trou qui n'existe pas. Diagnostic : il teste **un staging pas rebooté** (donc une vieille version), ou il regarde le mauvais champ. **À vérifier de SON côté avant de remonter** : reboot l'app + relis le champ « Valeur nominale d'une part de SCM (calculée) » — il est grisé et rempli tout seul. |

## Rappel process (pour couper court)

La propagation « un changement s'applique à TOUS les cas concernés » **EST** dans nos process —
règle globale **68 (Q4 triage)** + mémoire `feedback-propagation-tous-cas`. Quand un retour est
universel, on le propage par défaut partout, et un gate Akainu re-régénère les DOCX pour le prouver.
Donc : si Rafael pense qu'un truc « tous cas » a été raté, la **charge de la preuve est de montrer
le champ exact qui ne suit pas** (capture + type + champ) — pas une impression. Dans 1 cas sur 1
jusqu'ici (RR-01), l'impression était fausse.
</content>
