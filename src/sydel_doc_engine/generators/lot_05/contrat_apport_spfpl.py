from __future__ import annotations

import re
from pathlib import Path

from docx import Document

from sydel_doc_engine.domain.models import (
    Address,
    ApportTitres,
    DocumentGenerationContext,
    ProfessionalEntity,
)
from sydel_doc_engine.generators.lot_05.scm_cession_common import (
    mentions_conjoint,
    mentions_conjoint_ou_partenaire,
    mentions_partenaire_pacse,
)
from sydel_doc_engine.generators.lot_05.spfpl_common import (
    company_siege_display,
    quantite_titres,
    required_apport_titres,
    required_apporteur,
    required_commissaire_aux_apports,
    required_evaluateur_apport,
    required_int,
    required_societe_cible,
    required_societe_spfpl,
    required_text,
    validate_apport_context,
)
from sydel_doc_engine.rendering.docx_builder import (
    ensure_demeurant_au,
    keep_final_signature_block_together,
)
from sydel_doc_engine.utils.departements import departement_nom
from sydel_doc_engine.utils.grammar import (
    _has_real_decimal,
    accord_euros_apres_montant,
    euro_word,
    monetary_words_from_value,
)

OUTPUT_FILENAME = "contrat_apport_spfpl.docx"
_SOURCE_NAME = "Contrat d_apport SEL SPFPL.docx"

# SP1/SP3/SP4 (Albane 2026-06-25) : contrat d'apport SPFPL rebati FROM-SCRATCH (entierement non
# accentue, paraphrase) -> TOKEN-REPLACEMENT HYBRIDE du modele source : on CHARGE le modele
# (texte legal complet + accents preserves) et on remplace les placeholders. HYBRIDE car le
# modele HARDCODE deux societes TEMPLATE (« SYDEL » evaluateur, « TS EXPERTISE » commissaire) :
# on RECONSTRUIT ces 2 paragraphes depuis le ctx (evaluateur_apport / commissaire_aux_apports)
# pour ne pas shipper les societes template. SP2 : civilite de l'apporteur civile M./Mme.


def _source_path() -> Path:
    path = Path("project/source_documents/lot_05") / _SOURCE_NAME
    if not path.exists():
        raise ValueError(f"modele source introuvable pour {OUTPUT_FILENAME}: {path}")
    return path


def _txt(value: object) -> str:
    return str(value or "").strip()


def _date_fr(value: object) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value or "")


def _valeur_nominale_apport_fragment(apport_titres: ApportTitres) -> str:
    """Fragment « <valeur nominale en lettres> euro » du modele contrat d'apport (7.5).

    Le modele HARDCODE « [valeur_nominale_action_lettres] euro » (unite au SINGULIER).
    - ENTIER : les lettres sont des mots NUS (« cent ») -> on reconstitue BYTE-IDENTIQUE
      « cent euro » (on reprend le « euro » singulier du modele ; on ne passe PAS par
      `montant_lettres_avec_unite`, qui accorderait « cent euros » et casserait le gold).
    - DECIMAL (Albane 7.5, containment 2026-07-06) : on CALCULE la phrase monetaire complete
      DEPUIS LA FIGURE via `monetary_words_from_value` (« un centime d'euro ») et on la rend
      SEULE, ce qui ABSORBE le « euro » du modele via la cle combinee (plus de « ... euro »).
    Depuis le containment, `valeur_nominale_action_lettres` (= `number_words_from_value`) ne
    porte plus l'unite sur un decimal -> on ne peut plus discriminer via « euro » dans les
    lettres : on discrimine sur la FIGURE `valeur_nominale_action`.
    """
    lettres = required_text(
        apport_titres.valeur_nominale_action_lettres,
        "apport_titres.valeur_nominale_action_lettres",
    )
    figure = apport_titres.valeur_nominale_action
    if _has_real_decimal(figure):
        # Decimal : phrase monetaire complete calculee depuis la figure ; remplace « <token> euro ».
        return monetary_words_from_value(figure).strip()
    # Entier : mots nus + euro/euros ACCORDE sur la figure (Akainu batch2 M2, 2026-07-09).
    # L'ancien « euro » singulier fige du modele rendait « cent euro » (faux, valeur=100) :
    # le retour Rafael 09-07 « 100 -> euros » SUPERSEDE cet arbitrage de fidelite (regle 68
    # lecon 1 : partout = partout, on ne s'auto-arbitre jamais pour garder le modele).
    return f"{lettres.strip()} {euro_word(figure)}"


def _addr_display(address: Address | None, field_name: str) -> str:
    """Adresse en UNE chaine, PRIORITE a `adresse_affichee` (Akainu M1 : le ctx fournit
    l'adresse en `adresse_affichee` — pattern dominant lot_05 ; lire seulement num/voie/cp/ville
    sortait des adresses VIDES).

    Akainu M1 (round 2) : repli sur `required_text` (marqueur « (À COMPLÉTER : …) » visible,
    R10 Rafael) et JAMAIS une chaine vide — cohérent avec les jumeaux `company_siege_display` /
    `person_address_display`. Un `adresse_affichee=""` (le front pose toujours
    `Address(adresse_affichee=str(...) or "")`) + sous-champs vides rendait « Siège social :  »
    blanc : interdit."""
    if address is not None and address.adresse_affichee:
        return address.adresse_affichee.strip()
    if address is None:
        return required_text(None, field_name)
    num = required_text(address.num_voie, f"{field_name}.num_voie")
    voie = required_text(address.voie, f"{field_name}.voie")
    cp = required_text(address.cp, f"{field_name}.cp")
    ville = required_text(address.ville, f"{field_name}.ville")
    return f"{num} {voie}, {cp} {ville}"


def _entity_rep(entity: ProfessionalEntity) -> str:
    rep = entity.representant
    if rep is None:
        return ""
    return " ".join(
        x for x in (_txt(rep.civilite_affichage), _txt(rep.prenom), _txt(rep.nom)) if x
    )


def _evaluateur_paragraphe(ev: ProfessionalEntity) -> str:
    # SP1/SP3 : remplace le bloc hardcode « SYDEL » du modele par l'evaluateur du ctx (accentue).
    return (
        f"L'évaluation a été effectué par la Société {_txt(ev.denomination)}, "
        f"{_txt(ev.forme_sociale)} au capital de {_txt(ev.capital_social)}, dont le siège est "
        f"situé {company_siege_display(ev, 'evaluateur_apport')}, immatriculée au Registre du "
        f"Commerce et des Sociétés de {_txt(ev.ville_rcs)}, sous le n° {_txt(ev.numero_rcs)}, "
        f"représentée par {_entity_rep(ev)}."
    )


def _commissaire_paragraphe(co: ProfessionalEntity) -> str:
    # SP1/SP3 : remplace le bloc hardcode « TS EXPERTISE » du modele par le commissaire du ctx.
    return (
        f"Dans ce cadre, le cabinet {_txt(co.denomination)}, {_txt(co.forme_sociale)} au capital "
        f"de {_txt(co.capital_social)}, dont le siège est situé "
        f"{company_siege_display(co, 'commissaire_aux_apports')}, immatriculé au Registre du "
        f"Commerce et des Sociétés de {_txt(co.ville_rcs)}, sous le n° {_txt(co.numero_rcs)}, "
        f"représenté par {_entity_rep(co)}, en qualité de commissaire aux apports,"
    )


class ContratApportSpfplGenerator:
    """Contrat d'apport SPFPL — token-replacement HYBRIDE fidele au modele source (SP1-SP4)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_apport_context(ctx)
        apporteur = required_apporteur(ctx)
        societe_spfpl = required_societe_spfpl(ctx)
        societe_cible = required_societe_cible(ctx)
        apport_titres = required_apport_titres(ctx)
        evaluateur = required_evaluateur_apport(ctx)
        commissaire = required_commissaire_aux_apports(ctx)

        replacements = self._build_replacements(
            apporteur, societe_spfpl, societe_cible, apport_titres, ctx
        )
        eval_para = _evaluateur_paragraphe(evaluateur)
        comm_para = _commissaire_paragraphe(commissaire)

        document = Document(str(_source_path()))
        # Remplacement IN-PLACE : placeholders dans paragraphes + cellules ; reconstruction des
        # 2 paragraphes societes template (SYDEL/TS EXPERTISE) depuis le ctx.
        for paragraph in document.paragraphs:
            text = paragraph.text
            if "SYDEL" in text:
                _set_para_text(paragraph, eval_para)
            elif "TS EXPERTISE" in text:
                _set_para_text(paragraph, comm_para)
            else:
                rendered = _replace(text, replacements)
                if rendered != text:
                    _set_para_text(paragraph, rendered)
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        rendered = _replace(paragraph.text, replacements)
                        if rendered != paragraph.text:
                            _set_para_text(paragraph, rendered)

        self._assert_no_residual(document)
        # Rafael/Albane 2026-07-09 : « Demeurant [adresse] » -> « Demeurant au [adresse] ».
        ensure_demeurant_au(document)
        # KAN-36 (convergence @All 2026-07-16) : le bloc signature du contrat d'apport
        # (« Fait a … en N exemplaires » / « Le … » + les signataires « <apporteur> \t <societe> »
        # sur des paragraphes tab-joints) ne portait aucun keepNext -> scindable sur deux pages.
        # Les signataires sont des PARAGRAPHES (pas une table) : on solidarise via le helper
        # paragraphe (ancre « Fait a … » -> keepNext jusqu'a la fin). Byte-neutre cote texte.
        keep_final_signature_block_together(document)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        document.save(output_path)
        return output_path

    def _build_replacements(
        self, apporteur, societe_spfpl, societe_cible, apport_titres, ctx
    ) -> dict[str, str]:
        ordre = apporteur.ordre
        conjoint = apporteur.conjoint
        perso = _addr_display(
            apporteur.adresse_personnelle, "apporteur.adresse_personnelle"
        )
        siege = _addr_display(societe_spfpl.siege, "societe_spfpl.siege")
        dirigeant_fonction = required_text(
            societe_spfpl.dirigeant.fonction if societe_spfpl.dirigeant else None,
            "societe_spfpl.dirigeant.fonction",
        )
        return {
            "[civilite]": required_text(
                apporteur.civilite_affichage, "apporteur.civilite_affichage"
            ),
            "[prenom]": required_text(apporteur.prenom, "apporteur.prenom"),
            "[nom]": required_text(apporteur.nom, "apporteur.nom"),
            "[date_naissance]": _date_fr(apporteur.date_naissance),
            "[ville_naissance]": required_text(
                apporteur.ville_naissance, "apporteur.ville_naissance"
            ),
            "[departement_naissance]": required_text(
                apporteur.departement_naissance, "apporteur.departement_naissance"
            ),
            "[nationalite]": required_text(apporteur.nationalite, "apporteur.nationalite"),
            # Akainu M1 round 2 (2026-07-02) : le menu matrimonial complet ouvre l'APPORT au
            # NON-MARIE. Le modele P8 = « [situation_maritale] avec [nom_conjoint] » (« avec »
            # LITTERAL) -> un non-marie rendait « célibataire avec  » (« avec » orphelin). Cle
            # COMBINEE branchee via mentions_conjoint (comme l'acte de parts) : marie -> ligne
            # complete BYTE-IDENTIQUE ; sinon -> statut seul. Traitee en premier (longest-first).
            "[situation_maritale] avec [nom_conjoint]": _apporteur_maritale(apporteur, conjoint),
            "[situation_maritale]": required_text(
                apporteur.situation_maritale, "apporteur.situation_maritale"
            ),
            # Fallback (la cle combinee ci-dessus consomme P8) : conjoint marie OU partenaire
            # pacse renseigne -> « prenom nom », sinon "" (jamais de conjoint fantome).
            "[nom_conjoint]": (
                f"{_txt(conjoint.prenom)} {_txt(conjoint.nom)}".strip()
                if conjoint
                and mentions_conjoint_ou_partenaire(apporteur.situation_maritale)
                else ""
            ),
            "[profession_reglementee]": required_text(
                apporteur.profession_reglementee, "apporteur.profession_reglementee"
            ),
            "[ordre_professionnel]": required_text(
                ordre.professionnel if ordre else None, "apporteur.ordre.professionnel"
            ),
            # Albane 7.4/9.2 (2026-07-06) : departement de l'Ordre rendu par le NOM, plus le numero.
            "[departement_ordre]": departement_nom(
                required_text(
                    ordre.departement if ordre else None, "apporteur.ordre.departement"
                )
            ),
            "[numero_ordre]": required_text(
                ordre.numero if ordre else None, "apporteur.ordre.numero"
            ),
            "[numero_rpps]": required_text(
                ordre.numero_rpps if ordre else None, "apporteur.ordre.numero_rpps"
            ),
            # Akainu M1 : la phrase « Demeurant [num_voie_perso] [voie_perso], [cp_perso]
            # [ville_perso] » est remplacee EN BLOC par l'adresse affichee (le ctx la fournit
            # ainsi). Cle combinee traitee en premier (_replace trie par longueur desc) ; les
            # tokens nus -> vide (aucune fuite si occurrence isolee).
            "[num_voie_perso] [voie_perso], [cp_perso] [ville_perso]": perso,
            "[num_voie_perso]": "",
            "[voie_perso]": "",
            "[cp_perso]": "",
            "[ville_perso]": "",
            "[denomination_societe]": required_text(
                societe_spfpl.denomination, "societe_spfpl.denomination"
            ),
            # R4 (Albane 2026-07-07, « orthographe irréprochable ») : le front pose la forme
            # abregee NON accentuee (« par actions simplifiee ») -> accent restaure a la
            # sortie (« par actions simplifiée »). Texte genere (valeur de token), pas un
            # verbatim du modele source.
            "[forme_sociale]": required_text(
                societe_spfpl.forme_sociale, "societe_spfpl.forme_sociale"
            ).replace("simplifiee", "simplifiée"),
            "[capital_social]": required_text(
                societe_spfpl.capital_social, "societe_spfpl.capital_social"
            ),
            "[activite_spfpl]": required_text(societe_spfpl.activite, "societe_spfpl.activite"),
            "[ville_rcs]": required_text(societe_spfpl.ville_rcs, "societe_spfpl.ville_rcs"),
            # Akainu M1 : siege en bloc depuis l'adresse affichee (cle combinee, cf. perso).
            "[num_voie_siege] [voie_siege], [cp_siege] [ville_siege]": siege,
            "[num_voie_siege]": "",
            "[voie_siege]": "",
            "[cp_siege]": "",
            "[ville_siege]": "",
            "[fonction_dirigeant]": dirigeant_fonction,
            "[president_ou_gerant]": dirigeant_fonction,
            "[denomination_societe_apportee]": required_text(
                societe_cible.denomination, "societe_cible.denomination"
            ),
            "[forme_sociale_societe_apportee]": required_text(
                societe_cible.forme_sociale, "societe_cible.forme_sociale"
            ),
            "[capital_social_societe_apportee]": required_text(
                societe_cible.capital_social, "societe_cible.capital_social"
            ),
            "[ville_rcs_societe_apportee]": required_text(
                societe_cible.ville_rcs, "societe_cible.ville_rcs"
            ),
            "[numero_rcs_societe_apportee]": required_text(
                societe_cible.numero_rcs, "societe_cible.numero_rcs"
            ),
            "[adresse_siege_societe_apportee]": company_siege_display(
                societe_cible, "societe_cible"
            ),
            "[nb_parts_apportees]": quantite_titres(
                apport_titres.nb_parts, "nombre de parts apportées"
            ),
            "[plage_parts_apportees]": required_text(
                apport_titres.plage_parts, "apport_titres.plage_parts"
            ),
            "[parts_sociales_ou_actions]": required_text(
                apport_titres.nature_titres, "apport_titres.nature_titres"
            ),
            "[valeur_apport_par_part]": required_text(
                apport_titres.valeur_par_titre, "apport_titres.valeur_par_titre"
            ),
            "[valeur_apport_par_part_lettres]": required_text(
                apport_titres.valeur_par_titre_lettres, "apport_titres.valeur_par_titre_lettres"
            ),
            "[valeur_apport_global]": required_text(
                apport_titres.valeur_globale, "apport_titres.valeur_globale"
            ),
            "[valeur_apport_global_lettres]": required_text(
                apport_titres.valeur_globale_lettres, "apport_titres.valeur_globale_lettres"
            ),
            "[nb_actions]": str(
                required_int(
                    apport_titres.nb_actions_attribuees, "apport_titres.nb_actions_attribuees"
                )
            ),
            "[nb_actions_lettres]": required_text(
                apport_titres.nb_actions_attribuees_lettres,
                "apport_titres.nb_actions_attribuees_lettres",
            ),
            # 7.5 (Albane 2026-07-06) : le modele HARDCODE « [valeur_nominale_action_lettres] euro »
            # (unite figee au SINGULIER dans le docx). ENTIER -> on reproduit BYTE-IDENTIQUE
            # « cent euro » (cle nue = lettres seules, le « euro » du modele reste). DECIMAL ->
            # les lettres portent deja l'unite (« un centime d'euro ») ; on remplace la cle
            # COMBINEE (« <token> euro », traitee en premier car plus longue dans `_replace` trie
            # par longueur desc) par la phrase COMPLETE, ce qui ABSORBE le « euro » du modele et
            # evite « un centime d'euro euro ».
            "[valeur_nominale_action_lettres] euro": _valeur_nominale_apport_fragment(
                apport_titres
            ),
            "[valeur_nominale_action_lettres]": required_text(
                apport_titres.valeur_nominale_action_lettres,
                "apport_titres.valeur_nominale_action_lettres",
            ),
            "[lieu_signature]": required_text(
                ctx.signature.lieu if ctx.signature else None, "signature.lieu"
            ),
            "[date_signature]": _date_fr(ctx.signature.date if ctx.signature else None),
            "[nombre_exemplaires_lettres]": _exemplaires(ctx),
        }

    @staticmethod
    def _assert_no_residual(document) -> None:
        texts = [p.text for p in document.paragraphs]
        texts += [
            cell.text
            for table in document.tables
            for row in table.rows
            for cell in row.cells
        ]
        full = "\n".join(texts)
        if "[" in full or "]" in full:
            residual = re.findall(r"\[[^\]]+\]", full)
            raise ValueError(f"placeholder source residuel dans {OUTPUT_FILENAME}: {residual}")


def _apporteur_maritale(apporteur, conjoint) -> str:
    """Ligne matrimoniale de l'apporteur (contrat d'apport, modele P8).

    Akainu M1 round 2 (2026-07-02) : marie -> « <statut> avec <prenom nom conjoint> »
    BYTE-IDENTIQUE au modele ; non-marie -> statut seul (plus de « avec » orphelin). Garde
    partagee `mentions_conjoint` (R22-02), coherente avec l'acte de parts et l'attestation.
    """
    situation = required_text(apporteur.situation_maritale, "apporteur.situation_maritale")
    if mentions_conjoint(apporteur.situation_maritale) and conjoint:
        nom = f"{_txt(conjoint.prenom)} {_txt(conjoint.nom)}".strip()
        return f"{situation} avec {nom}"
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : le PARTENAIRE PACSE s'affiche aussi (« <statut>
    # avec <prenom nom> », modele P8 sans regime). « Pas de mention sans nom » : si le
    # partenaire n'a ni prenom ni nom -> statut seul (jamais un « avec » orphelin).
    if mentions_partenaire_pacse(apporteur.situation_maritale) and conjoint:
        nom = f"{_txt(conjoint.prenom)} {_txt(conjoint.nom)}".strip()
        if nom:
            return f"{situation} avec {nom}"
    return situation


def _set_para_text(paragraph, text: str) -> None:
    if paragraph.runs:
        paragraph.runs[0].text = text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(text)


def _replace(text: str, replacements: dict[str, str]) -> str:
    out = text
    for token in sorted(replacements, key=len, reverse=True):
        if token in out:
            out = out.replace(token, replacements[token])
    # Accord euro/euros (Rafael 2026-07-09, « partout = partout ») : l'unite « euros »
    # figee dans le DOCX source du contrat d'apport (« prix global de [lettres]
    # ([figure] €) euros ») devient fautive « 1 euros » pour une valeur singuliere.
    return accord_euros_apres_montant(out)


def _exemplaires(ctx: DocumentGenerationContext) -> str:
    apport = ctx.apport_titres
    if apport is not None and getattr(apport, "nombre_exemplaires_lettres", None):
        return str(apport.nombre_exemplaires_lettres)
    if ctx.document and ctx.document.nombre_exemplaires_lettres:
        return str(ctx.document.nombre_exemplaires_lettres)
    return "trois"
