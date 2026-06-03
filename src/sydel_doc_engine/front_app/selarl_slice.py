from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Final

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    generate_docx_files_for_document_codes,
    generate_zip_file,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Associe,
    CapitalContext,
    CessionBanque,
    Company,
    CompanyInscriptionOrdre,
    DecisionContext,
    DepotFonds,
    DirigeantNomine,
    DocumentContext,
    DocumentGenerationContext,
    DocumentSignataire,
    Domiciliation,
    DossierOptions,
    Emprunt,
    ExerciceLieu,
    ExerciceSocial,
    GeranceContext,
    Mandataire,
    OrdreAddress,
    OrdreProfessionnel,
    Person,
    RegimeCommunautaire,
    RegimeCommunautaireAvertissement,
    RegimeCommunautaireRenonciation,
    ReunionContext,
    ReunionPresident,
    Signature,
    SpfplConjoint,
    SpfplOrdre,
    StatutsSel,
)
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_CABINET,
    DEFAULT_MANDATAIRE_CIVILITE,
    DEFAULT_MANDATAIRE_FONCTION,
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE,
    DEFAULT_SEUIL_ACHAT_MATERIEL,
    DEFAULT_SEUIL_EMPRUNT,
    DEFAULT_TITRE_AFFICHAGE,
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    number_words_from_value,
)
from sydel_doc_engine.front_data import AddressUsage, BusinessRole, build_document_status_for_code

SELARL_V1_BASE_DOC_CODES: Final = (
    "DOC-001",
    "DOC-002",
    "DOC-003",
    "DOC-004",
    "DOC-034",
)
SELARL_V1_MEDECIN_STATUTS_CODE: Final = "DOC-017"
SELARL_V1_DENTISTE_STATUTS_CODE: Final = "DOC-016"
SELARL_V1_REGIME_RENONCIATION_CODE: Final = "DOC-005"
SELARL_V1_REGIME_AVERTISSEMENT_CODE: Final = "DOC-006"

PROFESSION_MEDECIN: Final = "medecin"
PROFESSION_DENTISTE: Final = "chirurgien_dentiste"
SELARL_V1_PROFESSIONS: Final = (PROFESSION_MEDECIN, PROFESSION_DENTISTE)

FRONT_DATA_ROLE_SCOPE: Final = (
    BusinessRole.PRATICIEN.value,
    BusinessRole.ASSOCIE.value,
    BusinessRole.GERANT.value,
    BusinessRole.SIGNATAIRE.value,
    BusinessRole.MANDATAIRE.value,
    BusinessRole.CONJOINT.value,
    BusinessRole.ORDRE_PROFESSIONNEL.value,
    BusinessRole.BANQUE.value,
)
FRONT_DATA_ADDRESS_SCOPE: Final = (
    AddressUsage.DOMICILE_PRATICIEN.value,
    AddressUsage.SIEGE_SOCIAL.value,
    AddressUsage.DOMICILIATION.value,
    AddressUsage.LIEU_EXERCICE.value,
    AddressUsage.ORDRE.value,
    AddressUsage.BANQUE.value,
)


@dataclass(frozen=True)
class SelarlDocumentRow:
    doc_code: str
    label: str
    status: str
    message: str


@dataclass(frozen=True)
class SelarlAdditionalAssocieInput:
    civilite: str = ""
    prenom: str = ""
    nom: str = ""
    nb_parts: int = 0


@dataclass(frozen=True)
class SelarlSliceInput:
    dossier_type_key: str
    dossier_reference: str = ""
    profession: str = PROFESSION_MEDECIN
    dossier_unipersonnel: bool = True
    multi_associes_doc004_limited: bool = False
    dentist_multi_associes_statuts_partial: bool = False
    regime_communautaire: bool = False
    derogation: bool = False
    site_distinct: bool = False
    cession: bool = False
    scm: bool = False
    civilite: str = ""
    genre: Gender = Gender.MASCULIN
    prenom: str = ""
    nom: str = ""
    titre_affichage: str = DEFAULT_TITRE_AFFICHAGE
    date_naissance: date | None = None
    ville_naissance: str = ""
    ville_naissance_article_au: bool = False
    departement_naissance: str = ""
    nationalite: str = ""
    nom_pere: str = ""
    nom_mere: str = ""
    adresse_num_voie: str = ""
    adresse_voie: str = ""
    adresse_cp: str = ""
    adresse_ville: str = ""
    situation_maritale: str = ""
    regime_matrimonial: str = ""
    numero_ordre: str = ""
    numero_rpps: str = ""
    departement_ordre: str = ""
    denomination: str = ""
    capital_social: str = ""
    capital_social_lettres: str = ""
    duree: str = "99 ans"
    nb_parts_total: int = 0
    associe_principal_nb_parts: int = 0
    additional_associes: tuple[SelarlAdditionalAssocieInput, ...] = ()
    president_seance_associe_index: int = 0
    nb_parts_total_lettres: str = ""
    valeur_nominale_part: str = ""
    valeur_nominale_part_lettres: str = ""
    siege_num_voie: str = ""
    siege_voie: str = ""
    siege_cp: str = ""
    siege_ville: str = ""
    ville_rcs: str = ""
    ordre_conseil: str = ""
    ordre_adresse_ligne_1: str = ""
    ordre_cp: str = ""
    ordre_ville: str = ""
    mandataire_civilite: str = DEFAULT_MANDATAIRE_CIVILITE
    mandataire_prenom: str = DEFAULT_MANDATAIRE_PRENOM
    mandataire_nom: str = DEFAULT_MANDATAIRE_NOM
    mandataire_fonction: str = DEFAULT_MANDATAIRE_FONCTION
    mandataire_cabinet: str = DEFAULT_MANDATAIRE_CABINET
    signature_lieu: str = ""
    signature_date: date | None = None
    signature_nombre_exemplaires: str = "quatre"
    prestataire_signature_electronique: str = DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE
    decision_date: date | None = None
    reunion_date_lettres: str = ""
    depot_banque_nom: str = ""
    depot_banque_adresse: str = ""
    exercice_debut: str = ""
    exercice_fin: str = ""
    exercice_cloture_premier: str = ""
    lieu_exercice_adresse: str = ""
    seuil_achat_materiel: str = DEFAULT_SEUIL_ACHAT_MATERIEL
    seuil_emprunt: str = DEFAULT_SEUIL_EMPRUNT
    conjoint_civilite: str = ""
    conjoint_genre: Gender = Gender.FEMININ
    conjoint_prenom: str = ""
    conjoint_nom: str = ""
    qualite_renoncee: str = "associe"
    date_courrier_avertissement: date | None = None

    @property
    def has_any_value(self) -> bool:
        return any(
            value.strip()
            for value in (
                self.dossier_reference,
                self.prenom,
                self.nom,
                self.denomination,
                self.capital_social,
                self.numero_ordre,
            )
        )


@dataclass(frozen=True)
class SelarlSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    document_rows: tuple[SelarlDocumentRow, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.selarl_slice"


def selected_selarl_document_codes(data: SelarlSliceInput) -> tuple[str, ...]:
    if data.dentist_multi_associes_statuts_partial:
        return ("DOC-004", SELARL_V1_DENTISTE_STATUTS_CODE)
    if data.multi_associes_doc004_limited:
        return ("DOC-004",)
    codes = [*SELARL_V1_BASE_DOC_CODES, _statuts_code(data.profession)]
    if data.regime_communautaire:
        codes.extend(
            (
                SELARL_V1_REGIME_RENONCIATION_CODE,
                SELARL_V1_REGIME_AVERTISSEMENT_CODE,
            )
        )
    return tuple(codes)


def build_selarl_plan(data: SelarlSliceInput) -> SelarlSlicePlan:
    blockers = validate_selarl_input(data)
    warnings = _warning_messages(data)
    document_codes = selected_selarl_document_codes(data)
    rows = _document_rows(data, blockers)

    if blockers:
        return SelarlSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            document_rows=rows,
            blockers=blockers,
            warnings=warnings,
        )
    return SelarlSlicePlan(
        can_generate=True,
        status="ready",
        reason=(
            "Pret pour generation dentiste multi-associes PARTIAL."
            if data.dentist_multi_associes_statuts_partial
            else "Pret pour generation DOC-004 multi-associes limite."
            if data.multi_associes_doc004_limited
            else "Pret pour generation SELARL V1 bornee."
        ),
        document_codes=document_codes,
        document_rows=rows,
        blockers=(),
        warnings=warnings,
    )


def validate_selarl_input(data: SelarlSliceInput) -> tuple[str, ...]:
    if data.dentist_multi_associes_statuts_partial:
        return _validate_dentist_multi_associes_statuts_partial_input(data)
    if data.multi_associes_doc004_limited:
        return _validate_multi_associes_doc004_input(data)

    blockers: list[str] = []
    if data.profession not in SELARL_V1_PROFESSIONS:
        blockers.append("Profession hors perimetre SELARL V1.")
    if not data.dossier_unipersonnel:
        blockers.append("La V1 ne couvre que le dossier unipersonnel.")
    if data.derogation:
        blockers.append("Derogations hors perimetre V1 : aucun DOC-013/DOC-014 genere.")
    if data.site_distinct:
        blockers.append("Site distinct hors perimetre V1 : traitement manuel requis.")
    if data.cession:
        blockers.append("Cession hors perimetre V1.")
    if data.scm:
        blockers.append("SCM hors perimetre V1.")

    blockers.extend(_missing_text_blockers(data))
    if data.date_naissance is None:
        blockers.append("Date de naissance du praticien requise.")
    if data.signature_date is None:
        blockers.append("Date de signature requise.")
    if data.decision_date is None:
        blockers.append("Date de decision requise.")
    if data.nb_parts_total < 1:
        blockers.append("Nombre de parts requis et superieur a zero.")
    if data.profession == PROFESSION_DENTISTE:
        blockers.extend(
            _missing_for_fields(
                data,
                (
                    ("conjoint_civilite", "Civilite du conjoint requise pour DOC-016."),
                    ("conjoint_prenom", "Prenom du conjoint requis pour DOC-016."),
                    ("conjoint_nom", "Nom du conjoint requis pour DOC-016."),
                ),
            )
        )
    if data.regime_communautaire:
        blockers.extend(
            _missing_for_fields(
                data,
                (
                    ("conjoint_civilite", "Civilite du conjoint requise pour DOC-005."),
                    ("conjoint_prenom", "Prenom du conjoint requis pour DOC-005."),
                    ("conjoint_nom", "Nom du conjoint requis pour DOC-005."),
                    (
                        "regime_matrimonial",
                        "Regime matrimonial requis quand DOC-005 est genere.",
                    ),
                ),
            )
        )
    return tuple(dict.fromkeys(blockers))


def _validate_dentist_multi_associes_statuts_partial_input(
    data: SelarlSliceInput,
) -> tuple[str, ...]:
    blockers = list(_validate_multi_associes_doc004_input(data))
    if data.profession != PROFESSION_DENTISTE:
        blockers.append(
            "Le sous-cas statuts multi-associes PARTIAL est limite au chirurgien-dentiste."
        )
    if data.regime_communautaire:
        blockers.append(
            "Regime communautaire hors perimetre du sous-cas dentiste multi-associes PARTIAL."
        )
    blockers.extend(_missing_text_blockers(data))
    blockers.extend(
        _missing_for_fields(
            data,
            (
                ("conjoint_civilite", "Civilite du conjoint requise pour DOC-016."),
                ("conjoint_prenom", "Prenom du conjoint requis pour DOC-016."),
                ("conjoint_nom", "Nom du conjoint requis pour DOC-016."),
            ),
        )
    )
    return tuple(dict.fromkeys(blockers))


def _validate_multi_associes_doc004_input(data: SelarlSliceInput) -> tuple[str, ...]:
    blockers: list[str] = []
    if data.profession not in SELARL_V1_PROFESSIONS:
        blockers.append("Profession hors perimetre SELARL DOC-004 limite.")
    if data.regime_communautaire:
        blockers.append("Regime communautaire hors perimetre du sous-cas DOC-004 limite.")
    if data.derogation:
        blockers.append("Derogations hors perimetre du sous-cas DOC-004 limite.")
    if data.site_distinct:
        blockers.append("Site distinct hors perimetre du sous-cas DOC-004 limite.")
    if data.cession:
        blockers.append("Cession hors perimetre du sous-cas DOC-004 limite.")
    if data.scm:
        blockers.append("SCM hors perimetre du sous-cas DOC-004 limite.")

    blockers.extend(_missing_doc004_text_blockers(data))
    if data.date_naissance is None:
        blockers.append("Date de naissance du gerant unique requise pour DOC-004.")
    if data.signature_date is None:
        blockers.append("Date de signature requise pour DOC-004.")
    if data.decision_date is None:
        blockers.append("Date de decision requise pour DOC-004.")
    if data.nb_parts_total < 1:
        blockers.append("Nombre total de parts requis et superieur a zero pour DOC-004.")
    if data.associe_principal_nb_parts < 1:
        blockers.append("Parts de l'associe gerant requises et superieures a zero.")
    if not data.additional_associes:
        blockers.append("Au moins un deuxieme associe est requis pour le sous-cas multi-associes.")

    associes = _doc004_associe_parts(data)
    if len(associes) < 2:
        blockers.append("Le sous-cas DOC-004 limite exige au moins deux associes.")
    for index, associe in enumerate(data.additional_associes, start=2):
        if not associe.civilite.strip():
            blockers.append(f"Civilite de l'associe {index} requise.")
        if not associe.prenom.strip():
            blockers.append(f"Prenom de l'associe {index} requis.")
        if not associe.nom.strip():
            blockers.append(f"Nom de l'associe {index} requis.")
        if associe.nb_parts < 1:
            blockers.append(f"Parts de l'associe {index} requises et superieures a zero.")

    if associes and sum(associes) != data.nb_parts_total:
        blockers.append(
            "La somme des parts des associes doit correspondre au nombre total de parts."
        )
    if not 0 <= data.president_seance_associe_index < max(len(associes), 1):
        blockers.append("President de seance invalide : choisir un associe existant.")
    return tuple(dict.fromkeys(blockers))


def _is_multi_associes_simple(data: SelarlSliceInput) -> bool:
    return data.multi_associes_doc004_limited or data.dentist_multi_associes_statuts_partial


def _doc004_associe_parts(data: SelarlSliceInput) -> list[int]:
    return [
        data.associe_principal_nb_parts,
        *(associe.nb_parts for associe in data.additional_associes),
    ]


def _missing_doc004_text_blockers(data: SelarlSliceInput) -> list[str]:
    doc004_fields = (
        ("dossier_reference", "Reference dossier requise."),
        ("civilite", "Civilite du gerant unique requise."),
        ("prenom", "Prenom du gerant unique requis."),
        ("nom", "Nom du gerant unique requis."),
        ("ville_naissance", "Ville de naissance du gerant unique requise."),
        ("departement_naissance", "Departement de naissance du gerant unique requis."),
        ("nationalite", "Nationalite du gerant unique requise."),
        ("adresse_num_voie", "Numero de voie du gerant unique requis."),
        ("adresse_voie", "Voie du gerant unique requise."),
        ("adresse_cp", "Code postal du gerant unique requis."),
        ("adresse_ville", "Ville du gerant unique requise."),
        ("denomination", "Denomination sociale requise."),
        ("capital_social", "Capital social requis."),
        ("siege_num_voie", "Numero de voie du siege requis."),
        ("siege_voie", "Voie du siege requise."),
        ("siege_cp", "Code postal du siege requis."),
        ("siege_ville", "Ville du siege requise."),
        ("signature_lieu", "Lieu de signature requis."),
    )
    return _missing_for_fields(data, doc004_fields)


def build_generation_context(data: SelarlSliceInput) -> DocumentGenerationContext:
    person_address = _address(
        data.adresse_num_voie,
        data.adresse_voie,
        data.adresse_cp,
        data.adresse_ville,
    )
    company_address = _address(
        data.siege_num_voie,
        data.siege_voie,
        data.siege_cp,
        data.siege_ville,
    )
    capital_social_lettres = data.capital_social_lettres or number_words_from_value(
        data.capital_social
    )
    nb_parts_total_lettres = data.nb_parts_total_lettres or number_words_from_value(
        data.nb_parts_total
    )
    valeur_nominale_part = data.valeur_nominale_part or calculate_nominal_value(
        data.capital_social,
        data.nb_parts_total,
    )
    valeur_nominale_part_lettres = (
        data.valeur_nominale_part_lettres or number_words_from_value(valeur_nominale_part)
    )
    reunion_date_lettres = data.reunion_date_lettres or date_to_french_words(data.decision_date)
    signature_prestataire = (
        data.prestataire_signature_electronique
        or DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE
    )
    seuil_achat_materiel = data.seuil_achat_materiel or DEFAULT_SEUIL_ACHAT_MATERIEL
    seuil_emprunt = data.seuil_emprunt or DEFAULT_SEUIL_EMPRUNT
    profession_label = _profession_label(data.profession)
    profession_plural = _profession_plural(data.profession)
    associes = _context_associes(data, person_address, profession_label, profession_plural)
    reunion_president = _reunion_president(data, associes)
    person = Person(
        genre=data.genre,
        civilite=data.civilite,
        prenom=data.prenom,
        nom=data.nom,
        titre_affichage=data.titre_affichage,
        adresse_personnelle_affichee=person_address.adresse_affichee,
        adresse_perso=person_address,
        date_naissance=data.date_naissance,
        ville_naissance=data.ville_naissance,
        ville_naissance_article_au=data.ville_naissance_article_au,
        nationalite=data.nationalite,
        nom_pere=data.nom_pere,
        nom_mere=data.nom_mere,
        fonction_dirigeant="gérant",
        numero_inscription_ordre=data.numero_ordre,
        qualification_principale=profession_label,
    )
    company = Company(
        forme_sociale="SELARL",
        forme_sociale_affichage="SELARL",
        forme_sociale_libelle_long="Societe d'exercice liberal a responsabilite limitee",
        forme_sociale_complete="societe d'exercice liberal a responsabilite limitee",
        forme_sociale_abregee="SELARL",
        denomination=data.denomination,
        denomination_courte=data.denomination,
        capital=data.capital_social,
        capital_social=data.capital_social,
        capital_social_lettres=capital_social_lettres,
        capital_variable=True,
        duree=data.duree,
        siege=company_address,
        ville_rcs=data.ville_rcs,
        nb_parts_total=data.nb_parts_total,
        inscription_ordre=CompanyInscriptionOrdre(
            departement=data.departement_ordre,
            ville=data.ordre_ville,
            numero=data.numero_ordre,
        ),
    )
    conjoint = _conjoint_person(data, person_address) if _needs_conjoint(data) else None
    return DocumentGenerationContext(
        structure="SELARL",
        dossier_options=DossierOptions(
            regime_communautaire=data.regime_communautaire,
            associe_unique=not _is_multi_associes_simple(data),
            derogation=False,
            site_distinct=False,
            cession=False,
            scm_cession=False,
        ),
        personne_signataire=person,
        conjoint=conjoint,
        signature=Signature(
            lieu=data.signature_lieu,
            date=_required_date(data.signature_date, "signature_date"),
            nombre_exemplaires=data.signature_nombre_exemplaires,
            prestataire_signature_electronique=signature_prestataire,
        ),
        societe=company,
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=company_address.adresse_affichee,
        ),
        ordre=_ordre(data, profession_label, profession_plural),
        mandataire=Mandataire(
            civilite_affichage=data.mandataire_civilite or DEFAULT_MANDATAIRE_CIVILITE,
            prenom=data.mandataire_prenom or DEFAULT_MANDATAIRE_PRENOM,
            nom=data.mandataire_nom or DEFAULT_MANDATAIRE_NOM,
            fonction=data.mandataire_fonction or DEFAULT_MANDATAIRE_FONCTION,
            cabinet=data.mandataire_cabinet or DEFAULT_MANDATAIRE_CABINET,
        ),
        associes=associes,
        dirigeant_nomine=DirigeantNomine(
            genre=data.genre,
            civilite_affichage=data.civilite,
            prenom=data.prenom,
            nom=data.nom,
            date_naissance=data.date_naissance,
            ville_naissance=data.ville_naissance,
            departement_naissance=data.departement_naissance,
            nationalite=data.nationalite,
            adresse_personnelle=person_address,
            fonction_affichage="gérant",
            ref_associe_index=0,
        ),
        decision=DecisionContext(date=_display_date(data.decision_date)),
        reunion=ReunionContext(
            date_lettres=reunion_date_lettres,
            president=reunion_president,
        ),
        capital=CapitalContext(
            nb_parts_total=data.nb_parts_total,
            valeur_nominale_part=valeur_nominale_part,
            nb_parts_representees=data.nb_parts_total,
            montant=data.capital_social,
            montant_lettres=capital_social_lettres,
            nombre_titres_total=data.nb_parts_total,
            nombre_titres_total_lettres=nb_parts_total_lettres,
            valeur_nominale_titre=valeur_nominale_part,
            valeur_nominale_titre_lettres=valeur_nominale_part_lettres,
            type_titre="parts sociales",
        ),
        gerance=GeranceContext(
            seuil_achat_materiel=seuil_achat_materiel,
            seuil_emprunt=seuil_emprunt,
        ),
        apport=Apport(
            montant=data.capital_social,
            montant_lettres=capital_social_lettres,
        ),
        regime_communautaire=_regime_communautaire(data),
        statuts_sel=StatutsSel(
            overlay=_statuts_overlay(data.profession),
            profession=profession_label,
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom=data.depot_banque_nom,
                adresse_affichee=data.depot_banque_adresse,
            ),
            montant=data.capital_social,
        ),
        exercice_social=ExerciceSocial(
            debut=data.exercice_debut,
            fin=data.exercice_fin,
            date_cloture_premier_exercice=data.exercice_cloture_premier,
            lieux=(
                ExerciceLieu(
                    adresse_affichee=data.lieu_exercice_adresse
                    or company_address.adresse_affichee
                ),
            ),
        ),
        document=DocumentContext(
            nombre_exemplaires_lettres=data.signature_nombre_exemplaires,
            signataire=DocumentSignataire(prenom=data.prenom, nom=data.nom),
        ),
        emprunt=Emprunt(actif=False),
        metadata={
            "front_slice": "track_b_selarl_v1",
            "dossier_reference": data.dossier_reference,
            "selarl_dentiste_multi_associes_statuts_partial": (
                "true" if data.dentist_multi_associes_statuts_partial else "false"
            ),
        },
    )


def generate_selarl_dossier(data: SelarlSliceInput, output_dir: Path) -> GeneratedDossier:
    plan = build_selarl_plan(data)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(data)
    docx_paths = generate_docx_files_for_document_codes(
        ctx,
        output_dir,
        plan.document_codes,
    )
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def front_data_scope_summary() -> tuple[str, ...]:
    return (
        "roles=" + ", ".join(FRONT_DATA_ROLE_SCOPE),
        "adresses=" + ", ".join(FRONT_DATA_ADDRESS_SCOPE),
    )


def _document_rows(
    data: SelarlSliceInput,
    blockers: tuple[str, ...],
) -> tuple[SelarlDocumentRow, ...]:
    generated_status = "blocked" if blockers else "generable"
    if data.dentist_multi_associes_statuts_partial:
        return (
            SelarlDocumentRow(
                doc_code="DOC-004",
                label=build_document_status_for_code("DOC-004").doc_label,
                status=generated_status,
                message=(
                    "PV multi-associes simple : gerant unique, unanimite totale."
                    if not blockers
                    else "Bloque par donnees ou scope du sous-cas multi-associes."
                ),
            ),
            SelarlDocumentRow(
                doc_code="DOC-016",
                label=build_document_status_for_code("DOC-016").doc_label,
                status="partial" if not blockers else "blocked",
                message=(
                    "Statuts dentiste multi-associes PARTIAL : apports/capital/repartition "
                    "cables, lock complet non revendique."
                    if not blockers
                    else "Bloque par donnees requises pour DOC-016."
                ),
            ),
            SelarlDocumentRow(
                doc_code="DOC-001/DOC-002/DOC-003/DOC-034",
                label="Pack SELARL unipersonnel",
                status="hors_scope",
                message="Non generes dans ce sous-cas statuts PARTIAL.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-005/DOC-006",
                label="Regime communautaire",
                status="hors_scope",
                message="Non couvert par le sous-cas dentiste multi-associes simple.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-031/DOC-032/DOC-033",
                label="Cession / SCM",
                status="hors_scope",
                message="Cession et SCM restent hors perimetre.",
            ),
        )
    if data.multi_associes_doc004_limited:
        return (
            SelarlDocumentRow(
                doc_code="DOC-004",
                label=build_document_status_for_code("DOC-004").doc_label,
                status=generated_status,
                message=(
                    "PV multi-associes limite : gerant unique, unanimite totale."
                    if not blockers
                    else "Bloque par donnees ou scope du sous-cas DOC-004 limite."
                ),
            ),
            SelarlDocumentRow(
                doc_code="DOC-016/DOC-017",
                label="Statuts SELARL multi-associes",
                status="hors_scope",
                message="Non generes : statuts multi-associes non verrouilles.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-001/DOC-002/DOC-003/DOC-034",
                label="Pack SELARL unipersonnel",
                status="hors_scope",
                message="Non generes dans ce sous-cas limite a DOC-004.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-005/DOC-006",
                label="Regime communautaire",
                status="hors_scope",
                message="Non couvert par le sous-cas DOC-004 multi-associes limite.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-031/DOC-032/DOC-033",
                label="Cession / SCM",
                status="hors_scope",
                message="Cession et SCM restent hors perimetre.",
            ),
        )

    rows = [
        SelarlDocumentRow(
            doc_code=code,
            label=build_document_status_for_code(code).doc_label,
            status=generated_status,
            message="Inclus dans SELARL V1." if not blockers else "Bloque par donnees ou scope.",
        )
        for code in selected_selarl_document_codes(data)
    ]
    if not data.regime_communautaire:
        rows.append(
            SelarlDocumentRow(
                doc_code=SELARL_V1_REGIME_AVERTISSEMENT_CODE,
                label=build_document_status_for_code(
                    SELARL_V1_REGIME_AVERTISSEMENT_CODE
                ).doc_label,
                status="hors_v1",
                message="Non genere : document conditionnel du regime communautaire.",
            )
        )
    rows.extend(
        (
            SelarlDocumentRow(
                doc_code="DOC-013/DOC-014",
                label="Derogations",
                status="hors_v1",
                message="Manuel / hors perimetre SELARL V1.",
            ),
            SelarlDocumentRow(
                doc_code="DOC-031/DOC-032/DOC-033",
                label="SCM et cession de parts SCM",
                status="hors_v1",
                message="Non expose dans cette slice.",
            ),
        )
    )
    return tuple(rows)


def _warning_messages(data: SelarlSliceInput) -> tuple[str, ...]:
    if data.dentist_multi_associes_statuts_partial:
        return (
            "Sous-cas limite : DOC-004 LOCKED et DOC-016 dentiste PARTIAL.",
            "Statuts multi-associes complets, plusieurs gerants, president externe, "
            "cession, SCM et votes non unanimes restent hors scope.",
            "Le president de seance doit etre choisi parmi les associes existants.",
        )
    if data.multi_associes_doc004_limited:
        return (
            "Sous-cas limite : generation de DOC-004 uniquement.",
            "Statuts multi-associes, plusieurs gerants, cession, SCM et votes non "
            "unanimes restent hors scope.",
            "Le president de seance doit etre choisi parmi les associes existants.",
        )
    warnings = [
        "SELARL V1 bornee : creation medecin ou chirurgien-dentiste, associe unique uniquement.",
    ]
    if data.regime_communautaire:
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
    return tuple(warnings)


def _missing_text_blockers(data: SelarlSliceInput) -> list[str]:
    base_fields = (
        ("dossier_reference", "Reference dossier requise."),
        ("civilite", "Civilite du praticien requise."),
        ("prenom", "Prenom du praticien requis."),
        ("nom", "Nom du praticien requis."),
        ("titre_affichage", "Titre d'affichage du signataire requis."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("nom_pere", "Nom du pere requis pour DOC-001."),
        ("nom_mere", "Nom de la mere requis pour DOC-001."),
        ("adresse_num_voie", "Numero de voie du praticien requis."),
        ("adresse_voie", "Voie du praticien requise."),
        ("adresse_cp", "Code postal du praticien requis."),
        ("adresse_ville", "Ville du praticien requise."),
        ("situation_maritale", "Situation matrimoniale requise pour les statuts."),
        ("regime_matrimonial", "Regime matrimonial requis pour les statuts."),
        ("numero_ordre", "Numero d'inscription a l'ordre requis."),
        ("numero_rpps", "Numero RPPS requis pour les statuts."),
        ("departement_ordre", "Departement d'inscription a l'ordre requis."),
        ("denomination", "Denomination sociale requise."),
        ("capital_social", "Capital social requis."),
        ("siege_num_voie", "Numero de voie du siege requis."),
        ("siege_voie", "Voie du siege requise."),
        ("siege_cp", "Code postal du siege requis."),
        ("siege_ville", "Ville du siege requise."),
        ("ville_rcs", "Ville RCS requise."),
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise."),
        ("ordre_cp", "Code postal de l'ordre requis."),
        ("ordre_ville", "Ville de l'ordre requise."),
        ("signature_lieu", "Lieu de signature requis."),
        ("depot_banque_nom", "Banque du depot des fonds requise."),
        ("depot_banque_adresse", "Adresse de la banque requise."),
        ("exercice_debut", "Debut d'exercice social requis."),
        ("exercice_fin", "Fin d'exercice social requise."),
        ("exercice_cloture_premier", "Date de cloture du premier exercice requise."),
    )
    return _missing_for_fields(data, base_fields)


def _missing_for_fields(
    data: SelarlSliceInput,
    fields: tuple[tuple[str, str], ...],
) -> list[str]:
    blockers = []
    for field_name, message in fields:
        value = getattr(data, field_name)
        if isinstance(value, str) and not value.strip():
            blockers.append(message)
    return blockers


def _required_date(value: date | None, field_name: str) -> date:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire.")
    return value


def _display_date(value: date | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


def _address(num_voie: str, voie: str, cp: str, ville: str) -> Address:
    display = f"{num_voie} {voie}, {cp} {ville}".strip()
    return Address(
        num_voie=num_voie,
        voie=voie,
        cp=cp,
        ville=ville,
        adresse_affichee=display,
    )


def _statuts_code(profession: str) -> str:
    if profession == PROFESSION_DENTISTE:
        return SELARL_V1_DENTISTE_STATUTS_CODE
    return SELARL_V1_MEDECIN_STATUTS_CODE


def _statuts_overlay(profession: str) -> str:
    if profession == PROFESSION_DENTISTE:
        return "selarl_dentiste"
    return "selarl_medecin"


def _profession_label(profession: str) -> str:
    if profession == PROFESSION_DENTISTE:
        return "chirurgien-dentiste"
    return "medecin"


def _profession_plural(profession: str) -> str:
    if profession == PROFESSION_DENTISTE:
        return "chirurgiens-dentistes"
    return "medecins"


def _ordre(
    data: SelarlSliceInput,
    profession_label: str,
    profession_plural: str,
) -> OrdreProfessionnel:
    return OrdreProfessionnel(
        conseil_departemental_libelle=data.ordre_conseil,
        departement_inscription=data.departement_ordre,
        destinataire_appel="Monsieur le President",
        profession_signataire_affichee=profession_label,
        profession_ligne_destinataire=profession_plural,
        profession_reglementee_pluriel=profession_plural,
        adresse_affichee=f"{data.ordre_adresse_ligne_1}\n{data.ordre_cp} {data.ordre_ville}",
        adresse_bloc_affiche=(
            f"{data.ordre_adresse_ligne_1}\n{data.ordre_cp} {data.ordre_ville}"
        ),
        adresse=OrdreAddress(
            ligne_1=data.ordre_adresse_ligne_1,
            cp=data.ordre_cp,
            ville=data.ordre_ville,
        ),
    )


def _context_associes(
    data: SelarlSliceInput,
    address: Address,
    profession_label: str,
    profession_plural: str,
) -> list[Associe]:
    associes = [
        _associe(
            data,
            address,
            profession_label,
            profession_plural,
            nb_parts=_primary_associe_nb_parts(data),
        )
    ]
    if _is_multi_associes_simple(data):
        valeur_nominale_part = data.valeur_nominale_part or calculate_nominal_value(
            data.capital_social,
            data.nb_parts_total,
        )
        associes.extend(
            Associe(
                genre=derive_gender_from_civilite(additional.civilite),
                civilite_affichage=additional.civilite,
                prenom=additional.prenom,
                nom=additional.nom,
                nb_parts=additional.nb_parts,
                profession=profession_label,
                profession_reglementee=profession_label,
                profession_reglementee_pluriel=profession_plural,
                qualification_principale=profession_label,
                qualite="associe",
                apport_numeraire=_parts_amount(additional.nb_parts, valeur_nominale_part),
                apport_numeraire_lettres=number_words_from_value(
                    _parts_amount(additional.nb_parts, valeur_nominale_part)
                ),
                nb_parts_lettres=number_words_from_value(additional.nb_parts),
            )
            for additional in data.additional_associes
        )
    return associes


def _primary_associe_nb_parts(data: SelarlSliceInput) -> int:
    if _is_multi_associes_simple(data):
        return data.associe_principal_nb_parts
    return data.nb_parts_total


def _parts_amount(nb_parts: int, valeur_nominale_part: str) -> str:
    try:
        amount = Decimal(str(valeur_nominale_part).replace(" ", "").replace(",", "."))
    except InvalidOperation:
        return ""
    total = amount * Decimal(nb_parts)
    if total == total.to_integral_value():
        return str(int(total))
    return format(total.normalize(), "f").replace(".", ",")


def _reunion_president(
    data: SelarlSliceInput,
    associes: list[Associe],
) -> ReunionPresident:
    president_index = (
        data.president_seance_associe_index if _is_multi_associes_simple(data) else 0
    )
    president = associes[president_index]
    return ReunionPresident(
        civilite_affichage=president.civilite_affichage,
        prenom=president.prenom,
        nom=president.nom,
        qualite="associe" if _is_multi_associes_simple(data) else "associe unique",
        civilite_president_seance=president.civilite_affichage,
        prenom_president_seance=president.prenom,
        nom_personne_seance=president.nom,
    )


def _associe(
    data: SelarlSliceInput,
    address: Address,
    profession_label: str,
    profession_plural: str,
    *,
    nb_parts: int,
) -> Associe:
    apport_montant = data.capital_social
    if _is_multi_associes_simple(data):
        apport_montant = _parts_amount(nb_parts, data.valeur_nominale_part)
    return Associe(
        genre=data.genre,
        civilite_affichage=data.civilite,
        prenom=data.prenom,
        nom=data.nom,
        nb_parts=nb_parts,
        profession=profession_label,
        profession_reglementee=profession_label,
        profession_reglementee_pluriel=profession_plural,
        qualification_principale=profession_label,
        titre_professionnel=data.titre_affichage,
        qualite="associe unique",
        date_naissance=data.date_naissance,
        ville_naissance=data.ville_naissance,
        departement_naissance=data.departement_naissance,
        nationalite=data.nationalite,
        situation_maritale=data.situation_maritale,
        regime_matrimonial=data.regime_matrimonial,
        conjoint=_spfpl_conjoint(data) if _needs_conjoint(data) else None,
        adresse_personnelle=address,
        adresse_personnelle_affichee=address.adresse_affichee,
        ordre=SpfplOrdre(
            professionnel=data.ordre_conseil or f"Ordre des {profession_plural}",
            departement=data.departement_ordre,
            ville=data.ordre_ville,
            numero=data.numero_ordre,
            numero_rpps=data.numero_rpps,
        ),
        apport_numeraire=apport_montant,
        apport_numeraire_lettres=number_words_from_value(apport_montant),
        nb_parts_lettres=number_words_from_value(nb_parts),
    )


def _needs_conjoint(data: SelarlSliceInput) -> bool:
    if data.multi_associes_doc004_limited and not data.dentist_multi_associes_statuts_partial:
        return False
    return data.profession == PROFESSION_DENTISTE or data.regime_communautaire


def _spfpl_conjoint(data: SelarlSliceInput) -> SpfplConjoint:
    return SpfplConjoint(
        civilite_affichage=data.conjoint_civilite,
        prenom=data.conjoint_prenom,
        nom=data.conjoint_nom,
    )


def _conjoint_person(data: SelarlSliceInput, personal_address: Address) -> Person:
    conjoint_address = personal_address if data.regime_communautaire else None
    return Person(
        genre=data.conjoint_genre,
        civilite=data.conjoint_civilite,
        prenom=data.conjoint_prenom,
        nom=data.conjoint_nom,
        adresse_personnelle_affichee=(
            conjoint_address.adresse_affichee if conjoint_address else None
        ),
        adresse_perso=conjoint_address,
    )


def _regime_communautaire(data: SelarlSliceInput) -> RegimeCommunautaire | None:
    if not data.regime_communautaire:
        return None
    return RegimeCommunautaire(
        avertissement=RegimeCommunautaireAvertissement(
            date_signature=data.date_courrier_avertissement,
        ),
        renonciation=RegimeCommunautaireRenonciation(
            lieu_signature=data.signature_lieu,
            date_signature=data.signature_date,
            nombre_exemplaires_lettres=data.signature_nombre_exemplaires,
        ),
        date_courrier_avertissement=data.date_courrier_avertissement,
        regime_matrimonial=data.regime_matrimonial,
        qualite_renoncee=data.qualite_renoncee,
    )
