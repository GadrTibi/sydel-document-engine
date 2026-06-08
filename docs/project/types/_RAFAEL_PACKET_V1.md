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

1. **SCM — satellites.** ✅ **Rafael a tranché 2026-06-08** : pacte / liste dépenses / contrat frais
   communs / RI **font partie du dossier SCM** (le canon l'emporte sur la note NotebookLM « opérations
   distinctes »). **FAIT** : pacte d'associés (DOC-026) + liste des dépenses communes (DOC-030) **câblés**
   (SCM à 2 associés, générés propres). **Restent ces points pour finir** :
   - **Pacte — n° RCS de la SCM** : le pacte imprime « immatriculée au RCS … sous le n° … » mais la SCM
     n'a **pas encore de n° RCS** le jour de la constitution. J'ai mis un **champ libre** (défaut « en
     cours d'immatriculation »). **Confirme le wording exact** de la mention, ou le pacte se signe-t-il
     **après** immatriculation (vrai n°) ?
   - **Règle des 2 associés** : le pacte ET la liste des dépenses exigent **exactement 2 associés** (les
     modèles sont bâtis pour 2). **Une SCM peut-elle en avoir 1 ou 3+ ?** Si oui, il faut généraliser les
     modèles (aujourd'hui : satellites générés **seulement si 2 associés**).
   - **Wording « chirurgien-dentiste / cabinet dentaire »** figé dans le pacte (verbatim du modèle) :
     OK pour **toute** SCM (médecin…) ou spécifique dentaire ?
   - **Contrat frais communs (DOC-027) + RI (DOC-028) — PAS encore câblés** : ils décrivent un accord
     entre les **sociétés d'exercice des praticiens** (chaque membre via sa **propre SEL**) + leurs
     **locaux**. Confirme : c'est bien **entre les SEL** (et non les personnes) ? Et **collecte-t-on
     l'identité de ces 2 SEL** (dénomination, RCS, représentant) **à la création de la SCM** ? Dès ta
     confirmation, je câble ces 2 derniers.
2. **SPFPL — note d'information.** Le canon la liste pour cession ET apport. Techniquement elle décrit
   l'**opération** (titres apportés/cédés, société cible). **Question pratique** : en création V1,
   recueille-t-on déjà les détails de l'opération pour produire la note, ou la note se fait-elle
   **après**, une fois l'opération réalisée ?
3. **SAS + SELAS — « parts sociales » / « gérant » dans des modèles en actions/Président.** Vérifié :
   le wording est **identique modèle source ↔ généré** (le moteur est donc fidèle, il ne l'invente
   pas). Les modèles SAS et SELAS multi contiennent, mot pour mot :
   - Art. 4 (siège) : « … que par décision d'un ou plusieurs associés représentant plus de la moitié
     des **parts sociales** ou par décision du **gérant** seul. »
   - SELAS Art. 23 : « S'il décide de conserver ses **parts sociales** … La mesure lui est notifiée
     par le **gérant** … » + rachat des **parts sociales**.
   Or une SAS/SELAS est en **actions** avec un **Président** (pas de parts sociales ni de gérant).
   **Question** : ces modèles ont-ils été adaptés d'un modèle SEL/civil sans corriger ces clauses
   (à corriger dans le `.docx` source : actions / Président), ou est-ce voulu ? Je **ne corrige pas
   une formulation juridique en douce** — je te le remonte.

## À relayer à Rafael MAINTENANT
Une **rétractation** honnête (les docs sont là, mon erreur) — pas une nouvelle liste de demandes.
Les arbitrages ci-dessus partiront **groupés**, précis, une fois les modèles tokenisés.
