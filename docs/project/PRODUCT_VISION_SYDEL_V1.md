# Vision produit Sydel — V1

> **Statut : BROUILLON pour relecture/correction par Gad (le boss).** Document durable, versionné.
> Auteur : product-manager (Claude). Date : 2026-06-04.
> Ce document **n'invente aucune règle juridique**. Il restitue l'intention produit telle que lisible
> dans le canon (`Documents_a_generer_par_cas_V3.docx`), les specs `docs/delivery/`, le réponse
> d'Albane, et l'état de complétion SELARL. Tout point non sourcé est classé HYPOTHÈSE ou QUESTION.
> Sources de vérité réelles (priment sur ce document) : le canon `.docx`, les modèles tokenisés
> `project/source_documents/`, les specs canoniques `docs/delivery/`, le NotebookLM de l'équipe.

---

## 1. Mission — en langage métier

**À quoi sert Sydel.** Sydel est une **usine à dossiers documentaires juridiques**. À partir des
informations d'un client (un praticien libéral et sa situation), elle produit automatiquement
l'ensemble des actes Word nécessaires à la **création ou la réorganisation de sa structure
d'exercice** : statuts, PV, procurations, déclarations, actes de cession, baux, courriers, etc. La
sortie est un paquet de fichiers `.docx` éditables, convertis en PDF et regroupés en un ZIP de
dossier.

**Pour qui.** Le cabinet (DAAT / l'associé qui pilote le métier) qui monte des dossiers de
structuration pour des **médecins et chirurgiens-dentistes** en France. Le client final est le
praticien ; l'utilisateur de l'outil est l'opérateur du cabinet.

**Quel problème client.** Aujourd'hui, ces dossiers sont assemblés à la main à partir de modèles
Word, en recopiant les mêmes informations (nom, adresse, capital, dates) dans des dizaines de
documents, avec un risque d'erreur, d'incohérence et un coût en temps important. Chaque cas
(médecin/dentiste, régime matrimonial, cession, SCM…) déclenche une combinaison différente de
documents.

**Promesse de valeur.** Saisir une seule fois les données d'un dossier, **sélectionner
automatiquement les bons documents selon le cas**, et générer un pack **fidèle au wording juridique
de référence**, **déterministe** (aucune IA générative dans la production : le texte vient des
modèles tokenisés, jamais d'une rédaction inventée), et reproductible. Gain : vitesse, cohérence des
données entre documents, fidélité juridique garantie par la source.

**Garde-fou central (identité produit).** Sydel **ne rédige jamais** de droit : elle **remplit** des
modèles validés. Toute formulation juridique provient du corpus source ou de la chaîne humaine
(associé → Albane). C'est la condition de confiance du produit.

---

## 2. Périmètre produit — matrice structures × familles de documents

Sydel vise, à terme, plusieurs **types de structures** d'exercice libéral et leurs satellites
(holding, société de moyens, immobilier) et plusieurs **familles de documents**. Le canon V3 ne
détaille explicitement que la branche **SELARL** ; les autres structures existent dans le moteur
(générateurs présents) et dans les modèles sources, mais leur cadrage produit est moins mûr.

### 2.1 Structures (lignes)

| Structure | Nature | État produit (juin 2026) |
|---|---|---|
| **SELARL** | Société d'exercice libéral à resp. limitée — pilote | Cas simples + régime communautaire = candidat technique avancé, en attente validation associé ; cessions/SCM câblées sur branche de revue ; multi-associés complet bloqué Albane |
| **SELAS** | Société d'exercice libéral par actions simplifiée | Modèles présents ; pilotée en parallèle (filière Naomi) ; **seule forme où une personne morale associée est possible** (voir §4) |
| **SPFPL / SPFPLAS** | Société de participations financières (holding de SEL) | Modèles + générateurs présents (statuts, apport, cession parts/actions) ; cadrage produit partiel |
| **SAS (holding)** | Holding sous forme SAS | Modèles + générateurs présents ; satellites |
| **SCM** | Société civile de moyens (partage de frais) | Statuts, règlement intérieur, pacte, cession de parts, liste de dépenses ; intervient comme satellite d'une SEL |
| **SCI** | Société civile immobilière | Modèles statuts présents ; cadrage produit non détaillé |
| **« Micro-holding » (société civile)** | Société civile servant d'associé personne morale en SELAS médecin | Mentionnée par Albane, **modèle fourni récemment** (`modele Statuts SELAS avec MH.docx`) ; non encore cadrée produit |

### 2.2 Familles de documents (colonnes)

- **Documents communs** (tous cas) : déclaration de non-condamnation, autorisation de
  domiciliation, procuration.
- **Création de structure** : statuts (par profession + forme), PV de nomination du gérant,
  demande d'inscription à l'ordre.
- **Régime matrimonial** : lettre de renonciation du conjoint, lettre d'avertissement au conjoint
  (si régime communautaire).
- **Cession de cabinet** (médical / dentaire) : acte de cession, compromis de cession, avenant au
  bail, appel de fonds.
- **SCM / cession de parts SCM** : PV d'AGE de cession de parts, courrier SDE (droits
  d'enregistrement), acte de cession des parts de la SCM à la SEL ; + satellites SCM (règlement
  intérieur, pacte, liste de dépenses) hors flux SELARL pilote.
- **Holding / SPFPL** : statuts SPFPL, contrat d'apport SEL→SPFPL, attestation sur le capital,
  acte de cession de parts/actions SPFPL, lettre option IS — **hors périmètre SELARL pilote**.
- **Dérogations** : exercice multi-sites avec la SEL, dérogation cumul SELARL BNC — **à remplir à
  la main** (manuel), pas de génération automatique.

### 2.3 Dans le périmètre vs hors périmètre (pour le pilote SELARL)

**Dans le périmètre SELARL (codé / codable) :**
- Documents communs (DOC-001/002/003).
- Création SELARL unipersonnelle médecin (DOC-017) ou dentiste (DOC-016) + PV gérant (DOC-004) +
  inscription à l'ordre (DOC-034).
- Régime communautaire (DOC-005 renonciation + DOC-006 avertissement).
- Cession de cabinet médical/dentaire (DOC-009/010/011/012) + avenant bail (DOC-007) + appel de
  fonds (DOC-008) — générateurs prêts, câblage front sur la branche de revue.
- Cession de parts SCM vers la SEL (DOC-031/032/033) — idem.

**Hors périmètre (manuel ou non couvert en V1) :**
- Dérogations et formulaire site distinct → **manuels** (à remplir à la main), affichés comme tels.

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. Les puces multi-associés et
> associé personne morale **SELARL** ci-dessous sont conservées pour mémoire mais ne sont plus un
> objectif produit. (La SELAS multi-actionnaire et la micro-holding en SELAS restent valables.)

- **Statuts SELARL multi-associés complets** (préambule/comparution/signatures pluriels, co-gérance,
  quorum/majorité non unanime, président de séance externe, associé absent) → **bloqués** en attente
  du wording ligne-par-ligne d'Albane (cf. `docs/delivery/selarl_multi_associes_questions_albane_v1.md`).
- Médecin multi-associés.
- SPFPL / SAS holding / SCI / satellites SCM → hors flux SELARL pilote (générateurs existent mais
  cadrage produit séparé).
- **Associé personne morale en SELARL** → voir dérive §4 (probablement HORS périmètre).

---

## 3. Classement de la connaissance : CONFIRMÉ / PROBABLE / HYPOTHÈSE / QUESTION OUVERTE

### CONFIRMÉ (sourcé canon / specs / Albane / état vérifié)
- C1. Sortie attendue = pack de `.docx` → PDF → ZIP, **déterministe**, sans IA générative en
  production. (mémoire projet + workflow produit)
- C2. La **sélection des documents dépend du cas** : tronc commun + branches conditionnelles
  (profession, régime, cession, SCM, dérogation). (canon V3)
- C3. SELARL **simple** (médecin/dentiste, unipersonnel) + **régime communautaire** = générés et
  vérifiés ; statut « candidat technique avancé » en attente de validation associé. (SELARL canonical status)
- C4. Acte et compromis de cession sont **4 documents distincts** (médical/dentaire ×
  acte/compromis), sélectionnés par une **étape explicite** ; ne jamais les fusionner ni produire
  l'un pour l'autre sans demande explicite. (arbitrage cession 4.1/4.2)
- C5. Le **crédit-vendeur** est un bloc conditionnel de l'**acte médical uniquement**, désactivé par
  défaut ; jamais en dentaire en V1. (arbitrage cession 4.5)
- C6. L'**adresse de domiciliation est toujours celle du siège social** ; le siège est en général
  identique au lieu d'exercice (cas par défaut, avec option d'une 3e adresse manuelle). (Albane)
- C7. Dans une cession de cabinet/SCM rattachée à une SEL en création : le **vendeur/cédant est
  toujours le praticien personne physique en BNC**, l'**acquéreur/cessionnaire est toujours la
  SEL en création**. (Albane)
- C8. Les **dérogations** (site distinct, cumul SELARL BNC) sont **à remplir à la main** : hors
  génération automatique. (canon V3 « à remplir à la main »)
- C9. Le **multi-associés complet** (statuts pluriels) n'est **pas livrable** sans wording fourni
  par Albane ; les hypothèses actuelles du PARTIAL sont « gérant unique + unanimité ». (questions Albane)

### PROBABLE (dérivé d'un modèle frère ou d'un usage, non verrouillé verbatim)
- P1. Le **menu de production en prod** expose une liste déroulante des structures validées ; une
  structure non finie reste gated/cachée. (mémoire projet — convention de déploiement)
- P2. La cession SCM peut être **bundlée** avec la création ou **autonome** ; la composition exacte
  du dossier reste à arbitrer côté UI. (plan de complétion, « reste UI »)
- P3. Le **canal de revue humaine** = preview Streamlit déployée depuis une branche `review/<structure>`
  (le ZIP/`generate_pack` devient outil interne de QA, pas le canal humain). (mémoire projet)

### HYPOTHÈSE (mon interprétation, à confirmer)
- H1. Les structures autres que SELARL (SELAS, SPFPL, SCM, SCI…) suivront la **même méthode**
  d'usine documentaire que SELARL, une fois la méthode extraite du pilote. (stratégie mémoire)
- H2. Le client cible reste **médecins + chirurgiens-dentistes uniquement** ; aucune autre
  profession réglementée n'est dans le périmètre V1. (déduit du canon — aucune autre profession citée)
- H3. La « micro-holding » (société civile associée d'une SELAS médecin) deviendra une **famille de
  documents à part entière** une fois le modèle d'Albane intégré. (déduit de la réponse Albane)

### QUESTION OUVERTE (bloquant ou nécessitant arbitrage — voir §7)
- Q1. **Associé personne morale en SELARL** : le canon V3 le prévoit, Albane dit que c'est faux
  (SELAS médecin + micro-holding uniquement). Voir dérive §4 / question boss n°1.
- Q2. Composition du dossier cession SCM (autonome vs bundlé) — UI.
- Q3. Périmètre de la V1 produit globale : SELARL seule d'abord, ou plusieurs structures en
  parallèle ?

---

## 4. État vs intention — dérives détectées

Format : intention attendue → comportement actuel → impact → sévérité → action recommandée.

### D1. Associé personne morale en SELARL (dérive juridique majeure)

> ⛔ ABANDONNÉ (décision Gad 2026-06-04) — SELARL reste unipersonnelle. La dérive est désormais sans
> objet **pour la SELARL** (plus de multi-associés ni d'associé personne morale SELARL). La possibilité
> d'un associé personne morale **en SELAS** via micro-holding reste valable et hors de cette abandon.

- **Intention (canon V3).** Le PV de nomination du gérant et la matrice SELARL prévoient un
  **associé personne morale** dans une SELARL (variables `denomination_societe_1`,
  `nb_parts_societe_1`). Le code suit ce canon.
- **Réalité (Albane, source juridique plus récente).** Un associé personne morale n'est possible
  **qu'en SELAS** (pas SELARL), **seulement pour des médecins**, et via une **société civile
  « micro-holding »** (pas une SPFPL). Modèle fourni : `modele Statuts SELAS avec MH.docx`.
- **Impact.** Le canon produit contredit l'avocate sur un point de droit ; touche directement le PV
  gérant SELARL et les statuts SELARL. Risque de générer un document juridiquement faux.
- **Sévérité : HAUTE** (fidélité juridique = cœur de la promesse).
- **Action recommandée.** **Ne rien coder/modifier** sur ce point sans arbitrage. Question boss
  n°1 ; Gad relaie à la chaîne humaine (NotebookLM / associé / Albane). Si tranché → **superséder le
  canon V3** sur ce point dans le journal de décisions, puis propager. (cf. mémoire PM
  `open-q-personne-morale-selarl`)

### D2. Étiquettes statuts inversées dans le canon V3 (coquille source)
- **Intention.** DOC-016 = statuts **chirurgien-dentiste**, DOC-017 = statuts **médecin**
  (mapping retenu dans `SELARL_CANONICAL_STATUS_V1`).
- **Réalité (canon V3).** Les libellés sont croisés : « Status chirurgien dentiste -> *SELARL
  chirurgien dentiste* » mais juste en dessous « Statuts **dentiste** -> *SELARL **médecins***.docx »,
  et la section « 3. Si chirurgien dentiste » renvoie au fichier dentiste tandis que la légende
  mélange dentiste/médecin.
- **Impact.** Coquille de **documentation source**, pas de comportement (le code mappe correctement
  par profession). Risque de confusion à la lecture du canon.
- **Sévérité : FAIBLE** (cosmétique documentaire).
- **Action recommandée.** Signaler à l'associé pour correction du canon V3 ; ne pas toucher au code.

### D3. Cessions / SCM : générateurs prêts mais front partiellement câblé
- **Intention.** Le canon SELARL inclut cession de cabinet et cession SCM comme branches
  conditionnelles.
- **Réalité.** Générateurs prêts et **scénarios générés** (packs OK) sur la branche `review/selarl`,
  mais le **sous-formulaire interactif** de saisie (~40 champs cession + bail) n'est pas encore
  branché dans le shell ; un placeholder `nombre_pages_lettres="vingt"` reste à remplacer par une
  saisie réelle.
- **Impact.** Le pack se génère par scénario, mais l'utilisateur ne peut pas encore saisir librement
  ces cas dans l'UI.
- **Sévérité : MOYENNE** (dette UI connue, non bloquante pour la revue par scénario).
- **Action recommandée.** Ticket UI dédié (déjà identifié `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`),
  sans toucher aux générateurs.

### D4. Couche genre/nombre incomplète (multi-associés câblé OFF en dur)
- **Intention (workflow produit).** Une couche **paramétrée genre × nombre × variante** que les
  générateurs consomment.
- **Réalité.** `utils/grammar.py` ne couvre que masculin/féminin singuliers ; **pas de système de
  pluriel** ; le multi-associés est forcé OFF (`skip_personne_2_line=True`).
- **Impact.** Bloque le multi-associés complet côté technique, en plus du blocage Albane côté
  wording.
- **Sévérité : MOYENNE** (dette d'architecture, alignée avec le blocage métier).
- **Action recommandée.** Chantier « couche genre/nombre » à cadrer **après** réception du wording
  pluriel d'Albane (pas avant — sinon on code une mécanique sans texte de référence).

### D5. Dérives de cohérence catalogue/forks (héritées, hors périmètre SELARL)
- 3 forks de générateurs (cession parts/actions SPFPL, attestation capital SAS vs SPFPL, squelette
  acte de cession 3×) ; coquille « cession d'action » dans le doc parts SPFPL ; `DOC-023` source_path
  cassé. **Aucune ne bloque la clôture SELARL** (offenders = SPFPL/SCM/SAS).
- **Sévérité : FAIBLE→MOYENNE**, à traiter quand on cadrera SPFPL/SAS, pas maintenant.

---

## 5. Critères d'acceptation produit — SELARL (vérifiables)

Ces critères définissent ce que « SELARL livrée » signifie côté produit. Ils sont vérifiables sur
les packs générés et sur l'UI.

- **CA-1 (tronc commun).** Pour tout dossier SELARL valide, le pack contient toujours les 3
  documents communs (déclaration de non-condamnation, autorisation de domiciliation, procuration) +
  le PV de nomination du gérant + la demande d'inscription à l'ordre.
- **CA-2 (statuts par profession).** Un dossier **médecin** génère les statuts médecin (DOC-017) ;
  un dossier **dentiste** génère les statuts dentiste (DOC-016) ; **jamais les deux**, jamais
  l'inverse.
- **CA-3 (régime communautaire).** Si et seulement si le régime communautaire est activé, le pack
  inclut **les deux** lettres conjoint (renonciation DOC-005 + avertissement DOC-006) ; sinon
  aucune.
- **CA-4 (cession de cabinet).** Si une cession est demandée, le pack produit l'acte **ou** le
  compromis selon l'**étape explicite** choisie, dans la **variante correspondant au type de
  cabinet** (médical/dentaire) ; aucune clause médicale dans un document dentaire et inversement ;
  le crédit-vendeur n'apparaît que sur l'acte médical et uniquement s'il est activé.
- **CA-5 (cession SCM).** Si une cession de parts SCM vers la SEL est demandée, le pack produit le
  PV d'AGE + le courrier SDE + l'acte de cession des parts SCM (DOC-031/032/033), avec la SEL en
  création comme cessionnaire et le praticien personne physique comme cédant.
- **CA-6 (fidélité du wording).** Le texte de chaque document généré est **identique au modèle
  tokenisé source**, hors substitution des variables ; aucune phrase rédigée par l'outil ; les
  mentions « à compléter à la main » et instructions internes (ex. « Ajouter en cas de CV ») ne sont
  jamais rendues.
- **CA-7 (cohérence des données partagées).** Une donnée saisie une fois (nom, adresse de siège =
  domiciliation, capital, dates) apparaît identique dans tous les documents qui l'utilisent.
- **CA-8 (honnêteté du périmètre).** Les cas non couverts (multi-associés complet, médecin
  multi-associés, dérogations, site distinct) sont affichés avec un statut explicite (manuel /
  hors-scope) ; l'UI ne propose jamais de générer un document que le moteur ne sait pas produire
  fidèlement.

> Le **100 % produit** de la SELARL simple reste conditionné à la **validation finale de l'associé**
> sur le pack de revue (et aux retours d'Albane sur les statuts dentiste, S3/S4).

---

## 6. Mon rôle de gardien produit dans le workflow

En tant que product-manager Sydel, ma mission dans la chaîne est de **protéger l'intention métier et
la fidélité juridique avant la vitesse de code** :

- **Restituer** chaque demande en langage opérationnel et classer l'information (confirmé / probable
  / hypothèse / question) **avant** tout code.
- **Détecter et remonter les dérives** entre le canon, les specs, le code et l'avis juridique — sous
  la forme intention → réalité → impact → sévérité → action — sans trancher moi-même une règle de
  droit.
- **Refuser d'inventer une règle ou un wording juridique** : si une règle manque, je dis exactement
  ce qui manque et je m'arrête (escalade via Gad → NotebookLM → associé → Albane).
- **Produire des critères d'acceptation** vérifiables sur les packs, contre lesquels
  l'implémentation est testée.
- **Préserver les workflows déjà validés** : ne pas régresser la SELARL simple ; tout changement de
  comportement est qualifié (aligné / évolution délibérée / dérive / dette).
- **Consigner les décisions** ratifiées dans le journal de décisions (code stable, ancienne décision
  superseded) et propager au canon — jamais enterrer une décision produit dans le chat.
- Je **n'écris pas de code** et ne décide pas l'architecture sauf si elle change le comportement
  produit. Gad tranche le produit/scope/technique/merge ; il **ne tranche pas** le wording juridique.

---

## 7. Questions au boss (Gad)

1. **Associé personne morale en SELARL (dérive D1).** Le canon V3 le prévoit, Albane dit que c'est
   faux (possible **uniquement en SELAS, pour médecins, via micro-holding société civile**). On
   superséde le canon V3 et on **retire** ce cas du PV/statuts SELARL ? Et on ouvre la
   « micro-holding SELAS » comme nouvelle famille ? (bloquant — je n'y touche pas sans ton GO)
2. **Périmètre V1 produit (Q3).** Le livrable V1 = **SELARL seule d'abord** (puis méthode rejouée
   sur les autres structures), ou plusieurs structures en parallèle dès maintenant (SELAS côté
   Naomi) ? Cela conditionne ce qu'on déclare « dans le périmètre ».
3. **Profession cible (H2).** On confirme que la V1 reste **médecins + chirurgiens-dentistes
   uniquement** ? Une autre profession réglementée est-elle envisagée à court terme ?
4. **Composition du dossier cession SCM (Q2).** Dans l'UI, la cession SCM doit-elle être un dossier
   **autonome**, un **add-on** à la création SELARL, ou **les deux** ? (impacte le sous-formulaire)
5. **Couche genre/nombre (D4).** On attend bien le wording pluriel d'Albane **avant** de construire
   la mécanique multi-associés, ou tu veux qu'on prépare la couche technique en amont (au risque de
   coder sans texte de référence) ?
6. **Définition de « SELARL terminée ».** Le 100 % produit = pack simple validé par l'associé, ou
   exiges-tu cession + SCM **câblées dans l'UI** (pas seulement par scénario) avant de déclarer la
   SELARL close ?
7. **Coquille canon V3 (D2).** Tu veux que je demande à l'associé de corriger les libellés statuts
   inversés dans le canon V3, ou on laisse (le code mappe correctement) ?
8. **Statut du modèle micro-holding.** `modele Statuts SELAS avec MH.docx` est dans les sources —
   doit-il être cadré/tokenisé dès maintenant, ou il attend l'arbitrage de la question 1 ?

---

*Fin V1. Ce document sera corrigé par Gad puis figé ; toute décision ratifiée doit être reportée au
journal de décisions du projet et propagée au canon.*
