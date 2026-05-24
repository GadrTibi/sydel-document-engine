# Rapport executif - GLOBAL-HUMAN-ANSWERS-INTEGRATION-001

## Objet

Integrer les reponses humaines deja obtenues, notamment la reponse d'Albane et le modele SELAS medecin avec micro-holding, dans l'audit global des variables afin de geler un registre canonique global V2.1.

Ce ticket est documentaire uniquement : aucun generateur, moteur DOCX/PDF/ZIP, UI ou wording juridique n'a ete modifie.

## Etat Git initial

- Branche initiale : `main`.
- `main` etait en avance de 2 commits sur `origin/main`.
- Fichiers non suivis initiaux : `docs/docssource_truth/`, `project/source_truth/albane_reponse_mail_selarl_v1.md`, `project/source_truth/modele Statuts SELAS avec MH.docx`.
- Source attendue sous nom normalise absente : `project/source_truth/modele_statuts_selas_medecin_micro_holding_v1.docx`.

## Questions V1 fermees

Questions V1 fermees par la reponse d'Albane : 4 sur 10.

| Question V1 | Decision integree |
|---|---|
| Q-001 - Ontologie des roles personne | Roles explicites ; aucune fusion silencieuse. |
| Q-002 - Adresses et formes affichees/decomposees | Trois adresses pivots : domicile praticien, lieu d'exercice/cabinet, siege social. |
| Q-003 - Domiciliation versus siege social | Domiciliation = siege social. |
| Q-004 - Roles de cession et societes d'operation | Dans le SELARL standard : vendeur/cedant = praticien BNC ; acquereur/cessionnaire = SEL en constitution. |

## Questions restantes

Questions encore ouvertes mais arbitrables en interne : 5.

- Q-005 : ordre professionnel et identifiants par inscrit.
- Q-006 : capital, titres, apports, prix et calculs proposes.
- Q-007 : signataire, mandataire et representant, notamment par document.
- Q-008 : dates homonymes.
- Q-010 : champs tiers et constantes locales.

Question basculee en backlog documentaire futur : 1.

- Q-009 : variables spec-only et template-only a traiter par famille documentaire.

## Decisions integrees dans le registre V2.1

- Creation de `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V2.md`.
- Creation de `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`.
- Integration de la reponse d'Albane comme arbitrage documentaire/metier prioritaire pour les sujets qu'elle ferme explicitement.
- Conservation du principe V2 : pas de fusion silencieuse et reutilisation seulement via role, option ou contexte documente.

## Nouvelles regles canoniques d'adresse

- `personne.praticien.adresse_domicile` : domicile du praticien.
- `exercice.lieu_principal.adresse` : lieu d'exercice / cabinet.
- `societe.{role}.siege.adresse` : siege social de la societe rolee.
- `domiciliation.adresse` = `societe.principale.siege.adresse`.
- `societe.principale.siege.adresse` = `exercice.lieu_principal.adresse` seulement via option explicite.
- `scm.adresse` = `exercice.lieu_principal.adresse` pour le cas standard.
- `scm_cedee.siege.adresse` n'est pas automatiquement egale a `scm_cession.cessionnaire.siege.adresse`.

## Nouvelles regles canoniques de parties

- Vendeur / cedant du fonds liberal : praticien personne physique exercant en BNC.
- Acquereur du fonds liberal : SEL en constitution.
- Cedant des parts de SCM : praticien personne physique exercant en BNC.
- Cessionnaire des parts de SCM : SEL en constitution.
- Bailleur : role propre au bail, non reutilise ailleurs sans option.
- Locataire : pas toujours SELARL en constitution ; le paragraphe varie selon presence d'une SCM et reste a traiter dans un ticket bail/cession.

## Cas futur SELAS + micro-holding

Le modele `project/source_truth/modele Statuts SELAS avec MH.docx` confirme un cas distinct :

- SELAS medecin, pas SELARL standard ;
- associe personne morale de type societe civile micro-holding, pas SPFPL selon Albane ;
- representant personne physique de la societe civile ;
- sujets propres : actions, actions de preference, droits financiers/droits de vote, representation de personne morale.

Decision : cas futur hors perimetre immediat, a traiter dans un ticket separe avant toute implementation.

## Contradictions documentees mais non implementees

| Sujet | Source humaine/client | Arbitrage produit interne | Suite |
|---|---|---|---|
| Filigrane PROJET | Albane applique un filigrane projet tant que la SEL n'est pas immatriculee. | Pas de mode Projet / filigrane en V1. | Contradiction documentee, non implementee. |
| Mode Projet | NotebookLM presente le mode Projet comme utile pour banque/Ordre. | Arbitrage interne precedent : exclu V1. | Ticket produit separe requis si decision contraire. |
| Adresses souvent identiques | Albane indique que tout est souvent centralise au cabinet. | Le registre conserve les roles d'adresse et impose des options explicites. | Pas de copie implicite globale. |
| Locataire du bail | Albane indique une variation selon SCM et suggere un champ libre possible. | Aucun changement moteur/documentaire dans ce ticket. | Backlog bail/cession. |

## Recommandation front

Oui, le registre canonique global V2.1 est suffisamment stable pour lancer l'architecture du nouveau front global.

Perimetre recommande : architecture de donnees, objets roles, adresses rolees, reutilisations explicites et mapping des blocs. Ne pas lancer encore de modification des generateurs, du wording juridique, du filigrane Projet ou d'un nouveau document SELAS + micro-holding sans ticket dedie.

## Validations

- Relecture documentaire des sources et du diff.
- Aucun test Python execute : aucun fichier Python modifie.

## Prochaine etape recommandee

Lancer `GLOBAL-FRONT-ARCHITECTURE-001` : concevoir l'architecture du nouveau front sur le registre V2.1, sans modifier le moteur documentaire ni les generateurs.
