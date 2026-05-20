# Rapport executif - GLOBAL-VARIABLE-IDENTITY-AUDIT-001

## Perimetre audite
- Variables auditees : 1334 slugs normalises distincts, issus de 12379 lignes documentaires.
- Documents couverts : 43 (`DOC-001` a `DOC-043`).
- Familles couvertes : 15.
- Groupes candidats : 49 champs canoniques proposes et 142 rapprochements representatifs en matrice.

## Typologie des relations
- SAME_FIELD : 16
- SAME_DATA_DIFFERENT_SHAPE : 30
- EXPLICIT_REUSE_ONLY : 16
- DISTINCT_FIELDS : 15
- UNCERTAIN_REQUIRES_HUMAN_DECISION : 65

## Principaux risques si fusion incorrecte
- Confondre des roles personne : signataire, dirigeant, associe, president, mandataire, conjoint, vendeur et cedant peuvent correspondre a des personnes differentes.
- Confondre des adresses : siege, domiciliation, adresse personnelle, cabinet, lieu d exercice et site declare ne sont pas equivalents par defaut.
- Confondre des societes : societe dossier, cible, cedee, acquereur, cessionnaire, apportee, SPFPL et SCM peuvent avoir denomination, capital, RCS et siege distincts.
- Deriver abusivement les montants : capital, apport, prix total, prix unitaire et composantes corporelles/incorporelles doivent rester tracables.
- Utiliser des variables spec-only ou template-only comme champs front definitifs sans validation documentaire.

## Gains attendus pour le futur front
- Remplacer les placeholders `personne_1/personne_2` par une fiche personne reutilisable avec roles explicites.
- Mutualiser les composants d adresse et generer les formes affichees sans perdre la distinction des lieux.
- Centraliser les blocs societe, RCS, ordre, capital, cession, bail et signature sous des objets rolees.
- Reduire les champs redemandes grace aux reutilisations explicites, tout en conservant des overrides pour les documents sensibles.

## Qualite des sources
- Source brute solide : inventaire global deja committe, 43 documents et 15 familles.
- Signal spec-only : 708 slugs uniquement observes dans les specs delivery.
- Signal template sans mapping V1 : 411 slugs presents dans des templates mais absents du code_mapping V1.
- La matrice est volontairement representative et groupee; elle evite une explosion pairwise et doit etre lue avec le CSV brut.

## Questions humaines restantes
- Nombre : 10 questions groupees.
- Fichier : `docs/project/GLOBAL_VARIABLE_OPEN_QUESTIONS_V1.md`.

## Prochaines etapes recommandees
1. Faire repondre les humains aux questions Q-001 a Q-010.
2. Geler une version V2.1 du registre canonique avec statuts valides et regles de reutilisation.
3. Ouvrir ensuite le ticket de rebuild front global sur la base du registre arbitre, pas sur les variables templates brutes.
