# Carnet de reproches à Rafael

> Ouvert sur demande de Gad (2026-06-24). On note ici, **avec preuves vérifiées**, les retours de
> Rafael qui sont **faux alors qu'il était à jour**. **Règle d'or** : on ne reproche QUE ce qui est
> **prouvé faux ET sous ses yeux** (fix déployé + Streamlit rebooté au moment du retour). Sinon =
> vrai retour (on le traite) ou notre gap de déploiement (notre faute).
>
> **Vérifié par gate adversarial (2026-06-24)** — workflow « avocat de la défense de Rafael » : 1 agent
> par reproche dont la **mission était de le RÉFUTER** + 1 critique de complétude (5 agents, ~490k
> tokens). Seuls les reproches qui ont **survécu à la défense** figurent en « tiennent ».

## ✅ Reproches qui TIENNENT (vérifiés)

| # | Date | Ce que Rafael a dit | Réalité (preuve vérifiée) | Verdict |
|---|---|---|---|---|
| RR-01 | 2026-06-24 | « ça ne s'est pas appliqué à la **SCM** pour la **valeur de la part** » | **FAUX, et il était à jour.** Valeur nominale de part SCM **auto-calculée**, champ grisé « (calculée) » (`calculate_nominal_value`, cession + création), test `test_selarl_scm_cedee_valeur_nominale_calculee` **vert**. Chronologie prouvée : push **05:14**, reboot **05:18**, son retour **09:58** → il avait la version corrigée **+ rebootée ~4 h avant**. | 🟥 **Connerie confirmée (HAUTE).** Ça marchait sous ses yeux. Aucune excuse de version périmée. |
| RR-03 | 2026-06-22 | A envoyé un mail à **Albane + David (les clients)** pour leur faire tester la SCM, avant qu'on ait fini/rebooté | **Faute de MÉTHODE confirmée (HAUTE).** Au moment du mail, le Streamlit n'était **pas rebooté** (Gad a rebooté **4 min après**, 12:29) → les clients voyaient l'ancienne version. Les messages « à retester » étaient adressés **à Rafael**, jamais « fais tester les clients ». Il a mobilisé seul le décideur + la juridique sur du non‑confirmé‑déployé. | 🟧 **Reproche de méthode (HAUTE, ~80%).** ⚠️ Caveat honnête : le fix SCM **était poussé** (`c2d3498`) → ce n'est PAS un bug fantôme. À lui dire sous l'angle **exposition‑client prématurée + coordination/reboot**, jamais « tu as fait tester un truc cassé ». |
| RR-04 | sur **plusieurs semaines**, révélé un **vendredi ~9h30** (avant son RDV de 10h) | A validé « **c'est bon, c'est bon** » de façon répétée pendant des semaines, **sans générer ni tester réellement** les documents | **Faute CAPITALE (HAUTE — recadrée sur le vécu de Gad).** Le reproche n'est **PAS** « il a vu 4/7 docs » — c'est l'**inverse**. Il n'a découvert qu'à **9h30, juste avant son RDV**, que la SELAS ne générait que **4 docs sur 7** → ça **prouve** qu'à chacun de ses « c'est bon » des semaines précédentes, **il ne générait même pas les documents** (sinon le 4/7 saute aux yeux au premier coup d'œil). On ne peut pas inspecter des docs qu'on n'a pas générés. | 🟥🟥 **LA PLUS GRAVE.** Process, workflows et règles bâtis sur ses **fausses validations** → **avancé dans le vide** pendant des semaines → **reconstruction en profondeur sur plusieurs jours.** Le 4/7 n'est pas le reproche : c'est la **preuve** du non‑test prolongé. _(La passe de vérif adversariale avait à tort « réfuté » ce point en lisant le 4/7 au 1er degré — elle a raté que la découverte tardive PROUVE le non‑test antérieur. Corrigé.)_ |

## ⛔ NE PAS lui ressortir — il avait RAISON ou c'était NOTRE bug

Ces points **paraissaient** des conneries mais la défense les a **réfutés**. Les brandir te ferait
**passer pour un con** : il a la preuve de son côté.

| Point | Ce qui s'est vraiment passé |
|---|---|
| **RR-02 — « il manque le compromis de cession cabinet médical »** (06-22 12:06) | ✅ **Rafael avait RAISON.** En SELAS‑acte, le compromis (DOC‑010) n'était **réellement pas généré** (l'étape filtrait). On a livré le fix **O24‑14 le soir même** (`10f3e9f`, 22:07 = **8 h après** son retour) puis le lendemain. Les docstrings des tests disent littéralement « avant le fix, le compromis manquait ». **Notre bug.** Sa remontée ne nommait aucune structure → le verdict « non‑bug » initial reposait sur une hypothèse fausse (« il testait du SELARL en acte »). |
| **R6/R9 — re-signal de R1/R3** (06-23) | Fixes codés (`ae234e9`) mais **pas déployés** quand il a re-signalé → il ne pouvait pas les voir. **Notre gap, pas sa faute.** |
| **« 10 euro sans s » sur le PV de nomination** (06-08) | ✅ Rafael avait raison : « euro » singulier hardcodé dans ~7 générateurs, jamais de vraie logique pluriel. |
| **« calculateur valeur de parts pas dupliqué pour la SELAS »** (06-18) | Excusé (pas de reboot confirmé entre le push 06-17 soir et le re-signal) **+ partiellement légitime** (il avait raison sur SAS/SPFPL encore en saisie libre à ce moment). |
| **« vendeur en cession pas sélectionnable parmi les associés »** (06-24) | Le selectbox existait, mais **« en haut du bloc, peu découvrable »** — verbatim de **notre propre** commit de fix (`d8393f8`) qui l'a déplacé. Légitime, UX réelle. |

## 🔎 Verdict de complétude (gate adversarial)

> **« RIEN DE SOLIDE EN PLUS — pas de mine cachée. »** Le critique a croisé les dates de commit git
> contre les timestamps de chaque re-signal + tracé **tous** les reboots confirmés du transcript
> (seulement **2** : 06-22 12:29 et 06-24 autour de RR-01). Tout autre candidat tombe dans le seau
> « excuse » (pas déployé / pas rebooté) ou « Rafael avait raison ».

## Le bilan, sans fard

Vérifié un par un — et **RR-04 change le poids du tout** :

- **🟥🟥 LA PLUS GRAVE — RR-04** : **validation à l'aveugle pendant des semaines** (« c'est bon » sans générer ni tester), prouvée par la découverte de dernière minute du 4/7. Tu as **avancé dans le vide** → **reconstruction de process / workflows / règles sur plusieurs jours.** Erreur **capitale** de confiance.
- **🟥 RR-01** : une connerie béton (faux, à jour, sous ses yeux).
- **🟧 RR-03** : faute de méthode (exposition‑client prématurée).
- **⛔ Ce qui TOMBE — RR-02** : là **il avait raison** (compromis = notre bug). Idem sur d'autres re-signals.

⚠️ **Le 4/7 a deux faces, ne les confonds pas** : (a) la SELAS était vraiment incomplète = **notre bug**, qu'on a corrigé (il avait raison de le signaler) ; (b) qu'il ne l'ait **vu qu'à la fin** après des semaines de « c'est bon » = **sa faute** (RR-04, il validait sans tester). Les deux sont vraies en même temps.

Donc le **vrai fond est lourd** : sa discipline de test était défaillante (RR-04 le prouve noir sur blanc) et ça a coûté des jours. Mais garde la rigueur sur les **bugs précis** : vérifie avant d'accuser (RR-02 = il avait raison).

## Le VRAI levier (à lui passer)

> *« Avant de remonter un bug, confirme que tu es sur le **dernier déploiement rebooté** — sinon on
> chasse des fantômes (cf. RR-01). Et quand tu remontes, donne la **structure + le champ exact**, pas
> une impression. »*

C'est ça qui fait gagner du temps des deux côtés — **bien plus que de lui sortir une liste qui se
retournerait contre toi.**
