from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from docx import Document

from sydel_doc_engine.domain.models import (
    CapitalSouscription,
    DocumentGenerationContext,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    StatutsPresident,
)
from sydel_doc_engine.generators.lot_05.scm_cession_common import mentions_conjoint
from sydel_doc_engine.rendering.docx_builder import apply_style_profile
from sydel_doc_engine.rendering.docx_template_fill import fill_docx_template

DOCUMENT_CODE = "CODE-STATUTS-SAS-001"
OUTPUT_FILENAME = "statuts_sas_spfpl_medecins.docx"
STATUTS_SAS_TYPE = "spfpl_medecins"
STATUTS_SAS_PROFESSION = "medecin"

# Dossier des modeles Word tokenises, resolu independamment du cwd.
_SOURCE_MODELS_DIR = (
    Path(__file__).resolve().parents[4] / "project" / "source_documents" / "lot_04"
)
_MODEL_NAME = "STATUTS_SAS_SPFPL_medecins_modele.docx"

# Normalisation byte-neutre vs la sortie de reference du moteur : le modele Albane
# porte des tabulations d'alignement (bloc capital/apports) que la sortie validee rend
# en espaces simples.
_TAB_RE = re.compile(r"[ ]*\t+[ ]*")


class StatutsSasGenerator:
    """Generateur des statuts SAS / SPFPL medecins V1.

    Token-replacement sur le modele Albane tokenise (STATUTS_SAS_SPFPL_medecins_modele.docx) :
    le texte juridique fige (les ~27 articles) vit dans le modele, seuls les [tokens] sont
    remplaces par les valeurs du dossier. Migration 2026-06-29 (decision PM) : l'ancienne
    version reconstruisait ~1100 lignes de prose en dur (perte de fidelite au modele) ; on
    lit desormais le document reel d'Albane. La couche de VALIDATION metier (actionnaire
    unique, coherence du capital, phrase matrimoniale stabilisee) est conservee a l'identique.

    Fidelite (gate Akainu 2026-06-29) : la PROSE juridique est byte-identique a la sortie
    validee (zero mot change) ; les espaces (NBSP / tabulations d'alignement) sont normalises
    en espaces simples comme la sortie de reference (cf. _normalize_paragraph). Le gras/souligne
    suit le MODELE d'Albane : 3 intitules ("Le soussigne :", l'entree du soussigne, la
    denomination a l'article 3) y gagnent l'emphase que l'ancien from-scratch avait laissee
    tomber -> rendu PLUS fidele au document source (et non une regression). Le defaut
    d'authoring du modele (ARTICLE 23 non souligne, seul des 27) a ete corrige dans le .docx.
    """

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        data = _ResolvedStatutsSas.from_context(ctx)
        replacements = _build_replacements(data)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        fill_docx_template(_resolve_model_path(), replacements, output_path)
        _apply_style_footer_normalize(output_path, data.denomination)
        # R0702-02 : pour un actionnaire NON MARIE, replie la comparution matrimoniale du modele
        # sur le seul statut (le modele est token-based, « sous le régime de »/« avec » sont
        # LITTERAUX -> pas remplaçables par token ; on post-traite). Marie -> non touche.
        _collapse_marital_sentence(output_path, data.actionnaire)
        return output_path


def _build_replacements(data: _ResolvedStatutsSas) -> dict[str, str]:
    """Mappe les [tokens] du modele aux valeurs resolues du dossier."""
    actionnaire = data.actionnaire
    ordre = _required_ordre(actionnaire)
    # R0702-02 : le conjoint + le regime n'existent QUE pour un actionnaire MARIE (menu complet
    # « Situation matrimoniale »). Garde partagee mentions_conjoint : marie -> tokens remplis
    # (BYTE-IDENTIQUE a avant) ; sinon -> "" et la ligne de comparution du modele est repliee sur le
    # seul statut en post-traitement (_collapse_marital_sentence). Le statut est TOUJOURS rendu.
    _is_married = mentions_conjoint(actionnaire.situation_maritale)
    if _is_married:
        conjoint = _required_conjoint(actionnaire)
        _regime_token = _required_text(
            actionnaire.regime_matrimonial, "actionnaire_unique.regime_matrimonial"
        )
        _civilite_conjoint = _required_text(
            conjoint.civilite_affichage, "actionnaire_unique.conjoint.civilite"
        )
        _prenom_conjoint = _required_text(conjoint.prenom, "actionnaire_unique.conjoint.prenom")
        _nom_conjoint = _required_text(conjoint.nom, "actionnaire_unique.conjoint.nom")
    else:
        _regime_token = _civilite_conjoint = _prenom_conjoint = _nom_conjoint = ""
    return {
        "[denomination_societe]": data.denomination,
        "[capital_social]": data.capital_social,
        "[capital_lettres]": data.capital_social_lettres,
        "[adresse_siege]": data.adresse_siege,
        "[nb_actions]": str(data.nb_actions_total),
        "[nb_actions_lettres]": data.nb_actions_total_lettres,
        "[valeur_nominale_action]": data.valeur_nominale_action,
        "[valeur_nominale_action_lettres]": data.valeur_nominale_action_lettres,
        "[civilite]": _required_text(
            actionnaire.civilite_affichage, "actionnaire_unique.civilite_affichage"
        ),
        "[prenom]": _required_text(actionnaire.prenom, "actionnaire_unique.prenom"),
        "[nom]": _required_text(actionnaire.nom, "actionnaire_unique.nom"),
        "[date_naissance]": _format_display_date(
            actionnaire.date_naissance, "actionnaire_unique.date_naissance"
        ),
        "[ville_naissance]": _required_text(
            actionnaire.ville_naissance, "actionnaire_unique.ville_naissance"
        ),
        "[departement_naissance]": _required_text(
            actionnaire.departement_naissance, "actionnaire_unique.departement_naissance"
        ),
        "[nationalite]": _required_text(
            actionnaire.nationalite, "actionnaire_unique.nationalite"
        ),
        "[adresse_personnelle]": _person_address(actionnaire, "actionnaire_unique"),
        "[situation_maritale]": _required_text(
            actionnaire.situation_maritale, "actionnaire_unique.situation_maritale"
        ),
        "[regime_matrimonial]": _regime_token,
        "[civilite_conjoint]": _civilite_conjoint,
        "[prenom_conjoint]": _prenom_conjoint,
        "[nom_conjoint]": _nom_conjoint,
        "[numero_ordre]": _required_text(ordre.numero, "actionnaire_unique.ordre.numero"),
        "[numero_rpps]": _required_text(
            ordre.numero_rpps, "actionnaire_unique.ordre.numero_rpps"
        ),
        "[ordre_departemental]": _required_text(
            ordre.departement, "actionnaire_unique.ordre.departement"
        ),
        "[qualification_principale]": _qualification(actionnaire),
        "[nom_banque]": data.banque_nom,
        "[debut_exercice]": data.exercice_debut,
        "[fin_exercice]": data.exercice_fin,
        "[date_cloture_exercice_1]": data.exercice_cloture_1,
        "[lieu_signature]": data.signature_lieu,
    }


def _resolve_model_path() -> Path:
    candidate = _SOURCE_MODELS_DIR / _MODEL_NAME
    if not candidate.is_file():
        raise ValueError(f"Modele introuvable pour {DOCUMENT_CODE} : {candidate}.")
    return candidate


def _apply_style_footer_normalize(output_path: Path, denomination: str) -> None:
    document = Document(str(output_path))
    apply_style_profile(document)
    footer_text = f"{denomination} \u2013 Statuts constitutifs"
    # Le modele porte le token dans le pied de page (parfois duplique en first/even-page) que
    # fill_docx_template ne traverse pas : on le complete ici.
    for section in document.sections:
        for footer in (section.footer, section.first_page_footer, section.even_page_footer):
            for paragraph in footer.paragraphs:
                if "[denomination_societe]" in paragraph.text:
                    paragraph.text = footer_text
    for paragraph in document.paragraphs:
        _normalize_paragraph(paragraph)
    document.save(str(output_path))


def _collapse_marital_sentence(output_path: Path, actionnaire: SpfplPerson) -> None:
    """Replie la comparution matrimoniale sur le SEUL statut pour un actionnaire NON MARIE.

    R0702-02 : le modele SAS ecrit « <statut> sous le régime de <regime> avec <Civ Prénom Nom> » ;
    pour un non-marie, regime + conjoint sont vides (« sous le régime de  avec » orphelin). On
    remplace le paragraphe de comparution par le seul statut (« Célibataire »). Meme approche que la
    SPFPL (collapse, PAS de wording source invente). Un MARIE n'est PAS touche (byte-identique)."""
    if mentions_conjoint(actionnaire.situation_maritale):
        return
    statut = _required_text(
        actionnaire.situation_maritale, "actionnaire_unique.situation_maritale"
    )
    document = Document(str(output_path))
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text.startswith(statut) and "sous le régime de" in text and "avec" in text:
            if paragraph.runs:
                paragraph.runs[0].text = statut
                # n3 (Akainu) : SUPPRIME les runs suivants (plus de run vide residuel) plutot que
                # de les vider — le paragraphe ne porte plus que le seul run « <statut> ».
                for run in paragraph.runs[1:]:
                    run._element.getparent().remove(run._element)
            else:
                paragraph.text = statut
            break
    document.save(str(output_path))


def _normalize_paragraph(paragraph) -> None:
    """Aligne le rendu du modele sur la sortie de reference (byte-neutre).

    Le modele porte des espaces insecables (NBSP, typographie guillemets/deux-points) et des
    tabulations d'alignement ; la sortie validee les rend en espaces simples. On normalise par
    run (preserve gras/souligne) puis on retire les espaces de fin de paragraphe.
    """
    for run in paragraph.runs:
        text = run.text
        if "\xa0" in text:
            text = text.replace("\xa0", " ")
        if "\t" in text:
            text = _TAB_RE.sub(" ", text)
        if text != run.text:
            run.text = text
    runs = paragraph.runs
    index = len(runs) - 1
    while index >= 0:
        stripped = runs[index].text.rstrip()
        if stripped != runs[index].text:
            runs[index].text = stripped
        if stripped:
            break
        index -= 1


class _ResolvedStatutsSas:
    def __init__(
        self,
        *,
        denomination: str,
        capital_social: str,
        capital_social_lettres: str,
        nb_actions_total: int,
        nb_actions_total_lettres: str,
        valeur_nominale_action: str,
        valeur_nominale_action_lettres: str,
        adresse_siege: str,
        actionnaire: SpfplPerson,
        president: StatutsPresident,
        banque_nom: str,
        exercice_debut: str,
        exercice_fin: str,
        exercice_cloture_1: str,
        signature_lieu: str,
    ) -> None:
        self.denomination = denomination
        self.capital_social = capital_social
        self.capital_social_lettres = capital_social_lettres
        self.nb_actions_total = nb_actions_total
        self.nb_actions_total_lettres = nb_actions_total_lettres
        self.valeur_nominale_action = valeur_nominale_action
        self.valeur_nominale_action_lettres = valeur_nominale_action_lettres
        self.adresse_siege = adresse_siege
        self.actionnaire = actionnaire
        self.president = president
        self.banque_nom = banque_nom
        self.exercice_debut = exercice_debut
        self.exercice_fin = exercice_fin
        self.exercice_cloture_1 = exercice_cloture_1
        self.signature_lieu = signature_lieu

    @classmethod
    def from_context(cls, ctx: DocumentGenerationContext) -> _ResolvedStatutsSas:
        _validate_sas_scope(ctx)
        societe = _required_societe_spfpl(ctx)
        actionnaire = _required_actionnaire(ctx)
        president = _required_president(ctx)
        capital = _required_capital_souscription(ctx)
        _validate_actionnaire_unique(ctx, actionnaire, president, capital)
        _validate_capital(societe, actionnaire, capital)
        _validate_marital_sentence(actionnaire)

        if ctx.depot_fonds is None or ctx.depot_fonds.banque is None:
            raise ValueError(f"depot_fonds.banque est obligatoire pour {DOCUMENT_CODE}.")
        if ctx.exercice_social is None:
            raise ValueError(f"exercice_social est obligatoire pour {DOCUMENT_CODE}.")

        depot_montant = ctx.depot_fonds.montant
        capital_social = _required_text(societe.capital_social, "societe_spfpl.capital_social")
        if depot_montant is not None and depot_montant.strip() != capital_social:
            raise ValueError(
                "depot_fonds.montant doit etre coherent avec "
                f"societe_spfpl.capital_social pour {DOCUMENT_CODE}."
            )

        return cls(
            denomination=_required_text(societe.denomination, "societe_spfpl.denomination"),
            capital_social=capital_social,
            capital_social_lettres=_required_text(
                societe.capital_social_lettres,
                "societe_spfpl.capital_social_lettres",
            ),
            nb_actions_total=_required_int(
                societe.nb_actions_total,
                "societe_spfpl.nb_actions_total",
            ),
            nb_actions_total_lettres=_required_text(
                societe.nb_actions_total_lettres,
                "societe_spfpl.nb_actions_total_lettres",
            ),
            valeur_nominale_action=_required_text(
                societe.valeur_nominale_action,
                "societe_spfpl.valeur_nominale_action",
            ),
            valeur_nominale_action_lettres=_required_text(
                societe.valeur_nominale_action_lettres,
                "societe_spfpl.valeur_nominale_action_lettres",
            ),
            adresse_siege=_address_display(societe),
            actionnaire=actionnaire,
            president=president,
            banque_nom=_required_text(ctx.depot_fonds.banque.nom, "depot_fonds.banque.nom"),
            exercice_debut=_required_text(
                ctx.exercice_social.debut,
                "exercice_social.debut",
            ),
            exercice_fin=_required_text(ctx.exercice_social.fin, "exercice_social.fin"),
            exercice_cloture_1=_required_text(
                ctx.exercice_social.date_cloture_premier_exercice,
                "exercice_social.date_cloture_premier_exercice",
            ),
            signature_lieu=ctx.signature.lieu,
        )


def _validate_sas_scope(ctx: DocumentGenerationContext) -> None:
    if ctx.structure != "SAS":
        raise ValueError(f"dossier.structure doit etre SAS pour {DOCUMENT_CODE}.")
    if ctx.statuts_sas is None:
        raise ValueError(f"statuts_sas est obligatoire pour {DOCUMENT_CODE}.")
    statuts_type = _required_text(ctx.statuts_sas.type, "statuts_sas.type").lower()
    profession = _required_text(ctx.statuts_sas.profession, "statuts_sas.profession").lower()
    if statuts_type != STATUTS_SAS_TYPE:
        raise ValueError(f"statuts_sas.type doit etre {STATUTS_SAS_TYPE} pour {DOCUMENT_CODE}.")
    if _normalize_profession(profession) != STATUTS_SAS_PROFESSION:
        raise ValueError(
            f"statuts_sas.profession doit etre {STATUTS_SAS_PROFESSION} pour {DOCUMENT_CODE}."
        )


def _validate_actionnaire_unique(
    ctx: DocumentGenerationContext,
    actionnaire: SpfplPerson,
    president: StatutsPresident,
    capital: CapitalSouscription,
) -> None:
    if ctx.associes and len(ctx.associes) != 1:
        raise ValueError("les statuts SAS V1 sont limites a un actionnaire unique.")
    if len(capital.souscripteurs) != 1:
        raise ValueError(
            "capital_souscription.souscripteurs doit contenir exactement un "
            f"souscripteur pour {DOCUMENT_CODE}."
        )
    if president.ref_associe_index != 0:
        raise ValueError(f"president.ref_associe_index doit etre 0 pour {DOCUMENT_CODE}.")
    _required_text(president.prenom, "president.prenom")
    _required_text(president.nom, "president.nom")
    _required_text(president.adresse_personnelle_affichee, "president.adresse_personnelle_affichee")
    if not _same_text(president.prenom, actionnaire.prenom) or not _same_text(
        president.nom,
        actionnaire.nom,
    ):
        raise ValueError(
            "president doit designer la meme personne que actionnaire_unique "
            f"pour {DOCUMENT_CODE}."
        )


def _validate_capital(
    societe: SocieteSpfpl,
    actionnaire: SpfplPerson,
    capital: CapitalSouscription,
) -> None:
    societe_total = _required_int(societe.nb_actions_total, "societe_spfpl.nb_actions_total")
    actionnaire_actions = _required_int(actionnaire.nb_actions, "actionnaire_unique.nb_actions")
    capital_total = _required_int(
        capital.nb_actions_total,
        "capital_souscription.nb_actions_total",
    )
    souscripteur = capital.souscripteurs[0]
    souscripteur_actions = _required_int(
        souscripteur.nb_actions,
        "capital_souscription.souscripteurs[0].nb_actions",
    )
    if len({societe_total, actionnaire_actions, capital_total, souscripteur_actions}) != 1:
        raise ValueError(
            "societe_spfpl.nb_actions_total, actionnaire_unique.nb_actions et "
            "capital_souscription doivent etre coherents pour "
            f"{DOCUMENT_CODE}."
        )
    valeur_societe = _required_text(
        societe.valeur_nominale_action,
        "societe_spfpl.valeur_nominale_action",
    )
    valeur_capital = _required_text(
        capital.valeur_nominale_action,
        "capital_souscription.valeur_nominale_action",
    )
    if valeur_societe != valeur_capital:
        raise ValueError(
            "societe_spfpl.valeur_nominale_action doit correspondre a "
            "capital_souscription.valeur_nominale_action pour "
            f"{DOCUMENT_CODE}."
        )
    if not _same_text(souscripteur.prenom, actionnaire.prenom) or not _same_text(
        souscripteur.nom,
        actionnaire.nom,
    ):
        raise ValueError(
            "capital_souscription.souscripteurs[0] doit correspondre a "
            f"actionnaire_unique pour {DOCUMENT_CODE}."
        )


def _validate_marital_sentence(actionnaire: SpfplPerson) -> None:
    # R0702-02 (Gad 2026-07-02) : le SAS accepte DESORMAIS tout statut matrimonial (menu complet
    # « Situation matrimoniale », comme la SPFPL). Le statut est toujours requis ; le regime + le
    # conjoint ne sont exiges (fail-loud) QUE pour un MARIE. Pour un non-marie, la ligne de
    # comparution du modele (« <statut> sous le régime de ... avec ... ») est repliee sur le SEUL
    # statut en post-traitement (_collapse_marital_sentence) — pas de wording source invente.
    _required_text(actionnaire.situation_maritale, "actionnaire_unique.situation_maritale")
    if mentions_conjoint(actionnaire.situation_maritale):
        _required_text(actionnaire.regime_matrimonial, "actionnaire_unique.regime_matrimonial")
        _required_conjoint(actionnaire)


def _required_societe_spfpl(ctx: DocumentGenerationContext) -> SocieteSpfpl:
    if ctx.societe_spfpl is None:
        raise ValueError(f"societe_spfpl est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.societe_spfpl


def _required_actionnaire(ctx: DocumentGenerationContext) -> SpfplPerson:
    if ctx.actionnaire_unique is None:
        raise ValueError(f"actionnaire_unique est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.actionnaire_unique


def _required_president(ctx: DocumentGenerationContext) -> StatutsPresident:
    if ctx.president is None:
        raise ValueError(f"president est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.president


def _required_capital_souscription(ctx: DocumentGenerationContext) -> CapitalSouscription:
    if ctx.capital_souscription is None:
        raise ValueError(f"capital_souscription est obligatoire pour {DOCUMENT_CODE}.")
    return ctx.capital_souscription


def _required_conjoint(person: SpfplPerson) -> SpfplConjoint:
    if person.conjoint is None:
        raise ValueError(f"actionnaire_unique.conjoint est obligatoire pour {DOCUMENT_CODE}.")
    _required_text(person.conjoint.civilite_affichage, "actionnaire_unique.conjoint.civilite")
    _required_text(person.conjoint.prenom, "actionnaire_unique.conjoint.prenom")
    _required_text(person.conjoint.nom, "actionnaire_unique.conjoint.nom")
    return person.conjoint


def _required_ordre(person: SpfplPerson) -> SpfplOrdre:
    if person.ordre is None:
        raise ValueError(f"actionnaire_unique.ordre est obligatoire pour {DOCUMENT_CODE}.")
    return person.ordre


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value.strip()


def _required_int(value: int | None, field_name: str) -> int:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    return value


def _address_display(societe: SocieteSpfpl) -> str:
    if societe.siege is None:
        raise ValueError(f"societe_spfpl.siege est obligatoire pour {DOCUMENT_CODE}.")
    if societe.siege.adresse_affichee:
        return societe.siege.adresse_affichee.strip()
    return (
        f"{_required_text(societe.siege.num_voie, 'societe_spfpl.siege.num_voie')} "
        f"{_required_text(societe.siege.voie, 'societe_spfpl.siege.voie')}, "
        f"{_required_text(societe.siege.cp, 'societe_spfpl.siege.cp')} "
        f"{_required_text(societe.siege.ville, 'societe_spfpl.siege.ville')}"
    )


def _person_address(person: SpfplPerson, field_name: str) -> str:
    if person.adresse_personnelle_affichee:
        return person.adresse_personnelle_affichee.strip()
    if person.adresse_personnelle is None:
        raise ValueError(f"{field_name}.adresse_personnelle est obligatoire pour {DOCUMENT_CODE}.")
    if person.adresse_personnelle.adresse_affichee:
        return person.adresse_personnelle.adresse_affichee.strip()
    return (
        f"{_required_text(person.adresse_personnelle.num_voie, f'{field_name}.adresse.num_voie')} "
        f"{_required_text(person.adresse_personnelle.voie, f'{field_name}.adresse.voie')}, "
        f"{_required_text(person.adresse_personnelle.cp, f'{field_name}.adresse.cp')} "
        f"{_required_text(person.adresse_personnelle.ville, f'{field_name}.adresse.ville')}"
    )


def _person_name(person: SpfplPerson, field_name: str) -> str:
    return (
        f"{_required_text(person.civilite_affichage, f'{field_name}.civilite_affichage')} "
        f"{_required_text(person.prenom, f'{field_name}.prenom')} "
        f"{_required_text(person.nom, f'{field_name}.nom')}"
    )


def _conjoint_name(conjoint: SpfplConjoint) -> str:
    return (
        f"{_required_text(conjoint.civilite_affichage, 'actionnaire_unique.conjoint.civilite')} "
        f"{_required_text(conjoint.prenom, 'actionnaire_unique.conjoint.prenom')} "
        f"{_required_text(conjoint.nom, 'actionnaire_unique.conjoint.nom')}"
    )


def _qualification(person: SpfplPerson) -> str:
    if person.qualification_principale:
        return person.qualification_principale.strip()
    return _required_text(person.profession, "actionnaire_unique.qualification_principale")


def _format_display_date(value: date | str | None, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} est obligatoire pour {DOCUMENT_CODE}.")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")
    return _required_text(value, field_name)


def _same_text(left: str | None, right: str | None) -> bool:
    if left is None or right is None:
        return False
    return left.strip().casefold() == right.strip().casefold()


def _normalize_profession(value: str) -> str:
    return value.casefold().replace("é", "e").replace("è", "e").replace("ê", "e")
