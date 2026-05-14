# DAAT x SYDEL - ARBITRAGES V1
## Batch SPFPL specifique

Ticket : `ARBITRAGE-SPFPL-001`

## 1. Objet

Fermer les arbitrages principaux du batch SPFPL specifique avant tout ticket de code.

Ce fichier complete :
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`

Ce fichier ne code rien, ne modifie aucun wording source dans un document de production et ne modifie aucun fichier de pilotage projet.

## 2. Sources relues

Memoire projet :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`

Specs SPFPL :
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

## 3. Synthese des arbitrages

| Point | Decision V1 | Classement |
|---|---|---|
| Wording cession vs apport | Le type d'operation pilote un wording unique. La double formule source cession/apport ne doit jamais etre rendue telle quelle. | tranche |
| PV d'agrement classes cession mais rediges en apport | Les PV du chemin `SPFPL_CESSION` sont des PV d'agrement de cession. Le vocabulaire d'apport observe dans les sources est un ecart source a corriger uniquement dans le cadre de cet arbitrage documente. | tranche |
| Commissaire aux apports | Le role canonique est `commissaire_aux_apports`, pas commissaire aux comptes. Un seul commissaire selectionne doit etre fourni. | tranche |
| Donnees commissaire / evaluateur | La selection et les informations du commissaire et de l'evaluateur restent fournies manuellement dans le contexte dossier V1 ou par un referentiel valide ulterieurement. | manuel V1 |
| Liste dynamique des souscripteurs | L'automatisation V1 de l'attestation capital SPFPL est limitee a un actionnaire unique. Plusieurs souscripteurs restent hors automatisation V1. | manuel V1 |
| Acte de cession d'actions absent | Le document reste inventorie mais non source, non specifie et non automatisable. Aucun autre acte ne doit etre utilise en substitution. | bloquant |

## 4. Points tranches

### 4.1 Wording cession vs apport

Decision :
- le futur moteur ne doit pas rendre la double formule source `acquerir/de recevoir en apport en nature` ;
- `operation_spfpl.type == cession` selectionne un wording de cession uniquement ;
- `operation_spfpl.type == apport` selectionne un wording d'apport uniquement ;
- si le type d'operation est absent, contradictoire ou double dans un meme document, la generation doit bloquer.

Valeurs texte admises pour la note d'information V1 :

| Operation | `note_information.operation_phrase` | `note_information.operation_nom` |
|---|---|---|
| `cession` | `d'acquerir` | `cession` |
| `apport` | `de recevoir en apport en nature` | `apport` |

Pour les PV d'agrement du chemin `SPFPL_CESSION` :
- le classement de la source de verite prime : ces PV restent des documents de cession ;
- les formulations source de type `contrat d'apport`, `autorise l'apport` ou `parts apportees` ne doivent pas etre reprises dans un rendu `SPFPL_CESSION` ;
- le futur ticket code devra porter une note explicite indiquant que cette adaptation de wording est couverte par le present arbitrage.

### 4.2 Commissaire aux apports

Decision :
- le libelle canonique retenu est `commissaire_aux_apports` ;
- la mention `Attestation nomination comm. aux comptes` de la source de verite est traitee comme un libelle metier divergent, car le DOCX source disponible porte sur un commissaire aux apports ;
- le rendu automatise ne doit jamais conserver le litteral `OU` ni deux commissaires alternatifs ;
- un seul commissaire aux apports selectionne doit etre fourni au generateur.

Regle de blocage future :
- generation bloquee si `commissaire_aux_apports` est absent ;
- generation bloquee si plusieurs commissaires sont fournis sans choix explicite ;
- generation bloquee si le rendu final conserverait une option non tranchee.

### 4.3 Evaluateur et commissaire

Decision :
- `evaluateur_apport` et `commissaire_aux_apports` restent deux roles distincts ;
- les entites fixes observees dans certaines sources ne doivent pas etre hard-codees dans un generateur ;
- la V1 accepte une saisie manuelle controlee de ces roles dans le contexte dossier.

## 5. Points laisses manuels V1

### 5.1 Liste dynamique des souscripteurs

Decision :
- l'attestation sur le capital / liste des souscripteurs SPFPL V1 est automatisable seulement pour un actionnaire unique ;
- `capital_souscription.souscripteurs[]` peut rester le role canonique cible, mais la cardinalite automatisee V1 est limitee a `1` ;
- toute situation a plusieurs souscripteurs reste a preparer manuellement en V1.

Regle de blocage future :
- generation bloquee si le contexte contient plusieurs souscripteurs ;
- generation bloquee si le nombre de souscripteurs ne peut pas etre determine ;
- generation bloquee si les accords singulier/pluriel necessaires ne sont pas couverts par une spec ulterieure.

### 5.2 Selection du commissaire et de l'evaluateur

Decision :
- le moteur V1 ne choisit pas lui-meme un commissaire aux apports ;
- le moteur V1 ne choisit pas lui-meme un evaluateur d'apport ;
- ces informations sont fournies par saisie dossier controlee ou par un futur referentiel valide.

## 6. Points bloquants restants

### 6.1 Acte de cession d'actions

Decision :
- l'acte de cession d'actions reste hors automatisation V1 ;
- le document est inventorie dans `project/source_truth/Documents_a_generer_par_cas.docx`, mais aucune source DOCX confirmee n'est associee ;
- l'acte de cession de parts ne doit pas servir de substitut ;
- les fichiers `.doc` ou documents voisins du raw dump ne suffisent pas a confirmer une source canonique.

Statut documentaire :

| Etape | Statut |
|---|---|
| Inventorie | oui |
| Valide | non |
| Source recue | non |
| Analyse | non |
| Specifie | non |
| Pret a coder | non |

Condition de reouverture :
- recevoir ou confirmer une source DOCX canonique pour l'acte de cession d'actions ;
- produire une analyse et une spec dediees ;
- documenter tout ecart avec l'acte de cession de parts.

## 7. Effet sur les futurs tickets code SPFPL

Peuvent avancer vers un ticket code dedie, sous reserve des autres prerequis de spec et de tests :
- note d'information, avec wording pilote par `operation_spfpl.type` ;
- PV d'agrement cession, avec adaptation de wording documentee par le present arbitrage ;
- contrat d'apport, si `evaluateur_apport` et `commissaire_aux_apports` sont fournis ;
- designation du commissaire aux apports, si un commissaire unique est fourni ;
- attestation capital SPFPL, uniquement en configuration actionnaire unique.

Restent exclus du code V1 :
- liste dynamique multi-souscripteurs ;
- acte de cession d'actions ;
- tout rendu conservant une double option non tranchee, notamment `OU` ou une formule cession/apport double.

## 8. Statut

`ARBITRAGE-SPFPL-001` ferme les arbitrages principaux requis avant code SPFPL specifique, sans changement de code Python.

Prochaine etape recommandee :
- ouvrir un ticket code limite a une seule sous-famille SPFPL, en commencant par la note d'information ou par les PV d'agrement cession selon la priorite metier.
