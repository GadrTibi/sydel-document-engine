# Questions humaines ouvertes - variables globales V1

Objectif : reduire au minimum les arbitrages humains avant de figer le registre canonique global V2. Les questions ci-dessous regroupent les ambiguites par famille metier et evitent les comparaisons pairwise inutiles.

## Q-001 - Ontologie des roles personne
- Variables concernees : nom/prenom/civilite/genre/date_naissance pour personne_1, personne_2, associe, signataire, dirigeant, president, actionnaire_unique, mandataire, conjoint
- Pourquoi il y a ambiguite : Les templates legacy utilisent des index personne_n tandis que les specs recentes utilisent des roles metier. Fusionner par proximite casserait les cas multi-personnes.
- Choix possibles :
  - A - Creer une fiche Personne reutilisable puis l assigner a des roles explicites.
  - B - Garder un formulaire separe par role meme si des donnees se repetent.
  - C - Hybride: fiche Personne + verrouillage des roles sensibles.
- Recommandation Codex : C - fiche Personne globale, mais aucune reutilisation automatique hors regle explicite.
- Reponse attendue : A / B / C / libre

## Q-002 - Adresses et formes affichees/decomposees
- Variables concernees : adresse_siege, societe_siege_*, domiciliation_adresse_affichee, adresse_personnelle_*, adresse_cabinet, adresse_lieu_exercice, site_declare_adresse_affichee
- Pourquoi il y a ambiguite : Les adresses ont des formes affichees et des composants; les lieux siege, domiciliation, cabinet, exercice et personne peuvent etre identiques ou differents selon le dossier.
- Choix possibles :
  - A - Stocker chaque adresse par role et deriver l affiche.
  - B - Un champ adresse global reutilisable partout.
  - C - Adresse par role avec bouton explicite identique a.
- Recommandation Codex : C - adresse par role + reutilisation explicite, jamais implicite.
- Reponse attendue : A / B / C / libre

## Q-003 - Domiciliation versus siege social
- Variables concernees : domiciliation_adresse_affichee, domiciliation_adresse_domiciliation_affichee, adresse_siege, societe_siege_adresse_affichee
- Pourquoi il y a ambiguite : Le DOC-002 et le Lot 1 ont historiquement une adresse de domiciliation proche du siege, mais la source canonique V1 demande prudence.
- Choix possibles :
  - A - Domiciliation toujours egale au siege.
  - B - Domiciliation separee.
  - C - Separee avec option explicite domiciliation = siege.
- Recommandation Codex : C - option explicite, valeur derivee seulement si cochee.
- Reponse attendue : A / B / C / libre

## Q-004 - Roles de cession et societes d operation
- Variables concernees : cedant/vendeur/acquereur/cessionnaire/apporteur/societe_cible/societe_cedee/societe_apportee/societe_spfpl
- Pourquoi il y a ambiguite : Les memes mots recouvrent des parties differentes selon cession cabinet, cession parts, apport, SPFPL et SCM.
- Choix possibles :
  - A - Uniformiser cedant/vendeur et acquereur/cessionnaire.
  - B - Garder tous les roles distincts.
  - C - Table de roles operationnels avec equivalences par type operation.
- Recommandation Codex : C - roles distincts + equivalences par type operation valide.
- Reponse attendue : A / B / C / libre

## Q-005 - Identifiants ordre et profession
- Variables concernees : numero_rpps, ordre_numero_rpps, numero_ordre, ordre_departemental, departement_ordre, societe_inscription_ordre_*
- Pourquoi il y a ambiguite : Le numero peut appartenir a une personne ou a une societe inscrite; le departement ordinal peut ressembler a un departement de naissance.
- Choix possibles :
  - A - Un bloc Ordre unique par dossier.
  - B - Un bloc Ordre par personne/societe inscrite.
  - C - Bloc Ordre role par inscrit avec selection de profession.
- Recommandation Codex : C - bloc Ordre role par inscrit.
- Reponse attendue : A / B / C / libre

## Q-006 - Capital, titres, apports et prix
- Variables concernees : capital_social, nb_parts, nb_actions, valeur_nominale, apport_*, cession_parts_*, cession_actions_*, prix_*
- Pourquoi il y a ambiguite : Les montants peuvent etre lies par calcul mais representent souvent des instants ou entites differentes: capital, souscription, apport, cession, prix unitaire/total.
- Choix possibles :
  - A - Deriver tout ce qui est calculable automatiquement.
  - B - Demander chaque montant/document separement.
  - C - Structure operationnelle avec calculs proposes mais modifiables.
- Recommandation Codex : C - calculs controles, source conservable et overrides explicites.
- Reponse attendue : A / B / C / libre

## Q-007 - Signataire, mandataire et representant
- Variables concernees : signataire_*, document_signataire_*, mandataire_*, representant_*, dirigeant_nomine_*
- Pourquoi il y a ambiguite : Un mandataire ou representant peut signer certains documents mais ce n est pas vrai par defaut.
- Choix possibles :
  - A - Un champ signataire global.
  - B - Signataire par document uniquement.
  - C - Fiche personne + role signataire par document avec preselection explicite.
- Recommandation Codex : C - preselection explicite, signataire par document/lot.
- Reponse attendue : A / B / C / libre

## Q-008 - Dates homonymes
- Variables concernees : date_signature, date_decision, date_pv, date_bail, date_effet_contrat, date_entree_jouissance, date_realisation_limite
- Pourquoi il y a ambiguite : Les dates proches lexicalement correspondent a des evenements juridiques differents.
- Choix possibles :
  - A - Date dossier unique par defaut.
  - B - Toutes les dates distinctes.
  - C - Date dossier proposee en prefill mais chaque evenement reste modifiable.
- Recommandation Codex : C - prefill possible, stockage distinct par evenement.
- Reponse attendue : A / B / C / libre

## Q-009 - Variables spec-only et template-only
- Variables concernees : 708 slugs seulement spec_delivery; 411 slugs template_docx sans code_mapping V1
- Pourquoi il y a ambiguite : Certaines variables peuvent etre des hypotheses de spec, des derives, ou des placeholders template non branches.
- Choix possibles :
  - A - Les inclure toutes dans le front V2.
  - B - Les exclure tant qu elles ne sont pas confirmees par template et mapping.
  - C - Les classer en backlog de verification document par document.
- Recommandation Codex : C - verification par famille avant schema UI final.
- Reponse attendue : A / B / C / libre

## Q-010 - Champs tiers et constantes locales
- Variables concernees : banque_*, depot_fonds_*, impots_*, service_enregistrement_*, prestataire_signature_electronique
- Pourquoi il y a ambiguite : Certains champs peuvent relever du parametrage cabinet/SYDEL plutot que du dossier client.
- Choix possibles :
  - A - Les demander au front dossier.
  - B - Les sortir en parametrage global.
  - C - Parametrage global avec override dossier.
- Recommandation Codex : C - parametrage global avec override documente.
- Reponse attendue : A / B / C / libre

