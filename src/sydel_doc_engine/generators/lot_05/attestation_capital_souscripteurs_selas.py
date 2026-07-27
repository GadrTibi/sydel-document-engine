from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    CapitalSouscripteur,
    CapitalSouscription,
    DocumentGenerationContext,
    SocieteSpfpl,
)
from sydel_doc_engine.generators.lot_01.civilite import civilite_civile
from sydel_doc_engine.rendering.docx_builder import (
    add_company_identity_block,
    add_paragraph,
    add_spacer,
    keep_final_signature_block_together,
    new_document,
)
from sydel_doc_engine.utils.dates import format_date_fr
from sydel_doc_engine.utils.grammar import euro_word, montant_avec_euros, subject_line

OUTPUT_FILENAME = "attestation_capital_souscripteurs_selas.docx"
DOCUMENT_CODE = "CODE-SELAS-ATTESTATION-CAPITAL-001"
SELAS_STRUCTURE = "SELAS"

# KAN-46 (Rafael) : « reprendre la mise en forme globale » — meme aeration que les
# attestations soeurs SAS/SPFPL : un espaceur entre les GROUPES (designation societe,
# bloc titre, corps, certification, signature).
_ATTESTATION_GROUP_SPACER_PT = 10

# KAN-2 (Rafael, rejeté 2×) : « Tous les documents doivent pouvoir être générés, MÊME SANS AUCUN
# champ. » Un champ manquant -> marqueur métier « (À COMPLÉTER : libellé) », jamais un raise ni une
# valeur inventée. Libellé MÉTIER via spfpl_libelles.libelle_metier ; repli LOCAL si l'import échoue
# -> marqueur toujours sans point / underscore / crochet / chiffre.
try:  # pragma: no cover - import trivial
    from sydel_doc_engine.generators.lot_05.spfpl_libelles import libelle_metier as _libelle_metier
except Exception:  # pragma: no cover - repli défensif
    _libelle_metier = None


def _libelle(field_name: str) -> str:
    if _libelle_metier is not None:
        return _libelle_metier(field_name)
    raw = field_name.replace("[", "").replace("]", "").replace("_", " ").replace(".", " ")
    words = [w.rstrip("0123456789").lower() for w in raw.split()]
    return " ".join(w for w in words if w)


def _marqueur(field_name: str) -> str:
    return f"(À COMPLÉTER : {_libelle(field_name)})"


class AttestationCapitalSouscripteursSelasGenerator:
    """Generateur from-scratch de l'attestation capital / liste des souscripteurs SELAS.

    Variante MULTI-SOUSCRIPTEURS (1..6 associes), apports en NUMERAIRE.

    Le wording est reproduit VERBATIM depuis le modele Albane 2026-06-17
    (MODELE_Attestation_capital_liste_souscripteurs.docx). Chaque souscripteur
    genere une ligne de repartition et une ligne d'apport en numeraire ; le
    montant en numeraire d'un souscripteur est determine par
    nb_actions x valeur_nominale (capital SELAS = numeraire pur).

    EXCEPTION au verbatim — R3 durci (Rafael 2026-07-07, supersede A26-45/49) :
    les slots de personne du modele (« au Dr X », « Le Docteur X a fait un
    apport », « par le President, Docteur X ») rendent la civilite CIVILE
    (Monsieur/Madame accordee au genre), « Docteur »/« Dr » ne sort jamais.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedAttestationSelas.from_context(ctx)
        document = new_document()

        add_company_identity_block(
            document,
            [
                data.denomination,
                "Société d'exercice libérale par Actions simplifiées de "
                f"{data.profession}",
                f"Au capital de {montant_avec_euros(data.capital_social)}",
                f"Siège social : {data.adresse_siege}",
                "En cours d'immatriculation",
            ],
        )
        # KAN-46 : aeration entre la designation de la societe et le bloc titre.
        add_spacer(document, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        add_paragraph(document, "ATTESTATION", alignment=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
        add_paragraph(
            document,
            "Liste des souscripteurs",
            alignment=WD_ALIGN_PARAGRAPH.CENTER,
            bold=True,
        )
        # KAN-46 : aeration entre le bloc titre et le corps.
        add_spacer(document, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        add_paragraph(
            document,
            f"{data.soussigne} {data.president_civilite_phrase} {data.president_signature}, "
            f"Président de la Société {data.denomination}, atteste que le capital de ladite "
            "société est réparti de la manière suivante :",
            alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
        )
        add_paragraph(document, f"Capital social : {data.capital_social} € en numéraire")
        add_paragraph(
            document,
            # Akainu batch2 M1 (2026-07-09) : accord euro/euros via euro_word (« euro » etait
            # code en dur -> « 10 euro » ; siloing vs les 3 attestations soeurs SAS/SPFPL/cession).
            f"Nombre d'actions: {data.nb_actions_total} actions d'un montant de "
            f"{data.valeur_nominale_action} {euro_word(data.valeur_nominale_action)} chacune",
        )
        add_paragraph(document, "Répartition : ")
        for repartition in data.repartition_lignes:
            add_paragraph(document, repartition)
        # KAN-46 (Rafael) : reporter l'ADRESSE de la banque, pas juste son nom.
        add_paragraph(
            document,
            f"Capital social de {data.capital_social} € entièrement libéré et déposé "
            f"dans les livres de la banque {data.banque}, {data.banque_adresse}",
        )
        for apport in data.apport_lignes:
            add_paragraph(document, apport)
        # KAN-46 : aeration avant la clause de certification.
        add_spacer(document, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        add_paragraph(
            document,
            "Le présent état qui constate la souscription d'actions de la société "
            f"{data.denomination}, ainsi que le versement de la somme de "
            f"{montant_avec_euros(data.capital_social)} correspondant à la totalité du nominal "
            "desdites actions, est certifié exact, sincère et véritable par le Président, "
            # KAN-46 : point final apres le nom (« ... par le President, <Nom>. »).
            f"{data.president_identite}.",
        )
        # KAN-46 : aeration avant le bloc de signature.
        add_spacer(document, space_after_pt=_ATTESTATION_GROUP_SPACER_PT)
        add_paragraph(document, f"Fait à {data.ville_siege}")
        add_paragraph(document, f"Le {data.date_signature}")
        add_paragraph(document, data.president_signature)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        # KAN-36 : bloc signature final solidaire (une seule page).
        keep_final_signature_block_together(document)
        document.save(output_path)
        return output_path


class _ResolvedAttestationSelas:
    def __init__(
        self,
        *,
        denomination: str,
        profession: str,
        capital_social: str,
        adresse_siege: str,
        ville_siege: str,
        banque: str,
        banque_adresse: str,
        nb_actions_total: int | str,
        valeur_nominale_action: str,
        repartition_lignes: list[str],
        apport_lignes: list[str],
        soussigne: str,
        president_civilite_phrase: str,
        president_identite: str,
        president_signature: str,
        date_signature: str,
    ) -> None:
        self.denomination = denomination
        self.profession = profession
        self.capital_social = capital_social
        self.adresse_siege = adresse_siege
        self.ville_siege = ville_siege
        self.banque = banque
        self.banque_adresse = banque_adresse
        self.nb_actions_total = nb_actions_total
        self.valeur_nominale_action = valeur_nominale_action
        self.repartition_lignes = repartition_lignes
        self.apport_lignes = apport_lignes
        self.soussigne = soussigne
        self.president_civilite_phrase = president_civilite_phrase
        self.president_identite = president_identite
        self.president_signature = president_signature
        self.date_signature = date_signature

    @classmethod
    def from_context(
        cls,
        ctx: DocumentGenerationContext,
    ) -> _ResolvedAttestationSelas:
        _validate_scope(ctx)
        societe = _required_societe_spfpl(ctx)
        capital = _required_capital_souscription(ctx)
        souscripteurs = _required_souscripteurs(capital.souscripteurs)
        president = capital.president or souscripteurs[0]

        # KAN-2 : AFFICHAGE des quantités -> marqueur si manquant ; le CALCUL (montant en numéraire
        # = nb_actions × valeur nominale, cohérence de répartition) lit les valeurs BRUTES et se
        # neutralise si incomplet. Dossier complet -> sortie byte-identique.
        nb_actions_total_display = _required_int(
            capital.nb_actions_total,
            "capital_souscription.nb_actions_total",
        )
        valeur_nominale_action = _required_text(
            capital.valeur_nominale_action,
            "capital_souscription.valeur_nominale_action",
        )
        valeur_nominale = _euro_amount_or_none(valeur_nominale_action)

        repartition_lignes: list[str] = []
        apport_lignes: list[str] = []
        total_actions = 0
        toutes_actions_connues = True
        for index, souscripteur in enumerate(souscripteurs):
            field = f"capital_souscription.souscripteurs[{index}]"
            nb_actions_display = _required_int(souscripteur.nb_actions, f"{field}.nb_actions")
            nb_actions_brut = souscripteur.nb_actions
            if nb_actions_brut is None:
                toutes_actions_connues = False
            else:
                total_actions += nb_actions_brut
            # R3 durci (Rafael 2026-07-07, siloing) : « au Dr X » / « Le Docteur X a
            # fait un apport » etaient RESTES dans cette variante pluripersonnelle
            # alors que l'unipersonnelle etait deja civile -> les DEUX slots rendent
            # la civilite CIVILE du souscripteur (Monsieur/Madame, accordee a SON
            # genre), jamais le titre « Dr / Docteur ».
            nom_complet = _souscripteur_signature(souscripteur, field)
            civilite = civilite_civile(
                _required_text(
                    souscripteur.civilite_affichage,
                    f"{field}.civilite_affichage",
                ),
                souscripteur.genre,
            )
            repartition_lignes.append(
                f"{nb_actions_display} actions attribuées à {civilite} {nom_complet},"
            )
            if valeur_nominale is not None and nb_actions_brut is not None:
                montant_numeraire = montant_avec_euros(
                    _format_amount(valeur_nominale * Decimal(nb_actions_brut))
                )
            else:
                montant_numeraire = _marqueur("apport en numeraire du souscripteur")
            apport_lignes.append(
                f"{civilite} {nom_complet} a fait un apport de "
                f"{montant_numeraire} en numéraire."
            )

        if (
            capital.nb_actions_total is not None
            and toutes_actions_connues
            and total_actions != capital.nb_actions_total
        ):
            raise ValueError(
                "La répartition des souscripteurs doit correspondre à "
                f"capital_souscription.nb_actions_total pour {DOCUMENT_CODE}."
            )

        # R3 (Albane 2026-07-07) : « Docteur » n'est pas une civilité — le slot
        # « par le Président, __ » rend la civilité CIVILE (Monsieur/Madame),
        # jamais le titre d'affichage. R3 durci (Rafael 2026-07-07) : accord au
        # genre DU PRESIDENT quand le modele le porte ; repli sur le genre du
        # signataire (appelants legacy sans genre — comportement historique).
        president_civilite = civilite_civile(
            _required_text(
                president.civilite_affichage,
                "capital_souscription.president.civilite_affichage",
            ),
            president.genre or ctx.personne_signataire.genre,
        )
        president_signature = _souscripteur_signature(
            president,
            "capital_souscription.president",
        )

        return cls(
            denomination=_required_text(societe.denomination, "societe_spfpl.denomination"),
            profession=_required_text(societe.profession, "societe_spfpl.profession"),
            capital_social=_required_text(
                societe.capital_social,
                "societe_spfpl.capital_social",
            ),
            adresse_siege=_company_siege_display(societe, "societe_spfpl"),
            ville_siege=_company_ville(societe, "societe_spfpl"),
            banque=_required_banque(ctx),
            banque_adresse=_required_banque_adresse(ctx),
            nb_actions_total=nb_actions_total_display,
            valeur_nominale_action=valeur_nominale_action,
            repartition_lignes=repartition_lignes,
            apport_lignes=apport_lignes,
            soussigne=subject_line(ctx.personne_signataire.genre),
            president_civilite_phrase=_addressing_civilite(ctx.personne_signataire.genre),
            president_identite=f"{president_civilite} {president_signature}",
            president_signature=president_signature,
            date_signature=format_date_fr(ctx.signature.date),
        )


def _validate_scope(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != SELAS_STRUCTURE:
        raise ValueError(
            f"dossier.structure doit etre {SELAS_STRUCTURE} pour {DOCUMENT_CODE}."
        )


def _required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    if ctx.societe_spfpl is None:
        raise ValueError(f"societe_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_spfpl


def _required_capital_souscription(
    ctx: DocumentGenerationContext,
) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.capital_souscription


def _required_souscripteurs(
    souscripteurs: list[CapitalSouscripteur],
) -> list[CapitalSouscripteur]:
    if not souscripteurs:
        raise ValueError(
            "capital_souscription.souscripteurs doit contenir au moins un souscripteur "
            f"pour {DOCUMENT_CODE}."
        )
    return souscripteurs


def _required_banque(ctx: DocumentGenerationContext) -> str:
    if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
        raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
    return _required_text(ctx.depot_fonds.banque.nom, "depot_fonds.banque.nom")


def _required_banque_adresse(ctx: DocumentGenerationContext) -> str:
    # KAN-46 : l'adresse de la banque, en marqueur « (À COMPLÉTER : adresse de la
    # banque) » si absente (KAN-2), jamais une valeur inventée.
    if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
        raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
    return _required_text(
        ctx.depot_fonds.banque.adresse_affichee,
        "depot_fonds.banque.adresse_affichee",
    )


def _required_text(value: str | None, field_name: str) -> str:
    # KAN-2 : champ vide -> marqueur, jamais un raise. Champ rempli -> byte-identique.
    if value is None or not value.strip():
        return _marqueur(field_name)
    return value.strip()


def _required_int(value: int | None, field_name: str) -> int | str:
    # KAN-2 : entier manquant en AFFICHAGE -> marqueur (le CALCUL lit la valeur brute, cf.
    # from_context). Valeur présente -> int inchangé.
    if value is None:
        return _marqueur(field_name)
    return value


def _euro_amount_or_none(value: str) -> Decimal | None:
    # KAN-2 : montant non numérique / manquant (y compris un marqueur « (À COMPLÉTER : …) »)
    # -> None, jamais un raise. Le calcul en numéraire est alors neutralisé (marqueur affiché).
    normalized = (
        (value or "")
        .lower()
        .replace("euros", "")
        .replace("euro", "")
        .replace("€", "")
        .replace(" ", "")
        .replace(" ", "")
        .replace(",", ".")
        .strip()
    )
    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None


def _format_amount(amount: Decimal) -> str:
    """Rend un montant euro sans decimale parasite (1000.00 -> 1000, 1.50 -> 1,50)."""
    normalized = amount.normalize()
    if normalized == normalized.to_integral_value():
        return f"{int(normalized)}"
    return format(normalized, "f").replace(".", ",")


def _souscripteur_signature(souscripteur: CapitalSouscripteur, field_name: str) -> str:
    return (
        f"{_required_text(souscripteur.prenom, f'{field_name}.prenom')} "
        f"{_required_text(souscripteur.nom, f'{field_name}.nom')}"
    )


def _addressing_civilite(genre: Gender) -> str:
    """Civilite d'adresse du president dans « Je soussigné ... » (Monsieur/Madame).

    Derivee verbatim du modele (« Je soussigné Monsieur Alain FEDOROWSKY »). Le
    titre d'affichage (« Docteur ») ne porte pas le genre : la forme d'adresse est
    accordee sur le genre du signataire (accord en genre demande par les retours),
    jamais inventee.
    """
    return "Madame" if genre == Gender.FEMININ else "Monsieur"


def _company_siege_display(societe: SocieteSpfpl, field_name: str) -> str:
    # KAN-2 : siège absent -> marqueur, jamais un raise.
    if societe.siege is None:
        return _marqueur(f"{field_name}.siege")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    return (
        f"{_required_text(societe.siege.num_voie, f'{field_name}.siege.num_voie')} "
        f"{_required_text(societe.siege.voie, f'{field_name}.siege.voie')}, "
        f"{_required_text(societe.siege.cp, f'{field_name}.siege.cp')} "
        f"{_required_text(societe.siege.ville, f'{field_name}.siege.ville')}"
    )


def _company_ville(societe: SocieteSpfpl, field_name: str) -> str:
    # KAN-2 : siège absent -> marqueur, jamais un raise.
    if societe.siege is None:
        return _marqueur(f"{field_name}.siege.ville")
    return _required_text(societe.siege.ville, f"{field_name}.siege.ville")
