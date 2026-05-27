# Open Debts And Risks

Date : 2026-05-27

## Dettes ouvertes

| ID | Sujet | Risque | Traitement |
|---|---|---|---|
| YB-DEBT-001 | Source docs Boss Delta absente sur disque au pre-flight | Risque de divergence si une piece jointe complete existe hors repo | Capture session ajoutee ; remplacer par piece complete si fournie. |
| YB-DEBT-002 | Ancien canon pilote SELARL / cobayes | Risque de lancer une UAT sur un modele obsolete | Pilote et UAT mis en pause jusqu'a `YB-S12-007`. |
| YB-DEBT-003 | Multi-bureaux non absorbe dans code/front | Risque de melanger les contextes bureaux | Traiter en premier dans `YB-S12-002`. |
| YB-DEBT-004 | Modele Lead/Atelier/Relance non implemente | Risque de faire du code sur objets obsoletes | Specifier dans `YB-S12-003` avant code. |
| YB-DEBT-005 | REFAIS_AG ancien / refaitage | Risque de renvoyer une fiche invalidee en prospection brute | Specifier dans `YB-S12-004`. |
| YB-DEBT-006 | Relance boss | Risque d'autoriser des modifications structurantes par telepro | Specifier ACL et mode lecture seule dans `YB-S12-005`. |
| YB-DEBT-007 | Atelier non attribue | Risque d'auto-attribution non voulue | Specifier file manuelle dans `YB-S12-006`. |

## Risques de reprise

- Ne pas considerer `SELARL-COMPLETE-COMPLEX-SUBFORMS-001` comme prochain
  ticket : il est supplante par le bridge Boss Delta.
- Ne pas relancer le test utilisateur local, les cobayes ou Naomi avant rebuild
  pilote.
- Ne pas creer de vue cross-bureau fusionnee pour "faciliter" l'usage.
- Ne pas ajouter de statut systeme special pour Sarah, Ethan ou autres noms.
- Ne pas introduire `chef telepro` sans nouveau mandat PM.
