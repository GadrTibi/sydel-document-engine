# Paquet Rafael — CORRIGÉ (2026-06-07)

> ⚠️ **CORRECTION MAJEURE.** La V1 de ce paquet affirmait que des modèles « manquaient ». **C'était
> FAUX.** Vérification sur le vrai arbre (`project/source_documents/<type>/`) : **tous les modèles sont
> présents.** L'erreur venait du **premier audit B0 tourné sur le mauvais clone** (primary/main, qui
> n'a que `lot_01-05`) → conclusion « manquant » propagée **sans re-vérification**. Rafael avait raison
> (« y a tous les docs »). Leçon codifiée : [[trap-false-missing-from-wrong-clone]].

## Modèles soi-disant « manquants » → en fait PRÉSENTS
| Réclamé V1 (à tort) | Réalité (chemin) |
| :--- | :--- |
| SCI « Lettre d'option IS » | `sci/lettre option IS.docx` (+ `lot_05/lettre option IS.docx`) |
| SCM « Liste des dépenses communes » .docx | `lot_05/Liste dépenses communes SCM.docx` (+ `.doc` legacy) |
| SCP / PV nomination gérant | `lot_02/PV nomination gérant - transforme.docx` (+ `scm/`, `sci/`) |
| Dossiers par type complets | `scm/ sci/ scp/ scs/ spfpl/ sas/` tous présents |

→ **On a TOUTE la matière documentaire.** Le build n'est PAS bloqué par des docs manquants.

## Ce qui reste GENUINEMENT ouvert (à confirmer une fois les modèles tokenisés — pas un dump à Rafael)
Ne PAS reposer ces points en bloc : d'abord épuiser les modèles tokenisés (rule 20), puis confirmer
le strict résiduel. Arbitrages produit/métier réels :
- **SCP — nature** : l'objet du modèle = « gestion d'un portefeuille de titres, à l'exclusion de toute
  opération commerciale » → société civile **de portefeuille/patrimoniale** (déductible du modèle
  lui-même) ; reste le **GO/NO-GO périmètre** (canon classe SCP « hors moteur »). → décision produit.
- **SELAS — scope** : multi 2-5 + personne morale + DG (vs V1 unipersonnel). → décision produit (Gad/Rafael).
- **SCI — PM en SCI standard** : NotebookLM dit autorisé, le moteur bloque par prudence → confirmer pour débloquer.
- **SPFPL — vocabulaire** : PV nommés « cession » au wording « apport » → confirmer la correction.

## Seul élément RÉELLEMENT absent du repo
- **Modèle SELAS multi « Reynaud »** : pas dans `source_documents` (seul `Statuts_SELAS_medecin.docx`
  mono existe). **Action Gad** : il est dans `Downloads` → le déposer pour tokenisation (neutralisé,
  jamais committé avec données réelles). Ce n'est pas une demande Rafael.

## Ajouts 2026-06-08 (sources épuisées — vraies questions de pratique)

> Modèle SELAS multi « Reynaud » = **RÉSOLU** (tokenisé/neutralisé, DOC-044 livré). Le seul élément
> « absent » du repo ne l'est plus.

Deux docs que le **canon liste comme systématiques** mais que je n'ai **pas** pu câbler sans ton
arbitrage de pratique (j'ai d'abord vérifié le code — ce ne sont pas des questions techniques) :

1. **SCM — pacte d'associés / contrat à frais communs / règlement intérieur / liste des dépenses
   communes.** Le canon les met dans le bundle SCM. **Question pratique** : les produit-on
   **systématiquement à la constitution** d'une SCM, ou sont-ce des actes **distincts / ultérieurs**
   (signés à part, pas dans le dossier de création) ? (Impact : on les met dans le dossier auto ou
   on les laisse en option.)
2. **SPFPL — note d'information.** Le canon la liste pour cession ET apport. Techniquement elle décrit
   l'**opération** (titres apportés/cédés, société cible). **Question pratique** : en création V1,
   recueille-t-on déjà les détails de l'opération pour produire la note, ou la note se fait-elle
   **après**, une fois l'opération réalisée ?

## À relayer à Rafael MAINTENANT
Une **rétractation** honnête (les docs sont là, mon erreur) — pas une nouvelle liste de demandes.
Les arbitrages ci-dessus partiront **groupés**, précis, une fois les modèles tokenisés.
