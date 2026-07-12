from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Final

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    generate_docx_files_for_document_codes,
    generate_zip_file,
    rename_dnc_with_signataire,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Associe,
    BailContext,
    CapitalContext,
    CessionBanque,
    CessionContext,
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
    ScmCessionContext,
    Signature,
    SpfplConjoint,
    SpfplOrdre,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsSel,
)
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
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
    accentuate_french_months,
    calculate_nominal_value,
    date_to_french_words,
    format_grouped_numeric_value,
    group_montant,
    groupe_montants_associe,
    is_capital_divisible,
    number_words_from_value,
    parse_associe_birthdate,
    split_numero_voie,
)
from sydel_doc_engine.front_data import AddressUsage, BusinessRole, build_document_status_for_code
from sydel_doc_engine.orchestrator.service import (
    APPEL_FONDS_DOCUMENT_ID,
    BAIL_AVENANT_DOCUMENT_ID,
    CESSION_CABINET_DOCUMENT_IDS,
)

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

# Placeholder : le nombre de pages de l'acte de cession est saisi dans le
# sous-formulaire cession (a cabler). Valeur type en attendant.
CESSION_DOCUMENT_PAGES_LETTRES_DEFAUT: Final = "vingt"

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
class SelarlSliceInput:
    dossier_type_key: str
    dossier_reference: str = ""
    profession: str = PROFESSION_MEDECIN
    dossier_unipersonnel: bool = True
    regime_communautaire: bool = False
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
    # M2 (Akainu, 2026-06-30, parite avec les slices SELAS) : connecteur grammatical
    # (« de » / « du » / « des ») place avant le departement dans le destinataire de la
    # demande d'inscription a l'Ordre (R5). Sans ce champ, le SELARL retombait sur « de »
    # et ne pouvait pas produire « du Calvados » / « des Hauts de Seine ». Defaut « de ».
    connecteur_departement: str = "de"
    denomination: str = ""
    capital_social: str = ""
    capital_social_lettres: str = ""
    duree: str = "99 ans"
    nb_parts_total: int = 0
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
    # Retour Albane 2026-06-10 : « Madame la Présidente » si le president de
    # l'ordre est une femme (verifie a chaque fois) ; defaut « Monsieur le President ».
    ordre_president_feminin: bool = False
    mandataire_civilite: str = DEFAULT_MANDATAIRE_CIVILITE
    mandataire_prenom: str = DEFAULT_MANDATAIRE_PRENOM
    mandataire_nom: str = DEFAULT_MANDATAIRE_NOM
    mandataire_fonction: str = DEFAULT_MANDATAIRE_FONCTION
    mandataire_cabinet: str = DEFAULT_MANDATAIRE_CABINET
    signature_lieu: str = ""
    signature_date: date | None = None
    signature_nombre_exemplaires: str = "quatre"
    prestataire_signature_electronique: str = DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les cas
    # (DecisionContext la derive de signature_date). Ce champ n'est JAMAIS lu pour la sortie ;
    # il est conserve car les adaptateurs SELAS uni (_to_selarl_input) le passent encore
    # (= signature_date) et un test de non-regression injecte une valeur divergente pour
    # prouver qu'elle est ignoree. Le formulaire SELARL ne le collecte plus (champ mort retire).
    decision_date: date | None = None
    reunion_date_lettres: str = ""
    depot_banque_nom: str = ""
    depot_banque_adresse: str = ""
    exercice_debut: str = ""
    exercice_fin: str = ""
    exercice_cloture_premier: str = ""
    lieu_exercice_adresse: str = ""
    # 2e lieu d'exercice (ADDITIF, ticket 2.2) : le siege reste TOUJOURS le lieu
    # #1 ; ces deux champs n'alimentent un lieux[1] que s'ils sont fournis
    # ENSEMBLE (contrat aligne sur la SELAS, cf. validate_selas_second_lieu).
    second_lieu_exercice_nom: str = ""
    second_lieu_exercice_adresse: str = ""
    seuil_achat_materiel: str = DEFAULT_SEUIL_ACHAT_MATERIEL
    seuil_emprunt: str = DEFAULT_SEUIL_EMPRUNT
    conjoint_civilite: str = ""
    conjoint_genre: Gender = Gender.FEMININ
    conjoint_prenom: str = ""
    conjoint_nom: str = ""
    qualite_renoncee: str = "associé"
    date_courrier_avertissement: date | None = None
    cession_context: CessionContext | None = None
    bail_context: BailContext | None = None
    scm_cession_context: ScmCessionContext | None = None
    # Retours V3 2026-06-17 (SELARL multi-associes) — ADDITIF. `membres_additionnels`
    # = associes (personne physique OU morale) AJOUTES au praticien principal (lui
    # toujours membre #1 et signataire). Vide -> parcours unipersonnel historique
    # inchange. `praticien_nb_parts` = part du praticien quand multi (defaut : tout
    # le capital, comportement mono).
    membres_additionnels: tuple[StatutsCivilsAssocie, ...] = ()
    praticien_nb_parts: int = 0
    # Apport en euros du praticien quand multi. Vide -> derive du capital total
    # (cas mono / praticien seul detenteur). TODO V3 : wording exact de la ligne
    # d'apport par membre a confirmer (le ticket fige la repartition art. 8, pas
    # le libelle d'apport art. 7) -> parque, non invente.
    praticien_apport: str = ""

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

    @property
    def is_multi_associes(self) -> bool:
        """Dossier multi-associes ssi au moins un membre additionnel au praticien."""
        return len(self.membres_additionnels) >= 1


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
    codes = [*SELARL_V1_BASE_DOC_CODES, _statuts_code(data.profession)]
    if data.regime_communautaire:
        codes.extend(
            (
                SELARL_V1_REGIME_RENONCIATION_CODE,
                SELARL_V1_REGIME_AVERTISSEMENT_CODE,
            )
        )
    if data.cession_context is not None:
        type_cabinet = (data.cession_context.type_cabinet or "").strip().lower()
        # MD1 (Albane 2026-07-10) : le COMPROMIS de cession doit etre edite AU MEME TITRE que
        # l'acte. On genere DESORMAIS l'acte ET le compromis ENSEMBLE pour le type de cabinet
        # (comme la SELAS depuis O24-14) — l'etape n'est plus filtrante (le gate orchestrateur
        # `_cession_cabinet_enabled` autorise les deux pour une SEL). Avant : seul le document
        # correspondant a l'etape saisie sortait -> le compromis manquait au bundle acte.
        for doc_id, (_expected_etape, expected_type) in CESSION_CABINET_DOCUMENT_IDS.items():
            if type_cabinet == expected_type:
                codes.append(doc_id)
        # Appel de fonds = document commun « Si cession » : present pour toute cession
        # (medical comme dentaire), des que le type de cabinet est renseigne.
        if type_cabinet:
            codes.append(APPEL_FONDS_DOCUMENT_ID)
    if data.bail_context is not None:
        codes.append(BAIL_AVENANT_DOCUMENT_ID)
    if data.scm_cession_context is not None:
        codes.extend(("DOC-031", "DOC-032", "DOC-033"))
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
        reason="Pret pour generation SELARL V1 bornee.",
        document_codes=document_codes,
        document_rows=rows,
        blockers=(),
        warnings=warnings,
    )


def validate_selarl_input(data: SelarlSliceInput) -> tuple[str, ...]:  # noqa: C901
    blockers: list[str] = []
    if data.profession not in SELARL_V1_PROFESSIONS:
        blockers.append("Profession hors perimetre SELARL V1.")
    if not data.dossier_unipersonnel and not data.is_multi_associes:
        # Dossier declare non-unipersonnel mais aucun membre additionnel saisi.
        blockers.append("Dossier multi-associes : ajouter au moins un membre.")
    blockers.extend(_multi_membres_blockers(data))
    # Derogation / site distinct : hors outil. Les formulaires sont a remplir a la main
    # (retour associe Rafael) et ne sont plus exposes dans l'interface ; rien a valider ici.
    if data.cession and data.cession_context is None:
        blockers.append("Cession demandee mais donnees cession manquantes.")
    if data.scm and data.scm_cession_context is None:
        blockers.append("Cession de parts SCM demandee mais donnees SCM manquantes.")
    # F1 (Albane 2026-07-10) : les champs SCM ne sont plus PRE-REMPLIS par la fixture ->
    # ils demarrent vides. Les champs REQUIS par les generateurs SCM (DOC-031/032/033) sont
    # bloques ICI avec un message clair, plutot que de laisser crasher la generation.
    blockers.extend(_scm_cession_blockers(data.scm_cession_context))
    # O24-05 (re-Akainu tour 3, MAJEUR) : la valeur nominale de la SCM cedee est auto-calculee
    # (capital / nb parts). Sans garde de divisibilite, un capital non divisible produit une
    # valeur fractionnaire a precision infinie imprimee CRUMENT dans le DOCX. Meme garde que
    # les 6 types principaux (is_capital_divisible). Couvre le chemin SCM cession (SELARL + SELAS).
    _scm_cedee = (
        data.scm_cession_context.scm_cedee if data.scm_cession_context is not None else None
    )
    if _scm_cedee is not None and not is_capital_divisible(
        _scm_cedee.capital_social, _scm_cedee.nb_parts_total
    ):
        blockers.append(
            "Le capital de la SCM cedee doit etre divisible par le nombre de parts "
            "(la valeur nominale d'une part doit etre un nombre entier)."
        )

    blockers.extend(_missing_text_blockers(data))
    if data.date_naissance is None:
        blockers.append("Date de naissance du praticien requise.")
    if data.signature_date is None:
        blockers.append("Date de signature requise.")
    # SU4/SCS2 (Albane) : plus de blocker « Date de decision » — le champ dedie est supprime
    # du formulaire (la date du PV = la date de signature dans tous les cas, derivee par
    # DecisionContext). Le champ dataclass `decision_date` est CONSERVE : il reste alimente
    # par les adaptateurs SELAS uni (_to_selarl_input -> signature_date) et sert de garde de
    # non-regression (test : un decision_date divergent ne doit JAMAIS apparaitre en sortie).
    if data.nb_parts_total < 1:
        blockers.append("Nombre de parts requis et superieur a zero.")
    # Dogfood 2026-06-22 : capital non divisible par le nb de parts -> valeur nominale a
    # 28 chiffres + lettres cassees. Garde de divisibilite (couche partagee ; vaut aussi
    # pour la SELAS uni medecin qui derive de ce chemin).
    if not is_capital_divisible(data.capital_social, data.nb_parts_total):
        blockers.append(
            "Le capital social doit etre divisible par le nombre de parts "
            "(la valeur nominale d'une part doit etre un nombre entier)."
        )
    if data.profession == PROFESSION_DENTISTE or _is_married(data):
        blockers.extend(
            _missing_for_fields(
                data,
                (
                    ("conjoint_civilite", "Civilite du conjoint requise pour les statuts."),
                    ("conjoint_prenom", "Prenom du conjoint requis pour les statuts."),
                    ("conjoint_nom", "Nom du conjoint requis pour les statuts."),
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
    blockers.extend(_cession_blockers(data))
    return tuple(dict.fromkeys(blockers))


def _multi_membres_blockers(data: SelarlSliceInput) -> list[str]:  # noqa: C901
    """Bloqueurs UTILES du multi-associes (retours V3 2026-06-17).

    Le moteur revalide la coherence du capital ; ici on remonte tot, avant
    generation, les saisies incompletes (identite minimale + parts > 0) et la
    coherence du total (praticien + membres = capital)."""
    if not data.is_multi_associes:
        return []
    blockers: list[str] = []
    if data.praticien_nb_parts < 1:
        blockers.append("Multi-associes : nombre de parts du praticien requis (> 0).")
    total = data.praticien_nb_parts
    for index, membre in enumerate(data.membres_additionnels, start=2):
        nb = (membre.parts.nb if membre.parts else None) or 0
        total += nb
        if nb < 1:
            blockers.append(f"Multi-associes : parts du membre {index} requises (> 0).")
        if membre.type_personne == "personne_morale":
            if not (membre.denomination or "").strip():
                blockers.append(f"Multi-associes : denomination du membre {index} requise.")
        else:
            if not all(
                (value or "").strip()
                for value in (membre.civilite_affichage, membre.prenom, membre.nom)
            ):
                blockers.append(
                    f"Multi-associes : identite du membre {index} requise "
                    "(civilite, prenom, nom)."
                )
            # Dogfood 2026-06-22 : le generateur exige l'inscription a l'ordre du membre
            # (departement + numero + RPPS) ; sans eux, crash a la generation.
            for field, name in (
                ("ordre_departemental", "departement de l'ordre"),
                ("numero_ordre", "numero d'inscription a l'ordre"),
                ("numero_rpps", "numero RPPS"),
            ):
                if not str(getattr(membre, field, "") or "").strip():
                    blockers.append(
                        f"Multi-associes : {name} du membre {index} requis."
                    )
            # Identite du membre requise pour les STATUTS (chaque associe y est decrit
            # « ne le ... a ..., de nationalite ..., demeurant ... »). La FILIATION
            # (noms des parents) n'est PLUS requise : elle ne servait qu'a la DNC du
            # membre, et un membre NON gerant n'a plus de DNC (Albane 2026-07-09,
            # DNC = gerant uniquement — supersede Rafael matin + verrou R11).
            blockers.extend(_membre_statuts_identity_blockers(membre, index))
    if data.nb_parts_total and total != data.nb_parts_total:
        blockers.append(
            "Multi-associes : la somme des parts (praticien + membres) doit egaler "
            f"le nombre total de parts ({data.nb_parts_total})."
        )
    return blockers


def _membre_statuts_identity_blockers(
    membre: StatutsCivilsAssocie, index: int
) -> list[str]:
    """Identite du membre requise pour les STATUTS (chaque associe y est decrit
    « ne le ... a ..., de nationalite ..., demeurant ... » — champs `_required_text`
    du generateur, crash sinon). La FILIATION (nom_pere / nom_mere) n'est PLUS exigee :
    elle ne servait qu'a la DNC du membre, et un membre NON gerant n'a plus de DNC
    (Albane 2026-07-09, DNC = gerant uniquement)."""
    blockers: list[str] = []
    if parse_associe_birthdate(membre.date_naissance) is None:
        blockers.append(
            f"Multi-associes : date de naissance du membre {index} requise "
            "(JJ/MM/AAAA ou « 1 janvier 1980 »)."
        )
    for field, name in (
        ("ville_naissance", "ville de naissance"),
        ("nationalite", "nationalite"),
    ):
        if not str(getattr(membre, field, "") or "").strip():
            blockers.append(
                f"Multi-associes : {name} du membre {index} requise."
            )
    adresse_structuree = membre.adresse_personnelle or _parse_address_full(
        str(membre.adresse_personnelle_affichee or "")
    )
    if adresse_structuree is None:
        blockers.append(
            f"Multi-associes : adresse personnelle du membre {index} requise "
            "(N° et voie, CP Ville)."
        )
    return blockers


def _cession_blockers(data: SelarlSliceInput) -> list[str]:  # noqa: C901
    """Bloqueurs UTILES de la cession, montres dans le plan avant generation.

    Retours client 2026-06-11 : seuls les champs reellement indispensables
    bloquent (identite du vendeur, prix total). Tout le reste est facultatif et
    laisse une zone a completer a la main dans les documents.
    """
    cession = data.cession_context
    if cession is None:
        return []
    blockers: list[str] = []
    vendeur = cession.vendeur
    if vendeur is None:
        blockers.append("Cession : identite du vendeur requise.")
    else:
        vendor_fields = (
            (vendeur.civilite_affichage, "civilite du vendeur"),
            (vendeur.prenom, "prenom du vendeur"),
            (vendeur.nom, "nom du vendeur"),
            (vendeur.date_naissance, "date de naissance du vendeur"),
            (vendeur.ville_naissance, "ville de naissance du vendeur"),
            (vendeur.nationalite, "nationalite du vendeur"),
            (vendeur.adresse_affichee, "adresse du vendeur"),
            (vendeur.situation_maritale, "situation matrimoniale du vendeur"),
        )
        for value, label in vendor_fields:
            if value is None or (isinstance(value, str) and not value.strip()):
                blockers.append(f"Cession : {label} requis(e).")
    prix = cession.prix
    if prix is None or not (prix.total or "").strip():
        blockers.append("Cession : prix total requis.")
    elif not (prix.total_lettres or "").strip():
        blockers.append(
            "Cession : prix total en lettres requis (montant non entier : saisir a la main)."
        )
    for index, salarie in enumerate(cession.salaries):
        if not all(
            (value or "").strip()
            for value in (salarie.civilite_affichage, salarie.prenom, salarie.nom)
        ):
            blockers.append(
                f"Cession : identite complete du salarie {index + 1} requise "
                "(civilite, prenom, nom)."
            )
    etape = (cession.etape or "").strip().lower()
    type_cabinet = (cession.type_cabinet or "").strip().lower()
    if etape == "acte" and type_cabinet == "medical":
        credit = cession.financement.credit_vendeur if cession.financement else None
        if credit is None or not credit.actif:
            blockers.append(
                "Acte medical : la clause credit-vendeur du modele est figee — "
                "renseigner le credit-vendeur (montant, duree, taux)."
            )
        elif not all(
            (value or "").strip()
            for value in (
                credit.montant,
                credit.duree,
                credit.taux,
                credit.majoration_interet_retard,
            )
        ):
            blockers.append(
                "Credit-vendeur : montant, duree, taux et majoration requis."
            )
        scm = cession.scm
        if scm is not None and scm.actif and not (scm.nb_parts_a_ceder or "").strip():
            blockers.append("Cession de parts SCM : nombre de parts a ceder requis.")
    return blockers


def _scm_cession_blockers(scm_cession: ScmCessionContext | None) -> list[str]:
    """Bloqueurs des champs SCM REQUIS par les generateurs (DOC-031/032/033).

    F1 (Albane 2026-07-10) : les champs SCM ne sont plus pre-remplis par la fixture ;
    on remonte donc TOT, avant generation, les champs indispensables laisses vides
    (identite / capital / RCS de la SCM cedee, nombre de parts cedees, prix global) —
    sinon les generateurs levent (« ... est obligatoire ») en pleine generation.
    """
    if scm_cession is None:
        return []
    blockers: list[str] = []
    cedee = scm_cession.scm_cedee
    if cedee is None:
        blockers.append("Cession de parts SCM : identite de la SCM cedee requise.")
    else:
        siege_ok = cedee.siege is not None and bool(
            (cedee.siege.adresse_affichee or "").strip()
        )
        text_fields = (
            ((cedee.denomination or "").strip(), "denomination de la SCM cedee"),
            ((cedee.capital_social or "").strip(), "capital social de la SCM cedee"),
            ((cedee.ville_rcs or "").strip(), "ville du RCS de la SCM cedee"),
            ((cedee.numero_rcs or "").strip(), "numero RCS de la SCM cedee"),
        )
        for value, label in text_fields:
            if not value:
                blockers.append(f"Cession de parts SCM : {label} requise.")
        if not siege_ok:
            blockers.append("Cession de parts SCM : siege de la SCM cedee requis.")
        if not (cedee.nb_parts_total or 0) > 0:
            blockers.append(
                "Cession de parts SCM : nombre total de parts de la SCM cedee requis (> 0)."
            )
    parts_cedees = scm_cession.parts_cedees
    if parts_cedees is None or not (parts_cedees.nb or 0) > 0:
        blockers.append("Cession de parts SCM : nombre de parts cedees requis (> 0).")
    prix = scm_cession.prix
    if prix is None or not (prix.global_ or "").strip():
        blockers.append("Cession de parts SCM : prix global requis.")
    return blockers


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
    capital_social_display = format_grouped_numeric_value(data.capital_social)
    valeur_nominale_part_lettres = (
        data.valeur_nominale_part_lettres or number_words_from_value(valeur_nominale_part)
    )
    # B1/SCS2 (Albane 2026-06-25) : date de reunion (PV) = date de signature, comme la decision.
    reunion_date_lettres = data.reunion_date_lettres or date_to_french_words(data.signature_date)
    signature_prestataire = (
        data.prestataire_signature_electronique
        or DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE
    )
    # R5 (Albane 2026-07-07) : seuils de gerance groupes par 3 (« 5 000 € », « 10 000 € »)
    # a la construction du contexte — les defauts (« 5000 »/« 10000 ») et une saisie brute
    # partaient non groupes dans l'article 17 des statuts.
    seuil_achat_materiel = group_montant(
        data.seuil_achat_materiel or DEFAULT_SEUIL_ACHAT_MATERIEL
    )
    seuil_emprunt = group_montant(data.seuil_emprunt or DEFAULT_SEUIL_EMPRUNT)
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
        departement_naissance=data.departement_naissance,
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
        forme_sociale_libelle_long="Société d'exercice libéral à responsabilité limitée",
        forme_sociale_complete="société d'exercice libéral à responsabilité limitée",
        forme_sociale_abregee="SELARL",
        denomination=data.denomination,
        denomination_courte=data.denomination,
        capital=capital_social_display,
        capital_social=capital_social_display,
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
            associe_unique=not data.is_multi_associes,
            derogation=False,
            site_distinct=False,
            cession=data.cession_context is not None,
            scm_cession=data.scm_cession_context is not None,
        ),
        cession=data.cession_context,
        bail=data.bail_context,
        scm_cession=data.scm_cession_context,
        personne_signataire=person,
        conjoint=conjoint,
        signature=Signature(
            # SU3 (Albane 2026-06-25) : ville de signature = ville du siege DANS TOUS LES CAS.
            lieu=(data.siege_ville or data.signature_lieu),
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
        # SCS2/SU4 (Albane 2026-06-25, propag. Q4) : date de decision (PV) = date de signature.
        decision=DecisionContext(date=_display_date(data.signature_date)),
        reunion=ReunionContext(
            date_lettres=reunion_date_lettres,
            president=reunion_president,
        ),
        capital=CapitalContext(
            nb_parts_total=data.nb_parts_total,
            valeur_nominale_part=valeur_nominale_part,
            nb_parts_representees=data.nb_parts_total,
            montant=capital_social_display,
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
        # R3/A5 (Albane 2026-06-26) : l'apport porte ici alimente les lettres de regime
        # communautaire (« en apportant X euros » / « somme en numeraire de X »). Ce doit
        # etre l'apport INDIVIDUEL de l'associe renoncant, PAS le capital social total.
        # `_praticien_apport_montant` rend l'apport saisi (repli capital si seul detenteur).
        apport=Apport(
            montant=_praticien_apport_montant(data),
            montant_lettres=number_words_from_value(_praticien_apport_montant(data)),
        ),
        regime_communautaire=_regime_communautaire(data),
        statuts_sel=StatutsSel(
            overlay=_statuts_overlay(data.profession),
            profession=profession_label,
            membres=_statuts_membres(data, person_address, profession_label),
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom=data.depot_banque_nom,
                adresse_affichee=data.depot_banque_adresse,
            ),
            montant=capital_social_display,
        ),
        exercice_social=ExerciceSocial(
            # LIVE-03 : re-accentue les mois saisis librement (« 1er aout » -> « 1er août »)
            # EN AMONT du generateur, qui reste un echo fidele du modele de reference.
            # debut accentue comme fin/cloture (oubli releve par re-Akainu T4).
            debut=accentuate_french_months(data.exercice_debut),
            fin=accentuate_french_months(data.exercice_fin),
            date_cloture_premier_exercice=accentuate_french_months(
                data.exercice_cloture_premier
            ),
            # lieux[0] = lieu d'exercice #1 (le siege par defaut ; un
            # `lieu_exercice_adresse` legacy reste lu en fallback pour
            # retro-compat -> rendu 1-lieu byte-identique). lieux[1] = 2e lieu
            # ADDITIF (ticket 2.2), append UNIQUEMENT si nom ET adresse fournis
            # ensemble (contrat SELAS, cf. validate_selas_second_lieu).
            lieux=_selarl_lieux_exercice(data, company_address),
        ),
        document=DocumentContext(
            nombre_exemplaires_lettres=data.signature_nombre_exemplaires,
            nombre_pages_lettres=(
                CESSION_DOCUMENT_PAGES_LETTRES_DEFAUT
                if data.cession_context is not None
                else None
            ),
            signataire=DocumentSignataire(prenom=data.prenom, nom=data.nom),
        ),
        emprunt=Emprunt(actif=False),
        metadata={
            "front_slice": "track_b_selarl_v1",
            "dossier_reference": data.dossier_reference,
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
    # DNC = GERANT UNIQUEMENT (Albane, Direction Juridique, 2026-07-09 — supersede le
    # retour Rafael du matin « 1 DNC par associe » + verrou R11 ; Rafael a confirme
    # « Albane a raison »). En SELARL le gerant est le praticien (signataire du tronc
    # commun) : sa DNC — la seule — vient de l'orchestrateur, renommee ci-dessous
    # (O24-02). Les membres additionnels NON gerants ne recoivent PAS de DNC.
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)
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
    if data.scm_cession_context is None:
        rows.append(
            SelarlDocumentRow(
                doc_code="DOC-031/DOC-032/DOC-033",
                label="SCM et cession de parts SCM",
                status="hors_v1",
                message="Non expose : activez SCM et fournissez les donnees.",
            )
        )
    return tuple(rows)


def _warning_messages(data: SelarlSliceInput) -> tuple[str, ...]:
    warnings = [
        "SELARL V1 bornee : creation medecin ou chirurgien-dentiste, associe unique uniquement.",
    ]
    if data.regime_communautaire:
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
    return tuple(warnings)


def _missing_text_blockers(data: SelarlSliceInput) -> list[str]:
    base_fields = (
        # F2 (Albane 2026-07-10) : la reference dossier ne BLOQUE plus l'edition (inutile,
        # on ne telecharge pas le formulaire). Le champ reste saisi (metadata) mais optionnel.
        ("civilite", "Civilite du praticien requise."),
        ("prenom", "Prenom du praticien requis."),
        ("nom", "Nom du praticien requis."),
        ("titre_affichage", "Titre d'affichage du signataire requis."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("nom_pere", "Nom du pere requis pour DOC-001."),
        ("nom_mere", "Nom de la mere requis pour DOC-001."),
        # Numero + voie fusionnes en un seul champ (retours client 2026-06-11,
        # ticket 1.5) : la valeur complete vit dans adresse_voie.
        ("adresse_voie", "Numero et voie du praticien requis."),
        ("adresse_cp", "Code postal du praticien requis."),
        ("adresse_ville", "Ville du praticien requise."),
        ("situation_maritale", "Situation matrimoniale requise pour les statuts."),
        ("regime_matrimonial", "Regime matrimonial requis pour les statuts."),
        ("numero_ordre", "Numero d'inscription a l'ordre requis."),
        ("numero_rpps", "Numero RPPS requis pour les statuts."),
        ("departement_ordre", "Departement d'inscription a l'ordre requis."),
        ("denomination", "Denomination sociale requise."),
        ("capital_social", "Capital social requis."),
        ("siege_voie", "Numero et voie du siege requis."),
        ("siege_cp", "Code postal du siege requis."),
        ("siege_ville", "Ville du siege requise."),
        ("ville_rcs", "Ville RCS requise."),
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise."),
        ("ordre_cp", "Code postal de l'ordre requis."),
        ("ordre_ville", "Ville de l'ordre requise."),
        ("signature_lieu", "Lieu de signature requis."),
        # F3 (Albane 2026-07-10) : la BANQUE du depot des fonds ne BLOQUE plus l'edition
        # (rarement connue au debut — coherent avec l'assouplissement micro-holding A8
        # 2026-07-09). Vide, les statuts / l'attestation laissent une zone a completer.
        # Adresse de la banque : deja FACULTATIVE (retours client 2026-06-11, ticket 3.2).
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


def _selarl_lieux_exercice(
    data: SelarlSliceInput, company_address: Address
) -> tuple[ExerciceLieu, ...]:
    """Construit les lieux d'exercice SELARL (1 ou 2), ticket 2.2 ADDITIF.

    - lieux[0] = lieu d'exercice #1 : le siege par defaut. Le champ legacy
      `lieu_exercice_adresse`, s'il est renseigne seul, reste lu en fallback
      (retro-compat) -> le rendu 1-lieu reste byte-identique a l'existant.
    - lieux[1] = 2e lieu d'exercice : ajoute UNIQUEMENT si `second_lieu_exercice_nom`
      ET `second_lieu_exercice_adresse` sont fournis ENSEMBLE (contrat aligne sur
      la SELAS, cf. validate_selas_second_lieu). Si un seul des deux est saisi,
      le 2e lieu est ignore cote front (la validation moteur leve si le contexte
      le porte malgre tout, comme pour la SELAS).
    """
    lieu_1 = ExerciceLieu(
        adresse_affichee=data.lieu_exercice_adresse or company_address.adresse_affichee
    )
    nom_2 = (data.second_lieu_exercice_nom or "").strip()
    adresse_2 = (data.second_lieu_exercice_adresse or "").strip()
    if nom_2 and adresse_2:
        return (lieu_1, ExerciceLieu(nom=nom_2, adresse_affichee=adresse_2))
    return (lieu_1,)


def _address(num_voie: str, voie: str, cp: str, ville: str) -> Address:
    # Champ unique « Numero et voie » (ticket 1.5) : si le numero n'est pas
    # fourni separement, il est extrait de la tete de la voie pour alimenter
    # les generateurs qui consomment numero et voie separement.
    if not (num_voie or "").strip():
        num_voie, voie = split_numero_voie(voie)
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
    return "médecin"


def _profession_plural(profession: str) -> str:
    if profession == PROFESSION_DENTISTE:
        return "chirurgiens-dentistes"
    return "médecins"


def _ordre(
    data: SelarlSliceInput,
    profession_label: str,
    profession_plural: str,
) -> OrdreProfessionnel:
    return OrdreProfessionnel(
        conseil_departemental_libelle=data.ordre_conseil,
        departement_inscription=data.departement_ordre,
        # M2 (Akainu, 2026-06-30) : connecteur grammatical du destinataire R5, cable depuis
        # le formulaire SELARL (parite SELAS). Defaut « de » si non renseigne.
        connecteur_departement=data.connecteur_departement or "de",
        destinataire_appel=(
            "Madame la Présidente"
            if data.ordre_president_feminin
            else "Monsieur le Président"
        ),
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
    # `ctx.associes` reste l'associe REPRESENTATIF (praticien) — longueur 1 dans tous
    # les cas. En multi, la liste complete des membres vit dans `statuts_sel.membres`.
    nb_parts = (
        data.praticien_nb_parts if data.is_multi_associes else data.nb_parts_total
    )
    return [
        _associe(
            data,
            address,
            profession_label,
            profession_plural,
            nb_parts=nb_parts or data.nb_parts_total,
        )
    ]


def _statuts_membres(
    data: SelarlSliceInput,
    address: Address,
    profession_label: str,
) -> list[StatutsCivilsAssocie]:
    """Liste complete des membres SELARL (retours V3 2026-06-17). Vide en mono.

    Membre #1 = le praticien principal (toujours signataire), construit depuis la
    fiche praticien ; suivent les membres additionnels saisis. Le calcul du nombre
    d'associes decoule de la longueur de cette liste (tous signataires = associes)."""
    if not data.is_multi_associes:
        return []
    praticien = StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=data.genre,
        civilite_affichage=data.civilite,
        prenom=data.prenom,
        nom=data.nom,
        profession=profession_label,
        date_naissance=data.date_naissance,
        ville_naissance=data.ville_naissance or None,
        departement_naissance=data.departement_naissance or None,
        nationalite=data.nationalite or None,
        situation_maritale=data.situation_maritale or None,
        adresse_personnelle_affichee=address.adresse_affichee,
        ordre_departemental=data.departement_ordre or None,
        numero_ordre=data.numero_ordre or None,
        numero_rpps=data.numero_rpps or None,
        apport=StatutsCivilsApport(
            montant=_praticien_apport_montant(data),
            montant_lettres=number_words_from_value(_praticien_apport_montant(data)),
        ),
        parts=StatutsCivilsParts(
            nb=data.praticien_nb_parts,
            nb_lettres=number_words_from_value(data.praticien_nb_parts),
        ),
        est_signataire=True,
    )
    # R5 (Albane 2026-07-07) : montants des membres additionnels (apport individuel,
    # capital d'une personne morale) groupes par 3 a la construction du contexte —
    # copies pydantic, les objets saisis au shell / scenarios ne sont jamais mutes.
    return [praticien, *(groupe_montants_associe(m) for m in data.membres_additionnels)]


def _praticien_apport_montant(data: SelarlSliceInput) -> str:
    """Apport en euros du praticien. Saisi explicitement, sinon repli sur le capital
    total (cas praticien seul detenteur). Pas d'invention de calcul parts -> euros."""
    if (data.praticien_apport or "").strip():
        return format_grouped_numeric_value(data.praticien_apport)
    return format_grouped_numeric_value(data.capital_social)


def _reunion_president(
    data: SelarlSliceInput,
    associes: list[Associe],
) -> ReunionPresident:
    president = associes[0]
    return ReunionPresident(
        civilite_affichage=president.civilite_affichage,
        prenom=president.prenom,
        nom=president.nom,
        qualite="associe unique",
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
    # R3/A5 (Albane 2026-06-26) : l'apport numeraire de l'associe est son apport
    # INDIVIDUEL (repli capital si seul detenteur), pas systematiquement le capital
    # social total. Coherent avec `_statuts_membres` (meme helper).
    apport_montant = _praticien_apport_montant(data)
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
            # ST6 (Albane 2026-07-10) : preposition « de / du » choisie au formulaire, cablee
            # jusqu'a la ligne d'identite des statuts SEL. Defaut « de » si non renseignee.
            connecteur_departement=data.connecteur_departement or "de",
        ),
        apport_numeraire=apport_montant,
        apport_numeraire_lettres=number_words_from_value(apport_montant),
        nb_parts_lettres=number_words_from_value(nb_parts),
    )


def _needs_conjoint(data: SelarlSliceInput) -> bool:
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : le PARTENAIRE PACSE figure aussi a la comparution
    # -> le conjoint doit etre transmis au generateur pour un pacse (pas seulement marie/dentiste).
    return (
        data.profession == PROFESSION_DENTISTE
        or data.regime_communautaire
        or _is_married(data)
        or _is_pacse(data)
    )


def _is_married(data: SelarlSliceInput) -> bool:
    return "mari" in data.situation_maritale.casefold()


def _is_pacse(data: SelarlSliceInput) -> bool:
    return "pacs" in data.situation_maritale.casefold()


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
            lieu_signature=(data.siege_ville or data.signature_lieu),  # SU3 : = ville du siege
            date_signature=data.signature_date,
            nombre_exemplaires_lettres=data.signature_nombre_exemplaires,
        ),
        date_courrier_avertissement=data.date_courrier_avertissement,
        regime_matrimonial=data.regime_matrimonial,
        qualite_renoncee=data.qualite_renoncee,
    )
