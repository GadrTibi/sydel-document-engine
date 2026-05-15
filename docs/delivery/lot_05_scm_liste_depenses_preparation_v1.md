# Lot 05 - preparation source liste depenses communes SCM V1

Ticket : `PREP-SCM-LISTE-DEPENSES-CONVERT-001`

## Objet

Obtenir une source DOCX exploitable pour la liste des depenses communes SCM, a partir du fichier legacy `.doc` deja place dans les sources Lot 05.

Ce fichier ne code rien, ne modifie aucun wording juridique et ne vaut pas spec canonique ou spec texte.

## Source legacy

Source legacy retenue :

```text
project/source_documents/lot_05/Liste depenses communes SCM.doc
```

Note : le fichier physique conserve son nom exact sur disque avec accent dans `depenses`.

Hash SHA-256 de la source legacy :

```text
EF210A05C40C251F44969F7450060AC113496371A9FFA64677755EA2DCC770C6
```

## Source DOCX preparee

Source DOCX preparee :

```text
project/source_documents/lot_05/Liste depenses communes SCM.docx
```

Hash SHA-256 du DOCX converti :

```text
5F3EB3C59AE0A663277B8101DE3EE6E9B817F9E53C36BFF2B3FD5D682B171423
```

## Conversion realisee

Conversion effectuee localement via l'outil Microsoft Office :

```text
C:\Program Files\Microsoft Office\root\Office16\Wordconv.exe -oice -nme <source.doc> <cible.docx>
```

Tentative directe via Word COM : non retenue comme chemin final, car l'automatisation a suspendu Word sans produire de DOCX.

Conversion retenue : reussie avec `Wordconv.exe`.

## Controles effectues

Controle OpenXML :

- archive DOCX lisible ;
- `word/document.xml` present ;
- 21 entrees dans l'archive DOCX ;
- texte extrait depuis `word/document.xml` : 1218 caracteres apres nettoyage XML ;
- marqueurs confirmes dans le texte extrait : placeholders societe, `DENOMINATION DE LA DEPENSE`, `SCM`, lignes de depenses communes.

## Conclusion

Source convertie : oui.

Le DOCX resultant est place dans `project/source_documents/lot_05/` et peut servir de source documentaire pour une future analyse/spec des satellites SCM.

## Prochaine action recommandee

Lancer `SPEC-SCM-SATELLITES-001`, avec analyse separee de la liste des depenses communes SCM avant tout code documentaire.
