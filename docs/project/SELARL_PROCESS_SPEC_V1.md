# Spécification processus SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Cette spec reconstruit la logique produit du pilote SELARL à partir de la source de vérité V2, sans modifier l'UI, le moteur DOCX/PDF/ZIP ni les générateurs.

Source V2 utilisée : `project/source_truth/Documents_a_generer_par_cas_V2.docx`.

## A. Choix de qualification du dossier SELARL

| Question métier | Valeurs | Usage |
|---|---|---|
| Profession | `medecin`, `chirurgien_dentiste` | Sélection des statuts SELARL et des champs ordre/profession. |
| Site distinct | oui / non | Affiche le formulaire CD94 manuel. |
| SCM cession | oui / non | Affiche le mini-batch cession de parts SCM vers SELARL. |
| Régime communautaire | oui / non | Affiche les lettres conjoint / renonciation. |
| Dérogation | oui / non | Affiche les formulaires de dérogation et la pièce manuelle SEL BNC. |
| Cession | oui / non | Affiche bail, appel de fonds et cession de cabinet selon sous-choix. |
| Si cession : type de cabinet | `cabinet_medical`, `cabinet_dentaire`, `aucun` | Sélectionne les actes/compromis médicaux ou dentaires. |

Règle de cohérence : `cabinet_medical` ou `cabinet_dentaire` ne peut être actif que si `cession = oui`. Si `cession = non`, le type de cabinet doit être `aucun`.

Point d'attention source : la V2 fournie contient une anomalie de libellé autour de la ligne des statuts médecins. Le fichier source pointe vers le modèle médecins ; la qualification produit conserve donc le choix `medecin` demandé par le ticket et déjà présent dans le catalogue.

## B. Documents attendus par bloc

| Bloc | Documents attendus |
|---|---|
| Documents communs dans tous les cas | Déclaration sur l'honneur de non-condamnation ; Autorisation de domiciliation ; Procuration. |
| Documents SELARL de base | PV nomination gérant ; Demande d'inscription à l'ordre. |
| Documents chirurgien-dentiste | Statuts SELARL chirurgien-dentiste. |
| Documents médecin | Statuts SELARL médecin. |
| Documents site distinct | Formulaire de déclaration préalable de site distinct CD94 avec la SEL, manuel. |
| Documents SCM cession | PV AGE cession part SCM ; Courrier SDE cession SCM ; Acte de cession des parts de la SCM vers SELARL. |
| Documents régime communautaire | Lettre de renonciation à revendiquer la qualité d'associé ; Lettre d'avertissement au conjoint. |
| Documents dérogation | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL ; Dérogation SEL BNC manuelle ; Demande de dérogation cumul SELARL BNC. |
| Documents cession | Avenant contrat de bail ; Appel de fonds SEL. |
| Documents cabinet médical | Acte de cession d'un cabinet médical ; Compromis de cession d'un cabinet médical. |
| Documents cabinet dentaire | Acte de cession d'un cabinet dentaire ; Compromis de cession d'un cabinet dentaire. |

## C. Documents et variables par document

| Bloc métier | Document | Fichier source | DOC | Statut | Variables nécessaires | Bloc UI principal |
|---|---|---|---|---|---|---|
| Commun | Déclaration sur l'honneur de non-condamnation | `Declaration sur l'honneur de non condamnation.docx` | `DOC-001` | générable | `signataire`, `signataire.adresse_personnelle`, `signature` | Professionnel / gérant ; Signature |
| Commun | Autorisation de domiciliation | `Autorisation de domiciliation.docx` | `DOC-002` | générable | `signataire`, `societe`, `domiciliation.adresse_affichee`, `signature` | Société ; Siège social ; Signature |
| Commun | Procuration | `Procuration.docx` | `DOC-003` | générable | `signataire`, `societe`, `societe.siege`, `signature` | Mandataire / signataire ; Société |
| SELARL base | PV nomination gérant | `PV nomination gerant.docx` | `DOC-004` | générable | `societe`, `associes[]`, `dirigeant_nomine`, `decision`, `reunion`, `capital`, `emprunt`, `bien_immobilier`, `signature` | Société ; Associés ; Professionnel / gérant ; Banque / financement |
| SELARL base | Demande d'inscription à l'ordre | `Demande d'inscription a l'ordre.docx` | `DOC-034` | générable | `signataire`, `societe`, `ordre`, `mandataire`, `signature`, `dossier.options.derogation` | Ordre professionnel ; Mandataire / signataire |
| Chirurgien-dentiste | Statuts SELARL chirurgien-dentiste | `Modele statuts SELARL chirurgien dentiste sans communaute.docx` | `DOC-016` | générable | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` | Société ; Associés ; Professionnel / gérant |
| Médecin | Statuts SELARL médecin | `Modele statuts SELARL medecins.docx` | `DOC-017` | générable | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` | Société ; Associés ; Professionnel / gérant |
| Site distinct | Formulaire de déclaration préalable de site distinct CD94 avec la SEL | `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` | aucun | manuel | Données ordinales et site distinct, à confirmer par juriste avant automatisation | Ordre professionnel ; Conditions spécifiques |
| SCM cession | PV AGE cession part SCM | `PV AGE cession part SCM.docx` | `DOC-031` | générable | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.associes_*[]`, `signature` | SCM |
| SCM cession | Courrier SDE cession SCM | `Courrier SDE.docx` | `DOC-032` | générable | `scm_cession`, `scm_cession.enregistrement`, `scm_cession.signataire_sde`, `signature` | SCM ; Signature |
| SCM cession | Acte de cession des parts de la SCM vers SELARL | `Acte de cession des parts de la SCM a la SELARL.docx` | `DOC-033` | générable | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.cedant`, `scm_cession.prix`, `signature` | SCM |
| Régime communautaire | Lettre de renonciation à revendiquer la qualité d'associé | `Lettre de renonciation a revendiquer la qualite d'associe.docx` | `DOC-005` | générable | `signataire`, `conjoint`, `societe`, `apport`, `regime_communautaire.renonciation`, `signature` | Régime matrimonial / conjoint |
| Régime communautaire | Lettre d'avertissement au conjoint | `Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.docx` | `DOC-006` | générable | `signataire`, `conjoint`, `societe`, `apport`, `regime_communautaire.avertissement`, `signature` | Régime matrimonial / conjoint |
| Dérogation | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL | `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx` | `DOC-013` | générable comme formulaire à compléter | `derogation`, `site_declare`, `sites_existants[]`, `societe`, `signature` | Ordre professionnel ; Conditions spécifiques |
| Dérogation | Dérogation SEL BNC | non précisé dans la source V2 | aucun | manuel | Pièce manuelle ; zones narratives sensibles | Conditions spécifiques |
| Dérogation | Demande de dérogation cumul SELARL BNC | `Demande de derogation cumul SELARL - BNC.docx` | `DOC-014` | générable comme formulaire à compléter | `derogation`, `societe`, `signature` | Conditions spécifiques |
| Cession | Avenant contrat de bail | `Avenant Contrat de bail.docx` | `DOC-007` | générable | `bail`, `societe`, `cession.cabinet`, `signature` | Bail ; Cession de cabinet |
| Cession | Appel de fonds SEL | `appel de fond sel.docx` | `DOC-008` | générable | `societe`, `cession.financement`, `cession.vendeur`, `cession.acquereur`, `signature` | Banque / financement ; Cession de cabinet |
| Cabinet médical | Acte de cession d'un cabinet médical | `Acte de cession d_un cabinet medical.docx` | `DOC-009` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` | Cession de cabinet |
| Cabinet médical | Compromis de cession d'un cabinet médical | `Compromis de cession d_un cabinet medical.docx` | `DOC-010` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` | Cession de cabinet |
| Cabinet dentaire | Acte de cession d'un cabinet dentaire | `Acte de cession d'un cabinet dentaire.docx` | `DOC-011` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` | Cession de cabinet |
| Cabinet dentaire | Compromis de cession d'un cabinet dentaire | `Compromis de cession d_un cabinet dentaire.docx` | `DOC-012` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` | Cession de cabinet |

## Documents hors flux SELARL pilote

- `Demande de dérogation cumul SELARL salariée` n'est pas dans le flux SELARL pilote V2 ; elle est rattachée au chemin SELAS dans le catalogue et reste non implémentée.
- `PV d'autorisation d'emprunt` n'apparaît pas comme document autonome dans la source V2 ni dans le catalogue SELARL. L'emprunt est une branche conditionnelle du `DOC-004` PV nomination gérant, pilotée par `emprunt.actif`.

## Points d'ambiguïté à valider

- Confirmer le libellé source de la ligne statuts médecin dans la V2.
- Confirmer si le formulaire site distinct CD94 doit rester seulement manuel dans l'Assistant ou être prérempli dans une phase ultérieure.
- Confirmer si `DOC-013` et `DOC-014` doivent rester visibles comme formulaires à compléter ou devenir des documents finalisés.
- Confirmer le périmètre d'appel de fonds SEL pour les cessions non dentaires, car le moteur V1 le limite historiquement.
