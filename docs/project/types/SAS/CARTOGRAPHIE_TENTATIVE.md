# SAS — Cartographie TENTATIVE des cas → documents (V1)

> ╔══════════════════════════════════════════════════════════════════════════════╗
> ║  CARTE OFFICIELLE « cas → documents » **MANQUANTE** pour le type SAS.            ║
> ║  Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` est        ║
> ║  **ENTIÈREMENT SELARL** (0 occurrence de SAS / SASU / SPFPL — vérifié sur le     ║
> ║  contenu, pas le nom). Le regroupement ci-dessous est **PROBABLE / inféré**     ║
> ║  des modèles disponibles. **NE PAS l'utiliser comme vérité.**                   ║
> ║  → À FAIRE CONFIRMER par **NotebookLM puis Rafael** (cf. NOTEBOOKLM_PROMPTS.md). ║
> ╚══════════════════════════════════════════════════════════════════════════════╝

**Date :** 2026-06-05 · **Base :** les 7 modèles de `project/source_documents/sas/` (cf. INVENTAIRE_MODELES.md).
**Méthode :** inférence par analogie avec la structure des SEL du canon (« dans tous les cas » / cas spécifiques)
+ lecture du contenu des modèles. Aucune règle, aucun cas, aucun wording n'a été inventé : ce qui n'est pas
attesté par un modèle est marqué **(inféré)** ou **(?)**.

---

## Regroupement PROBABLE par cas

### Cas A — Création SAS (socle « dans tous les cas ») — *probable*
Documents attestés par un modèle :
- Déclaration sur l'honneur de non-condamnation — `declaration_non_condamnation_transforme.docx`
- Autorisation de domiciliation — `autorisation_domiciliation_transforme.docx`
- Procuration — `procuration_transforme.docx`

> Ces trois documents sont « dans tous les cas » dans le canon SELARL ; **probable** que ce soit
> identique en SAS, mais **non confirmé** pour la SAS.

### Cas B — Statuts SAS (constitution) — *probable, mono-modèle*
- Statuts SAS / SPFPL médecins — `statuts_sas_spfpl_medecins_modele.docx`

> Seul statuts du corpus. Profession **médecin** uniquement (les SPFPL pharmaciens/dentistes vivent
> sous le type SPFPL). **Y a-t-il d'autres statuts SAS attendus (pharmacien, dentiste, SAS « simple »
> non-SPFPL) ?** → question Rafael.

### Cas C — Capital / souscription — *probable*
- Liste des souscripteurs (version courte) — `liste_souscripteurs_transforme.docx`
- Liste des souscripteurs (variante enrichie SPFPL) — `liste_souscripteurs_variante_copie_transforme.docx`

> **Deux variantes** du même document. Laquelle est la référence ? Sont-elles deux documents
> distincts ou deux états d'un même document ? → à trancher.
> (Codex parle aussi d'une « attestation sur le capital » — voir note plus bas : modèle introuvable.)

### Cas D — Gouvernance / président — *probable*
- PV rémunération du président — `pv_remuneration_president_transforme.docx`

> Couvre la décision de rémunération du président (absence de rémunération jusqu'à clôture du 1er
> exercice dans la lecture Codex). **Manque-t-il un PV de nomination du président** (analogue au « PV
> nomination gérant » SELARL) ? Aucun modèle de nomination trouvé dans `Création SAS`. → question.

### Cas E — Variante actionnaire unique (SASU) — *(?) hors corpus copié*
- Candidat : `statuts SASU Holding - transforme.docx` (présent sur le Drive, **non copié**, hors
  `Création SAS`).

> La SASU (unipersonnelle) est-elle un cas du type SAS, ou un type/holding à part ? → arbitrage.

---

## Cas du canon SELARL **sans équivalent attesté** côté SAS (inféré — à confirmer)

Pour mémoire, le canon SELARL connaît aussi : régime communautaire (renonciation / avertissement),
cession (avenant bail, appel de fonds, actes & compromis cabinet médical/dentaire), SCM cession,
dérogation, site distinct. **Aucun de ces cas n'est attesté par un modèle dans `Création SAS`.**

Questions ouvertes en découlant (→ NotebookLM/Rafael) :
- La SAS a-t-elle un cas **cession** (d'actions) ? Un cas **régime communautaire** ? (le statuts SAS
  contient déjà un bloc conjoint/régime matrimonial → peut-être une renonciation associée, non fournie).
- Existe-t-il pour la SAS une **demande d'inscription à l'ordre** (analogue SELARL) ?

---

## Divergences structurelles SAS vs SELARL (faits, non inférés)

- **Actions** (`[nb_actions]`, `[valeur_nominale_action]`) côté SAS vs **parts** côté SELARL.
- Dirigeant = **président** (`[fonction_dirigeant]`, `[qualite_associe]`) vs **gérant** SELARL.
- Capital « souscrit » (`[montant_sous]`) + liste de souscripteurs propre à la SAS.

---

## Écart entre cette carte inférée et ce que Codex a déjà codé (à réconcilier)

Le registre `src/.../registry/catalog.py` + `domain/case_catalog.py` déclarent **déjà** pour `CaseType.SAS` :
`statuts_sas`, `declaration_non_condamnation`, `autorisation_domiciliation`, `procuration`,
`attestation_capital_sas`, `pv_remuneration_president`, et une entrée « Liste des souscripteurs ».

⚠️ Points de friction relevés (à vérifier, **zéro confiance** dans l'auto-déclaration Codex) :
1. **`attestation_capital_sas` / « Attestation sur le capital - apport - liste des souscripteurs.docx »** :
   ce **modèle source est INTROUVABLE** dans `Création SAS` (ni ailleurs sous ce nom). Codex référence un
   `project/source_import/raw_drive_dump/Creation SAS/…` qui **n'existe pas** dans ce repo. → soit le
   modèle manque, soit c'est la variante « Liste des souscripteurs enrichie ». **À élucider.**
2. Codex a **inventé l'assemblage** SAS (il n'y a pas de canon SAS) → cette carte Codex **n'est PAS
   ratifiée**. Elle vaut hypothèse, au même titre que la présente.
3. Le périmètre Codex est verrouillé à **SPFPL médecins / actionnaire unique** : cohérent avec le seul
   statuts disponible, mais c'est une **restriction non confirmée** comme étant LE périmètre du type SAS.

> **Conclusion :** tant que NotebookLM/Rafael n'a pas fourni la liste des cas SAS et la carte
> cas → documents, **aucune cartographie n'est canonique** — ni celle-ci, ni celle implicite dans le code.
