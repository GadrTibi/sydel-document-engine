# Ticket — Retours fonctionnels par cas — sociétés unipersonnelles, SPFPL par cession de dentiste et documents associés

> VERBATIM CLIENT (Albane/équipe juridique), reçu Gad 2026-07-06. Spec = ce texte.

## 1. Toutes sociétés unipersonnelles — supprimer le montant d'apport de l'associé unique
Supprimer le champ montant d'apport de l'associé unique ; reprendre auto le capital social comme apport ; pas de double saisie.

## 2. Créations de société (tous modèles sauf exceptions) — plages de numérotation parts/actions
Supprimer les champs de plages quand non utilisés dans les modèles ; conserver seulement où utile (SELAS pluripersonnelle, éventuellement SCM) ; si plage non complétée, pas de phrase incomplète dans les docs.

## 3. Tous formulaires greffe/RCS — BONUS déduction auto du greffe/RCS depuis la ville du siège
Proposer auto le greffe compétent depuis la ville du siège ; champ modifiable ; si trop complexe, garder l'existant.

## 4. Tous questionnaires longs — BONUS lisibilité
Mieux séparer visuellement : infos associé / société créée / société cible / société achetée (titres, séparateurs, encadrés, accordéons, blocs repliables, fond/bordure par catégorie).

## 5. Tous formulaires personne physique — Prénom vs Prénoms complets
« Prénom » = usuel (docs courants) ; « Prénoms complets » = tous les prénoms, uniquement où juridiquement nécessaire (DNC). Actuellement « Prénoms complets » repris partout = incorrect. Renommer si besoin : « Tous les prénoms figurant à l'état civil ».

## 6. SPFPL cession dentiste — questionnaire
- 6.1 Case « Même adresse que le siège de la SPFPL » pour l'adresse société cible (reprise auto, modifiable).
- 6.2 Libellé « Société cible (SEL) ».
- 6.3 Nom du conjoint/partenaire (marié OU pacsé) : ajouter champs nom + prénom conjoint ; repris dans les docs ; pas de mention PACS/mariage sans nom.
- 6.4 BONUS import Kbis société cible (dénomination/siège/capital/RCS/SIREN…).
- 6.5 Profession société cible préremplie par défaut = profession du formulaire (ex. chirurgien-dentiste), modifiable.
- 6.6 Champ « Profession » dans l'identité de l'associé unique (absent, mais repris dans les statuts). Défaut « chirurgien-dentiste », modifiable (orthodontistes possibles ; « chirurgien-dentiste » reste pour les mentions ordinales). Repris correctement dans les statuts.
- 6.7 Doublon adresse société cible (apparaît 2×) → un seul bloc adresse, réutilisé partout.
- 6.8 Nom de la société dans le titre des statuts : « Statuts [Nom de la société] » (comme d'autres).

## 7. SPFPL cession dentiste — statuts
- 7.1 Utiliser « Prénom » (pas « Prénoms complets ») dans les statuts.
- 7.2 Chaque élément de la liste du soussigné commence par une MAJUSCULE.
- 7.3 Régime PACS/mariage : afficher le régime + le nom du conjoint/partenaire si renseigné (saisie possible).
- 7.4 Département de l'Ordre : NOM du département, pas le numéro (« Seine-et-Marne » pas « 77 »). La variable renvoie au mauvais champ.
- 7.5 Article 8 valeur nominale : « Il est divisé en X actions de 0,01 (0,01) » → manque « euro(s) » ; montant en LETTRES avant, CHIFFRES entre parenthèses. Ex. « X actions de un euro (1 €) chacune » ou « de un centime d'euro (0,01 €) chacune ».
- 7.6 Annexe : supprimer les cadres multiples inutiles ; liste simple et lisible.

## 8. SPFPL cession dentiste — note d'information
- 8.1 Reprendre la mise en forme selon le modèle d'origine (lisible).
- 8.2 Variable « il prévoit d'acquérir X parts » renvoie au mauvais champ (nb actions SPFPL au lieu des parts cédées à la holding). Utiliser « parts cédées à la holding » ; renommer le libellé « parts cédées au holding » → « parts cédées à la holding ».

## 9. SPFPL cession dentiste — demande d'inscription à l'Ordre
- 9.1 Mise en forme VALIDÉE (rien à faire).
- 9.2 Destinataire : NOM du département (« Seine-et-Marne » pas « 77 »).
- 9.3 Choix « de / du / des » avant le département (ex. de Seine-et-Marne / du Jura / des Bouches-du-Rhône).
- 9.4 Clarifier « Département Ordre » et « Conseil départemental » : supprimer « Conseil départemental » si inutile ; garder un champ « Département de l'Ordre — nom du département, ex. Seine-et-Marne ».

## 10. SPFPL cession dentiste — autorisation de domiciliation
VALIDÉE, ne pas modifier.

## 11. SPFPL cession dentiste — attestation sur le capital
MANQUANTE dans le parcours → l'ajouter (générée dans le dossier).

## 12. SPFPL cession dentiste — acte de cession
- 12.1 Mise en forme quasi illisible → reprendre complètement (proche du modèle d'origine) AVANT de traiter les variables.
- 12.2 Identité société acquéreur (SPFPL en cours de constitution) : forme complète « Société de Participations Financières de Profession Libérale de Chirurgiens-Dentistes par actions simplifiée » + « immatriculée au RCS de [ville] sous le numéro en cours ». 2e ligne actuelle « par action simplifié » incorrecte. Pas de « en cours » isolé/incorrect.
- 12.3 Capital divisé en X parts de [valeur nominale] : manque « euro(s) ».
- 12.4 Inscription Ordre : préposition de/du/des (ex. « du » au lieu de « de »).
- 12.5 Répartition capital : si SPFPL détient 0 part, supprimer entièrement la ligne ; la répartition semble apparaître 2× → supprimer le doublon.
- 12.6 Prix de cession : « Prix de cession de un euros » → « un euro » singulier ; montant global inverse les parenthèses (lettres puis chiffres entre parenthèses). Ex. « un euro (1 €) ».
- 12.7 Paiement : « Le prix est payé au moyen d'un chèque ou virement. » (supprimer « par le moyen »).

## 13. SPFPL cession dentiste — PV
Première résolution affiche la plage des parts (« numérotées de ... inclus ») même non renseignée. Si non complétée → supprimer entièrement la mention ; pas de phrase incomplète.

## 14. Critères d'acceptation globaux (18)
1. Unipersonnelles : champs apport associé unique supprimés.
2. Créations : plages parts/actions demandées seulement si utiles.
3. Personne physique : prénom principal dans docs courants.
4. Personne physique : prénoms complets réservés aux docs qui les nécessitent.
5. SPFPL cession dentiste : plus de doublon d'adresse.
6. SPFPL cession dentiste : « Société cible (SEL) » clarifié.
7. SPFPL cession dentiste : nom conjoint/partenaire saisissable + repris.
8. SPFPL cession dentiste : profession associé unique préremplie mais modifiable.
9. SPFPL cession dentiste : société cible reprend par défaut la profession.
10. Statuts SPFPL cession dentiste : bonnes variables prénom/conjoint/Ordre/valeur nominale/annexe.
11. Note d'info : bonne variable « parts cédées à la holding ».
12. Demande Ordre : nom du département, pas le numéro.
13. SPFPL cession dentiste : choix de/du/des disponibles + repris.
14. SPFPL cession dentiste : attestation sur le capital générée.
15. Acte de cession : remis en forme + corrigé sur variables principales.
16. Acte de cession : lignes à 0 part supprimées.
17. Docs : montants harmonisés (lettres puis chiffres entre parenthèses).
18. PV SPFPL cession dentiste : plage de parts supprimée si non renseignée.
