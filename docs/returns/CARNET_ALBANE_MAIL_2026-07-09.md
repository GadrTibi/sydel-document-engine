# Retours Albane — email « Re: Validation documents - Suite » (2026-07-09, 12h00)

Source : mail direct Albane LALLEMAND (Direction Juridique SYDEL). Contexte = **création MICRO-HOLDING** (société civile). Verbatim = spec. Images extraites : `scratchpad/albane_mail/img_01..09.png`.

## FRONT / UX (saisie)

| # | Retour (verbatim condensé) | Image | Propagation | Statut |
|---|---|---|---|---|
| A1 | **Date de clôture** : champ pré-rempli mais hint « Format attendu : JJ/MM/AAAA » incohérent → **enlever le hint** | img_05 | micro (+ civils ?) | à faire |
| A2 | **Adresse siège = perso** : case cochée mais l'adresse perso de l'associé ne s'affiche pas | — | micro | à faire (bug) |
| A3 | **Apport → nb parts auto** : « le nombre de parts peut-il se mettre d'office avec une formule » (nb = montant apport / valeur nominale de la part) | img_03 | micro | à faire (défaut = montant/valeur_part) |
| A4 | **Dept naissance étranger** : ajouter « (ou pays si étranger) » | — | tous | à faire |
| A5 | **Fonction / Titre d'affichage confus** : « je ne sais pas quoi remplir » ; gérant micro = titre toujours le même ; « titre d'affichage » = ? | img_06 | micro | à faire (pré-remplir/clarifier/supprimer) |
| A6 | **Lettre option IS** : pas besoin de cocher, toujours présente | — | micro (civils IS) | à faire (toujours générée) |
| A7 | **CP + VILLE** : regrouper en une ligne | — | tous civils | à faire |
| A8 | **Blocages trop stricts** : pouvoir éditer même sans banque / régime matrimonial du 2e associé / parents d'un associé non-gérant | img_07 | tous | à faire (assouplir blocages non-critiques) |
| A9 | **SIE (BONUS)** : trouver le SIE depuis l'adresse, ou mettre le lien impots.gouv.fr ; « laisser en l'état n'est pas un souci » | — | — | BONUS (optionnel) |

## DOCUMENTS

| # | Retour | Image | Propagation | Statut |
|---|---|---|---|---|
| B1 | **Dates de naissance dans les STATUTS** au format « JJ mois AAAA » (pas JJ/MM/AAAA) | — | tous (convention) | à faire (même fix qu'avenant) |
| B2 | **SIREN inexistant** → toujours « en cours d'immatriculation » en dur dans les docs | — | tous | à faire |
| B3 | **Statuts art.7 capital** : présentation comme les modèles (aligner nb de parts, tirets sur les associés, espacer) | — | micro (+ civils) | à faire (mise en forme) |
| B4 | **Statuts signature** : centrer les noms des associés à la fin (comme img_09) | img_08→09 | micro | à faire |
| B5 | **Annexe** en 3 cadres → 1 seul (comme fix SPFPL) | img_04 | micro | à faire |
| B6 | **Domiciliation** : « dans les locaux du cabinet » → « dans les locaux au » (retirer « du cabinet ») pour TOUTES les sociétés civiles (OK garder pour SEL/SPFPL) | — | civils (SCI/SCM/SCS/micro) | à faire |
| B7 | **DNC uniquement pour les GÉRANTS** : « pas nécessaire de générer une DNC pour les associés qui ne sont pas gérants » | img_07 | tous | ⚠️ **CONFLIT** (voir note) |

## PV (micro-holding)

| # | Retour | Image | Statut |
|---|---|---|---|
| C1 | Entête + 1ʳᵉ phrase : retirer « micro holding » → « Société civile » (en dur) | — | à faire |
| C2 | « au capital de xx € » → « à capital variable, au capital minimum et effectif de » (comme statuts) | — | à faire |
| C3 | Date du PV dans l'encadré → format « 09 JUILLET 2026 » (entier, majuscule) | — | à faire |
| C4 | Noms de signature : permettre au client de signer sous son nom (noms + espace, comme img_09) | img_08→09 | à faire |
| C5 | **Procuration** : le nom en bas de l'associé → aligné à DROITE | — | à faire |

## B7 — DNC gérants uniquement — ✅ TRANCHÉ (Rafael 2026-07-09 16h59 : « ouais il a raison »)

Rafael concède : **DNC pour les GÉRANTS uniquement**, pas les associés non-gérants (Albane a raison, il avait oublié). Supersede son retour du matin « 1 DNC par associé ». → Inverser : la génération DNC ne vise que les gérants PP ; ajuster R11 (nb DNC = nb **gérants** PP, pas nb associés). Conséquence liée : un associé non-gérant n'a plus besoin de filiation/parents (cf. A8).

## Retours Rafael 2026-07-09 (5 docs micro-holding générés + accents)

| # | Retour | Propagation | Statut |
|---|---|---|---|
| R-D1 | **« Demeurant [adresse] » → « Demeurant au [adresse] »** sur CHAQUE adresse | tous (universel — ~19 spots ; la procuration a déjà « au ») | à faire + règle conformité |
| R-D2 | **Fautes d'orthographe / accents manquants** « un peu partout » dans les éléments injectés ET le moteur (micro-holding = type sans référentiel) | à cibler | ⚠️ linter R4 AVEUGLE (lexique) — voir note |

### ⚠️ Note accents — cause racine (même défaut que Docteur)
Notre linter R4 est un **lexique** (~50 mots) → il dit « 0 faute » sur les 5 docs alors que Rafael en voit. Un mot non accentué **hors liste** passe au vert. Fix systémique = détecteur **générique** (dico FR), mais aucun spellchecker installé. **En attente : les docs re-générés par Rafael + un exemple précis** pour cibler les mots exacts, puis (a) les corriger, (b) upgrader R4 vers un détecteur générique. PV `399c4e9a-PV_nomination_ge_rant.doc` = format .doc (illisible par python-docx) à convertir.

## Défauts logiques tranchés seul (défauts sensés, annoncés)
- A3 formule : nb parts = montant apport ÷ valeur nominale de la part (Albane écrit « prix × montant » mais la logique = division ; valeur nominale connue au contexte).
- A8 : rendre optionnels les champs non-critiques (banque si dépôt non fait, régime matrimonial/parents d'un associé NON-gérant) ; garder bloquants les champs vraiment requis pour les docs demandés.
- A5 « titre d'affichage » : c'est le titre pro (Docteur…) — clarifier le libellé ou pré-remplir « gérant » sur la fonction micro.
