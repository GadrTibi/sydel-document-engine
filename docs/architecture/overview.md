# Vue d'ensemble d'architecture

## But

Construire un moteur documentaire juridique déterministe, piloté par un référentiel métier par cas, mais exécuté **par document canonique**.

## Schéma logique

1. **Référentiel métier**
   - cas métier ;
   - structures concernées ;
   - règles documentaires.

2. **Registre documentaire canonique**
   - un document = une entrée canonique ;
   - mapping source ;
   - lot ;
   - statut du cycle documentaire.

3. **Registre moteur**
   - un document canonique = un générateur ;
   - condition générale ;
   - conditions spécifiques ;
   - règles grammaticales ;
   - gestion éventuelle des blocs répétables.

4. **Orchestrateur**
   - reçoit un contexte dossier ;
   - détermine les documents à générer ;
   - appelle les générateurs.

5. **Rendu**
   - DOCX ;
   - PDF ;
   - ZIP final.

## Découpage de code proposé

- `domain/` : objets métier et définitions documentaires
- `registry/` : catalogue et états du moteur
- `orchestrator/` : sélection des documents à produire
- `generators/` : un générateur par document
- `rendering/` : helpers DOCX / bundle
- `utils/` : grammaire, assemblage d'adresses, helpers communs
- `app/` : interface Streamlit minimale

## Règle clé

Le dépôt doit rester lisible même avec plusieurs dizaines de documents.
La dette de duplication doit être contrôlée dès les premiers lots.
