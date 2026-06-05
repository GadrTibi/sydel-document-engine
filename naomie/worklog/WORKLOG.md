# WORKLOG — la Chaloupe (le Mousse / Naomie) · projet Sydel

*Journal du flux du Mousse. Tenu par le second (Claude de Naomie). Source : les traces, pas l'oral.*
Périmètre : **SELAS — à confirmer Capitaine** · Branche : `naomie/selas/<ticket>` · Remote :
`https://github.com/GadrTibi/sydel-document-engine.git` · Compte Mousse : `naomiguetta10-prog`.

---

## Rapports boss (Capitaine)
*Différentiel, depuis les traces. Curseur = où en est le flux.*

| Date       | Période       | Synthèse                                                        | Curseur |
|------------|---------------|-----------------------------------------------------------------|---------|
| 2026-06-04 | armement      | Chaloupe armée — en attente du `GO dev` du Capitaine. Périmètre SELAS à confirmer. | NO-GO dev |
| 2026-06-04 | embarquement 1 | 1ʳᵉ embarquée du Mousse : clone neuf armé, protocole installé au global, briefing donné. Butin Codex localisé + diagnostiqué (lecture seule) = **Cas A** (1 commit non hissé). Bloqué au gate. | NO-GO dev — attente confirmation SELAS + GO dev |
| 2026-06-04 | HISSÉ ✅ | **Butin hissé** : accès *write* accordé à `naomiguetta10-prog`, `git push` OK. Branche `naomie/selas/recup-codex` (commit `4b0c106`) **visible sur GitHub**. PR à ouvrir. | Butin sur le navire — récupérable côté Capitaine |
| 2026-06-04 | audit butin | **Audit poussé du commit `4b0c106` demandé par le Capitaine** (3 relectures parallèles, lecture seule). Verdict : code **propre, 118/118 tests verts** (relancés en venv jetable), specs↔code alignées → **récupérable avec retouches mineures**. NotebookLM : **ne pas refaire** (plafond atteint, 0 citation source exploitable) ; suite = extraction passages DOCX réels + **revue humaine** (~11 points ouverts). SELAS V1 **gelé à un gate HUMAIN** (juriste/associé), pas un trou de dev. | Reco : GO dev sur la fondation technique ; génération doc SELAS = NO-GO tant que revue humaine non bouclée |

## Messages du Capitaine à transmettre au Mousse
*Le second transmet à Naomie puis passe le statut `à transmettre` → `transmis`.*

| Date       | Message                                                                 | Statut         |
|------------|-------------------------------------------------------------------------|----------------|
| 2026-06-04 | (placeholder) Confirmer le périmètre du Mousse : SELAS ? — réponse Capitaine attendue. | transmis |
| 2026-06-04 | **Passation Capitaine** : butin SELAS sain, mis à dispo tel quel. Correctif technique (2 DOCX SCI dupliqués + 2 imports) = **Second côté Gad**, PAS le Mousse. Génération SELAS = **NO-GO** tant que Rafael n'a pas tranché la revue juridique. **Manœuvre du Mousse = boucle NotebookLM** sur les points ouverts (1 question à la fois, réponse brute au worklog). | transmis |

## Décisions
*Décisions métier/produit prises (par le Capitaine) ou en attente.*

| Date       | Décision                                                                 | Statut    |
|------------|--------------------------------------------------------------------------|-----------|
| 2026-06-04 | Périmètre du Mousse = SELAS (« SELANCE / Célance » ≈ SELAS)              | À CONFIRMER Capitaine |

## Historique
*Faits horodatés du flux.*

- **2026-06-04** — Pack d'embarquement « la Chaloupe » créé dans le repo (`naomie/` + commande
  `/embarquer`). Chaloupe prête à être armée à la prochaine session de Naomie. NO-GO dev par défaut.
- **2026-06-04** — Mission d'ouverture notée : récupérer le travail SELAS commencé avec Codex (non
  poussé) et le pousser proprement sur `naomie/selas/<ticket>`, commits signés du compte de Naomie,
  puis Pack de passation. En attente confirmation périmètre + `GO dev`.
- **2026-06-04** — Pack raffiné : ajout du **Ton de bord — mode Mousse (pirate)** (gate « qui va là ? »
  corsaire ; accueil cadré habillé pirate ; interdits durs imagés mais intacts ; garde-fou anti-noyade)
  et de **`naomie/RECUP_CODEX.md`** (procédure béton pas-à-pas, pédagogie Git, pour retrouver + hisser le
  butin SELAS Codex). Ton normal avec le Capitaine. Aucun commit (laissé dans l'arbre pour relecture).
- **2026-06-04** — **Embarquement 1 du Mousse** exécuté (`/embarquer`) : (a) gate d'identité — Naomie
  confirmée le Mousse, mode pirate armé ; (b) protocole + règle copiés au global `~/.claude/` (1ʳᵉ install) ;
  (c) briefing de bord donné ; (d) remote du clone neuf vérifié OK, branche courante = `main` (cale dev
  `naomie/selas/<ticket>` pas encore créée, NO-GO).
- **2026-06-04** — **Récup Codex — diagnostic (lecture seule, RIEN modifié)**. Vieux dossier pointé par
  le Mousse : `/Users/naomiguetta/Desktop/sydel-document-engine`. État :
  - Branche courante : `codex/naomie-selas-snapshot-20260602`, arbre propre.
  - **Butin = 1 seul commit `4b0c106`** « wip: snapshot Naomi SELAS local work for reconciliation »,
    posé au-dessus de `origin/codex/naomie-selas-sprint`, **non hissé** (la branche snapshot n'est sur
    aucun remote) → **Cas A** (commits locaux, push oublié).
  - Remote du vieux dossier = OK (`GadrTibi/sydel-document-engine.git`).
  - Pavillon du commit butin : `Naomi Guetta <naomiguetta@macbook-air-de-naomi1.home>` (email machine,
    **pas** l'email du compte GitHub `naomiguetta10-prog`) → signature à régler avant futurs commits.
  - Stash présent : `codex safety stash before naomie sprint switch 2026-06-01` (réserve, à inspecter
    avant transplant si besoin).
  - **Conclusion** : butin **en sécurité** (commité), il manque le `push` propre sur `naomie/selas/<ticket>`.
    **Bloqué au gate** : pas de création de branche / push tant que SELAS non confirmée + NO-GO dev.

- **2026-06-04** — **Récup Codex — exécution (après `GO dev` + SELAS confirmés par le Capitaine)** :
  cale `naomie/selas/recup-codex` créée dans le vieux dossier (pointe sur `4b0c106`, 1 seul commit neuf
  à hisser). Auth : `gh auth login` complété, `gh` connecté en `naomiguetta10-prog` (vérifié via API).
  **Hissage REFUSÉ : 403 — `naomiguetta10-prog` n'a pas l'accès write** sur `GadrTibi/sydel-document-engine`.
  → Bloqué : le Capitaine doit ajouter le Mousse en **collaborateur (write)**. Butin toujours sûr (commité,
  non poussé). Aucun contournement (pas de push sous un autre compte, pas de fork sauvage).

## Pack de passation / Sync packet → Capitaine (2026-06-04)
*Le Mousse ne contacte pas la terre ferme : ce pack attend le Capitaine (via Gad). Rien de « fait » côté
remote — état structuré, pas de push.*

1. **Fait** : embarquement du Mousse + récupération **diagnostiquée** du butin SELAS Codex (lecture seule).
2. **Où** : vieux dossier `~/Desktop/sydel-document-engine`, branche `codex/naomie-selas-snapshot-20260602`,
   **commit butin `4b0c106`** (1 commit en avance sur `origin/codex/naomie-selas-sprint`, non hissé).
   Clone de travail neuf : `~/Desktop/dossier sans titre/Sydel-Naomie` (sur `main`, NO-GO).
3. **Vérifié** : remote OK des deux côtés ; butin commité donc non perdu.
4. **À VALIDER / DÉBLOQUER PAR LE CAPITAINE** :
   - ✅ ① périmètre **SELAS confirmé** par le Capitaine + ② **`GO dev` levé** (feu vert donné le 2026-06-04).
   - ⛔ **③ BLOCAGE ACCÈS (action Capitaine requise)** : `git push` refusé par GitHub —
     `remote: Permission to GadrTibi/sydel-document-engine.git denied to naomiguetta10-prog (403)`.
     Le compte du Mousse `naomiguetta10-prog` **n'a pas l'accès *write*** sur le dépôt. → **Le Capitaine
     (propriétaire `GadrTibi`) doit inscrire `naomiguetta10-prog` comme collaborateur (write)**
     (Settings → Collaborators → Add people). Le Mousse ne peut pas se l'octroyer.
   - ③bis signature : OK pour reconfigurer l'email local sur le compte `naomiguetta10-prog` pour les
     **futurs** commits ? (le commit `4b0c106` existant garde sa signature actuelle, sauf consigne.)
5. **À DÉPLOYER** : rien (le Mousse ne déploie jamais).
6. **Décisions produit en attente** : aucune (SELAS tranché).
7. **Reste à faire (dès l'accès *write* accordé)** : re-`git push -u origin naomie/selas/recup-codex`
   depuis le vieux dossier (cale + butin déjà prêts), vérifier la branche visible sur GitHub, puis
   PR à relire **par le Capitaine**. **Auth déjà OK** (`gh` connecté en `naomiguetta10-prog`).
   → **FAIT le 2026-06-04** : accès *write* accordé, `git push` OK, branche `naomie/selas/recup-codex`
   (commit `4b0c106`) **visible sur GitHub**. Récupérable côté Capitaine.

## Mise au point Capitaine sur les tests (2026-06-04)
Le Capitaine a rejoué la **suite COMPLÈTE** (ruff + pytest) sur `naomie/selas/recup-codex` : **3 échecs /
450 passés**. Le « 118 verts » de l'audit du Second était un **sous-ensemble** (pytest/ruff pas installés
sur le poste de Naomie). **Les 3 échecs ne sont pas du SELAS et pas la faute du Mousse** : le snapshot a
recopié **2 DOCX sources SCI en double** sous variante d'accent Unicode (« Modèle » de deux façons) → le
moteur attend 1 source, en trouve 2, s'arrête (casse 2 tests SCI + 1 cas dentaire). Correctif (suppr. 2
doublons + ranger 2 imports) = **Second côté Gad**, le Mousse ne pousse rien dessus. Bonus : la « refonte »
de `models.py` = en réalité **+4 champs** (le reste = fins de ligne) → intégration future simple.

## Boucle NotebookLM — points juridiques ouverts SELAS (depuis passation Capitaine 2026-06-04)
**Règle** : 1 question à la fois → Naomie colle la **réponse BRUTE** ci-dessous → le Second la structure.
Le Mousse **ne tranche aucune règle**, ne modifie aucun wording, n'invente rien.

File d'attente des questions (courtes, une par une) :
1. ✅ **TRAITÉE** — SELAS : « Présidente » au féminin quand la dirigeante est une femme, ou « Président »
   par défaut ? (préférence par personne ?) → réponse structurée ci-dessous.
2. ✅ **TRAITÉE** — Statuts SELAS : « actionnaire » ou « associé », et dans quels passages chacun ? →
   réponse structurée ci-dessous.
3. ✅ **TRAITÉE** — Plans/devis inscription à l'Ordre : bloquants ? → **OUI, bloquants** (réponse
   structurée ci-dessous).
4. ✅ **TRAITÉE** — Attestation de dépôt de capital / liste des souscripteurs : obligatoire ? → **OUI,
   obligatoire** (source citée : « Besoins Sydel (juridique).pdf ») — réponse structurée ci-dessous.
5. ✅ **TRAITÉE** — Médecin : questionnaire spécifique de l'Ordre ? → **OUI pour le médecin** ; **NON pour
   le dentiste** (réponse structurée ci-dessous).
6. ✅ **TRAITÉE** — Numérotation des actions « 1 à N » pour actionnaire unique : suffit-elle, ou détail
   particulier ? → suffit pour la V1 simple ; précisions hors-V1 notées (réponse structurée ci-dessous).

**✅ BOUCLE NOTEBOOKLM COMPLÈTE (6/6) — 2026-06-05.** Synthèse de fin de boucle + Pack de passation
Capitaine : voir `naomie/worklog/PACK_PASSATION_NOTEBOOKLM_SELAS_2026-06-05.md`.

**NE PAS insister sur NotebookLM** (déjà « non trouvé ») → directs chez **Rafael via le Capitaine** :
filiation dans la DNC · titre exact de la lettre de renonciation du conjoint · nomination du Président
dans les statuts vs acte séparé.

### Réponses brutes NotebookLM (collées par Naomie, structurées ensuite par le Second)

#### Q1 — Genre du titre de direction (Président / Présidente) · 2026-06-04
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** le titre **s'adapte à la
personne** → féminisation requise. Pour une dirigeante femme : **« Présidente »** (et tout terme accordé
au féminin).
- **Règle dégagée** : automatiser le passage au féminin (ex. `Président` → `Présidente`), au lieu des
  corrections manuelles que les anciens outils imposaient (« ne féminisent pas les documents »).
- **Variable nécessaire (confirmée)** : le **sexe / genre du praticien** est une **donnée obligatoire** à
  collecter pour piloter l'accord dans statuts et actes.
- **Cas à couvrir** : « monsieur » / « madame », et plusieurs dirigeantes (« deux nanas ») → accords au
  féminin/pluriel à gérer.
- **Limite de sourcing** : NotebookLM parle « des sources / documents » **sans citation exploitable
  précise** (cohérent avec l'audit : pas de passage source extrait). La règle générale (féminiser) est
  claire ; la **liste exhaustive des termes à accorder** et le **wording exact** restent à confirmer
  (sources DOCX + arbitrage humain).
- **Impact code** : conforte le champ genre obligatoire dans le schéma front SELAS et le principe d'une
  table d'accords. ⚠️ Ne PAS coder par substitution globale de chaînes (risque déjà identifié) ; pas de
  règle d'accord tranchée par le Mousse — c'est de la matière, pas une décision.

**Réponse brute (verbatim, collée par Naomie) :**
> D'après les sources, la forme du titre de direction pour une SELAS **doit s'adapter à la personne**.
> Voici les règles précisées dans les documents :
> - **Personnalisation systématique :** besoin de **« personnaliser le “ée” en féminin »** pour les
>   différents termes juridiques du dossier.
> - **Adaptation au genre :** si la dirigeante est une femme, le document doit être **féminisé**. Le
>   système doit traiter le cas d'un « monsieur » ou d'une « madame » (ou « deux nanas ») pour accorder
>   correctement le texte.
> - **Correction des anciens modèles :** les anciens outils **« ne féminisent pas les documents »**, d'où
>   corrections manuelles des juristes. Le futur moteur doit automatiser le féminin, ex. « Président » →
>   **« Présidente »**.
> - **Variables de genre :** le sexe du praticien est une donnée obligatoire pour piloter
>   l'**automatisation de la féminisation** dans les statuts et les actes.
> En résumé, pour une femme on écrit bien **« Présidente »** (ou tout terme accordé au féminin), l'un des
> objectifs majeurs étant de supprimer les « coquilles » liées au genre.

#### Q2 — « actionnaire » vs « associé » dans les statuts SELAS · 2026-06-04
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** distinction nette entre le
**générique « associé »** (les personnes / membres) et le **technique « action(naire) »** (le capital).
- **« Associé »** (personnes / qualité de membre) : fiches de saisie (« INFORMATIONS SUR L'ASSOCIÉ
  UNIQUE », « identité des associés »), articles statutaires, typologie **associé exerçant** (praticien) /
  **associé non-exerçant** (conjoint, enfants, personne morale), décisions collectives (« pactes
  d'associés », pluriel « les associés ont décidé »).
- **« Action(naire) »** (capital / titres) : titre techniquement exact des membres ; surtout, **remplacer
  impérativement « parts sociales » → « actions »** dans tous les passages financiers/capital (« action » =
  le mot qui revient le plus au passage SELARL→SELAS).
- **Cartographie par passage proposée** (⚠️ numéros d'articles NotebookLM **non vérifiés** sur les vrais
  DOCX) :
  | Passage | Terme |
  |---|---|
  | Préambule / Comparution | Associé (générique) |
  | Art. apports | Apporteur / Associé |
  | Art. capital social | divisé en **actions** (remplace « parts ») |
  | Répartition du capital | entre **associés**, avec un **nombre d'actions** |
  | Gouvernance | **Président** (remplace gérant) + **Associé** pour les décisions |
- **Règle dégagée** : garder **« associé »** pour désigner les individus ; substituer **« parts sociales »
  → « actions »** dans les passages capital/résolutions financières.
- **Limite de sourcing** : aucune citation source exploitable (réfs = le log NotebookLM lui-même, ex.
  « Comparaison SELARL/SELAS du 01/06 » ; verbatim peu rigoureux « quand on est sur une selle c'est des
  associés »). La **cartographie par article doit être confirmée sur les statuts DOCX réels** + arbitrage
  humain (rejoint la question ouverte « associé vs actionnaire dans l'UI » du pack de revue).

**Réponse brute (verbatim, collée par Naomie) :**
> D'après les sources, le choix « actionnaire »/« associé » en SELAS oppose la **terminologie technique**
> (titres) à l'usage **générique** (personnes).
> **1. « Associé » (générique/statutaire)** — présent partout car il définit la qualité des membres d'une
> SEL quel que soit le support du capital : fiches « INFORMATIONS SUR L'ASSOCIÉ UNIQUE » / « identité des
> associés » ; articles des statuts (« quand on est sur une selle c'est des associés ») ; typologie
> « associé exerçant » (praticien) / « associé non-exerçant » (conjoint, enfants, personne morale) ;
> décisions collectives (« pactes d'associés », pluriel « plusieurs associés »).
> **2. « Actionnaire » (technique/spécifique)** — titre exact des membres d'une SELAS, mais moins fréquent
> dans les échanges métier : la structure repose techniquement sur des actionnaires (cohérence à veiller) ;
> le passage SELARL→SELAS impose « actions » au lieu de « parts sociales » (« le mot qui revient le plus »).
> **Synthèse wording statuts** : Préambule/Comparution → Associé ; Art. 7 Apports → Apporteur/Associé ;
> Art. 8 Capital → divisé en « actions » (remplace « parts ») ; Répartition capital → entre « associés »
> mais avec un nombre d'actions ; Gouvernance → Président (remplace gérant) + Associé pour les décisions.
> **Règle** : maintenir « associé » pour les individus, mais substituer impérativement « parts sociales »
> par « actions » dans tous les passages financiers et résolutions liées au capital.

#### Q3 — Plans/devis pour l'inscription à l'Ordre : bloquants ? · 2026-06-05
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** **OUI — pièces BLOQUANTES**
pour le dossier d'inscription d'une SEL (médecin) au Conseil de l'Ordre.
- **Pourquoi** : l'Ordre exige plans des locaux + devis (matériel/travaux) pour vérifier que la société
  peut réellement exercer conformément à son objet social.
- **Risque si manquant** : les commissions ordinales siègent ~1×/mois ; sans plans/devis, la commission
  peut **refuser l'attestation** nécessaire à l'immatriculation au Greffe → décalage **d'un mois ou plus**.
- **Conséquence moteur** : ces pièces doivent être **obligatoires et bloquantes** dans l'avancement du
  dossier — le système doit les **exiger avant** de valider l'envoi à l'Ordre.
- **Effet sur l'audit** : **tranche l'un des 2 points “forts”** (plans/devis Ordre). Reste le 2ᵉ point fort
  (attestation de dépôt de capital, Q4). ⚠️ Réponse claire mais toujours **sans citation source précise** →
  à confirmer en revue humaine avant d'en faire une règle dure du moteur.

**Réponse brute (verbatim, collée par Naomie) :**
> Pour l'inscription d'une **SELAS de médecin** (ou toute autre SEL) auprès du Conseil de l'Ordre, les
> plans des locaux et les devis de matériel/travaux sont des **pièces bloquantes** pour le succès du
> dossier.
> - **Justification de l'objet social** : l'Ordre exige ces éléments pour vérifier que la société peut
>   réellement pratiquer son activité conformément à son objet social.
> - **Risque de retard important** : les commissions de l'Ordre se réunissent ~1×/mois ; si les plans/devis
>   manquent, la commission peut refuser de délivrer l'attestation nécessaire à l'immatriculation au
>   Greffe → décalage d'un mois entier, voire plus.
> - **Conséquence pour le moteur** : documents identifiés comme **obligatoires et bloquants** dans
>   l'avancement du dossier, pour éviter un échec devant la commission ordinale.
> Il est donc recommandé que le système demande et impose le dépôt de ces pièces (plans et devis) avant de
> valider l'envoi du dossier à l'Ordre.

#### Q4 — Attestation de dépôt de capital / liste des souscripteurs : obligatoire ? · 2026-06-05
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** **OUI — obligatoire** pour une
création de SELAS médecin. **Première réponse avec une source nommée** (interne projet, pas texte légal).
- **Source citée** : **« Besoins Sydel (juridique).pdf »**, diagramme « Page fiche création » → l'« attestat
  sur le k » (attestation sur le capital) est classé en **« documents à éditer obligatoires »**.
- **Définition** : le dépôt de capital = « versement obligatoire par le futur associé » à la constitution.
- **Liste des souscripteurs** : la **« répartition entre les associés »** et le **« nombre d'actions »**
  sont des variables critiques obligatoires de la fiche société → base de la liste des souscripteurs (en
  SELAS : **actions**, pas parts).
- **Effet sur l'audit** : **tranche le 2ᵉ point “fort”** → les **2 points forts sont désormais levés**
  (plans/devis = bloquants ; attestation capital = obligatoire). Tous deux à **ajouter aux pièces exigées**
  du pack V1.
- **Limite de sourcing** : la source est un **doc de besoins interne** (« Besoins Sydel (juridique).pdf »),
  pas une référence réglementaire opposable → suffisant pour exiger la pièce dans le moteur, à confirmer en
  revue humaine pour le fondement juridique.

**Réponse brute (verbatim, collée par Naomie) :**
> Pour une création de SELAS de médecin, **l'attestation de dépôt de capital est une pièce obligatoire**.
> - **Caractère obligatoire** : dans **« Besoins Sydel (juridique).pdf »**, diagramme de la « Page fiche
>   création », l'**« attestat sur le k »** (attestation sur le capital) est classé sous **« documents à
>   éditer obligatoires »**.
> - **Définition** : le dépôt de capital social = **« versement obligatoire par le futur associé »** d'une
>   somme lors de la constitution.
> - **Validation experts** : les transcriptions confirment que l'« attestation sur le capital » fait
>   partie du lot de documents nécessaires à la création.
> - **Liste des souscripteurs** : la **« répartition entre les associés »** et le **« nombre de parts ou
>   d'actions »** sont des variables critiques et obligatoires de la fiche société ; en SELAS (société par
>   actions), cette répartition constitue la base de la liste des souscripteurs.
> Pour une SELAS, le système doit adapter le vocabulaire pour parler d'**actions** et non de parts sociales
> dans ces documents financiers.

#### Q5 — Médecin : questionnaire spécifique de l'Ordre ? · 2026-06-05
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** **OUI** — pour un **médecin**
créant une SELAS, joindre un **questionnaire spécifique** au dossier Ordre. **Correction utile** : ce
questionnaire est requis pour le **médecin** mais **PAS pour le dentiste** (l'inverse de l'hypothèse posée
dans la question).
- **Nature** : pièce « en plus » qui s'ajoute aux documents transverses (procuration, demande d'inscription
  standard) **selon la profession**.
- **Autres professions concernées** : questionnaires similaires pour **vétérinaires, kinésithérapeutes,
  sages-femmes, infirmiers**.
- **Impact moteur** : prévoir une pièce conditionnelle **« questionnaire Ordre »** pilotée par la
  **profession** (présente pour médecin, absente pour dentiste). Affine la cartographie des pièces par
  métier.
- **Limite de sourcing** : appui = verbatim de transcription (« si c'est un médecin, il faut que je rajoute
  un questionnaire parce que j'ai pas besoin pour un dentiste »), pas de référence Ordre formelle → à
  confirmer (modèle exact du questionnaire) en revue humaine.

**Réponse brute (verbatim, collée par Naomie) :**
> Oui, pour un **médecin** qui crée une SELAS, il faut joindre un **questionnaire spécifique** au dossier
> destiné au Conseil de l'Ordre. Ce document fait partie des pièces « en plus » qui s'ajoutent aux
> documents transverses (procuration, demande d'inscription standard) selon la profession.
> Différence notable avec les dentistes : il faut ajouter ce questionnaire pour un médecin car il n'est
> **pas requis pour un dentiste**. Des questionnaires similaires existent pour d'autres professions
> réglementées : **vétérinaires, kinésithérapeutes, sages-femmes, infirmiers**.
> Passage exact : « Après tu vois, c'est juste que si c'est un médecin, il faut que je rajoute un
> questionnaire parce que j'ai pas besoin pour un dentiste. »

#### Q6 — Numérotation des actions (actionnaire unique) · 2026-06-05
**Synthèse (matière exploratoire NotebookLM — à valider, non opposable) :** pour la **V1 (actionnaire
unique, médecin, actions ordinaires)**, une suite **« 1 à N »** suffit ; les complications relevées sont
**hors périmètre V1** (et déjà bloquées côté code par les garde-fous de l'audit).
- **Numérotation précise** : usage du cabinet = numérotations « assez précises » (ex. « actions 1 à 10
  inclus » rattachées à un % de droits).
- **Dissociation des droits** (hors V1) : distinguer **droits de vote** vs **droits financiers**
  (1 % d'actions ≠ 1 % du résultat dans les montages dérogatoires).
- **Actions de préférence** (hors V1) : montages enfants/conjoint via micro-holding → catégories d'actions
  dissociant capital / pouvoir / bénéfices. *(Déjà bloqué en V1 : actions de préférence, multi-actionnaires,
  démembrement = garde-fous existants.)*
- **Wording** : Art. capital social → capital « divisé en un nombre précis d'**actions** ».
- **Non trouvé** : aucune règle de **numérotation spéciale** (code alphanumérique) au-delà de la suite
  numérique liée aux droits.

**5 questions de suite proposées par NotebookLM (NON posées — gérées par le Capitaine, cf. règle « non
trouvé → Rafael ») :** ① démembrement nu-propriété/usufruit dès la V1 ? · ② seuils de blocage/majorité par
défaut [non trouvé] · ③ clause d'agrément des héritiers par défaut [non trouvé] · ④ mention si capital
libéré partiellement (1/2, 1/4) [non trouvé] · ⑤ apports en industrie ou numéraire seul en V1 [non trouvé].
→ Toutes **hors V1** ou **non sourcées** : à arbitrer en revue humaine, **ne pas relancer NotebookLM**.

**Réponse brute (verbatim, collée par Naomie) :**
> La numérotation des actions en SELAS peut exiger une précision au-delà d'une simple suite « 1 à N ».
> - **Précision** : numérotations souvent « assez précises » dans les modèles du cabinet (ex. « parts 1 à
>   10 inclus » = un certain % de droits).
> - **Distinction des droits** : séparer droits de vote et droits financiers (dividendes) ; 1 % d'actions
>   peut ne pas donner 1 % du résultat (cas dérogatoire).
> - **Catégories (actions de préférence)** : prévues pour des montages enfants/conjoint via micro-holding,
>   dissociant capital / pouvoir / bénéfices (au-delà de l'actionnaire unique V1).
> - **Wording** : « actions » = mot le plus récurrent à adapter SELARL→SELAS ; Art. 8 (Capital) divisé en
>   un nombre précis d'actions.
> - **Non trouvé** : pas de règle de numérotation spéciale (code alphanumérique) hors suite numérique liée
>   aux droits.
> **5 questions importantes à poser ensuite** : ① démembrement nu-propriété/usufruit dès la V1 ? ② seuils
> de blocage (majorité) par défaut [non trouvé] ; ③ clause d'agrément des héritiers par défaut [non
> trouvé] ; ④ mention de libération partielle du capital (1/2, 1/4) [non trouvé] ; ⑤ apports en industrie
> ou numéraire seul en V1 [non trouvé].
