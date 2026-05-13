# DAAT x SYDEL - Spec technique V1
## Couche de rendu DOCX commune

## 1. Objet

Formaliser une couche de rendu DOCX commune et réutilisable pour les générateurs documentaires SYDEL.

Cette spec ne modifie pas le code métier. Elle prépare un futur ticket d'implémentation dans `src/sydel_doc_engine/rendering/docx_builder.py` afin d'éviter que chaque générateur recode localement les polices, marges, alignements, bordures, cartouches, blocs de signature et rappels légaux.

## 2. Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`
- `src/sydel_doc_engine/rendering/docx_builder.py`
- `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py`
- `src/sydel_doc_engine/generators/lot_01/autorisation_domiciliation.py`
- `src/sydel_doc_engine/generators/lot_01/procuration.py`
- `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`

ADR applicables :

- ADR-0002 : moteur construit par document canonique.
- ADR-0004 : génération DOCX propre from-scratch.
- ADR-0005 : mode Codex repo-first, traçable et limité.

## 3. Constat actuel

`docx_builder.py` ne fournit aujourd'hui que `new_document()`.

Les générateurs déjà codés configurent donc eux-mêmes :

- marges A4 à `2.5 cm` ;
- police `Roboto` en `10 pt` ;
- police Word via `w:ascii`, `w:hAnsi`, `w:eastAsia`, `w:cs` ;
- paragraphes simples ;
- paragraphes centrés ou justifiés ;
- cartouches de titre encadrés via `Table Grid` ;
- tableaux de signature alignés à droite ;
- bloc de rappel légal italique pour DOC-001.

Cet état fonctionne pour les premiers documents, mais il crée une duplication technique. Il augmente aussi le risque de rendu divergent entre documents canoniques.

Point d'écart visuel explicite : les encadrés de signature manquent aujourd'hui dans le rendu généré. Les générateurs produisent des zones ou lignes de signature, mais pas de bloc de signature encadré commun lorsque la source attend une signature dans un cadre.

## 4. Principe cible

La couche commune doit rester une couche de rendu, pas une couche métier.

Elle doit :

- créer et configurer les DOCX propres ;
- exposer des profils de style explicites ;
- fournir des helpers de paragraphes et de blocs réutilisables ;
- accepter des textes déjà préparés par les générateurs ;
- ne pas décider des conditions documentaires ;
- ne pas modifier le wording juridique ;
- ne pas introduire de logique d'IA générative.

Les générateurs doivent rester responsables de :

- choisir les blocs à générer ;
- assembler les variables métier ;
- appliquer les règles de grammaire documentées ;
- bloquer les cas non couverts par les specs.

## 5. Profil de style global

Profil V1 recommandé : `SydelDocxStyleProfile`.

Valeurs par défaut :

| Propriété | Valeur V1 |
|---|---|
| Format cible | A4 portrait |
| Marge haute | `2.5 cm` |
| Marge basse | `2.5 cm` |
| Marge gauche | `2.5 cm` |
| Marge droite | `2.5 cm` |
| Police principale | `Roboto` |
| Taille principale | `10 pt` |
| Couleur texte | noir |
| Espacement après paragraphe standard | `6 pt` |
| Espacement après paragraphe compact | `0 pt` ou `2 pt` |
| Espacement avant bloc notable | `10 pt` si nécessaire |
| Alignement corps par défaut | gauche |
| Alignement paragraphes juridiques longs | justifié |
| Alignement titres encadrés | centré |
| Alignement signatures simples | bloc à droite, texte à gauche dans le bloc |

La configuration de la police doit continuer à alimenter les attributs Word nécessaires :

- `w:ascii`
- `w:hAnsi`
- `w:eastAsia`
- `w:cs`

## 6. Styles de paragraphes et de blocs

### 6.1 Paragraphe standard

Usage :

- corps courant ;
- phrases d'identification ;
- phrases de clôture ;
- lignes simples du PV.

Style :

- `Roboto 10 pt` ;
- espace après `6 pt` ;
- alignement gauche par défaut ;
- gras optionnel ;
- italique optionnel ;
- souligné optionnel ;
- alignement surchargeable.

### 6.2 Paragraphe justifié

Usage :

- paragraphes juridiques longs ;
- déclaration DOC-001 ;
- autorisation DOC-002 ;
- paragraphes de mandat DOC-003 ;
- paragraphes de décisions du PV.

Style :

- base identique au paragraphe standard ;
- alignement justifié ;
- espace après `6 pt`.

### 6.3 Paragraphe centré compact

Usage :

- en-tête société du PV ;
- bloc mandataire SYDEL ;
- titres multi-lignes non encadrés.

Style :

- alignement centré ;
- espace après `0 pt` à `2 pt` ;
- gras et italique surchargeables ligne par ligne.

### 6.4 Titre de décision

Usage :

- `PREMIERE DECISION` ;
- `DEUXIEME DECISION` ;
- `TROISIEME DECISION`.

Style :

- paragraphe standard ;
- gras ;
- espace avant éventuel selon contexte ;
- pas de transformation automatique du texte.

## 7. Bloc titre encadré

Le bloc titre encadré doit remplacer les implémentations locales actuellement présentes dans DOC-001, DOC-002 et DOC-003.

Entrées :

- liste ordonnée de lignes de titre ;
- option de casse laissée au générateur ;
- largeur par défaut pleine largeur utile ;
- alignement du tableau centré ;
- bordure noire simple.

Style :

- tableau 1 colonne ;
- bordure visible sur les quatre côtés ;
- texte centré ;
- `Roboto 10 pt` ;
- lignes en gras par défaut ;
- espace vertical après le cartouche : un paragraphe vide ou un espacement contrôlé par le helper.

Exemples de lignes déjà couvertes :

- DOC-001 : `DECLARATION DE NON CONDAMNATION` + `EN APPLICATION DE L'ARTICLE A.123-51 du Code de Commerce`
- DOC-002 : `AUTORISATION DE DOMICILIATION`
- DOC-003 : `Procuration`

## 8. Bloc signature simple

Le bloc signature simple couvre les signatures non encadrées, actuellement utilisées dans les documents Lot 1 et dans le PV.

Entrées :

- lieu de signature ;
- date de signature ou nombre d'exemplaires selon document ;
- nom(s) des signataires ;
- image de signature optionnelle ;
- position : droite par défaut pour DOC-001/DOC-002/DOC-003, flux normal pour PV si signatures répétables.

Style DOC-001/DOC-002/DOC-003 :

- tableau 1 ligne / 2 colonnes ;
- colonne droite d'environ `7 cm` ;
- tableau aligné à droite ;
- contenu de la cellule droite aligné à gauche ;
- lignes `Fait à ...`, `Le ...`, puis nom ou zone de signature ;
- espace vertical prévu si aucune image n'est fournie.

Style PV :

- une ligne de nom par associé ;
- répétition dans l'ordre `associes[]` ;
- mention d'acceptation conservée comme paragraphe séparé ;
- pas de déduction métier dans le helper.

## 9. Bloc signature encadré

Le bloc signature encadré doit être ajouté comme variante commune, car il manque aujourd'hui dans le rendu généré.

But :

- produire une zone de signature visuellement encadrée lorsque la source documentaire ou la revue humaine l'exige ;
- éviter de recoder une table bordée spécifique dans chaque générateur.

Entrées :

- titre ou libellé optionnel ;
- lignes de métadonnées optionnelles : lieu, date, nom, qualité ;
- mention manuscrite optionnelle ;
- image de signature optionnelle ;
- hauteur minimale ;
- largeur ;
- alignement du bloc : droite, gauche, centré ou pleine largeur.

Style V1 :

- tableau 1 colonne encadré ;
- bordure noire simple ;
- largeur contrôlée ;
- hauteur minimale suffisante pour signature manuscrite ;
- texte interne aligné à gauche par défaut ;
- espacement interne lisible ;
- insertion de l'image si fournie, avec largeur bornée.

Règle importante :

- le helper ne doit pas décider qu'un document utilise une signature encadrée ;
- le générateur ou la spec du document doit choisir explicitement entre signature simple et signature encadrée.

## 10. Rappel légal

Le rappel légal doit devenir un bloc commun, au moins pour DOC-001.

Entrées :

- titre ou préfixe, par exemple `Rappel` ;
- suffixe optionnel, par exemple ` : Article L123-5 du code de commerce` ;
- paragraphes du rappel ;
- style de mise en évidence.

Style V1 :

- séparation visuelle avant le bloc ;
- titre en italique ;
- mot `Rappel` souligné si demandé ;
- suffixe en italique ;
- paragraphes en italique ;
- alignement justifié ;
- espace après compact, par exemple `3 pt`.

Contraintes :

- le helper ne contient pas le texte légal ;
- le texte reste dans la spec ou le générateur du document concerné ;
- aucun wording légal n'est corrigé ou enrichi dans la couche de rendu.

## 11. Marges, espacements et alignements

Règles communes :

- toutes les marges standard doivent être appliquées par un seul helper de configuration ;
- les espacements doivent être exprimés dans le profil de style, pas dispersés en constantes locales ;
- l'alignement justifié doit être réservé aux paragraphes longs ;
- les blocs centrés doivent rester des cas explicites : titre, en-tête société, mandataire ;
- les signatures à droite doivent utiliser un helper dédié, pas un tableau local dupliqué.

Points à préserver :

- DOC-001 doit rester sur une page avec rappel légal en bas si possible ;
- DOC-002 doit rester très sobre et mono-page ;
- DOC-003 doit conserver le bloc mandataire centré ;
- le PV doit conserver une structure lisible avec en-tête société centré, titres de décision en gras et signatures répétables.

## 12. Mécanisme de surcharge document par document

La couche commune doit permettre des surcharges contrôlées sans forcer chaque générateur à recréer ses propres helpers.

Mécanisme recommandé :

- un profil global par défaut ;
- des options passées aux helpers pour les écarts ponctuels ;
- éventuellement un profil documentaire léger, par exemple `document_style_overrides`, limité au rendu.

Exemples de surcharges acceptables :

- titre DOC-001 sur deux lignes ;
- espace après très compact pour l'en-tête société du PV ;
- signature simple ou encadrée selon document ;
- bloc mandataire DOC-003 en gras/italique ligne par ligne ;
- rappel légal uniquement pour DOC-001.

Exemples de surcharges interdites :

- changer un texte juridique dans un helper de style ;
- choisir une branche documentaire dans `docx_builder.py` ;
- déduire un rôle métier à partir d'un index ;
- insérer des constantes documentaires métier dans la couche de rendu commune.

## 13. Documents déjà impactés

### DOC-001 - Déclaration sur l'honneur de non-condamnation

Rendu déjà concerné :

- configuration globale du document ;
- cartouche titre encadré sur deux lignes ;
- paragraphes d'identité ;
- paragraphe de déclaration justifié et gras ;
- signature simple à droite avec image optionnelle ;
- rappel légal italique.

Ecart actuel :

- le rendu dispose d'une zone de signature, mais pas d'un bloc signature encadré commun.

### DOC-002 - Autorisation de domiciliation

Rendu déjà concerné :

- configuration globale du document ;
- cartouche titre encadré ;
- paragraphe unique justifié ;
- bloc final lieu/date/nom à droite.

Ecart actuel :

- le bloc final n'est pas encadré.

### DOC-003 - Procuration

Rendu déjà concerné :

- configuration globale du document ;
- cartouche titre encadré ;
- paragraphes de pouvoir ;
- bloc mandataire centré avec gras/italique ;
- bloc final lieu/date/nom à droite.

Ecart actuel :

- le bloc final n'est pas encadré.

### PV nomination gérant

Rendu déjà concerné :

- configuration globale du document ;
- en-tête société centré compact ;
- titre de PV centré et gras ;
- paragraphes de décisions ;
- signatures répétables des associés.

Ecart actuel :

- les signatures finales sont de simples lignes de nom ;
- aucun bloc signature encadré n'est généré ;
- si la revue humaine demande un cadre de signature ou une signature séparée du dirigeant non associé, le rendu commun devra être utilisé après décision métier.

## 14. Critères d'acceptation pour le futur ticket de code

Le futur ticket d'implémentation pourra être considéré terminé si :

- `docx_builder.py` expose le profil global et les helpers de rendu communs ;
- les duplications évidentes de configuration DOCX sont supprimées des générateurs migrés ;
- DOC-001, DOC-002, DOC-003 et PV nomination gérant gardent leur wording inchangé ;
- les tests existants restent verts ;
- au moins un test ou contrôle ciblé couvre le rendu du cartouche titre ;
- le bloc signature encadré est disponible, même si son activation reste document par document ;
- la migration ne branche pas de nouveau document ni de nouvelle règle métier.

## 15. Prochaine étape recommandée

Ouvrir un ticket technique dédié pour implémenter la couche commune dans `docx_builder.py`, puis migrer progressivement les générateurs déjà codés.

Ordre recommandé :

1. implémenter le profil global et les helpers sans changer les générateurs ;
2. migrer DOC-001, car il couvre titre encadré, signature simple et rappel légal ;
3. migrer DOC-002 et DOC-003 ;
4. migrer le PV nomination gérant ;
5. décider explicitement quels documents doivent activer le bloc signature encadré.

