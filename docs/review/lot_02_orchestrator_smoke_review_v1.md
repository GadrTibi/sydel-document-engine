# Revue smoke orchestrateur Lot 2 - SMOKE-ORCH-L2-001

## Objet

Verifier par generation reelle que l'orchestrateur dossier :
- inclut `pv_nomination_gerant.docx` pour une structure concernee par la famille PV nomination gerant ;
- exclut `pv_nomination_gerant.docx` pour une SAS.

Le smoke ne couvre ni PDF, ni ZIP, ni UI.

## Contexte positif

- Fichier contexte : `examples/contexts/lot_02_orchestrator_positive_example.yaml`
- Structure : `SCI`
- Dossier de sortie : `artifacts/lot_02_orchestrator_positive_smoke_test/`
- Resultat attendu : documents universels Lot 1 + PV nomination gerant.

Fichiers generes :
- `declaration_non_condamnation.docx`
- `autorisation_domiciliation.docx`
- `procuration.docx`
- `pv_nomination_gerant.docx`

Verification PV :
- `pv_nomination_gerant.docx` est present.

## Contexte negatif

- Fichier contexte : `examples/contexts/lot_02_orchestrator_negative_sas_example.yaml`
- Structure : `SAS`
- Dossier de sortie : `artifacts/lot_02_orchestrator_negative_sas_smoke_test/`
- Resultat attendu : documents universels Lot 1 uniquement.

Fichiers generes :
- `declaration_non_condamnation.docx`
- `autorisation_domiciliation.docx`
- `procuration.docx`

Verification PV :
- `pv_nomination_gerant.docx` est absent.

## Points ouverts

- Ce smoke valide la selection orchestrateur et la generation DOCX, mais ne vaut pas validation juridique du wording.
- Le rendu Word du PV reste soumis a revue humaine.
- PDF, ZIP et UI restent hors perimetre de ce ticket.
