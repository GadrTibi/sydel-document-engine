# Pack de passation — Boucle NotebookLM SELAS (points juridiques ouverts)

**Pour :** le Capitaine (Gad) → à transmettre à **Rafael** (associé) pour arbitrage
**Par :** le Second (Claude de Naomie), à partir des réponses NotebookLM rapportées par le Mousse
**Date :** 2026-06-05
**Périmètre :** SELAS médecin, V1 (actionnaire unique). Source = NotebookLM (matière exploratoire, **non
opposable**, citations rares). Le Mousse n'a **rien tranché ni reformulé** ; réponses brutes archivées
dans `naomie/worklog/WORKLOG.md` (section « Boucle NotebookLM »).

---

## 1. Ce qui a été fait
Boucle NotebookLM complète sur les **6 questions** validées dans la passation Capitaine du 2026-06-04.
1 question à la fois, réponse brute collée par Naomie, structurée par le Second. **6/6 traitées.**

## 2. Résultats — synthèse exploitable (à valider par Rafael)

| # | Question | Réponse NotebookLM | Statut sourcing |
|---|---|---|---|
| Q1 | Président / Présidente au féminin ? | **Le titre s'adapte à la personne → « Présidente » pour une femme.** Genre = donnée obligatoire ; automatiser le féminin (anti-coquilles). | Pas de source précise |
| Q2 | « actionnaire » vs « associé » ? | **« associé » pour les personnes** ; **« parts sociales » → « actions »** dans tout le capital/financier. Carte par article proposée (numéros **non vérifiés**). | Réfs = log interne |
| Q3 | Plans/devis Ordre : bloquants ? | **OUI, bloquants** : sans eux la commission ordinale peut refuser l'attestation → +1 mois. Le moteur doit les exiger avant envoi Ordre. | Pas de source précise |
| Q4 | Attestation dépôt capital obligatoire ? | **OUI, obligatoire** + liste des souscripteurs (répartition / nombre d'actions). | **Source nommée** : « Besoins Sydel (juridique).pdf » (interne) |
| Q5 | Médecin : questionnaire Ordre ? | **OUI pour le médecin ; NON pour le dentiste.** Pièce conditionnelle pilotée par la profession (idem vétérinaires, kinés, sages-femmes, infirmiers). | Verbatim transcription |
| Q6 | Numérotation actions « 1 à N » ? | **Suffit pour la V1 simple.** Précisions (dissociation droits vote/financiers, actions de préférence, démembrement) = **hors V1**, déjà bloquées par les garde-fous code. Pas de numérotation alphanumérique spéciale. | Pas de source précise |

## 3. Impacts moteur identifiés (sous réserve de validation Rafael)
- **Genre obligatoire** (Q1) : champ déjà prévu au schéma ; prévoir une **table d'accords** (pas de
  substitution globale de chaînes — risque connu). Wording féminin exact **à confirmer**.
- **Lexique associé/actions** (Q2) : règle « associé = personnes / actions = capital » ; **carte par article
  à recroiser sur les statuts DOCX réels**.
- **2 pièces à AJOUTER aux exigences du pack V1** : **plans/devis Ordre** (Q3, bloquants) et **attestation
  de dépôt de capital + liste des souscripteurs** (Q4). → lèvent les **2 points “forts”** de l'audit.
- **Pièce conditionnelle par profession** (Q5) : « questionnaire Ordre » présent pour médecin, absent pour
  dentiste.
- **Numérotation actions V1** (Q6) : « 1 à N » OK ; cas avancés restent hors périmètre.

## 4. À VALIDER PAR LE CAPITAINE / RAFAEL (terre ferme — hors du Mousse)
Points qui exigent un arbitrage humain avant d'en faire des règles dures du moteur :
- **a.** Wording féminin exact (liste des termes à accorder au-delà de « Présidente »).
- **b.** Carte « associé vs actions » par article, validée sur les vrais statuts.
- **c.** Confirmer plans/devis + attestation capital comme pièces **bloquantes/obligatoires** du pack V1.
- **d.** Fournir / valider le **modèle exact du questionnaire Ordre médecin**.

### Points « non trouvés » par NotebookLM → directs chez Rafael (ne pas relancer NotebookLM)
Hérités de la passation Capitaine :
- Filiation dans la **DNC** du président.
- **Titre exact** de la lettre de renonciation du conjoint (régime communautaire).
- Nomination du Président **dans les statuts** vs **acte séparé**.

Nouveaux, surgis en Q6 (tous **hors V1** ou non sourcés) :
- Démembrement nu-propriété / usufruit dès la V1 ?
- Seuils de blocage / majorité par défaut. *(non trouvé)*
- Clause d'agrément des héritiers par défaut. *(non trouvé)*
- Mention de libération partielle du capital (1/2, 1/4). *(non trouvé)*
- Apports en industrie vs numéraire seul en V1. *(non trouvé)*

## 5. À déployer / merger
**Rien par le Mousse.** Aucune génération SELAS activée. Tout merge/déploiement = Capitaine.

## 6. Reste à faire (après arbitrage Rafael)
- Intégrer les décisions validées dans les specs (pièces obligatoires, lexique, accords) — **côté Second/Gad**.
- Le correctif technique des 2 DOCX SCI dupliqués reste **côté Second de Gad** (non lié à cette boucle).
- Génération documentaire SELAS : **NO-GO** jusqu'à validation Rafael des points ci-dessus.

---
*Archive des réponses brutes + versions structurées : `naomie/worklog/WORKLOG.md`, section « Boucle
NotebookLM — points juridiques ouverts SELAS ».*
</content>
