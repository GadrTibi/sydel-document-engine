# Message Rafael (avec message Albane embarqué) — 2026-06-30

> Re-audit global de fin. 31 questions passées au crible → 17 déjà réglées (sources / build / décisions),
> 4 chantiers que je fais seul → restent quelques points pour Albane. Ci-dessous : 1 message à Rafael
> (contexte) + 1 message Albane prêt à copier-coller.

---

## À RAFAEL (contexte)

Salut Rafael,

Petit point avant qu'Albane teste en grand. On a fait un **re-audit global** du moteur : la quasi-totalité
est validée et fidèle à ses modèles.

Le truc à comprendre sur les questions ci-dessous : pendant des semaines, chaque fois qu'un wording métier
n'était pas 100 % clair, on n'a **pas bloqué** — on a appliqué le **défaut le plus sensé** et on a **parké**
la question pour confirmation plus tard (sinon on n'avançait jamais). Le produit **marche** avec ces défauts.
Là on arrive à un état propre, donc je sors les **quelques points** qui méritent vraiment l'avis d'Albane
avant de figer — surtout ceux où un document sortirait **faux** sans son arbitrage. Tout le reste, on garde
nos défauts (rien n'est cassé).

**Tu peux copier-coller le message ci-dessous directement à Albane :**

---

## À ALBANE (à copier-coller)

Bonjour Albane,

On a fait un **re-audit global** du moteur avant que tu testes en grand — la quasi-totalité est validée et
fidèle à tes modèles. Restent quelques points où on préfère ton feu vert avant de figer définitivement :

**1) Points où un document généré changerait selon ta réponse**
- **Inscription à l'Ordre** — tu nous as donné deux formes : « Conseil départemental de l'Ordre des médecins
  **du Rhône** » (26/06) et « Conseil départemental de l'Ordre **du Calvados des médecins** » (30/06).
  Laquelle est la forme définitive (pour tous les ordres) ? On a appliqué la version du 30/06.
- **Compromis de cession en SELAS** — le titre de clause affiche encore « Inscription de la **SELARL** au
  Tableau de l'Ordre… », figé du modèle SELARL. Pour une cession portée par une SELAS, il afficherait à tort
  « SELARL ». On le rend dynamique (forme réelle de l'acquéreur), ou tu le veux littéralement « SELARL » ?

**2) Nouveaux types (SASU Holding, micro holding) — fidélité à tes modèles**
- **SASU Holding — domiciliation** : on garde le symbole « € » + la date numérique (« 22/10/2025 ») de ton
  modèle SAS, ou les conventions communes qu'on applique à tous les types (« euros » en toutes lettres +
  date longue) ? Un seul modèle déroge, donc on te laisse trancher la cohérence.
- **Micro holding** : (a) on capture le **nom d'usage** « épouse <nom> » et on l'affiche en comparution comme
  ton modèle ? (b) sur la domiciliation, on met la **dénomination réelle** de la société, ou la forme
  générique « la Société micro holding » de ton modèle ?

**3) Détails cosmétiques** — on a mis un défaut raisonnable, dis-nous juste si ça te gêne : espace insécable
avant « Rappel : » (dans la déclaration de non-condamnation), présentation des statuts dentiste, date du
courrier d'avertissement au conjoint, et mise en toutes lettres d'une valeur nominale décimale.

Merci !

---

## Ne plus demander — 17 réglées (détail traçable)
SASU = 1 actionnaire (modèle+build+décision) · « de l'Ordre » gardé (30/06) · SP2/§14.2 Docteur (fait) ·
« Le Docteur » corps SPFPL (modèle, verbatim=civilité) · majoration 2 vs 3 points (« reprendre le modèle »
= chaque modèle) · RCS cible cession (cible immatriculée) · forme PV (modèle+fixes juin, fait) · R1
modèle=cible (oui) · **lettres SPFPL DOC-005/006 (tes modèles les contiennent → gardées)** · aération
(compact, décision Gad) · MH signature (toutes lettres, convention) · N4 plages « à » (français correct) ·
SASU « Fait pour servir » (omis, absent du modèle SAS).

## Chantiers — je les fais seul (aucune décision métier)
ANO-045 (DOC-045 au bundle SELAS) · A26-PV5 (profession+régime dans le PV) · A26-label (« PV nomination
dirigeant ») · labels date inter-SEL · SASU « Fait pour servir » omis · salarié incomplet (formulaire bloque) ·
MH signature (date longue + « Mme ») · N4 accent « à » généralisé.
