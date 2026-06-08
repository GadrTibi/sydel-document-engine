# Documents de référence — « Documents avec variables » (Drive, à jour)

> **Source :** export du Drive de Gad « Documents avec variables » (totalité des documents à générer,
> **tokenisés**, organisés par type d'entreprise). Importé le **2026-06-08**.
>
> **Rôle :** c'est le **jeu de modèles de RÉFÉRENCE à jour** — la source de vérité du *wording* des
> documents. Les générateurs lisent leurs modèles depuis `project/source_documents/` ; ce dossier-ci
> sert à **vérifier que `source_documents/` reste aligné** sur la dernière version du Drive.
>
> ## Traitement à l'import (data-safety)
> - **Métadonnées strippées** sur les 125 `.docx` (author / last_modified_by / title / etc.) : l'export
>   portait de vrais noms d'employés du cabinet dans les métadonnées — retirés avant versionnement.
> - **8 fichiers `.doc`** (ancien format, non lisibles par python-docx donc métadonnées non strippables)
>   **exclus** de l'import par prudence : `Liste dépenses communes SCM.doc`, `PV nomination gérant`
>   (SCP/SCS), `PV associé unique nomination DG` (SELAS), `Demande dérogation cumul SELARL salariée`,
>   `PV SPFPL autorisation emprunt`, actes de cession SPFPL (×2). Leurs équivalents `.docx` sont présents
>   quand ils existent.
> - **Corps vérifié** (audit multi-agents) : modèles tokenisés ([variables]) + texte juridique générique ;
>   aucune donnée réelle de tiers (client/patient). Coordonnées propres de SYDEL/DAAT = données de la firme.
>
> ## Comparaison repo ↔ référence (2026-06-08)
> - **À jour / identiques** : DNC, procuration, statuts SCI IRIS / SCS / SCM / SAS / SPFPL cession / SPFPL apport.
> - **Corrigé** : autorisation de domiciliation (notre modèle `source_documents/lot_01` était périmé +
>   rouge → remplacé par cette version à jour).
> - **SCI** : écarts triviaux (trait d'union « quatre-vingt-dix-neuf », sauts de ligne).
> - **SELAS multi** : on **garde le modèle Reynaud** (décision Gad 2026-06-08) ; la version SELAS de ce
>   dossier Drive (wording différent) **n'est pas adoptée**.
>
> ## À confirmer (wording → Gad / Rafael)
> - L'autorisation de domiciliation à jour **n'a plus le « € »** (« au capital de [capital_social] » sans
>   devise) → faut-il que `[capital_social]` porte « euros » ?
> - Switch préposition « au / à » devant l'adresse : non présent dans les modèles — à préciser si voulu.
