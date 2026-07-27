# Rapport — Bundles par cas vs Canon (vérification croisée)

Date : 2026-06-08
Périmètre : conformité du **bundle de création** réellement généré par chaque slice front, comparé au
canon `project/source_truth/Documents_a_generer_par_cas.docx` (V1).
Mode : lecture seule (aucun edit code, aucun git). Génération via le vrai chemin de production de chaque
type (type registry → slice → orchestrateur).
Critères par type : (a) tous les docs du canon hors cas non-création générés ? (b) manquants / en-trop ?
(c) placeholders résiduels `[...]` ?

---

## Tableau de synthèse

| Type | Bundle conforme canon | Docs générés | Attendus canon (création) | Manques | En-trop | Placeholders `[...]` |
|---|---|---|---|---|---|---|
| **SAS** | **OUI** | 6 | 6 (codes distincts) | aucun | aucun | 0 |
| **SCS** | **OUI** | 5 | 5 | aucun | aucun | 0 |
| **SCI** | **NON** | 5 | 5 inconditionnels + 1 conditionnel | DOC-022 (lettre option IS, « Si IS ») | aucun | 0 |
| **SCI IRIS** | **NON** | 5 | 5 inconditionnels + 1 conditionnel | DOC-022 (lettre option IS, « Si IS ») | aucun | 0 |
| **SCM** | **NON** | 6 | 8 (6 tronc + 4 satellites, doublons dédupliqués) | DOC-026, DOC-027, DOC-028, DOC-030 (4 satellites) | aucun | 0 |
| **SELAS** | **NON** | 6 | 6 inconditionnels | DOC-018 (statuts médecin, substitué par DOC-044) | aucun (substitution, pas ajout) | 0 |
| **SPFPL cession** | **NON** | 6 | 7 (bloc inconditionnel) | DOC-037 (Note d'information) | aucun | 0 |
| **SPFPL apport** | **NON** | 6 | 10 (7 systématiques + 3 « Apport doc ») | DOC-037, DOC-041, DOC-042, DOC-043 | aucun | 0 |

Conformes : **2 / 8** (SAS, SCS).
Non conformes : **6 / 8** (SCI, SCI IRIS, SCM, SELAS, SPFPL cession, SPFPL apport).
Placeholders `[...]` résiduels : **0 sur tous les types** — propreté de rendu unanime.
Documents en trop (hors canon) : **0 sur tous les types**.

---

## Détail par type

### SAS — CONFORME (OUI)
- **Générés (6)** : statuts_sas_spfpl_medecins (DOC-015), declaration_non_condamnation (DOC-001),
  autorisation_domiciliation (DOC-002), procuration (DOC-003),
  attestation_capital_liste_souscripteurs_sas (DOC-024), pv_remuneration_president (DOC-023).
- **Canon SAS** : 6 codes distincts (la ligne « liste des souscripteurs » du canon = même DOC-024 que
  l'attestation sur le capital, rendu une seule fois — déduplication légitime, confirmée par
  `case_catalog`). Le canon SAS ne demande NI PV nomination gérant NI demande d'inscription à l'ordre.
- **(a)** OUI, correspondance 1:1. **(b)** aucun manque, aucun en-trop. **(c)** 0 placeholder, fichiers
  réellement peuplés (statuts ≈ 33 074 car., données SPFPL MARTIN présentes).
- Réserve factuelle : pas de scénario figé `scenarios/sas.py` ; boussole reproductible portée par
  `_sas_payload()` dans `tests/unit/test_multi_type_front.py`. Périmètre couvert = SAS V1 = SPFPL
  médecins, actionnaire unique masculin marié (actionnaire féminin verrouillé hors périmètre).

### SCS — CONFORME (OUI)
- **Générés (5)** : statuts_scs (DOC-019), declaration_non_condamnation (DOC-001),
  autorisation_domiciliation (DOC-002), procuration (DOC-003), pv_nomination_gerant (DOC-004).
- **Canon SCS** (P47-P56) : 5 documents, tous de création, aucun cas conditionnel/non-création.
- **(a)** OUI 1:1. **(b)** aucun manque, aucun en-trop (confirmé par double différence symétrique vide
  contre le registre `build_seed_catalog`). **(c)** 0 placeholder.
- Complet par construction : le canon V1 ne prévoit ni cession ni régime communautaire pour SCS.

### SCI — NON CONFORME
- **Générés (5)** : statuts_sci (DOC-020) + tronc commun DOC-001/002/003 + PV gérant DOC-004.
- **Manque** : **DOC-022 « Lettre option IS »**, conditionnel canon « Si IS ». Le générateur existe et
  est testé (`LettreOptionIsGenerator`), mais inaccessible depuis le parcours SCI : `_dossier_options`
  ne met jamais `option_is=True`, le formulaire civil n'expose aucune bascule « option IS »
  (`grep option_is` sur `front_app` = 0). Un dossier SCI à l'IS ne peut pas produire la lettre.
- Drift front ↔ moteur (le moteur sait générer, le front n'offre pas l'option). Sévérité moyenne :
  pas de mauvais document produit, document légitime manquant pour les SCI à l'IS.
- **(c)** 0 placeholder. **En-trop** : aucun (l'absence de demande d'inscription à l'ordre est
  correcte — `DEMANDE_INSCRIPTION_ORDRE_STRUCTURES` exclut SCI).

### SCI IRIS — NON CONFORME
- **Générés (5)** : statuts_sci_iris (DOC-021) + DOC-001/002/003 + PV gérant DOC-004. Tous CLEAN.
- **Manque** : **DOC-022 « Lettre option IS »** (même cause que SCI). Incohérence corroborante :
  l'orchestrateur `select_documents("SCI IRIS")` renvoie 6 docs (dont DOC-022), le slice front n'en
  produit que 5 — divergence slice/orchestrateur sur DOC-022.
- **(c)** 0 placeholder. **En-trop** : aucun.
- Note de sévérité : si la convention V1 est « cas IRIS de création toujours sans option IS », le
  bundle 5 docs serait complet — mais cette restriction n'est écrite nulle part (aucune garde, aucun
  commentaire). Trou de couverture non documenté, pas une exclusion délibérée.

### SCM — NON CONFORME
- **Générés (6)** : statuts_scm, declaration_non_condamnation, autorisation_domiciliation, procuration,
  pv_nomination_gerant, demande_inscription_ordre.
- **Manquent (4 satellites, tous inconditionnels au canon SCM)** : **DOC-026** Pacte d'associés SCM,
  **DOC-030** Liste dépenses communes SCM, **DOC-027** Contrat frais communs, **DOC-028** Règlement
  intérieur SCM. Générateurs présents et `WorkflowStatus.TESTE`, mais exclus du bundle par
  `_creation_bundle_codes`.
- Cause racine : les satellites exigent l'identité juridique des deux sociétés d'exercice partenaires,
  **non collectée** par la saisie de création SCM (blocage métier réel). Exclusion délibérée et
  documentée (commentaire `civil_statuts_slice.py` L57-65), figée par le test
  `test_scm_slice_generates_clean` qui n'attend que 6 docs → dette connue et assumée, pas un bug
  accidentel — mais reste une non-conformité au canon.
- Incohérence à signaler : `warnings` du plan affiche `« + satellites SCM »` et le slice met
  `scm_satellites=True` alors qu'aucun satellite n'est émis (message trompeur vs comportement réel).
- **(c)** 0 placeholder. **En-trop** : aucun (doublons DNC/domiciliation du canon correctement dédupliqués).

### SELAS — NON CONFORME
- **Générés (6, bundle fixe non extensible)** : statuts_selas_multi (DOC-044),
  declaration_non_condamnation (DOC-001), autorisation_domiciliation (DOC-002), procuration (DOC-003),
  pv_nomination_gerant (DOC-004), demande_inscription_ordre (DOC-034).
- **Manque inconditionnel** : **DOC-018 « Statuts_SELAS_medecin.docx »** (statuts SELAS médecin, associé
  unique) — jamais généré, **substitué** par DOC-044 (statuts SELAS multi-associés). DOC-018 a un
  générateur câblé mais n'est atteignable par aucun chemin front. Substitution non documentée comme
  décision ratifiée au niveau du canon V1 fourni (doc-id ET nom de fichier divergent).
- Le slice SELAS est un bundle **fixe de 6**, sans aucune des branches conditionnelles que le canon
  SELAS prévoit (régime communautaire → DOC-005/006 ; SCM → DOC-031/032/033 ; cession → DOC-007 ;
  cabinets → DOC-009/010/011/012 ; dérogation → DOC-013) — alors que le moteur les supporte par
  ailleurs : divergence front ↔ moteur.
- Trou canon sévère : la ligne SELAS « Demande de dérog. cumul SELARL salarié »
  (`Demande_derogation_cumul_SELARL_salariee.doc`) n'a ni doc-id, ni entrée catalogue, ni générateur.
  À ne pas confondre avec DOC-014 (cumul SELARL-BNC, déclaré `structures=['SELARL']`).
- **(c)** 0 placeholder (les 32 « … » de statuts_selas_multi sont des points de conduite
  typographiques suivis d'une valeur réelle, pas des placeholders).
- **En-trop** : aucun document hors-canon (DOC-044 est une substitution, pas un ajout).
- Note de méthode : le canon existe en 3 variantes (`...`, `_V2`, `_V3`) et un arbitrage « V1-vs-V3 »
  est ouvert. Verdict établi strictement contre la V1 nommée dans la tâche ; à rejouer contre V3 si
  c'est la cible ratifiée.

### SPFPL cession — NON CONFORME
- **Générés (6)** : statuts_spfpl_cession (DOC-035), declaration_non_condamnation (DOC-001),
  autorisation_domiciliation (DOC-002), procuration (DOC-003), pv_nomination_gerant (DOC-004),
  demande_inscription_ordre (DOC-034). Plan `can_generate=True`, 0 blocker.
- **Manque** : **DOC-037 « Note d'information »**, placée par le canon dans le bloc **inconditionnel**
  (« dans tous les cas »), pas sous une garde « Si ». Générateur présent et testé. Le slice l'exclut
  volontairement : tenter DOC-037 avec le contexte du slice → échec dur « associes_cible est
  obligatoire » (roster cible avant/après = donnée d'OPÉRATION non collectée à la création).
  Exclusion techniquement fondée mais divergente du canon (qui traite la Note comme systématique).
- Les blocs conditionnels du canon (régime communautaire DOC-005/006 ; multi-associés DOC-039 bloqué
  V1 ; associé unique DOC-038/040/029) sont légitimement hors bundle de création (cas opération).
- **(c)** 0 placeholder (32 points de conduite « … » dans les statuts = formatage source légitime).
- **En-trop** : aucun.
- Arbitrage métier requis : Note d'information = document de création à câbler (avec collecte
  `associes_cible`), ou document d'opération à sortir explicitement du périmètre création ? À trancher
  côté associé métier, pas par un choix technique silencieux.

### SPFPL apport — NON CONFORME
- **Générés (6)** : statuts_spfpl_apport (DOC-036), declaration_non_condamnation (DOC-001),
  autorisation_domiciliation (DOC-002), procuration (DOC-003), pv_nomination_gerant (DOC-004),
  demande_inscription_ordre (DOC-034).
- **Manquent (4)** : **DOC-037** Note d'information (création systématique selon canon),
  **DOC-041** Contrat d'apport SEL→SPFPL, **DOC-043** Attestation nomination commissaire aux apports
  (section « Apport doc » du canon), **DOC-042** Attestation sur le capital / liste des souscripteurs.
  Preuve moteur : sur le contexte du slice, l'orchestrateur (catalogue complet, avant filtre) active
  **9 docs** (001/002/003/004/034/036 + 037, 041, 043) ; `_creation_bundle_codes` en retire 3. DOC-042
  n'apparaît même pas — le slice construit `CapitalSouscription` avec `souscripteurs=[]` alors que
  l'activation exige exactement 1 souscripteur (double cause : hors bundle + jamais déclenché).
- Périmètre volontairement restreint à la coquille de création du holding (opérations « hors bundle
  automatique »), mais divergent du canon. Incohérence interne : le `warnings` du plan annonce
  « … + note d'information » alors que `_creation_bundle_codes` n'inclut PAS DOC-037 (message contredit
  par le code).
- **(c)** 0 placeholder. **En-trop** : aucun.

---

## Verdict global

**Suite complète** : `python -m pytest tests/ -q` → **356 passed** en 34.63s
(basetemp `artifacts/_audit_tmp/pt_bundles_final`). Suite TOTALE relancée, aucun échec.

**Conformité bundles vs canon : NON GLOBAL.** 2 types sur 8 sont conformes (SAS, SCS) ; 6 sur 8
divergent du canon V1. La qualité de rendu est uniformément bonne (0 placeholder `[...]`, 0 document en
trop sur les 8 types) — les écarts sont exclusivement des **manques de couverture**, jamais des
documents parasites ni des sorties sales.

Trois familles de non-conformité :
1. **Conditionnel mort côté front** (SCI, SCI IRIS) : DOC-022 lettre option IS générable par le moteur
   mais sans bascule dans le formulaire ni câblage dans le slice ; l'orchestrateur le sélectionne, le
   slice non → drift front ↔ moteur, non documenté.
2. **Satellites / docs systématiques exclus par choix de scope** (SCM 4 satellites ; SPFPL cession
   DOC-037 ; SPFPL apport DOC-037 + 3 « Apport doc ») : exclusions techniquement fondées (données
   d'opération / sociétés partenaires non collectées à la création) mais divergentes du canon, et
   parfois **contredites par les `warnings` du plan** (SCM « + satellites SCM », SPFPL apport
   « + note d'information ») — messages trompeurs à corriger.
3. **Substitution de statuts non ratifiée** (SELAS) : DOC-018 statuts médecin remplacé par DOC-044
   statuts multi ; bundle figé sans aucune branche conditionnelle pourtant prévue au canon ;
   `Demande_derogation_cumul_SELARL_salariee.doc` totalement absent du moteur.

**Points d'arbitrage métier à remonter (associé, pas PM)** : (i) la Note d'information SPFPL est-elle
un document de création systématique ou d'opération ? (ii) l'option IS doit-elle être exposée à la
création SCI/SCI IRIS ? (iii) la substitution DOC-018→DOC-044 en SELAS est-elle ratifiée, et le canon
SELAS cible est-il V1 ou V3 ? (iv) les satellites SCM et les docs « Apport doc » sont-ils attendus dans
le bundle de création ou explicitement reportés en opération ?

**Dette technique immédiate (sans décision métier)** : corriger les `warnings` de plan trompeurs (SCM
et SPFPL apport annoncent des documents que le bundle ne produit pas), et le `scm_satellites=True` /
`select_documents` ↔ slice divergent — ces incohérences internes sont des bugs de surface
indépendants de l'arbitrage métier.
