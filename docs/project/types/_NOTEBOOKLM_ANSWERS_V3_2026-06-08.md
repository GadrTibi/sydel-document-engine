# Réponses NotebookLM V3 — 2026-06-08 (collées par Gad en session)

> Lecture du Second. Verbatim brut = message Gad du 2026-06-08 (transcript de session).
> **Cadre d'autocritique :** ces questions visaient une couche **usage/conseil/extension**, PAS la
> construction des générateurs (faite depuis les modèles tokenisés + le canon). Résultat confirmé
> ci-dessous : **aucune réponse ne change ce qui est construit ni ne révèle une construction à
> l'aveugle** — elles confirment, ou disent « pas dans les sources ». Cf. [[feedback-no-useless-action-on-request]].

## SAS (SPFPLAS)
- **Déjà su / confirmé :** SPFPL = uniquement SPFPLAS ; holding créée APRÈS la SEL (apport/cession des
  parts) ; commissaire aux apports obligatoire en parcours apport ; protection du conjoint comme SELARL ;
  genre = personnalisation manuelle ; souvent associé unique. (Tout déjà dans les synthèses / modèles.)
- **NOUVEAU actionnable :** la forme par actions n'est **pas réservée aux médecins** → ouverte
  **dentistes, orthodontistes, kinés, infirmiers, sages-femmes, vétérinaires**. ⚠️ = item de **périmètre
  (Gad)** : le V1 SAS est bâti sur le modèle **médecin** ; élargir = décision produit, pas un bug.
- **Pas dans les sources → Rafael (non bloquant) :** durée société / durée mandat président / figement
  de l'absence de rémunération président.
- **Impact build V1 : nul** (confirme le périmètre médecin actuel).

## SCS
- **Déjà su / confirmé :** montage investisseur (SPFPL commanditaire) + gestionnaire (praticien) pour
  immobilier ; répartition décidée par le cabinet ; décorrélation droits vote/financiers possible ;
  PM (SPFPL) peut être **commanditaire**.
- **Pas dans les sources (NON TROUVÉ, les ex-11/12/13 visés) → Rafael :** autres situations de montage ;
  pièges ; règle de plancher/type de parts commandité ; obligation de majorité des droits de vote au
  gestionnaire ; **plusieurs** commanditaires/commandités ; **PM commanditée** + qualité de commerçant.
- **Impact build V1 : nul** (le multi SCS reste à trancher par Rafael, comme déjà noté).

## SELAS
- **Déjà su / confirmé :** articulation SPFPL/SCM/SCI ; non-exerçant ≤ 25 % (SEL médicale) ; majorité
  des droits de vote aux exerçants ; état annuel du capital à l'Ordre ; pièges = erreurs de **saisie
  manuelle** (que le moteur déterministe élimine déjà) ; féminisation pilotée par civilité/sexe.
- **NOUVEAU (couche conseil) :** l'Ordre peut **bloquer l'immatriculation** faute de plans de locaux /
  devis de travaux (1ʳᵉ installation). Utile si on bâtit un jour une couche d'aiguillage ; pas le moteur.
- **Pas dans les sources → Rafael :** critères concrets SELAS vs SELARL ; forme féminisée « Directrice
  Générale ».
- **Impact build V1 : nul.**

## SPFPL
- **Déjà su / confirmé :** cession = numéraire (~1000 € + banque) ; apport = nature (capital élevé +
  contrat d'apport, pas de banque) ; commissaire aux apports en parcours apport ; non-exerçant ≤ 25 % ;
  Ordre statue ~1×/mois, exige les projets d'actes, bloque si pièces manquantes.
- **Pas dans les sources → Rafael (non bloquant) :** conditions du report **150-0 B ter** ; qui désigne
  le commissaire / cas de dispense ; critères fins cession vs apport.
- **Impact build V1 : nul** (mécanique apport/cession déjà portée par les modèles + parcours codés).

## Bilan transverse
- **Rien ne change le build.** Un seul vrai nouveau actionnable = **SAS ouverte à d'autres professions**
  (= décision de périmètre Gad, pas un correctif).
- **Gaps → Rafael, NON bloquants** (couche conseil/fiscal, pas le générateur) : SELAS-vs-SELARL critères,
  150-0 B ter, désignation/dispense commissaire, résiduel multi SCS, durée/mandat/rémunération président SAS.
- **Aucune nouvelle question NotebookLM nécessaire** n'émerge de ces réponses.
