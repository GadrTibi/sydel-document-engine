from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from sydel_doc_engine.domain.models import DocumentGenerationContext, SpfplPerson
from sydel_doc_engine.generators.lot_05.scm_cession_common import mentions_conjoint
from sydel_doc_engine.generators.lot_05.spfpl_common import (
    company_siege_display,
    elision_de,
    euro_word,
    montant_lettres_avec_unite,
    required_cedant,
    required_cession_parts,
    required_int,
    required_societe_cible,
    required_societe_spfpl,
    required_text,
    validate_cession_context,
)
from sydel_doc_engine.rendering.docx_builder import new_document_from_model
from sydel_doc_engine.utils.departements import departement_nom

OUTPUT_FILENAME = "acte_cession_parts_spfpl.docx"
_SOURCE_NAME = "Acte_cession_SPFPL_tiers_part_modele.docx"

# SP1/SP3/SP4 (Albane 2026-06-25) : ce generateur etait FROM-SCRATCH (texte code en
# dur, non accentue, ~15 sections, paraphrases vs le modele Albane qui en compte ~30 :
# GAP, RENONCIATION, SIGNIFICATION, AFFIRMATION DE SINCERITE...). « Tout revoir » = le
# rebatir en TOKEN-REPLACEMENT : on CHARGE le modele source (texte legal complet, accents
# et formulations d'Albane preserves par construction) et on remplace les placeholders.
# SP2 : le modele utilise [civilite_cedant] (M./Mme) en civilite et « Dr » abrege en
# repartition — JAMAIS « Le Docteur » en civilite ; la fidelite restaure donc la civilite
# civile demandee. Meme infra que les statuts civils (_source_path + remplacement).

# Lignes de repartition du capital : le modele porte 3 lignes figees
# (« - Dr [prenom] [nom] detenant [parts_personne_N] parts »). On les remplace par la
# repartition DYNAMIQUE (une ligne par associe reel via capital_before_lines).
_REPARTITION_MARKER = "[parts_personne_"


def _is_repartition_row(text: str, block_open: bool) -> bool:
    """Une ligne de repartition du capital : porte le placeholder fige
    « [parts_personne_N] », ou (bloc deja ouvert) une ligne « - … detenant … »
    residuelle des personnes 2/3 du modele a 3 lignes figees."""
    if _REPARTITION_MARKER in text:
        return True
    return block_open and bool(re.match(r"^\s*-\s", text)) and "detenant" in text.lower()


def _source_path() -> Path:
    path = Path("project/source_documents/lot_05") / _SOURCE_NAME
    if not path.exists():
        raise ValueError(f"modele source introuvable pour {OUTPUT_FILENAME}: {path}")
    return path


def _date_fr(value: object) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y")
    return str(value or "")


def _strip_euro(lettres: str) -> str:
    """Retire une unite « euro(s) » deja presente en fin de lettres (fixtures / robustesse)
    pour que l'accord `euro_word` sur le MONTANT ne double pas l'unite (« mille euros euros »).
    Ne touche pas les lettres seules (« mille » -> « mille »)."""
    return re.sub(r"\s+euros?$", "", lettres.strip(), flags=re.IGNORECASE)


def _person_address(person: SpfplPerson, field_name: str) -> str:
    if person.adresse_personnelle_affichee:
        return person.adresse_personnelle_affichee.strip()
    struct = person.adresse_personnelle
    if struct is not None and struct.adresse_affichee:
        return struct.adresse_affichee.strip()
    return required_text(
        person.adresse_personnelle_affichee,
        f"{field_name}.adresse_personnelle_affichee",
    )


def _repartition_lines(ctx: DocumentGenerationContext) -> list[str]:
    """Repartition du capital, FIDELE au modele : « Dr <prenom> <nom> detenant N part(s) »
    (abrege « Dr », accents preserves), une ligne par associe reel."""
    associes = ctx.associes_cible or []
    if not associes:
        raise ValueError(f"associes_cible est obligatoire pour {OUTPUT_FILENAME}.")
    lines: list[str] = []
    for index, associe in enumerate(associes):
        field = f"associes_cible[{index}]"
        nb_parts = required_int(associe.nb_parts_avant, f"{field}.nb_parts_avant")
        # 12.5(a) (Albane 2026-07-06) : ne PAS emettre la ligne d'un associe/SPFPL
        # detenant 0 part (ex. l'acquereur pre-liste avant la cession) — une ligne
        # « detenant 0 parts » n'a pas de sens dans la repartition du capital.
        if nb_parts <= 0:
            continue
        label = "part" if nb_parts == 1 else "parts"
        if associe.type == "personne_morale":
            who = required_text(associe.denomination, f"{field}.denomination")
        else:
            prenom = required_text(associe.prenom, f"{field}.prenom")
            nom = required_text(associe.nom, f"{field}.nom")
            who = f"Dr {prenom} {nom}"
        lines.append(f"{who} détenant {nb_parts} {label}")
    return lines


class ActeCessionPartsSpfplGenerator:
    """Generateur token-replacement de l'acte de cession de parts SPFPL (fidele au
    modele source Albane, cf. SP1-SP4 2026-06-25)."""

    def generate(self, ctx: DocumentGenerationContext, output_dir: Path) -> Path:
        validate_cession_context(ctx)
        cedant = required_cedant(ctx)
        cession_parts = required_cession_parts(ctx)
        societe_spfpl = required_societe_spfpl(ctx)
        societe_cible = required_societe_cible(ctx)
        representant = societe_spfpl.representant
        if representant is None:
            raise ValueError("societe_spfpl.representant est obligatoire.")

        replacements = self._build_replacements(
            ctx, cedant, cession_parts, societe_spfpl, societe_cible, representant
        )
        repartition = _repartition_lines(ctx)

        # 12.1 (Albane 2026-07-06) : RESTAURATION DE LA MISE EN FORME (« quasi illisible »). Le
        # generateur reconstruisait le corps dans un `new_document()` a plat (tout JUSTIFY/None,
        # 0 paragraphe vide, aucun gras/centrage) et JETAIT les 145 paragraphes vides d'aeration
        # du modele -> forme perdue. On herite desormais la FORME du modele via
        # `new_document_from_model` (marges, page, styles, header/footer, police charte SYDEL) puis
        # on RECOPIE chaque paragraphe du modele — vides COMPRIS — en reproduisant son alignement,
        # son espacement et le gras/italique/souligne de CHAQUE run, avec token-replacement PAR RUN.
        # Aucun token du modele ne traverse une frontiere de run (verifie 2026-07-06) -> le
        # remplacement par run preserve la forme sans casser les fixes 12.2-12.7 ni l'elision n3.
        source = Document(str(_source_path()))
        docx = new_document_from_model(_source_path())
        repartition_block_open = False
        for paragraph in source.paragraphs:
            text = paragraph.text
            if _is_repartition_row(text, repartition_block_open):
                # Premiere ligne d'un bloc de repartition -> emettre la liste dynamique (fidele au
                # modele : paragraphe JUSTIFY prefixe « -\t », une ligne par associe reel) ; lignes
                # suivantes du meme bloc fige (personne_2/3) du modele -> absorbees.
                if not repartition_block_open:
                    for line in repartition:
                        self._add_repartition_paragraph(docx, line)
                repartition_block_open = True
                continue
            repartition_block_open = False
            self._copy_paragraph(docx, paragraph, replacements)

        # SP3 (Akainu M1/M2) : PAS de bloc signature ajoute — le modele source porte DEJA sa
        # ligne de signature (« Dr <cedant> / La société <cessionnaire> / Représentée par … »),
        # rendue fidelement (accentuee) par le token-replacement ci-dessus. Un bloc ajoute la
        # dupliquait ET perdait les accents (« La societe »/« Representee »).
        self._assert_no_residual(docx)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / OUTPUT_FILENAME
        docx.save(output_path)
        return output_path

    @staticmethod
    def _copy_paragraph(docx, source_paragraph, replacements: dict[str, str]) -> None:
        """Recopie un paragraphe du MODELE dans la sortie en preservant sa FORME (12.1).

        Reproduit l'alignement, l'espacement (avant/apres, interligne) et le retrait du
        paragraphe source, puis chaque run avec son gras / italique / souligne, en appliquant
        le token-replacement PAR RUN (aucun token ne traverse une frontiere de run -> la mise
        en forme est preservee sans casser les remplacements). Les paragraphes VIDES du modele
        (aeration) sont recopies tels quels (aucun `continue` : la forme d'aeration est le
        coeur du retour 12.1)."""
        new_paragraph = docx.add_paragraph()
        new_paragraph.alignment = source_paragraph.alignment
        source_format = source_paragraph.paragraph_format
        new_format = new_paragraph.paragraph_format
        new_format.space_before = source_format.space_before
        new_format.space_after = source_format.space_after
        new_format.line_spacing = source_format.line_spacing
        # Retrait recopie DEFENSIVEMENT : certains paragraphes du modele portent une valeur de
        # retrait non entiere en twips (« 708.9999… ») que python-docx ne sait pas relire (leve
        # ValueError). Le retrait n'est pas structurant pour la lisibilite visee par 12.1
        # (alignement + aeration + gras/centrage le sont) -> on ignore un retrait illisible plutot
        # que d'echouer la generation.
        for attribute in ("left_indent", "first_line_indent"):
            try:
                setattr(new_format, attribute, getattr(source_format, attribute))
            except (ValueError, TypeError):
                continue
        for source_run in source_paragraph.runs:
            new_run = new_paragraph.add_run(_replace(source_run.text, replacements))
            new_run.bold = source_run.bold
            new_run.italic = source_run.italic
            new_run.underline = source_run.underline

    @staticmethod
    def _add_repartition_paragraph(docx, line: str) -> None:
        """Emet une ligne de repartition dynamique, FIDELE au modele : paragraphe JUSTIFY
        prefixe « -\\t » (le modele porte « -\\tDr <nom> détenant N parts » en JUSTIFY),
        au lieu de l'ancienne liste a retrait suspendu qui aplatissait la forme (12.1)."""
        paragraph = docx.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.add_run(f"-\t{line}")

    def _build_replacements(
        self, ctx, cedant, cession_parts, societe_spfpl, societe_cible, representant
    ) -> dict[str, str]:
        cible_total = required_int(societe_cible.nb_parts_total, "societe_cible.nb_parts_total")
        cible_capital = required_text(societe_cible.capital_social, "societe_cible.capital_social")
        ordre = cedant.ordre
        conjoint = cedant.conjoint

        # 12.3 (Albane 2026-07-06) : le modele porte « d’[valeur_nominale_part_lettres] de valeur
        # nominale ». Le front pose la valeur nominale en lettres SANS unite (« cent » pour un
        # entier ; la FIGURE « 0,01 » pour un decimal depuis le containment 2026-07-06) -> il
        # manquait « euro(s) ». On compose via le helper partage `montant_lettres_avec_unite`,
        # SEUL point qui calcule la phrase monetaire DEPUIS LA FIGURE : ENTIER -> « cent euros » ;
        # DECIMAL (Albane 7.5) -> « un centime d'euro » (aucun double euro). Fixture portant deja
        # « euros » : le garde `"euro" in lettres` la laisse telle quelle (robustesse).
        valeur_nominale_lettres = required_text(
            societe_cible.valeur_nominale_part_lettres,
            "societe_cible.valeur_nominale_part_lettres",
        )
        if "euro" in valeur_nominale_lettres.lower():
            valeur_nominale_display = valeur_nominale_lettres.strip()
        else:
            valeur_nominale_display = montant_lettres_avec_unite(
                valeur_nominale_lettres,
                societe_cible.valeur_nominale_part,
            )

        # 12.2 (Albane 2026-07-06) : identite de l'acquereur (SPFPL en cours de constitution).
        # Le front injecte la forme ABREGEE (« par actions simplifiee », non accentuee) dans
        # `forme_sociale` -> la 2e ligne d'identite rendait « par actions simplifiee » au lieu de
        # la forme LEGALE COMPLETE. On rend la forme complete validee (identique au titre des
        # statuts SPFPL, cf. statuts_spfpl_templates) : « Société de Participations Financières de
        # Profession Libérale de <Profession-Plurielle> par actions simplifiée ». La profession
        # plurielle vient du cedant (donnee de dossier), titre-casee (« Chirurgiens-Dentistes »).
        profession_pluriel = required_text(
            cedant.profession_reglementee_pluriel,
            "cedant.profession_reglementee_pluriel",
        )
        forme_sociale_complete_acquereur = (
            "Société de Participations Financières de Profession Libérale de "
            f"{profession_pluriel.title()} par actions simplifiée"
        )

        # 12.6 (Albane 2026-07-06) / B1 (Akainu 2026-07-06) : prix — accord « euro(s) » sur le
        # MONTANT et ordre LETTRES puis CHIFFRES. Le front pose desormais les lettres SANS unite
        # figee (« un », « mille ») ; on ACCORDE l'unite au montant via `euro_word` (« un euro »
        # pour 1, « mille euros » pour >1) -> plus de « un euros ». `_strip_euro` neutralise une
        # unite deja presente dans une fixture (« mille euros ») pour eviter un double « euro ».
        # (a) PRIX UNITAIRE : modele « [prix_unitaire_part_lettres] ([prix_unitaire_part]) euro
        #     part cedee ». Fragment LISIBLE « <lettres> euro(s) (<chiffres> €) » -> la ligne rend
        #     « prix de un euro (1 €) part cedee » (unite accolee aux lettres, lien euro<->part
        #     preserve, plus de « (1 000) part cedee » sans unite).
        # (b) PRIX TOTAL : modele « [prix_cession] € ([prix_cession_lettres]) » (chiffres puis
        #     lettres). Albane veut LETTRES puis CHIFFRES -> « <lettres> euro(s) (<chiffres> €) ».
        prix_unitaire_chiffres = required_text(
            cession_parts.prix_unitaire, "cession_parts.prix_unitaire"
        )
        prix_unitaire_lettres = _strip_euro(
            required_text(
                cession_parts.prix_unitaire_lettres, "cession_parts.prix_unitaire_lettres"
            )
        )
        prix_unitaire_euro = euro_word(cession_parts.prix_unitaire)
        prix_unitaire_fragment = (
            f"{prix_unitaire_lettres} {prix_unitaire_euro} ({prix_unitaire_chiffres} €)"
        )
        prix_cession_chiffres = required_text(
            cession_parts.prix_total, "cession_parts.prix_total"
        )
        prix_cession_lettres = _strip_euro(
            required_text(cession_parts.prix_total_lettres, "cession_parts.prix_total_lettres")
        )
        prix_cession_euro = euro_word(cession_parts.prix_total)
        prix_cession_fragment = (
            f"{prix_cession_lettres} {prix_cession_euro} ({prix_cession_chiffres} €)"
        )
        # R0702-02 / Akainu M1 (2026-07-02) : le menu matrimonial complet ouvre le cas NON-MARIE.
        # Le modele porte « [situation_maritale_cedant] avec [conjoint...] » (« avec » LITTERAL) ->
        # un non-marie faisait fuiter « célibataire avec (À COMPLÉTER : …) » (conjoint fantome +
        # placeholder shippe). On branche la ligne comme l'acte d'ACTIONS (garde PARTAGE
        # mentions_conjoint, R22-02) : marie -> ligne complete byte-identique ; sinon statut seul.
        # La cle COMBINEE (plus longue) est traitee AVANT les tokens simples par `_replace`, donc
        # elle consomme tout le fragment « [situation_maritale_cedant] avec [conjoint...] » de P36.
        cedant_maritale = required_text(cedant.situation_maritale, "cedant.situation_maritale")
        if mentions_conjoint(cedant.situation_maritale):
            conjoint_civilite = required_text(
                conjoint.civilite_affichage if conjoint else None,
                "cedant.conjoint.civilite_affichage",
            )
            conjoint_prenom = required_text(
                conjoint.prenom if conjoint else None, "cedant.conjoint.prenom"
            )
            conjoint_nom = required_text(conjoint.nom if conjoint else None, "cedant.conjoint.nom")
            ligne_maritale_cedant = (
                f"{cedant_maritale} avec {conjoint_civilite} {conjoint_prenom} {conjoint_nom}"
            )
        else:
            conjoint_civilite = conjoint_prenom = conjoint_nom = ""
            ligne_maritale_cedant = cedant_maritale
        repl = {
            # Cle COMBINEE (fragment matrimonial complet) : branche marie/non-marie, byte-identique
            # au modele pour un marie. Placee avant les tokens simples (longest-first, _replace).
            "[situation_maritale_cedant] avec [civilite_conjoint_cedant] "
            "[prenom_conjoint_cedant] [nom_conjoint_cedant]": ligne_maritale_cedant,
            # Cedant (personne physique)
            "[civilite_cedant]": required_text(
                cedant.civilite_affichage, "cedant.civilite_affichage"
            ),
            "[prenom_cedant]": required_text(cedant.prenom, "cedant.prenom"),
            "[nom_cedant]": required_text(cedant.nom, "cedant.nom"),
            "[profession_cedant]": required_text(cedant.profession, "cedant.profession"),
            "[date_naissance_cedant]": _date_fr(cedant.date_naissance),
            "[ville_naissance_cedant]": required_text(
                cedant.ville_naissance, "cedant.ville_naissance"
            ),
            "[departement_naissance_cedant]": required_text(
                cedant.departement_naissance, "cedant.departement_naissance"
            ),
            "[nationalite_cedant]": required_text(cedant.nationalite, "cedant.nationalite"),
            "[adresse_cedant]": _person_address(cedant, "cedant"),
            # Fallback (P36 est deja consomme par la cle combinee ci-dessus ; ces tokens simples
            # ne restent que pour robustesse s'ils apparaissaient ailleurs). Valeurs conjoint = ""
            # pour un non-marie (jamais de « (À COMPLÉTER) » ni de conjoint fantome).
            "[situation_maritale_cedant]": cedant_maritale,
            "[numero_rpps_cedant]": required_text(
                ordre.numero_rpps if ordre else None, "cedant.ordre.numero_rpps"
            ),
            # 12.4 (Albane 2026-07-06) : le modele fige « du [departement] » devant le departement
            # de l'Ordre -> « des chirurgiens-dentistes du Paris » (agrammatical). On rend la
            # preposition correcte via `elision_de` (« de Paris », « d’Ardeche ») avec une cle
            # COMBINEE qui consomme le « du » fige du modele (traitee avant le token simple).
            # Albane 7.4/9.2 (2026-07-06) : le departement de l'Ordre s'affiche par le NOM
            # (« Seine-et-Marne »), plus par le numero (« 77 »). `departement_nom` enveloppe la
            # VALEUR ; `elision_de` reste la couche externe (12.4, preposition correcte).
            "du [ordre_departemental_cedant]": elision_de(
                departement_nom(
                    required_text(
                        ordre.departement if ordre else None, "cedant.ordre.departement"
                    )
                )
            ),
            "du [departement_inscription_societe]": elision_de(
                departement_nom(
                    required_text(
                        ordre.departement if ordre else None, "cedant.ordre.departement"
                    )
                )
            ),
            "[ordre_departemental_cedant]": departement_nom(
                required_text(
                    ordre.departement if ordre else None, "cedant.ordre.departement"
                )
            ),
            "[profession_reglementee]": required_text(
                cedant.profession_reglementee, "cedant.profession_reglementee"
            ),
            "[profession_reglementee_pluriel]": required_text(
                cedant.profession_reglementee_pluriel, "cedant.profession_reglementee_pluriel"
            ),
            "[civilite_conjoint_cedant]": conjoint_civilite,
            "[prenom_conjoint_cedant]": conjoint_prenom,
            "[nom_conjoint_cedant]": conjoint_nom,
            # Societe cedee (cible)
            "[denomination_societe_cedee]": required_text(
                societe_cible.denomination, "societe_cible.denomination"
            ),
            "[forme_sociale_complete]": required_text(
                societe_cible.forme_sociale_complete, "societe_cible.forme_sociale_complete"
            ),
            "[capital_social_societe_cedee]": cible_capital,
            "[nb_parts_total_societe_cedee]": str(cible_total),
            "[ville_rcs_societe_cedee]": required_text(
                societe_cible.ville_rcs, "societe_cible.ville_rcs"
            ),
            "[numero_rcs_societe_cedee]": required_text(
                societe_cible.numero_rcs, "societe_cible.numero_rcs"
            ),
            "[adresse_siege]": company_siege_display(societe_cible, "societe_cible"),
            "[departement_inscription_societe]": departement_nom(
                required_text(
                    ordre.departement if ordre else None, "cedant.ordre.departement"
                )
            ),
            # 12.3 (Albane 2026-07-06) : « d’[valeur…] de valeur nominale ». La valeur porte
            # desormais l'unite accordee (« cent euros » / « un euro », cf. valeur_nominale_display)
            # -> plus de « de cent de valeur nominale ». Elision : « cent euros » commence par une
            # consonne -> « DE cent euros » (pas « d’cent euros »). La cle combinee (plus longue)
            # est traitee en premier.
            "d’[valeur_nominale_part_lettres]": elision_de(valeur_nominale_display),
            "[valeur_nominale_part_lettres]": valeur_nominale_display,
            # Societe cessionnaire (SPFPL acquereur)
            "[denomination_societe_cessionnaire]": required_text(
                societe_spfpl.denomination, "societe_spfpl.denomination"
            ),
            # 12.2 (Albane 2026-07-06) : forme LEGALE COMPLETE de l'acquereur (SPFPL en cours de
            # constitution), pas l'abrege « par actions simplifiee » injecte par le front.
            "[forme_sociale_acquereur]": forme_sociale_complete_acquereur,
            "[capital_social_cessionnaire]": required_text(
                societe_spfpl.capital_social, "societe_spfpl.capital_social"
            ),
            "[ville_rcs_cessionnaire]": required_text(
                societe_spfpl.ville_rcs, "societe_spfpl.ville_rcs"
            ),
            "[numero_rcs_acquereur]": required_text(
                societe_spfpl.numero_rcs, "societe_spfpl.numero_rcs"
            ),
            "[adresse_siege_cessionnaire]": company_siege_display(societe_spfpl, "societe_spfpl"),
            "[civilite_acquereur_representant]": required_text(
                representant.civilite_affichage, "representant.civilite_affichage"
            ),
            "[civilite_representant_cessionnaire_courte]": required_text(
                representant.civilite_courte, "representant.civilite_courte"
            ),
            "[prenom_representant_cessionnaire]": required_text(
                representant.prenom, "representant.prenom"
            ),
            "[nom_representant_cessionnaire]": required_text(representant.nom, "representant.nom"),
            "[fonction_acquereur_representant]": required_text(
                representant.fonction, "representant.fonction"
            ),
            # Cession
            "[nb_parts_cedees]": str(
                required_int(cession_parts.nb_parts, "cession_parts.nb_parts")
            ),
            "[nb_parts_cedees_lettres]": required_text(
                cession_parts.nb_parts_lettres, "cession_parts.nb_parts_lettres"
            ),
            # 12.6 (Albane 2026-07-06) : cles COMBINEES (traitees avant les tokens simples) pour
            # (a) accorder « euro(s) » au prix UNITAIRE et (b) inverser l'ordre du prix TOTAL en
            # LETTRES puis CHIFFRES. La cle unitaire consomme le « euro » fige du modele (l'unite
            # accordee est deja dans `prix_unitaire_fragment`) ; la cle totale consomme « € (…) ».
            # n3 (Albane 2026-07-06) : ELISION euphonique « de un euro » -> « d’un euro ». Le
            # modele colle un « de » LITTERAL devant chaque prix (« le prix de … », « un prix
            # de … ») ; on etend la cle combinee pour consommer AUSSI ce « de » fige et rendre la
            # preposition via `elision_de` (« d’un euro » pour 1, « de mille euros » pour >1). La
            # cle la plus longue (avec « le prix »/« un prix ») est traitee avant les tokens.
            "le prix de [prix_unitaire_part_lettres] ([prix_unitaire_part]) euro": (
                f"le prix {elision_de(prix_unitaire_fragment)}"
            ),
            "un prix de [prix_cession] € ([prix_cession_lettres])": (
                f"un prix {elision_de(prix_cession_fragment)}"
            ),
            "[prix_unitaire_part]": required_text(
                cession_parts.prix_unitaire, "cession_parts.prix_unitaire"
            ),
            "[prix_unitaire_part_lettres]": required_text(
                cession_parts.prix_unitaire_lettres, "cession_parts.prix_unitaire_lettres"
            ),
            "[prix_cession]": required_text(cession_parts.prix_total, "cession_parts.prix_total"),
            "[prix_cession_lettres]": required_text(
                cession_parts.prix_total_lettres, "cession_parts.prix_total_lettres"
            ),
            # Signature
            "[lieu_signature]": required_text(ctx.signature.lieu, "signature.lieu"),
            "[date_signature]": _date_fr(ctx.signature.date),
            "[nombre_exemplaires_lettres]": required_text(
                cession_parts.nombre_exemplaires_lettres
                or (ctx.document.nombre_exemplaires_lettres if ctx.document else None),
                "cession_parts.nombre_exemplaires_lettres",
            ),
            # 12.7 (Albane 2026-07-06) : phrase de paiement — « par le moyen … ou d’un virement »
            # (incorrect) -> wording valide d'Albane « Le prix est payé au moyen d’un chèque ou
            # virement. ». Texte FIXE du modele : on le remplace mot pour mot (apostrophe courbe
            # U+2019, byte-identique au modele). Aucun crochet -> hors garde anti-résidu.
            "Le prix est payé ce jour par le moyen d’un chèque ou d’un virement.": (
                "Le prix est payé au moyen d’un chèque ou virement."
            ),
        }
        return repl

    @staticmethod
    def _assert_no_residual(docx) -> None:
        full = "\n".join(p.text for p in docx.paragraphs)
        if "[" in full or "]" in full:
            residual = re.findall(r"\[[^\]]+\]", full)
            raise ValueError(f"placeholder source residuel dans {OUTPUT_FILENAME}: {residual}")


def _replace(text: str, replacements: dict[str, str]) -> str:
    out = text
    # Tokens les plus LONGS d'abord : une cle combinee « d’[valeur…] » (gestion de l'elision)
    # doit etre traitee AVANT le token simple « [valeur…] » qu'elle contient.
    for token in sorted(replacements, key=len, reverse=True):
        if token in out:
            out = out.replace(token, replacements[token])
    return out

