"""Construction des fragments de contexte des documents de CREATION communs.

Le canon (`Documents_a_generer_par_cas.docx`) impose, pour chaque type, un BUNDLE
de creation = tronc commun (DNC, domiciliation, procuration) + documents
systematiques du type (statuts, PV nomination gerant, demande d'inscription a
l'ordre...) + conditionnel regime communautaire (renonciation + avertissement).

Le SELARL produit deja ce bundle complet via son slice dedie. Ce module factorise
la fabrication des fragments de `DocumentGenerationContext` requis par les
generateurs COMMUNS (lot_01 / lot_02) pour que les autres slices puissent emettre
le meme bundle, sans dupliquer la logique ni reinventer de regle metier : on ne
fait que MAPPER une saisie deja collectee vers les champs que les generateurs
existants exigent.

Codes communs cables ici :
- DOC-001 declaration de non-condamnation (lot_01)
- DOC-002 autorisation de domiciliation (lot_01)
- DOC-003 procuration (lot_01)
- DOC-004 PV nomination gerant (lot_02)
- DOC-034 demande d'inscription a l'ordre (lot_02)
- DOC-005 / DOC-006 regime communautaire (lot_02)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from unicodedata import combining, normalize

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Associe,
    CapitalContext,
    Company,
    DecisionContext,
    DirigeantNomine,
    Domiciliation,
    Mandataire,
    OrdreAddress,
    OrdreProfessionnel,
    Person,
    RegimeCommunautaire,
    RegimeCommunautaireAvertissement,
    RegimeCommunautaireRenonciation,
    ReunionContext,
    ReunionPresident,
)
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_CABINET,
    DEFAULT_MANDATAIRE_CIVILITE,
    DEFAULT_MANDATAIRE_FONCTION,
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    date_to_french_words,
    number_words_from_value,
)

# Codes des documents communs (tronc + lot_02) referencables par les bundles.
DOC_DECLARATION_NON_CONDAMNATION = "DOC-001"
DOC_AUTORISATION_DOMICILIATION = "DOC-002"
DOC_PROCURATION = "DOC-003"
DOC_PV_NOMINATION_GERANT = "DOC-004"
DOC_DEMANDE_INSCRIPTION_ORDRE = "DOC-034"
DOC_REGIME_RENONCIATION = "DOC-005"
DOC_REGIME_AVERTISSEMENT = "DOC-006"

TRONC_COMMUN_CODES: tuple[str, ...] = (
    DOC_DECLARATION_NON_CONDAMNATION,
    DOC_AUTORISATION_DOMICILIATION,
    DOC_PROCURATION,
)
REGIME_COMMUNAUTAIRE_CODES: tuple[str, ...] = (
    DOC_REGIME_RENONCIATION,
    DOC_REGIME_AVERTISSEMENT,
)


@dataclass
class FounderIdentity:
    """Identite du signataire / gerant utilisee par les documents communs.

    Regroupe le strict necessaire aux generateurs communs (DNC, domiciliation,
    procuration, PV gerant, demande d'inscription a l'ordre). Aucune valeur n'est
    inventee : ce sont des saisies collectees par le slice du type.
    """

    genre: Gender
    civilite: str
    prenom: str
    nom: str
    titre_affichage: str = "Docteur"
    fonction_dirigeant: str = "gérant"
    # Etat civil (DNC) :
    date_naissance: date | None = None
    ville_naissance: str = ""
    departement_naissance: str = ""
    nationalite: str = ""
    nom_pere: str = ""
    nom_mere: str = ""
    # Adresse personnelle structuree (DNC + procuration + PV gerant) :
    adresse_num_voie: str = ""
    adresse_voie: str = ""
    adresse_cp: str = ""
    adresse_ville: str = ""
    # Profession / ordre (demande d'inscription) :
    qualification_principale: str = ""
    profession_pluriel: str = ""


@dataclass
class CompanyAddress:
    num_voie: str = ""
    voie: str = ""
    cp: str = ""
    ville: str = ""

    @property
    def display(self) -> str:
        return f"{self.num_voie} {self.voie}, {self.cp} {self.ville}".strip(" ,")

    def to_address(self) -> Address:
        return Address(
            num_voie=self.num_voie,
            voie=self.voie,
            cp=self.cp,
            ville=self.ville,
            adresse_affichee=self.display,
        )


@dataclass
class OrdreInput:
    conseil_departemental_libelle: str = ""
    departement_inscription: str = ""
    adresse_ligne_1: str = ""
    cp: str = ""
    ville: str = ""
    numero: str = ""


@dataclass
class CommonDocsInput:
    """Saisies necessaires aux documents communs d'un dossier de creation."""

    founder: FounderIdentity
    capital_social: str
    nb_parts_total: int
    valeur_nominale_part: str
    siege: CompanyAddress
    signature_lieu: str
    signature_date: date | None
    decision_date: date | None
    signature_nombre_exemplaires: str = "quatre"
    ordre: OrdreInput = field(default_factory=OrdreInput)
    type_titre: str = "parts sociales"
    # Regime communautaire (optionnel) :
    regime_communautaire: bool = False
    regime_matrimonial: str = ""
    qualite_renoncee: str = "associé"
    conjoint_civilite: str = ""
    conjoint_genre: Gender = Gender.FEMININ
    conjoint_prenom: str = ""
    conjoint_nom: str = ""


def founder_person(common: CommonDocsInput) -> Person:
    f = common.founder
    address = common.founder_address()
    return Person(
        genre=f.genre,
        civilite=f.civilite,
        prenom=f.prenom,
        nom=f.nom,
        titre_affichage=f.titre_affichage,
        adresse_personnelle_affichee=address.adresse_affichee,
        adresse_perso=address,
        date_naissance=f.date_naissance,
        ville_naissance=f.ville_naissance,
        nationalite=f.nationalite,
        nom_pere=f.nom_pere,
        nom_mere=f.nom_mere,
        fonction_dirigeant=f.fonction_dirigeant,
        numero_inscription_ordre=common.ordre.numero,
        qualification_principale=f.qualification_principale,
    )


def _founder_address(common: CommonDocsInput) -> Address:
    f = common.founder
    display = f"{f.adresse_num_voie} {f.adresse_voie}, {f.adresse_cp} {f.adresse_ville}".strip(
        " ,"
    )
    return Address(
        num_voie=f.adresse_num_voie,
        voie=f.adresse_voie,
        cp=f.adresse_cp,
        ville=f.adresse_ville,
        adresse_affichee=display,
    )


# Methode attachee a CommonDocsInput pour reutilisation.
CommonDocsInput.founder_address = _founder_address  # type: ignore[attr-defined]


def domiciliation(siege: Address) -> Domiciliation:
    return Domiciliation(adresse_domiciliation_affichee=siege.adresse_affichee)


def default_mandataire() -> Mandataire:
    return Mandataire(
        civilite_affichage=DEFAULT_MANDATAIRE_CIVILITE,
        prenom=DEFAULT_MANDATAIRE_PRENOM,
        nom=DEFAULT_MANDATAIRE_NOM,
        fonction=DEFAULT_MANDATAIRE_FONCTION,
        cabinet=DEFAULT_MANDATAIRE_CABINET,
    )


def ordre_professionnel(common: CommonDocsInput) -> OrdreProfessionnel:
    o = common.ordre
    f = common.founder
    bloc = f"{o.adresse_ligne_1}\n{o.cp} {o.ville}"
    return OrdreProfessionnel(
        conseil_departemental_libelle=o.conseil_departemental_libelle,
        departement_inscription=o.departement_inscription,
        destinataire_appel="Monsieur le Président",
        profession_signataire_affichee=f.qualification_principale,
        profession_ligne_destinataire=f.profession_pluriel or f.qualification_principale,
        profession_reglementee_pluriel=f.profession_pluriel or f.qualification_principale,
        adresse_affichee=bloc,
        adresse_bloc_affiche=bloc,
        adresse=OrdreAddress(ligne_1=o.adresse_ligne_1, cp=o.cp, ville=o.ville),
    )


def capital_context(common: CommonDocsInput) -> CapitalContext:
    return CapitalContext(
        nb_parts_total=common.nb_parts_total,
        valeur_nominale_part=common.valeur_nominale_part,
        nb_parts_representees=common.nb_parts_total,
        montant=common.capital_social,
        montant_lettres=number_words_from_value(common.capital_social),
        nombre_titres_total=common.nb_parts_total,
        nombre_titres_total_lettres=number_words_from_value(common.nb_parts_total),
        valeur_nominale_titre=common.valeur_nominale_part,
        valeur_nominale_titre_lettres=number_words_from_value(common.valeur_nominale_part),
        type_titre=common.type_titre,
    )


def dirigeant_nomine(common: CommonDocsInput) -> DirigeantNomine:
    f = common.founder
    return DirigeantNomine(
        genre=f.genre,
        civilite_affichage=f.civilite,
        prenom=f.prenom,
        nom=f.nom,
        date_naissance=f.date_naissance,
        ville_naissance=f.ville_naissance,
        departement_naissance=f.departement_naissance,
        nationalite=f.nationalite,
        adresse_personnelle=common.founder_address(),
        fonction_affichage=f.fonction_dirigeant,
        ref_associe_index=0,
    )


def reunion_context(common: CommonDocsInput) -> ReunionContext:
    f = common.founder
    return ReunionContext(
        date_lettres=date_to_french_words(common.decision_date),
        president=ReunionPresident(
            civilite_affichage=f.civilite,
            prenom=f.prenom,
            nom=f.nom,
            qualite="associé unique",
            civilite_president_seance=f.civilite,
            prenom_president_seance=f.prenom,
            nom_personne_seance=f.nom,
        ),
    )


def decision_context(common: CommonDocsInput) -> DecisionContext:
    return DecisionContext(date=_display_date(common.decision_date))


def regime_communautaire(common: CommonDocsInput) -> RegimeCommunautaire | None:
    if not common.regime_communautaire:
        return None
    return RegimeCommunautaire(
        avertissement=RegimeCommunautaireAvertissement(
            date_signature=common.signature_date,
        ),
        renonciation=RegimeCommunautaireRenonciation(
            lieu_signature=common.signature_lieu,
            date_signature=common.signature_date,
            nombre_exemplaires_lettres=common.signature_nombre_exemplaires,
        ),
        date_courrier_avertissement=common.signature_date,
        regime_matrimonial=common.regime_matrimonial,
        qualite_renoncee=common.qualite_renoncee,
    )


def conjoint_person(common: CommonDocsInput) -> Person | None:
    if not common.regime_communautaire:
        return None
    address = common.founder_address()
    return Person(
        genre=common.conjoint_genre,
        civilite=common.conjoint_civilite,
        prenom=common.conjoint_prenom,
        nom=common.conjoint_nom,
        adresse_personnelle_affichee=address.adresse_affichee,
        adresse_perso=address,
    )


def founder_associe(common: CommonDocsInput) -> Associe:
    """Associe unique signataire (PV gerant : parts = totalite du capital)."""
    f = common.founder
    return Associe(
        genre=f.genre,
        civilite_affichage=f.civilite,
        prenom=f.prenom,
        nom=f.nom,
        nb_parts=common.nb_parts_total,
        nb_parts_lettres=number_words_from_value(common.nb_parts_total),
        profession=f.qualification_principale,
        profession_reglementee=f.qualification_principale,
        profession_reglementee_pluriel=f.profession_pluriel or f.qualification_principale,
        qualification_principale=f.qualification_principale,
        titre_professionnel=f.titre_affichage,
        qualite="associé unique",
        date_naissance=f.date_naissance,
        ville_naissance=f.ville_naissance,
        departement_naissance=f.departement_naissance,
        nationalite=f.nationalite,
        adresse_personnelle=common.founder_address(),
        adresse_personnelle_affichee=common.founder_address().adresse_affichee,
    )


def company_with_common_fields(
    base: Company,
    common: CommonDocsInput,
    *,
    capital_with_euros: str | None = None,
) -> Company:
    """Complete une `Company` avec les champs requis par les docs communs.

    - `capital` / `capital_social` : DOC-002 exige un capital non vide.
    - `siege` structure : DOC-002 / DOC-003 / DOC-004 exigent num_voie/voie/cp/ville.
    """
    update: dict[str, object] = {}
    if not (base.capital or "").strip():
        update["capital"] = capital_with_euros or common.capital_social
    if not (base.capital_social or "").strip():
        update["capital_social"] = capital_with_euros or common.capital_social
    if base.siege is None or not (base.siege.num_voie or "").strip():
        update["siege"] = common.siege.to_address()
    if not update:
        return base
    return base.model_copy(update=update)


def _display_date(value: date | None) -> str | None:
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


_FRENCH_MONTHS: dict[str, int] = {
    "janvier": 1,
    "fevrier": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "decembre": 12,
}


def parse_birth_date(value: object) -> date | None:
    """Parse une date de naissance saisie en dd/mm/aaaa OU en francais long.

    Accepte « 01/01/1980 », « 1 janvier 1980 », « 1er janvier 1980 ». Aucune
    invention : retourne None si la chaine n'est pas une date reconnaissable.
    """
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    iso = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if iso is not None:
        day, month, year = (int(part) for part in iso.groups())
        return _safe_date(year, month, day)
    normalized = "".join(c for c in normalize("NFKD", text.lower()) if not combining(c))
    match = re.fullmatch(r"(\d{1,2})(?:er)?\s+([a-z]+)\s+(\d{4})", normalized.strip())
    if match is None:
        return None
    day = int(match.group(1))
    month = _FRENCH_MONTHS.get(match.group(2))
    year = int(match.group(3))
    if month is None:
        return None
    return _safe_date(year, month, day)


def _safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None
