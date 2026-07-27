from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import (
    ApportTitres,
    AssocieCible,
    CapitalSouscription,
    CessionParts,
    DocumentGenerationContext,
    ProfessionalEntity,
    SocieteCible,
    SocieteSpfpl,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    mentions_conjoint,
    mentions_partenaire_pacse,
    partenaire_pacse_clause,
)
from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier
from sydel_doc_engine.utils.departements import departement_nom
from sydel_doc_engine.utils.grammar import (  # noqa: F401
    elision_de,
    euro_word,
    montant_avec_euros,
    montant_lettres_avec_unite,
)

DOCUMENT_CODE = "CODE-SPFPL-AGR-INFO-001"
CORE_DOCUMENT_CODE = "CODE-SPFPL-CORE-001"

SPFPL_CESSION_STRUCTURE = "SPFPL cession"
SPFPL_APPORT_STRUCTURE = "SPFPL apport"
OPERATION_CESSION = "cession"
OPERATION_APPORT = "apport"
SUPPORTED_NOTE_OPERATIONS = {OPERATION_CESSION, OPERATION_APPORT}


def required_text(value: str | None, field_name: str) -> str:
    # R10 (Rafael 2026-06-24) : une donnee manquante NE bloque PAS la generation -> marqueur
    # visible « (À COMPLÉTER : …) », a completer a la main, au lieu de lever.
    # KAN-2 M1 (Rafael 2026-07-15, motif n°1 des rejets) : le marqueur porte un LIBELLÉ MÉTIER
    # lisible (« prénom de l'associé unique »), JAMAIS le chemin technique (« actionnaire_unique.
    # prenom ») ni des crochets d'index. `libelle_metier` traduit le field_name ; sortie NOMINALE
    # (valeur présente) inchangée.
    if value is None or not value.strip():
        return f"(À COMPLÉTER : {libelle_metier(field_name)})"
    return value.strip()


def required_int(value: int | None, field_name: str) -> int:
    """Point de CALCUL : rend un int, pour les soustractions/comparaisons de répartition.

    NE PAS s'en servir pour AFFICHER une quantité de titres -> `quantite_titres` ci-dessous.
    C'est la confusion des deux qui a fait revenir KAN-2 deux fois : le front (`_i()` =
    `number_input(min_value=0)`) pose TOUJOURS 0 et jamais None -> cette fonction ne levait
    donc jamais, et imprimait le zéro tel quel dans des actes signables.
    """
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def quantite_titres(value: int | None, libelle: str) -> str:
    """AFFICHAGE d'une quantité de titres (parts / actions). KAN-2 + Akainu B1 (2026-07-15).

    Une quantité NON RENSEIGNÉE ne s'affirme JAMAIS à zéro : un acte SIGNABLE qui déclare
    « apporte 0 parts sociales » est FAUX — et c'est PIRE que le blocage que le client a fait
    retirer. Le front ne sait pas exprimer « vide » sur ces slots (0 = champ jamais touché) :
    ici, à l'AFFICHAGE, 0 et None sont donc le même cas — « non rempli ».

    Périmètre volontairement limité au FIL DU TEXTE. Les TABLEAUX de répartition avant/après
    gardent leur « 0 » : c'est une valeur RÉELLE (la holding détient 0 part AVANT la cession),
    pas un champ vide.

    `libelle` = intitulé MÉTIER (« nombre de parts cédées »), jamais un nom de token ni un
    chemin technique — Akainu M2 : « (À COMPLÉTER : CESSION_PARTS.PRIX_TOTAL_LETTRES) » ne veut
    rien dire pour le client qui relit son acte. `libelle_metier` = filet (un libellé déjà métier
    traverse inchangé ; un chemin technique passé par erreur est tout de même traduit).
    """
    if not value:
        return f"(À COMPLÉTER : {libelle_metier(libelle)})"
    return str(value)


def spfpl_forme_sociale_complete(profession_pluriel: str) -> str:
    """Designation legale COMPLETE de la SPFPL (convention P2, Albane 2026-07-06/07) :
    « Société de Participations Financières de Profession Libérale de <Profession-Plurielle>
    par actions simplifiée ». MEME construction que l'acte de cession
    (acte_cession_parts_spfpl) et que le titre des statuts (statuts_spfpl_templates) :
    profession au PLURIEL, titre-casee (« Chirurgiens-Dentistes »), forme legale complete
    ACCENTUEE — jamais le singulier ni l'abrege « par actions simplifiee ».
    """
    return (
        "Société de Participations Financières de Profession Libérale de "
        f"{profession_pluriel.title()} par actions simplifiée"
    )


def format_display_date(value: date | str | None, field_name: str) -> str:
    # KAN-2 : date manquante -> marqueur « (À COMPLÉTER : <libellé métier>) », non bloquant (R10).
    if value is None:
        return f"(À COMPLÉTER : {libelle_metier(field_name)})"
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return required_text(value, field_name)


# KAN-2 (Rafael) : un OBJET manquant NE bloque JAMAIS. Instance VIDE (champs None) -> ses champs
# sortent en marqueurs « (À COMPLÉTER : …) » (required_text) ou « (À COMPLÉTER : <libellé>) »
# (quantite_titres). Zero blocage : generer meme sans AUCUN champ rempli.
def required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    return ctx.societe_spfpl if ctx.societe_spfpl is not None else SocieteSpfpl()


def required_societe_cible(ctx: DocumentGenerationContext) -> SocieteCible:
    return ctx.societe_cible if ctx.societe_cible is not None else SocieteCible()


def required_cedant(ctx: DocumentGenerationContext) -> SpfplPerson:
    return ctx.cedant if ctx.cedant is not None else SpfplPerson()


def required_apporteur(ctx: DocumentGenerationContext) -> SpfplPerson:
    return ctx.apporteur if ctx.apporteur is not None else SpfplPerson()


def required_apport_titres(ctx: DocumentGenerationContext) -> ApportTitres:
    return ctx.apport_titres if ctx.apport_titres is not None else ApportTitres()


def required_cession_parts(ctx: DocumentGenerationContext) -> CessionParts:
    if ctx.cession_parts is None:
        raise ValueError(f"cession_parts est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.cession_parts


def required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {CORE_DOCUMENT_CODE}.")
    return ctx.capital_souscription


def required_evaluateur_apport(ctx: DocumentGenerationContext) -> ProfessionalEntity:
    if ctx.evaluateur_apport is None:
        raise ValueError(f"evaluateur_apport est obligatoire pour {CORE_DOCUMENT_CODE}.")
    return ctx.evaluateur_apport


def required_commissaire_aux_apports(ctx: DocumentGenerationContext) -> ProfessionalEntity:
    if ctx.commissaire_aux_apports is None:
        raise ValueError(
            f"commissaire_aux_apports est obligatoire pour {CORE_DOCUMENT_CODE}."
        )
    return ctx.commissaire_aux_apports


def validate_cession_context(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != SPFPL_CESSION_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SPFPL_CESSION_STRUCTURE} pour {DOCUMENT_CODE}."
        )
    if ctx.dossier_options is None or not ctx.dossier_options.cession:
        raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    operation_type = operation_spfpl_type(ctx)
    if operation_type != OPERATION_CESSION:
        raise ValueError(
            "operation_spfpl.type doit etre cession pour les PV d'agrement "
            f"{DOCUMENT_CODE}."
        )


def validate_apport_context(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != SPFPL_APPORT_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SPFPL_APPORT_STRUCTURE} pour "
            f"{CORE_DOCUMENT_CODE}."
        )
    if ctx.dossier_options is None or not ctx.dossier_options.apport:
        raise ValueError(f"dossier.options.apport doit etre vrai pour {CORE_DOCUMENT_CODE}.")
    operation_type = operation_spfpl_type(ctx)
    if operation_type != OPERATION_APPORT:
        raise ValueError(
            f"operation_spfpl.type doit etre apport pour {CORE_DOCUMENT_CODE}."
        )


def validate_associe_unique(ctx: DocumentGenerationContext, expected: bool) -> None:
    if ctx.dossier_options is None:
        raise ValueError(f"dossier.options est obligatoire pour {DOCUMENT_CODE}.")
    if ctx.dossier_options.associe_unique is not expected:
        attendu = "vrai" if expected else "faux"
        raise ValueError(
            f"dossier.options.associe_unique doit etre {attendu} pour {DOCUMENT_CODE}."
        )


def operation_spfpl_type(ctx: DocumentGenerationContext) -> str:
    if ctx.operation_spfpl is None:
        raise ValueError(f"operation_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    operation_type = required_text(ctx.operation_spfpl.type, "operation_spfpl.type").lower()
    if operation_type not in SUPPORTED_NOTE_OPERATIONS:
        supported = ", ".join(sorted(SUPPORTED_NOTE_OPERATIONS))
        raise ValueError(
            f"operation_spfpl.type doit etre dans [{supported}] pour {DOCUMENT_CODE}."
        )
    return operation_type


def operation_party(ctx: DocumentGenerationContext) -> SpfplPerson:
    if operation_spfpl_type(ctx) == OPERATION_CESSION:
        return required_cedant(ctx)
    return required_apporteur(ctx)


def validate_note_context(ctx: DocumentGenerationContext) -> str:
    operation_type = operation_spfpl_type(ctx)
    if operation_type == OPERATION_CESSION:
        if ctx.structure != SPFPL_CESSION_STRUCTURE:
            raise ValueError(
                f"dossier.structure doit etre {SPFPL_CESSION_STRUCTURE} pour la note "
                f"{DOCUMENT_CODE}."
            )
        if ctx.dossier_options is None or not ctx.dossier_options.cession:
            raise ValueError(f"dossier.options.cession doit etre vrai pour {DOCUMENT_CODE}.")
    else:
        if ctx.structure != SPFPL_APPORT_STRUCTURE:
            raise ValueError(
                f"dossier.structure doit etre {SPFPL_APPORT_STRUCTURE} pour la note "
                f"{DOCUMENT_CODE}."
            )
        if ctx.dossier_options is None or not ctx.dossier_options.apport:
            raise ValueError(f"dossier.options.apport doit etre vrai pour {DOCUMENT_CODE}.")
    return operation_type


def person_display(person: SpfplPerson, field_name: str) -> str:
    # R3 durci (Rafael 2026-07-07, defense en profondeur) : cette soeur rendait la
    # civilite BRUTE alors que person_short_identity / representant_display /
    # associe_display_name etaient deja routees -> tout slot de personne passe par
    # civilite_civile (sortie byte-identique quand la donnee est deja civile, cas
    # nominal §14.2 ; un « Docteur »/« Dr » pose en civilite devient Monsieur/Madame).
    # getattr : certains appelants passent des modeles SANS genre (ex. ReunionPresident
    # du PV d'agrement) -> None (masculin par defaut si titre), comme associe_display_name.
    civilite = civilite_civile(
        required_text(person.civilite_affichage, f"{field_name}.civilite_affichage"),
        getattr(person, "genre", None),
    )
    return (
        f"{civilite} "
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def person_signature(person: SpfplPerson, field_name: str) -> str:
    return (
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def person_identity_sentence(person: SpfplPerson, field_name: str) -> str:
    # Akainu M1 round 2 (2026-07-02) : le SPFPL n'est PLUS marie-only (R0702-02 : menu
    # matrimonial complet). L'ancienne garde « affiche le conjoint si conjoint present » rendait
    # « avec (À COMPLÉTER) » pour un non-marie (le front pose toujours un conjoint vide). On gate
    # desormais sur le STATUT via `mentions_conjoint` (garde PARTAGE unique, R22-02), comme les
    # actes de cession/apport. Marie -> « avec <conjoint> » BYTE-IDENTIQUE ; sinon -> statut seul.
    conjoint = person.conjoint
    conjoint_display = ""
    if conjoint is not None and mentions_conjoint(person.situation_maritale):
        # R3 durci (Rafael 2026-07-07, defense en profondeur) : civilite du conjoint
        # routee aussi (SpfplConjoint ne porte pas de genre -> masculin par defaut si
        # un titre y etait pose ; M./Mme/Monsieur/Madame passent inchanges).
        conjoint_civilite = civilite_civile(
            required_text(
                conjoint.civilite_affichage,
                f"{field_name}.conjoint.civilite_affichage",
            ),
            None,
        )
        conjoint_display = (
            " avec "
            f"{conjoint_civilite} "
            f"{required_text(conjoint.prenom, f'{field_name}.conjoint.prenom')} "
            f"{required_text(conjoint.nom, f'{field_name}.conjoint.nom')}"
        )
    elif mentions_partenaire_pacse(person.situation_maritale):
        # Albane 6.3/7.3 (RATIFIE 2026-07-06) : le PARTENAIRE PACSE s'affiche aussi (« avec
        # {Civilite Prenom Nom} », pas de « sous le régime de … »). « Pas de mention sans
        # nom » : partenaire_pacse_clause -> "" si le partenaire n'est pas renseigne.
        conjoint_display = partenaire_pacse_clause(conjoint)
    return (
        f"{person_display(person, field_name)}, "
        f"{required_text(person.profession, f'{field_name}.profession')}, "
        f"ne le {format_display_date(person.date_naissance, f'{field_name}.date_naissance')} "
        f"a {required_text(person.ville_naissance, f'{field_name}.ville_naissance')} "
        f"({required_text(person.departement_naissance, f'{field_name}.departement_naissance')}) "
        f"de nationalite {required_text(person.nationalite, f'{field_name}.nationalite')}, "
        f"demeurant au {person_address_display(person, field_name)}, "
        f"{required_text(person.situation_maritale, f'{field_name}.situation_maritale')}"
        f"{conjoint_display}."
    )


def person_address_display(person: SpfplPerson, field_name: str) -> str:
    if person.adresse_personnelle_affichee:
        return person.adresse_personnelle_affichee.strip()
    if person.adresse_personnelle is None:
        raise ValueError(
            f"{field_name}.adresse_personnelle est obligatoire pour {CORE_DOCUMENT_CODE}."
        )
    address = person.adresse_personnelle
    return (
        f"{required_text(address.num_voie, f'{field_name}.adresse_personnelle.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.adresse_personnelle.voie')}, "
        f"{required_text(address.cp, f'{field_name}.adresse_personnelle.cp')} "
        f"{required_text(address.ville, f'{field_name}.adresse_personnelle.ville')}"
    )


def person_short_identity(person: SpfplPerson, field_name: str) -> str:
    # R3 durci (Rafael 2026-07-07, supersede A26-45/49) : jamais « Docteur »/« Dr »
    # en sortie — civilité CIVILE accordée au genre porté par la personne.
    civilite = civilite_civile(
        required_text(person.civilite_affichage, f"{field_name}.civilite_affichage"),
        person.genre,
    )
    return (
        f"{civilite} "
        f"{required_text(person.prenom, f'{field_name}.prenom')} "
        f"{required_text(person.nom, f'{field_name}.nom')}"
    )


def ordre_sentence(person: SpfplPerson, field_name: str) -> str:
    if person.ordre is None:
        raise ValueError(f"{field_name}.ordre est obligatoire pour {CORE_DOCUMENT_CODE}.")
    profession_pluriel = required_text(
        person.profession_reglementee_pluriel,
        f"{field_name}.profession_reglementee_pluriel",
    )
    ordre_departement = departement_nom(
        required_text(person.ordre.departement, f"{field_name}.ordre.departement")
    )
    return (
        "Inscrit au Tableau de l'ordre départemental des "
        f"{profession_pluriel} "
        f"du {ordre_departement} "
        "sous le numéro RPPS "
        f"{required_text(person.ordre.numero_rpps, f'{field_name}.ordre.numero_rpps')}."
    )


def company_siege_display(societe: SocieteSpfpl | SocieteCible, field_name: str) -> str:
    if societe.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {DOCUMENT_CODE}.")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    parts = [
        required_text(societe.siege.num_voie, f"{field_name}.siege.num_voie"),
        required_text(societe.siege.voie, f"{field_name}.siege.voie"),
        required_text(societe.siege.cp, f"{field_name}.siege.cp"),
        required_text(societe.siege.ville, f"{field_name}.siege.ville"),
    ]
    return f"{parts[0]} {parts[1]}, {parts[2]} {parts[3]}"


def professional_entity_presentation(entity: ProfessionalEntity, field_name: str) -> str:
    if entity.siege is None:
        raise ValueError(f"{field_name}.siege est obligatoire pour {CORE_DOCUMENT_CODE}.")
    representant = required_representant(entity.representant, f"{field_name}.representant")
    # Rafael 2026-07-09 (transverse devise) : unite derivee si montant nu (idempotent).
    capital = montant_avec_euros(
        required_text(entity.capital_social, f"{field_name}.capital_social")
    )
    return (
        f"{required_text(entity.denomination, f'{field_name}.denomination')}, "
        f"{required_text(entity.forme_sociale, f'{field_name}.forme_sociale')} "
        f"au capital de {capital}, "
        f"dont le siège est situé {address_display(entity.siege, f'{field_name}.siege')}, "
        "immatriculée au Registre du Commerce et des Sociétés de "
        f"{required_text(entity.ville_rcs, f'{field_name}.ville_rcs')} "
        f"sous le numéro {required_text(entity.numero_rcs, f'{field_name}.numero_rcs')}, "
        f"représentée par {representant_display(representant, f'{field_name}.representant')}"
    )


def address_display(address, field_name: str) -> str:
    if address.adresse_affichee:
        return address.adresse_affichee.strip()
    return (
        f"{required_text(address.num_voie, f'{field_name}.num_voie')} "
        f"{required_text(address.voie, f'{field_name}.voie')}, "
        f"{required_text(address.cp, f'{field_name}.cp')} "
        f"{required_text(address.ville, f'{field_name}.ville')}"
    )


def required_representant(
    representant: SpfplRepresentant | None,
    field_name: str,
) -> SpfplRepresentant:
    if representant is None:
        raise ValueError(f"{field_name} est obligatoire pour {CORE_DOCUMENT_CODE}.")
    return representant


def representant_display(representant: SpfplRepresentant, field_name: str) -> str:
    # R3 durci (Rafael 2026-07-07) : un titre (« Docteur »/« Dr ») posé en civilité de
    # représentant est rendu civil (le modèle SpfplRepresentant ne porte pas de genre
    # -> masculin par défaut, comme derive_gender_from_civilite côté front).
    civilite = civilite_civile(
        required_text(representant.civilite_affichage, f"{field_name}.civilite_affichage"),
        None,
    )
    return (
        f"{civilite} "
        f"{required_text(representant.prenom, f'{field_name}.prenom')} "
        f"{required_text(representant.nom, f'{field_name}.nom')}"
    )


def associe_display_name(associe: AssocieCible, field_name: str) -> str:
    if associe.type == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    # R3 durci (Rafael 2026-07-07) : « Docteur » (option historique du sélecteur des
    # associés cible) est rendu civil ; Monsieur/Madame passent inchangés.
    civilite = civilite_civile(
        required_text(associe.civilite_affichage, f"{field_name}.civilite_affichage"),
        getattr(associe, "genre", None),
    )
    return (
        f"{civilite} "
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def associe_signature_name(associe: AssocieCible, field_name: str) -> str:
    if associe.type == "personne_morale":
        return required_text(associe.denomination, f"{field_name}.denomination")
    return (
        f"{required_text(associe.prenom, f'{field_name}.prenom')} "
        f"{required_text(associe.nom, f'{field_name}.nom')}"
    )


def capital_after_lines(ctx: DocumentGenerationContext) -> list[str]:
    """Repartition du capital de la cible APRES l'operation, une ligne par associe.

    KAN-2 (Rafael 2026-07-14) : « tous les documents doivent pouvoir etre generes, meme si je ne
    remplis aucun champ » -> une repartition ABSENTE ou INCOHERENTE (total != parts totales) ne
    fait plus echouer la generation : elle sort en zone « (À COMPLÉTER : … ) » / telle quelle, a
    corriger a la main. Les anciennes gardes levaient APRES que le plan ait annonce « generable »
    (Akainu B2/B3).

    Akainu B4 : un nombre NON RENSEIGNE ne sort JAMAIS en valeur affirmee. 0 EST la valeur d'un
    champ non rempli (`number_input(min_value=0)`) -> « 0 parts sociales » serait une affirmation
    fausse dans un acte ; on rend un marqueur.
    """
    if not ctx.associes_cible:
        return ["(À COMPLÉTER : répartition du capital de la société cible après l'opération)"]

    lines: list[str] = []
    for index, associe in enumerate(ctx.associes_cible):
        field_name = f"associes_cible[{index}]"
        nb_parts = associe.nb_parts_apres or 0
        if nb_parts <= 0:
            lines.append(
                f"{associe_display_name(associe, field_name)}, titulaire de "
                "(À COMPLÉTER : nombre de parts sociales)"
            )
            continue
        part_label = "part sociale" if nb_parts == 1 else "parts sociales"
        details = (
            f"{associe_display_name(associe, field_name)}, titulaire de "
            f"{nb_parts} {part_label}"
        )
        if associe.numero_part_unique:
            details += f", numérotée {associe.numero_part_unique}"
        elif associe.plage_parts:
            details += f", numérotées de {associe.plage_parts}"
        lines.append(details)
    return lines


def capital_before_lines(ctx: DocumentGenerationContext) -> list[str]:
    societe_cible = required_societe_cible(ctx)
    total = required_int(societe_cible.nb_parts_total, "societe_cible.nb_parts_total")
    if not ctx.associes_cible:
        raise ValueError(f"associes_cible est obligatoire pour {CORE_DOCUMENT_CODE}.")

    lines: list[str] = []
    total_before = 0
    for index, associe in enumerate(ctx.associes_cible):
        field_name = f"associes_cible[{index}]"
        nb_parts = required_int(associe.nb_parts_avant, f"{field_name}.nb_parts_avant")
        total_before += nb_parts
        part_label = "part" if nb_parts == 1 else "parts"
        # Orthographe (Rafael 2026-07-07) : « détenant » accentué.
        lines.append(
            f"{associe_display_name(associe, field_name)} détenant {nb_parts} {part_label}"
        )

    if total_before != total:
        raise ValueError(
            "La repartition avant operation doit correspondre a "
            f"societe_cible.nb_parts_total pour {CORE_DOCUMENT_CODE}."
        )
    return lines


def presence_lines(ctx: DocumentGenerationContext) -> list[str]:
    """Associes presents ou representes a l'assemblee, une ligne chacun.

    KAN-2 (Rafael 2026-07-14) : aucun blocage — une liste vide ou un total qui ne couvre pas les
    parts totales ne fait plus echouer la generation (les gardes levaient APRES que le plan ait
    annonce « generable », Akainu B2/B3) : la zone sort « (À COMPLÉTER : … ) » / telle quelle et se
    corrige a la main. Akainu B4 : un nombre non renseigne (0 = valeur du champ non rempli) sort en
    marqueur, jamais en « 0 parts » affirme.
    """
    lines: list[str] = []
    for index, associe in enumerate(ctx.associes_cible):
        if not associe.est_present_ou_represente:
            continue
        field_name = f"associes_cible[{index}]"
        nb_parts = associe.nb_parts_avant or 0
        if nb_parts <= 0:
            lines.append(
                f"{associe_display_name(associe, field_name)} détenant "
                "(À COMPLÉTER : nombre de parts)"
            )
            continue
        part_label = "part" if nb_parts == 1 else "parts"
        # Orthographe (Rafael 2026-07-07) : « détenant » accentué.
        lines.append(
            f"{associe_display_name(associe, field_name)} détenant {nb_parts} {part_label}"
        )

    if not lines:
        return ["(À COMPLÉTER : associés présents ou représentés à l'assemblée)"]
    return lines


