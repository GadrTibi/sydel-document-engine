# DAAT x SYDEL - PREPARATION SOURCE V1
## Acte de cession d'actions SPFPL

Ticket : `CONVERT-ACTE-ACTIONS-001`

## 1. Objet

Obtenir une source DOCX exploitable pour l'acte de cession d'actions SPFPL, a partir du candidat legacy identifie lors de l'audit V1.

Ce fichier ne code rien, ne modifie aucun wording juridique et ne vaut pas spec canonique ou spec texte.

## 2. Origine de la source

Source legacy retenue :

```text
project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/Cession/Acte_cession_SPFPL_tiers_modele.doc
```

Source DOCX preparee :

```text
project/source_documents/lot_05/Acte_cession_SPFPL_tiers_modele.docx
```

Origine documentaire : raw dump legacy `Création SPFPL/cession spfpl/Cession`.

Niveau de confiance : eleve.

Raison du niveau de confiance :
- le fichier legacy avait deja ete identifie comme candidat probable dans `docs/delivery/lot_05_acte_cession_actions_audit_v1.md` ;
- le corps du document vise une `Cession d'actions` ;
- les marqueurs `OBJET DU CONTRAT`, `CESSION D'ACTIONS` et `[nb_actions_cedees]` sont presents apres conversion ;
- les candidats voisins deja analyses correspondent a des actes de cession de parts et ne doivent pas servir de substitut.

## 3. Conversion realisee

Conversion effectuee localement via l'outil Microsoft Office :

```text
C:\Program Files\Microsoft Office\root\Office16\Wordconv.exe -oice -nme
```

Tentative directe via Word COM : non retenue comme chemin final, car l'ouverture automatisee du `.doc` legacy a echoue puis a suspendu Word sur une tentative de reparation/ouverture de document ancien.

Conversion retenue : reussie avec `Wordconv.exe`.

## 4. Controles effectues

Hash SHA-256 de la source legacy :

```text
CEB0B34231993E5054C450A1EAB4C6EA2C2E9929C117A3AE312F769486BEC674
```

Hash SHA-256 du DOCX converti :

```text
E615D60C11C67180233FC8B810A29C73755B1EC74B147E5548D4574DD03FDF8D
```

Controle OpenXML :
- archive DOCX lisible ;
- `word/document.xml` present ;
- 21 entrees dans l'archive DOCX ;
- texte extrait depuis `word/document.xml` : 15955 caracteres ;
- marqueurs confirmes dans le texte extrait : `Cession d'actions`, `OBJET DU CONTRAT`, `CESSION D'ACTIONS`, `nb_actions_cedees`.

## 5. Conclusion

Source convertie : oui.

Le DOCX resultant est place dans `project/source_documents/lot_05/` et peut servir de source documentaire pour une future analyse/spec de l'acte de cession d'actions SPFPL.

## 6. Prochaine action recommandee

Creer une spec canonique et une spec texte dediees a l'acte de cession d'actions SPFPL avant toute implementation.
