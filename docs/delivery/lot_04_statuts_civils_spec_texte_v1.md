# DAAT x SYDEL - SPEC TEXTE V1
## Famille `statuts civils` - SPEC-STATUTS-CIVILS-001

## 1. Objet

Stabiliser la specification texte V1 de la famille documentaire `statuts civils`, avant tout codage.

Cette spec complete la spec canonique :
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`

Elle couvre quatre sources :
- statuts SCS ;
- statuts SCI ;
- statuts SCI IRIS ;
- statuts SCM.

Objectif V1 :
- decrire la structure texte de chaque sous-famille ;
- distinguer les blocs communs et non fusionnables ;
- identifier les zones repetables d'associes ;
- signaler les blocs manuels ;
- documenter les points ouverts qui doivent bloquer tout codage automatique ambigu.

Cette spec n'est pas une reecriture des statuts. Le futur code devra reprendre le wording depuis les sources validees ou depuis une spec texte plus detaillee approuvee, sans harmonisation implicite.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_civils_spec_canonique_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources DOCX Lot 04 lues :
- `project/source_documents/lot_04/Statuts_SCS_modele.docx`
- `project/source_documents/lot_04/Modele statuts SCI.docx`
- `project/source_documents/lot_04/Modele statuts SCI IRIS.docx`
- `project/source_documents/lot_04/Statuts SCM.docx`

## 3. Decisions texte V1

### 3.1 Documents separes

La V1 conserve quatre textes canoniques distincts :
- `LOT04-STATUTS-SCS`
- `LOT04-STATUTS-SCI`
- `LOT04-STATUTS-SCI-IRIS`
- `LOT04-STATUTS-SCM`

Raison :
- la SCS repose sur des roles commandite / commanditaire absents des autres sources ;
- la SCI IRIS ajoute des blocs fiscaux et de resultat absents de la SCI simple ;
- la SCM a un objet de moyens et une logique professionnelle distincte ;
- les statuts sont des documents longs et sensibles, donc la similarite de structure ne suffit pas a fusionner.

### 3.2 Wording

Regle V1 :
- aucune correction de style, grammaire ou formulation juridique ne doit etre faite par le generateur ;
- les anomalies source doivent etre rendues telles quelles ou bloquer si elles rendent la generation incoherente ;
- les blocs communs peuvent etre mutualises techniquement seulement si le texte source exact est conserve par variante.

### 3.3 Repetition des associes

Regle V1 :
- les lignes d'associes, apports, parts et signatures doivent etre considerees comme repetables ;
- `personne_1`, `personne_2`, `personne_3` sont des aliases source, pas des roles metier ;
- les roles specifiques, notamment SCS et SCM, doivent piloter le rendu.

## 4. Structure texte SCS

Source :
- `project/source_documents/lot_04/Statuts_SCS_modele.docx`

Structure observee :
1. page de garde ;
2. comparution des associes ;
3. `TITRE I - FORME - OBJET - DENOMINATION - SIEGE - DUREE` ;
4. `ARTICLE 1 - Forme` ;
5. `ARTICLE 2 - Objet` ;
6. `ARTICLE 3 - Denomination sociale` ;
7. `ARTICLE 4 - Siege social` ;
8. `ARTICLE 5 - Duree` ;
9. `ARTICLE 6 - Apports` ;
10. `ARTICLE 7 - Capital social` ;
11. `ARTICLE 8 - Variabilite du capital` ;
12. `ARTICLE 9 - Modification du capital` ;
13. `ARTICLE 10 - Comptes courants` ;
14. `ARTICLE 11 - Representation des parts sociales` ;
15. `ARTICLE 12 - Indivisibilite des parts sociales` ;
16. `ARTICLE 13 - Droits et obligations des associes` ;
17. `ARTICLE 14 - Cession et transmissions des parts sociales` ;
18. `ARTICLE 15 - Faillite - Interdiction et Incapacite d'un associe` ;
19. `ARTICLE 16 - Nomination, revocation et demission des gerants` ;
20. `ARTICLE 17 - Gerant personne morale` ;
21. `ARTICLE 18 - Pouvoirs de la gerance` ;
22. `ARTICLE 19 - Remuneration de la gerance` ;
23. `ARTICLE 20 - Commissaires aux comptes` ;
24. `TITRE IV - DECISIONS COLLECTIVES` ;
25. articles decisions collectives, assemblee generale et consultation ecrite ;
26. titre exercice / comptes / affectation ;
27. dissolution / liquidation ;
28. dispositions diverses ;
29. pouvoirs et publicite ;
30. annexe.

Blocs texte propres :
- distinction des associes commandites et commanditaires ;
- responsabilite des commandites ;
- capital variable avec capital social maximal ;
- qualite associe commandite / commanditaire dans la repartition des parts ;
- gerance personne morale.

Zones repetables :
- associes commandites ;
- associes commanditaires ;
- eventuel associe personne morale dans la repartition du capital ;
- apports par role ;
- parts et plages de parts.

Elements manuels / sensibles :
- situation matrimoniale ;
- banque et adresse de banque ;
- qualite associe ;
- nombre d'exemplaires ;
- coherence entre commandite, commanditaire et repartition des parts.

## 5. Structure texte SCI

Source :
- `project/source_documents/lot_04/Modele statuts SCI.docx`

Structure observee :
1. page de garde ;
2. identification de trois associes physiques dans la source ;
3. `ARTICLE 1 - FORME` ;
4. `ARTICLE 2 - OBJET` ;
5. `ARTICLE 3 - DENOMINATION` ;
6. `ARTICLE 4 - SIEGE SOCIAL` ;
7. `ARTICLE 5 - DUREE` ;
8. `ARTICLE 6 - APPORTS` ;
9. `ARTICLE 7 - CAPITAL SOCIAL` ;
10. `ARTICLE 8 - MODIFICATIONS DU CAPITAL SOCIAL` ;
11. `ARTICLE 9 - AVANCES A LA SOCIETE` ;
12. `ARTICLE 10 - TITRES DES ASSOCIES` ;
13. `ARTICLE 11 - DROITS ATTACHES AUX PARTS` ;
14. `ARTICLE 12 - INDIVISIBILITE DES PARTS` ;
15. `ARTICLE 13 - REUNION DE TOUTES LES PARTS EN UNE SEULE MAIN` ;
16. `ARTICLE 14 - SCELLES` ;
17. `ARTICLE 15 - RESPONSABILITE DES ASSOCIES` ;
18. `ARTICLE 16 - DECES ET INCAPACITE D'UN ASSOCIE` ;
19. `ARTICLE 17 - RETRAIT D'UN ASSOCIE` ;
20. `ARTICLE 18 - CESSION DE PARTS` ;
21. `ARTICLE 19 - TRANSMISSION PAR DECES DES PARTS` ;
22. `ARTICLE 20 - TRANSMISSION PAR DECES OU EN SUITE DE LIQUIDATION DE COMMUNAUTE ENTRE EPOUX` ;
23. `ARTICLE 21 - ADMINISTRATION DE LA SOCIETE` ;
24. `ARTICLE 22 - POUVOIRS, OBLIGATIONS, REMUNERATION` ;
25. `ARTICLE 23 - RESPONSABILITE DES GERANTS` ;
26. `ARTICLE 24 - DECISIONS COLLECTIVES DES ASSOCIES` ;
27. `ARTICLE 25 - DROIT D'INFORMATION DES ASSOCIES` ;
28. `ARTICLE 26 - ASSEMBLEES GENERALES` ;
29. `ARTICLE 27 - CONSULTATIONS PAR CORRESPONDANCE` ;
30. `ARTICLE 28 - DECISION UNANIME DANS UN ACTE` ;
31. `ARTICLE 29 - ASSEMBLEE GENERALE ORDINAIRE` ;
32. `ARTICLE 30 - ASSEMBLEE GENERALE EXTRAORDINAIRE` ;
33. `ARTICLE 31 - EXERCICE SOCIAL` ;
34. `ARTICLE 32 - COMPTES SOCIAUX` ;
35. `ARTICLE 33 - AFFECTATION ET REPARTITION DES BENEFICES` ;
36. `ARTICLE 34 - DISSOLUTION, LIQUIDATION` ;
37. `ARTICLE 35 - CONTESTATIONS` ;
38. `ARTICLE 36 - JOUISSANCE DE LA PERSONNALITE MORALE, IMMATRICULATION AU REGISTRE DU COMMERCE ET DES SOCIETES` ;
39. `ARTICLE 37 - AUTORISATION D'ENGAGEMENTS` ;
40. `ARTICLE 38 - POUVOIRS, PUBLICITE` ;
41. signature ;
42. annexe des actes accomplis pour le compte de la societe en formation.

Blocs texte propres :
- mention `SCI` dans les actes et documents de la societe ;
- capital social variable avec capital autorise ;
- article 33 simple de distribution ou reserve du benefice ;
- absence d'article fiscal dedie.

Zones repetables :
- associes physiques ;
- apports par associe ;
- repartition des parts par associe ;
- signature par associe.

Elements manuels / sensibles :
- situations matrimoniales ;
- banque et adresse de banque ;
- date de cloture du premier exercice ;
- annexe des actes accomplis ;
- option IS hors statuts, par lettre separee.

## 6. Structure texte SCI IRIS

Source :
- `project/source_documents/lot_04/Modele statuts SCI IRIS.docx`

Structure observee :
- articles 1 a 37 proches de la SCI ;
- `ARTICLE 38 - DECLARATION FISCALE` ;
- `ARTICLE 39 - POUVOIRS, PUBLICITE` ;
- annexe finale.

Blocs communs avec SCI :
- forme ;
- objet immobilier ;
- denomination ;
- siege ;
- duree ;
- apports ;
- capital social ;
- modifications du capital ;
- gerance ;
- decisions collectives ;
- dissolution ;
- contestations ;
- autorisation d'engagements.

Blocs non fusionnables avec SCI :
- mention `SCI IRIS` dans les actes et documents emanant de la societe ;
- article 7 structure en `7.1 Repartition du capital` et `7.2 Variabilite du capital` ;
- presence d'une denomination d'associe personne morale dans la repartition du capital ;
- numerotation des parts par debut / fin ;
- article 33 de resultat distinguant resultat courant et resultat exceptionnel ;
- groupes de parts avec quote-part de resultat exceptionnel ;
- clauses de demembrement usufruit / nue-propriete liees au benefice exceptionnel ;
- article 38 de declaration fiscale.

Zones repetables :
- associes physiques ;
- associe personne morale ou bloc de denomination ;
- groupes de parts ;
- quotes-parts de resultat exceptionnel ;
- signatures.

Elements manuels / sensibles :
- groupes de parts ;
- quotes-parts de resultat exceptionnel ;
- declaration fiscale ;
- option IS hors statuts, par lettre separee ;
- coherence entre repartition du capital, groupes de parts et resultat exceptionnel.

## 7. Structure texte SCM

Source :
- `project/source_documents/lot_04/Statuts SCM.docx`

Structure observee :
1. page de garde ;
2. comparution d'une personne morale representee et d'une personne physique ;
3. `TITRE I` ;
4. `Article 1 - Forme` ;
5. `Article 2 - Denomination` ;
6. `Article 3 - Siege social` ;
7. `Article 4 - Objet social` ;
8. `Article 5 - Duree` ;
9. `TITRE II` ;
10. `Article 6 - Apports` ;
11. `Article 7 - Capital social` ;
12. `Article 8 - Augmentation du capital` ;
13. `Article 9 - Droits et obligations attaches aux parts sociales` ;
14. `Article 10 - Cession de parts entre vifs` ;
15. `Article 11 - Cession a titre gratuit` ;
16. `Article 12 - Retrait volontaire d'un associe` ;
17. `Article 13 - Cession apres deces` ;
18. `TITRE III ADMINISTRATION` ;
19. `Article 14 - Gerance` ;
20. `TITRE IV DECISIONS COLLECTIVES` ;
21. articles 15 a 18 sur assemblees, representation, quorum et majorite ;
22. `TITRE V COMPTES SOCIAUX` ;
23. articles 19 a 22 sur exercice, comptes, ressources et pertes ;
24. `TITRE VI PROROGATION-TRANSFORMATION - DISSOLUTION - LIQUIDATION` ;
25. articles 23 a 26 ;
26. `TITRE VII DIVERS` ;
27. articles 27 a 30, dont litiges, contre-lettre, domicile et communication du contrat.

Blocs texte propres :
- objet centre sur les moyens professionnels ;
- engagement de personnel auxiliaire et operations n'alterant pas le caractere civil ;
- redevance annuelle et appels de fonds ;
- ressources sociales et contribution aux pertes ;
- tentative de conciliation devant le President du Conseil departemental ;
- communication du contrat.

Zones repetables :
- associes personnes morales ;
- associes personnes physiques ;
- representants des personnes morales ;
- apports par associe ;
- parts par associe.

Elements manuels / sensibles :
- profession de la personne physique ;
- profession de la personne morale ;
- representant et fonction ;
- numero RCS et ville RCS de la personne morale ;
- situation matrimoniale ;
- banque et adresse de banque ;
- repartition des parts, avec anomalie source a arbitrer.

## 8. Blocs communs transverses

Blocs mutualisables seulement en structure :
- page de garde ;
- comparution ;
- forme ;
- denomination ;
- siege ;
- duree ;
- apports ;
- capital ;
- droits des associes ;
- cession / transmission ;
- gerance ou administration ;
- decisions collectives ;
- comptes ;
- dissolution / liquidation ;
- contestations ou litiges ;
- pouvoirs / publicite ;
- signature ;
- annexe.

Ces blocs ne sont pas mutualisables en texte sans comparaison ligne a ligne et validation juridique.

## 9. Blocs non fusionnables recapitulatifs

| Sous-famille | Blocs non fusionnables |
|---|---|
| SCS | commandites, commanditaires, capital maximal, responsabilite des commandites, gerance personne morale |
| SCI | article 33 simple, mention SCI, absence de declaration fiscale source, repartition du capital simple |
| SCI IRIS | declaration fiscale, resultat exceptionnel, groupes de parts, mention SCI IRIS, associe personne morale dans la repartition |
| SCM | objet de moyens, associes professionnels, ressources sociales, charges/redevances, conciliation ordinale |

## 10. Placeholders et rendu texte

Regle de rendu :
- les placeholders entre crochets ne doivent jamais etre rendus tels quels dans une sortie finalisee ;
- les champs manuels explicitement conserves doivent etre rendus comme zones a completer seulement si la spec de code le decide ;
- un champ sensible absent doit bloquer plutot que produire un texte incomplet.

Familles de placeholders :
- societe ;
- siege ;
- associes physiques ;
- associes personnes morales ;
- representants ;
- apports ;
- parts ;
- banque ;
- exercice ;
- fiscalite ;
- signature.

## 11. Criteres avant code

Avant tout ticket de code, il faudra disposer :
- d'une decision sur le nombre d'associes dynamiques supporte en V1 ;
- d'une decision sur les associes personnes morales dans SCI IRIS et SCM ;
- d'un arbitrage sur l'anomalie de repartition des parts SCM ;
- d'une strategie de reprise du texte long : source DOCX lue comme reference, ou spec texte article par article plus detaillee ;
- d'une decision sur les signatures dynamiques ;
- d'une decision sur le traitement `document finalise` vs `formulaire a completer` pour les champs manuels ;
- d'une spec separee pour la lettre option IS si elle entre dans le perimetre ;
- d'une spec separee pour les documents satellites SCM si ces documents entrent dans le perimetre.

## 12. Points ouverts

- SCI et SCI IRIS sont proches mais juridiquement non fusionnees en V1.
- SCI IRIS contient des clauses de resultat exceptionnel et de declaration fiscale a valider humainement avant code.
- SCM contient une anomalie de placeholder sur la repartition des parts : le meme placeholder de parts personne physique apparait pour deux lignes de repartition.
- SCS contient des roles commandite / commanditaire qui ne doivent pas etre deduits du rang de l'associe.
- Les situations matrimoniales restent des textes sensibles a fournir explicitement.
- Les documents satellites SCM et la lettre option IS restent hors automatisation dans cette spec.
- La validation juridique fine du wording source reste requise avant implementation.
