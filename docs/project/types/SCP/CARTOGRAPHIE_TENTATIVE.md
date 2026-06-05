# SCP — Cartographie TENTATIVE des cas (V1)

> ## ⚠️ CARTE OFFICIELLE « cas → documents » **MANQUANTE**
> Le canon `project/source_truth/Documents_a_generer_par_cas_V3.docx` (et ses versions V1/V2) est
> **entièrement SELARL**. **Vérifié 2026-06-05 : aucune occurrence de « SCP » ni de « société civile
> professionnelle » dans les 3 versions du canon.** La SCP n'apparaît dans le corpus que comme **mention
> incidente** (une « société civile professionnelle » citée dans des statuts SELAS), **jamais** comme
> type d'entreprise avec sa propre liste de cas/documents.
>
> **Il n'existe donc AUCUNE carte « cas → documents » pour la SCP.** Tout regroupement ci-dessous est
> **PROBABLE (`dérivé`)**, reconstruit à partir des **seuls modèles Drive** — pas du canon. **À CONFIRMER
> par NotebookLM puis Rafael avant tout code.** Voir `NOTEBOOKLM_PROMPTS.md` (Bloc 1 = obtenir la liste
> officielle des cas SCP + ce qu'EST réellement ce « SCP »).

---

## ⚠️ Ambiguïté structurante préalable : qu'est-ce que « SCP » ici ?

Avant même de cartographier des cas, **il faut savoir de quel type d'entreprise on parle.** Le dossier
Drive est nommé « Création SCP » mais l'objet social des statuts décrit une **société civile de détention
de participations / portefeuille de titres** (objet = prise de participation, gestion d'un portefeuille,
« à l'exclusion de toute opération commerciale »), **PAS** l'exercice en commun d'une profession
réglementée (qui est le propre d'une **S**ociété **C**ivile **P**rofessionnelle d'exercice).

Trois lectures possibles, **non tranchées** :
- (a) **SCP = Société Civile Professionnelle** d'exercice → alors la trame statutaire fournie est **la
  mauvaise** (ou incomplète) et il manque les clauses d'exercice professionnel.
- (b) **SCP = société civile de portefeuille / holding patrimoniale** des praticiens → le sigle « SCP »
  est un raccourci interne trompeur ; c'est cohérent avec l'objet réel des statuts.
- (c) **SCP = société civile « support »** d'une SCM / d'un patrimoine immobilier professionnel.

**Cette question est le Bloc 1.0 des prompts. Rien ne se code avant qu'elle soit tranchée.**

---

## Ce dont on dispose réellement

- **5 modèles `.docx` tokenisés** (cf. `INVENTAIRE_MODELES.md`) issus du dossier Drive « Création SCP » :
  Statuts, Fiche de création, Autorisation de domiciliation, Déclaration de non-condamnation, Procuration.
- **1 modèle `.doc` legacy non extrait** : PV de nomination du gérant (à reconvertir).
- **1 PDF** : « SCP IR Note assistance à la déclaration » (note fiscale IR — périmètre à confirmer).
- **Aucune liste de cas**, aucune règle « tel cas → tels documents », **aucun retour humain (lock)**
  propre à la SCP.

## Regroupement PROBABLE par cas (hypothèse de travail — NON ratifiée)

> Légende statut : `dérivé` = déduit des modèles, jamais confirmé.

### Cas A — « Création d'une SCP / société civile » (hypothèse principale) — `dérivé`
Le dossier Drive ne contient **que** des documents de **constitution**. Hypothèse : un seul cas livré.
| Document (modèle) | Rôle présumé | Statut source |
|---|---|---|
| `Modèle Statuts SCP - transforme.docx` | Acte constitutif (objet = société civile de participations — cf. ambiguïté ci-dessus). | tokenisé |
| `Fiche de création de Société Civile - transforme.docx` | Fiche récap / collecte (jusqu'à 5 associés, 2 gérants). | tokenisé |
| `PV nomination gérant - transforme.doc` | Nomination du/des gérant(s) (peut inclure un volet emprunt/acquisition — à vérifier). | **`.doc` legacy non extrait** |
| `Autorisation de domiciliation - transforme.docx` | Domiciliation du siège (commun). | tokenisé |
| `Déclaration sur l_honneur de non condamnation - transforme.docx` | Déclaration de non-condamnation (commun). | tokenisé |
| `procuration - transforme.docx` | Mandat aux formalités (commun). | tokenisé |

**Ouvert :**
- **Demande d'inscription à l'ordre ?** Présente pour les SEL ; **absente** du dossier Drive SCP. Ne PAS
  l'ajouter sans confirmation (et dépend de la nature réelle du type — cf. ambiguïté).
- **Régime communautaire / conjoint ?** Lettres de renonciation et d'avertissement au conjoint
  **absentes** du dossier SCP. Ne PAS les ajouter sans confirmation.
- **Pacte d'associés / règlement intérieur ?** **Absents** du dossier SCP (présents pour la SCM). À
  confirmer s'ils existent pour ce type.
- **Note fiscale IR (PDF) :** livrable à produire ou simple note d'aide ? (Bloc 4.)

### Cas B — autres cas (cession, entrée/sortie d'associé, modification, dissolution…) — **INCONNUS**
Le dossier Drive **ne contient aucun** document de cession, de modification ou de dissolution pour la SCP.
**Aucune hypothèse n'est posée ici** : l'existence et le contenu de ces cas sont une **question ouverte**
(Bloc 1). Ne rien inventer.

---

## Divergence avec le code existant

**Aucune.** Vérifié 2026-06-05 : **`SCP` n'apparaît nulle part dans `src/`** (ni `case_catalog.py`, ni
`registry/`, ni `generators/`, ni `scenarios/`, ni `front_app/`). **Codex n'a rien construit pour la
SCP.** La fondation part donc d'une page blanche — ce qui est un avantage : pas d'extrapolation Codex à
challenger (contrairement à la SCM), mais aussi aucun acquis technique.

---

## Synthèse — ce qui DOIT venir de NotebookLM/Rafael avant tout code
1. **Quelle est la vraie nature du type « SCP »** (professionnelle d'exercice / portefeuille / support) ?
2. **Liste officielle des cas** (au-delà de la seule création).
3. **Carte création : liste exacte et ordre des documents**, systématiques vs conditionnels.
4. **Borne du nombre d'associés** (2 ? 5 ? N ?) et **nombre de gérants**.
5. **Statut des documents « communs »** vs spécifiques, et des documents absents (inscription ordre,
   régime communautaire, pacte/règlement).
