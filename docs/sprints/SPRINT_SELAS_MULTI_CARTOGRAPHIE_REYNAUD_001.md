# SELAS multi-associés — Cartographie des variables à tokeniser (001)

**Date :** 2026-06-05
**Source :** cas réel `Statuts SELAS DU DR ISABELLE REYNAUD.docx` (38 articles), analysé par le Second côté Capitaine.
**But :** débloquer la tokenisation **sans transférer le fichier patiente** (données réelles → jamais versionnées). Ici = **inventaire des variables**, pas de valeurs réelles.
**Périmètre :** statuts SELAS médecins **multi-associés (2 à 5)**. **NO-GO génération** maintenu — ceci est du **cadrage**, pas du code.

> ⚠️ Ce que ce cas réel contient : **2 associés dont 1 personne morale** (une société civile), une **présidence**, des **directeurs généraux** (art. 15), une **répartition d'actions par associé**, et la règle « la répartition ne retire jamais la **majorité des droits de vote aux exerçants** ». Plusieurs de ces points dépendent de l'**arbitrage Rafael** (voir pack passation) — la cartographie les liste mais ne tranche rien.

## A. Variables « société » (1 par dossier)
| Token | Zone | Note |
|---|---|---|
| `denomination_sociale` | Art. 3 + titre | « SELAS DU DR … » — dépend du choix de dénomination |
| `forme_sociale` | Art. 1 | fixe = SELAS (libellé exact à conserver) |
| `objet_social` | Art. 2 | texte type médecine — vérifier variantes profession |
| `siege_social_adresse` | Art. 4 | adresse complète |
| `lieu_exercice` | Art. 5 | peut différer du siège |
| `duree_annees` | Art. 6 | typiquement 99 ans |
| `capital_montant` | Art. 8 | € |
| `nombre_actions_total` | Art. 8 | entier |
| `valeur_nominale_action` | Art. 8 | € / action (cohérence capital = N × VN) |

## B. Variables « associé » — **RÉPÉTÉES N fois (N = 2..5)** ⟵ cœur du multi
Bloc à **pluraliser** ; un jeu par associé. Distinguer **personne physique** vs **personne morale** (cf. Q-C Rafael).
| Token (par associé `i`) | Zone | Personne physique | Personne morale |
|---|---|---|---|
| `associe[i].civilite` | comparution | Madame/Monsieur | n/a |
| `associe[i].prenom` / `.nom` | comparution | ✔ | dénomination sociale |
| `associe[i].date_naissance` / `.lieu` | comparution | ✔ | n/a |
| `associe[i].nationalite` | comparution | ✔ | n/a |
| `associe[i].adresse` | comparution | domicile | siège |
| `associe[i].profession` / `.specialite` | comparution | médecin + spécialité | n/a |
| `associe[i].ordre_numero` | comparution | n° tableau de l'Ordre | n/a |
| `associe[i].forme_pm` / `.rcs` / `.representant` | comparution | n/a | forme, RCS, représentant légal |
| `associe[i].est_exercant` | gouvernance | détermine la **règle majorité droits de vote** | souvent non-exerçant |
| `associe[i].nombre_actions` | Art. 8 (répartition) | ✔ | ✔ |

## C. Les 4 ancrages à pluraliser (couche nombre — réutilisée de SELARL)
1. **Comparution** : « LES SOUSSIGNÉ(E)S » + accord genre/nombre + N blocs B.
2. **Apports (Art. 7)** : N lignes d'apport en numéraire + total.
3. **Répartition (Art. 8)** : tableau N lignes (associé → nombre d'actions), total, **garde-fou majorité exerçants**.
4. **Signatures** : N signataires.

## D. Gouvernance (dépend des arbitrages Rafael)
| Token | Zone | Dépend de |
|---|---|---|
| `president.identite` / `.pouvoirs` / `.remuneration` | Art. 14 | accord genre → Président/**Présidente** |
| `dg[].identite` / `.pouvoirs` / `.duree` / `.revocation` / `.remuneration` | Art. 15 | **Q-B Rafael : gère-t-on les DG ?** (présents dans Reynaud) |
| `clause_agrement` / `quorum` / `majorite` | Art. 13/16 | décisions collectives multi |

## E. Couche genre (réutilisée — paires exactes, jamais de regex de terminaison)
Président/Présidente, Soussigné(e)(s), Associé(e)(s), Né(e), accords des duos/groupes selon le genre de **chaque** associé.

## F. Points en attente d'arbitrage (ne pas tokeniser en dur avant Rafael)
- **DG** (Q-B) : inclure la section art. 15 ou la sortir du 1er jet ?
- **Associé personne morale** (Q-C) : accepté ou médecins physiques seulement ? + inscrire la **règle dure** « majorité des droits de vote aux exerçants » comme garde-fou moteur ?
- **Représentativité** (Q-D) : ce cas n'est qu'**un** exemple (2 associés dont 1 morale) ; il manque des modèles 3/4/5 + genres pour figer la trame.

## Prochaine manœuvre (Mousse)
À partir de cette cartographie : structurer l'inventaire des variables côté schéma front/data **sans coder le générateur** ; surligner les zones dépendantes des arbitrages Rafael (section F). Le `.docx` réel reste chez le Capitaine ; cette carte suffit pour démarrer le cadrage. La génération reste **NO-GO**.
