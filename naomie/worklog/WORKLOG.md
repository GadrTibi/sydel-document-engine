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

---

## REPRISE 2026-06-05 — Direction MULTI-ASSOCIÉS (2 à 5) · note Capitaine 9ac5853
**Nouvelle cible** : statuts SELAS **multi-associés (2 à 5)** ; unipersonnel **rangé** (pas en code). Socle
(DNC, domiciliation, procuration, Ordre, schéma front) **réutilisable** ; ce sont **les statuts** qui passent
multi. **NO-GO génération** maintenu. Réf : `docs/sprints/SPRINT_SELAS_REPRISE_MULTI_ASSOCIES_001.md`.

**Règle de flux (nouvelle)** : Mousse cadre les questions → **NotebookLM d'abord** → si insuffisant, Mousse
**formule la question pour Rafael** → **Capitaine** (seul à transmettre) → Rafael → Capitaine → Mousse.

### Blocage matière : `.docx` Reynaud absent (2026-06-05)
Le cas réel `Statuts SELAS DU DR ISABELLE REYNAUD.docx` (à tokeniser) **n'est PAS sur le disque** de Naomie
(recherche exhaustive : aucun fichier « reynaud », plus récent `.docx` = 2026-06-02). → **À fournir par le
Capitaine** (données réelles patiente — ne jamais versionner le doc réel, seulement le modèle tokenisé).
Cartographie des variables **en attente du fichier**. Entre-temps : boucle NotebookLM Q-B/Q-C/Q-D.

### Boucle NotebookLM multi-associés
#### Q-B — Directeur Général aux côtés du Président ? · 2026-06-05
**Résultat : « non trouvé » côté NotebookLM → escalade Rafael (via Capitaine), ne pas insister.**
- DG **non défini / non détaillé** dans les modèles & transcriptions ; sources centrées sur le **Président**
  (terme obligatoire en SELAS, remplace « Gérant »).
- **Obligatoire : non** ; **fréquence : non trouvée**. Le périmètre privilégié visait un **Président unique**.
- Nomination d'un dirigeant : **dans les statuts** ou par **PV de nomination** ; infos mini = nom, prénom,
  téléphone ; **pouvoirs = clause « ultra personnalisée »** (pas de règle type pour un DG).
- **Question formulée pour RAFAEL (via Capitaine)** : *« Pour des statuts SELAS multi-associés (2–5)
  médecins, faut-il gérer les Directeurs Généraux (le cas réel Reynaud en prévoit, art. 15), ou les laisser
  hors de ce premier jet ? Si on les gère : règles types de nomination et de pouvoirs ? »* (+ sous-points
  NotebookLM « non trouvés » : DG par un associé non-exerçant/personne morale ? signatures actes Ordre par
  les deux dirigeants ? lien DG ↔ actions de préférence ?)

**Réponse brute Q-B (verbatim, collée par Naomie) :**
> Le terme de Directeur Général n'est pas défini ni détaillé dans les modèles/transcriptions ; les sources
> se concentrent sur le **Président** (terme obligatoire en SELAS, remplaçant « Gérant »). Caractère
> obligatoire : **non trouvé** (le périmètre V1 privilégiait un **Président unique**). Fréquence : **non
> trouvé**. Nomination d'un dirigeant : dans les **statuts** ou par **PV de nomination** ; infos mini = nom,
> prénom, téléphone ; pouvoirs = clause **« ultra personnalisée »**. En résumé, rôle de DG **non trouvé**
> dans les modèles types ; le système identifie d'abord « qui sont les dirigeants » et gère la substitution
> « Gérant » → « Président ». [5 questions de suite proposées, majoritairement « non trouvé ».]

#### Q-C — Un associé peut-il être une personne morale ? · 2026-06-05
**Résultat : OUI — possible et courant (réponse riche). Décision de périmètre du 1ᵉʳ jet = Capitaine.**
- **Personne morale associée = possible/courant** (ex. détention 25 % par une entité tierce).
- **Holdings** : **SPFPL** (Société de Participations Financières de Professions Libérales) = holding
  **spécifique/obligatoire** pour détenir les titres d'une SEL santé ; **micro-holding (société civile)** =
  véhicule pour intégrer la famille (conjoint, enfants). Schéma : SCI (immobilier) ↔ micro-holding ↔ SPFPL.
- **Catégories d'associés** : **exerçant** (le praticien qui exerce ici) vs **non-exerçant** (médecin
  n'exerçant pas ici, personnes physiques tierces conjoint/enfants, **personnes morales** SPFPL/micro-holding).
- **⚠️ RÈGLE DURE (garde-fou candidat, à valider Rafael)** : la répartition du capital **ne peut jamais
  retirer la MAJORITÉ DES DROITS DE VOTE aux associés EXERÇANTS**.
- **Dissociation droits** : actions de préférence possibles pour non-exerçants → **1 % d'actions ≠ 1 % du
  résultat** ; le moteur doit distinguer **droits de vote** et **droits financiers** dans la répartition.
- **Contrôle ordinal** : l'Ordre contrôle ces montages, exige souvent de **consulter les projets d'actes
  avant signature**.
- **Impact moteur (si personne morale autorisée au 1ᵉʳ jet)** : collecter raison sociale, type de holding
  (SPFPL / société civile), représentant, qualité exerçant/non-exerçant ; + garde-fou majorité exerçants.
- **À ESCALADER (décision périmètre, Capitaine)** : accepte-t-on les **associés personnes morales dès le
  premier jet multi**, ou on se limite aux **médecins personnes physiques** (le reste réutilisant le socle) ?
- **Limite de sourcing** : plus fournie que d'habitude, mais toujours **sans citation précise** → la **règle
  dure (majorité exerçants)** et le périmètre **à confirmer Rafael** avant d'en faire des règles du moteur.

**Réponse brute Q-C (verbatim, collée par Naomie) :**
> Il est possible et courant qu'une **personne morale** soit associée d'une SELAS de médecins (cœur des
> stratégies de restructuration patrimoniale du cabinet).
> **1. Détention par personne morale** : possible (ex. 25 % par une entité tierce) ; **SPFPL** = holding
> spécifique **obligatoire** pour détenir les parts/actions d'une SEL ; **micro-holding (société civile)**
> pour intégrer la famille ; schéma SCI ↔ micro-holding ↔ SPFPL.
> **2. Exerçant / non-exerçant** : exerçant = le praticien ; non-exerçant = médecin n'exerçant pas ici,
> personnes physiques tierces (conjoint, enfants), **personnes morales** (SPFPL, micro-holding).
> **3. Encadrement du capital** : la répartition ne peut jamais retirer la **majorité des droits de vote aux
> associés exerçants** ; **actions de préférence** possibles pour non-exerçants (décorréler capital / droits
> financiers / vote) ; **1 % des actions ≠ 1 % du résultat** ; l'Ordre contrôle strictement et consulte
> souvent les projets d'actes avant signature.
> En résumé, la SELAS peut être rattachée à des personnes morales (SPFPL, micro-holding) pour optimiser la
> circulation des revenus.

#### Q-D — Modèle de référence unique, ou plusieurs ? · 2026-06-05
**Résultat : PAS de modèle unique. Trame de base par profession, déclinée à la main ; multi = « ultra
personnalisé ». → 1 cas (Reynaud) ne suffit pas : signalement Capitaine (autres modèles via Rafael).**
- **Hiérarchie** : socle = **modèle par profession** (médecin ≠ dentiste : contraintes ordinales
  différentes) → **trame de base** déclinée/adaptée manuellement par dossier.
- **Nombre** : ~**60 % des dossiers = unipersonnel** (le plus simple) ; le multi (2–5) est jugé
  **« impossible »** à couvrir par multiplication de modèles fixes (trop de combinaisons).
- **Changements unipersonnel → multi** : (a) **décisions collectives** (quorum/majorité) au lieu de la
  décision d'associé unique ; (b) **clauses d'agrément** indispensables et complexes ; (c) **Art. 8 Capital**
  réécrit : **numérotation précise des actions par associé** (ex. « actions n°1 à 100 ») ; (d)
  **pluralisation** de tout l'acte (« les associés », « les soussignés »).
- **Genre** : **Président → Présidente** ; accords **Soussigné(e) / Associé(e) / Né(e)** ; cas des duos
  (deux messieurs / deux dames / couple mixte). *(Conforte Q1.)*
- **Verdict métier** : moteur = automatiser la **base** (noms, parts, genre, pluriel, agrément, décisions
  collectives) ; les juristes gardent une **« souplesse »** de finition manuelle sur brouillon Word.
- **À ESCALADER (Capitaine → Rafael)** : le doc Reynaud est **un exemple**, pas LE référent ; il **manque
  des modèles** couvrant 2/3/4/5 associés et les genres → demander d'autres modèles tokenisables.

**Réponse brute Q-D (verbatim, collée par Naomie) :**
> Pas de modèle statique unique. Hiérarchie : **un modèle par profession** (médecin/dentiste, contraintes
> ordinales différentes) ; une **trame de base** déclinée/adaptée manuellement. ~**60 % des dossiers sont
> unipersonnels** (le plus simple) ; les cas 2–5 associés sont jugés **« impossibles »** à couvrir par
> multiplication de modèles fixes.
> **Changements 2–5 associés** : décisions **collectives** (quorum/majorité) ; **clauses d'agrément**
> indispensables/complexes ; **Art. 8** réécrit avec **numérotation précise des actions** par associé
> (ex. « actions n°1 à 100 ») ; **pluralisation** (« les associés », « les soussignés »).
> **Genre** : « Président » → « Présidente » ; accords « Soussigné(e) », « Associé(e) », « Né(e) » ; duos
> (deux messieurs / deux dames / couple mixte).
> **Verdict** : multi = rédaction **« ultra personnalisée »** ; le moteur automatise la base (noms, parts,
> genre) mais les juristes gardent une **souplesse** de correction manuelle sur brouillon Word.

---

### 🏁 Fin de trio cadrage multi-associés (Q-B/C/D) — 2026-06-05
- **Q-B (Directeurs Généraux)** : NotebookLM « non trouvé » → **question Rafael**.
- **Q-C (associé personne morale)** : **OUI possible/courant** (SPFPL, micro-holding) + **règle dure**
  (majorité droits de vote aux exerçants) ; **décision de périmètre du 1ᵉʳ jet = Capitaine**.
- **Q-D (modèles)** : pas de référent unique ; **manque de modèles** multi → **signalement Capitaine**.
- **Blocage matière** : `.docx` Reynaud **absent** du disque → **à fournir par le Capitaine**.
- **Bundle pour Rafael / Capitaine** : `naomie/worklog/PACK_PASSATION_MULTI_ASSOCIES_2026-06-05.md`.
- **NO-GO génération** maintenu. Aucune ligne de code écrite (cadrage uniquement).

### Raffinement NotebookLM Q-B/C/D (2ᵉ passe, 2026-06-05) — relancé par Naomie
**Q-B (DG)** : NotebookLM **recommande d'écarter les DG du 1ᵉʳ jet** (priorité simplicité, 60 % unipersonnel,
focus « Gérant »→« Président », DG = « ultra personnalisé »). Si intégrés : nomination statuts **ou** PV ;
données mini nom/prénom/tél ; pouvoirs = rédaction manuelle. **Toujours [non trouvé]** : terme « DG » jamais
explicite, répartition pouvoirs Président/DG, fréquence. → ⚠️ **NotebookLM *recommande*, ne *décide* pas** ;
or le **cas réel Reynaud A des DG (art. 15)** → **contradiction à trancher par le Capitaine/Rafael**, Q-B
**reste ouverte**.

**Q-C (personne morale)** : confirmé **fréquent/central** (SPFPL holding obligatoire + micro-holding société
civile ; ex. 25 % ; fiche « Société » avec champs sociétés reliées/filiales ; minoritaires conjoint/enfants
en actions de préférence). 🎯 **PÉPITE — clause exacte de la règle dure (Art. 8), verbatim source cabinet** :
> « En aucun cas la répartition du capital ne pourra être modifiée dans des conditions qui retireraient la
> majorité des droits de vote aux associés exerçant dans la société. »
→ Exploitable comme **clause fixe** du moteur (sous validation Rafael). Reste une **décision de périmètre**
(accepter personne morale dès le 1ᵉʳ jet ?) = Capitaine.

**Q-D (modèles)** : reconfirme **aucun modèle multi prêt à l'emploi** dans les sources ; règles de
transformation (LES SOUSSIGNÉS, Art. 8 numéroté, quorum/majorité, accords genre + **Apporteur(se)**, duos).
**Point actionnable** : il faudra faire **valider par un expert** une **formule de sommation des apports** +
un **tableau de répartition dynamique à N lignes** — **inexistants dans les sources**. → confirme que le
**wording multi déterministe ne viendra PAS de NotebookLM** (plafond atteint) mais des **vrais modèles +
validation humaine**.

**Verdict du Second (satisfaisant ?)** : **bonne matière, plafond NotebookLM atteint** — on a tout extrait,
Q-C donne même la clause exacte. **MAIS pas “suffisant pour coder”** : (1) Q-B/Q-C portent des **décisions de
périmètre** que NotebookLM ne tranche pas (et Q-B **contredit** le cas réel) → **Rafael/Capitaine** ; (2) Q-D
**confirme** que le wording multi n'existe pas dans les sources → **vrais modèles + validation humaine**
requis. **Ne pas relancer NotebookLM** sur ces points.
