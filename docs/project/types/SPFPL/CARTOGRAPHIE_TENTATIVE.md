# SPFPL — Cartographie TENTATIVE des cas → documents

> ============================================================================
> ⚠️ NUANCE IMPORTANTE PAR RAPPORT AU BRIEF
> Le brief partait du principe : « AUCUNE carte officielle cas → documents pour SPFPL ».
> **C'est partiellement faux et il faut le savoir.** Une carte officielle SPFPL **EXISTE** dans le
> canon le plus ANCIEN : `project/source_truth/Documents_a_generer_par_cas.docx` (V1). Elle couvre
> deux cas — **SPFPL cession** et **SPFPL apport** — avec leur liste de documents.
> **MAIS** : (a) les versions plus récentes du canon (`_V2.docx`, `_V3.docx`) ont **SUPPRIMÉ** toute
> la section SPFPL → on ne sait pas si c'est volontaire (SPFPL retirée du périmètre) ou un oubli ;
> (b) la carte V1 est **incomplète** vs les modèles réellement présents sur le Drive (voir « Hors
> carte » plus bas) ; (c) un acte (« cession d'actions ») est listé **sans modèle** rattaché.
> ➜ **La carte cas→documents N'EST DONC PAS À INVENTER, mais À CONFIRMER : quelle version du canon
> fait foi (V1 qui contient SPFPL, ou V3 qui l'a retirée ?), et la liste des cas est-elle bien
> cession + apport seulement ?** → C'est la question n°1 pour NotebookLM / Rafael.
> Aucun cas ni wording n'est inventé ci-dessous : les cases listées proviennent SOIT du canon V1,
> SOIT d'un regroupement par dossier Drive (signalé « regroupement Drive, NON canonique »).
> ============================================================================

## A. Carte OFFICIELLE V1 (recopiée du canon, non inventée)

### Cas « SPFPL cession » (canon V1)
- **Docs à générer dans tous les cas** : Déclaration non-condamnation ; Autorisation de domiciliation ;
  Procuration.
- **Statuts** : `Statuts_SPFPLAS_dentistes_cession.docx`.
- **PV nomination gérant** : `PV nomination gérant.docx` *(modèle SPFPL tokenisé NON trouvé sur Drive)*.
- Demande d'inscription à l'ordre ; (rappel) Déclaration non-condamnation ; (rappel) Autorisation de
  domiciliation ; **Note d'informations** (`NOTE D'INFORMATION.docx`).
- **Si régime communautaire** : Lettre de renonciation ; Lettre d'avertissement au conjoint.
- **Si plusieurs associés** : `PV SELARL agrément cession SPFPL - SELARL plusieurs associés`.
- **Si associé unique** : `PV SELARL agrément cession SPFPL - SELARL 1 associé`.
- **Acte de cession de parts** : `Acte_cession_SPFPL_tiers_part_modele.docx`.
- **Acte de cession d'actions** : *(ligne présente au canon V1 mais SANS modèle nommé)* → à clarifier.

### Cas « SPFPL apport » (canon V1)
- **Docs à générer dans tous les cas** : Déclaration non-condamnation ; Autorisation de domiciliation ;
  Procuration.
- **Statuts** : `Statuts SPFPLAS dentistes - apport.docx`.
- **PV nomination gérant** : `PV nomination gérant.docx` *(modèle SPFPL tokenisé NON trouvé sur Drive)*.
- Demande d'inscription à l'ordre ; (rappel) Déclaration non-condamnation ; (rappel) Autorisation de
  domiciliation ; **Note d'informations**.
- **Si régime communautaire** : Lettre de renonciation ; Lettre d'avertissement au conjoint.
- **Apport doc** : Contrat d'apport (`Contrat d_apport SEL SPFPL.docx`) ; Attestation sur le capital
  (`Attestation sur le capital - apport - liste des souscripteurs.docx`) ; Attestation de nomination du
  commissaire aux apports (`attestation nomination commissaire aux apports - transforme.docx`).

## B. Modèles Drive HORS carte V1 (regroupement Drive, NON canonique — à arbitrer)

Ces modèles existent sur le Drive mais ne sont **pas rattachés** à un cas par le canon V1. Regroupement
proposé **par dossier Drive uniquement** — ne pas le traiter comme une règle métier :

| Regroupement Drive | Modèles concernés | Statut |
|---|---|---|
| Statuts par **forme/profession** | `STATUTS SAS SPFPL médecins`, `Statuts SAS SPFPL pharmaciens` | Le canon V1 ne mappe **que** la SPFPL-AS dentistes. SAS médecins/pharmaciens = formes/professions **non couvertes par la carte** → cas supplémentaires ? variantes profession ? |
| Combo **`cession + apport`** | dossier Drive `cession + apport/` (contrat d'apport enrichi, attestations, régime communauté) | Le Drive a un 3e dossier « cession + apport » → **3e cas** (opération mixte) ou simple rangement ? Non tranché par le canon. |
| **Liste des souscripteurs** | `Liste des souscripteurs - transforme.docx` | Présent au Drive, **absent** de la carte V1 SPFPL. À rattacher (création/souscription ?). |
| **Appel des fonds** | `appel des fonds spfpl - transforme.docx` | Présent, **absent** de la carte V1. Probable « si cession » (analogue SELARL) mais NON confirmé. |
| **RM Sydel** (fiche patrimoniale) | `RM Sydel SPFPL - transforme.docx` | Paraît être un document interne de conseil, **hors chaîne d'actes**. À confirmer : doit-il être généré ? |
| **PV autorisation d'emprunt** | `PV SPFPL autorisation empruntt.doc` (legacy `.doc`, non tokenisé) | Présent au Drive mais non récupérable + absent de la carte. |
| **Actes de cession** (legacy) | `Acte_cession_parts_Dr_SPFPL_modele.doc`, `Acte_cession_SPFPL_tiers_modele.doc` | Legacy `.doc`. Le 2e (`_tiers_modele`) correspond probablement à l'« acte de cession d'**actions** » manquant de la carte V1. À reconvertir. |

## C. Variantes transverses à confirmer (genre / profession / nombre)
- **Profession** : statuts existent en dentistes (SPFPL-AS), médecins (SAS), pharmaciens (SAS). Quelles
  professions sont dans le périmètre, et la profession est-elle une **variable** ou un **modèle distinct** ?
- **Nombre d'associés** : la carte distingue « associé unique » vs « plusieurs associés » (PV agrément).
  Le canon V1 (section « Règles ») dit 1 à 6 associés possibles, modèle unique à étendre.
- **Genre** : aucun lock humain SPFPL trouvé → à traiter comme la SELARL (paires de chaînes exactes),
  après confirmation.

## D. Ce qui doit être tranché AVANT de cartographier pour de bon
1. **Quelle version du canon fait foi** pour SPFPL (V1 contient SPFPL ; V2/V3 l'ont retirée) ?
2. **Liste exacte des cas** : cession + apport seulement, ou aussi « cession + apport » mixte ?
3. **Forme sociale** : la SPFPL est-elle une **SARL** (parts) **ou** une **SAS** (actions), ou les deux
   selon le cas ? Les modèles mélangent parts (cession de parts) et actions (statuts SAS, `nb_actions`).
4. Les modèles « hors carte » (liste souscripteurs, appel de fonds, RM Sydel, SAS médecins/pharmaciens)
   sont-ils dans le périmètre, et dans quel cas ?
