"""Cablage de l'attestation souscripteurs SELAS (DOC-045) pour les slices UNI.

ANO-045 : le document DOC-045 « Attestation sur le capital / liste des souscripteurs
SELAS » est requis au canon pour tout dossier SELAS. Les slices SELAS unipersonnelles
(medecin / dentiste) reutilisent le constructeur de contexte SELARL uni, qui NE
construit PAS les objets requis par le generateur d'attestation (`societe_spfpl`,
`depot_fonds`, `capital_souscription`). Ce module factorise le cablage commun aux deux
slices uni : decision d'attestabilite + construction des trois objets + attache au
contexte deja produit.

Un dossier UNIPERSONNEL a UN seul associe personne PHYSIQUE detenant la TOTALITE des
actions : il est donc TOUJOURS attestable (aucun cas personne morale, aucune somme
d'actions incoherente). Le module reste neanmoins defensif (associe present, capital,
actions) pour ne jamais produire un objet incomplet.

Le wording est identique au cas SELAS multi (`selas_multi_slice`) : forme sociale =
libelle long SELAS, profession = profession reglementee au pluriel capitalisee (parite
modele d'Albane « ... de Médecins »), un unique souscripteur = l'associe president.
"""

from __future__ import annotations

from sydel_doc_engine.domain.models import (
    Address,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    DepotFonds,
    DocumentGenerationContext,
    SocieteSpfpl,
)
from sydel_doc_engine.front_app.field_derivations import group_montant

# Code de l'attestation souscripteurs SELAS (parite selas_multi_slice).
DOC_ATTESTATION_SELAS = "DOC-045"

# Libelle long de la forme sociale SELAS (parite modele + slices SELAS).
_SELAS_FORME_LIBELLE_LONG = "Société d'exercice libéral par actions simplifiée"


def selas_uni_attestable(payload: dict[str, object]) -> bool:
    """Un dossier SELAS unipersonnel est-il attestable (DOC-045) ?

    Vrai si l'associe unique (personne physique) est nomme, le capital est renseigne
    et le nombre total d'actions est >= 1. Un unipersonnel n'a jamais de personne
    morale ni de somme d'actions incoherente : l'attestation est le cas nominal."""
    if not str(payload.get("nom") or payload.get("prenom") or "").strip():
        return False
    if not str(payload.get("capital_social") or "").strip():
        return False
    if int(payload.get("nb_actions_total") or 0) < 1:
        return False
    if not str(payload.get("banque_nom") or "").strip():
        return False
    return True


def _profession_pluriel_capitalise(ctx: DocumentGenerationContext) -> str:
    """Profession (pluriel) capitalisee pour l'entete de l'attestation (DOC-045).

    Le contexte SELARL reutilise porte la profession reglementee au pluriel sur
    `ctx.ordre.profession_reglementee_pluriel` (« médecins » / « chirurgiens-
    dentistes »). Le modele d'Albane l'affiche capitalisee (« Médecins »). Repli sur
    la qualification du signataire si l'ordre est absent (jamais invente)."""
    pluriel = ""
    if ctx.ordre is not None:
        pluriel = str(ctx.ordre.profession_reglementee_pluriel or "").strip()
    if not pluriel and ctx.personne_signataire is not None:
        pluriel = str(ctx.personne_signataire.qualification_principale or "").strip()
    if not pluriel:
        return ""
    return pluriel[0].upper() + pluriel[1:]


def _siege_address(ctx: DocumentGenerationContext, payload: dict[str, object]) -> Address:
    """Adresse structuree du siege pour la SocieteSpfpl (attestation).

    Utilise l'adresse deja portee par la societe du contexte si presente, sinon la
    reconstruit depuis les champs siege du payload (num / voie / cp / ville)."""
    if ctx.societe is not None and ctx.societe.siege is not None:
        return ctx.societe.siege
    num = str(payload.get("siege_num") or "")
    voie = str(payload.get("siege_voie") or "")
    cp = str(payload.get("siege_cp") or "")
    ville = str(payload.get("siege_ville") or "")
    display = f"{num} {voie}, {cp} {ville}".strip(" ,")
    return Address(num_voie=num, voie=voie, cp=cp, ville=ville, adresse_affichee=display)


def attach_attestation_to_ctx(
    ctx: DocumentGenerationContext,
    payload: dict[str, object],
) -> DocumentGenerationContext:
    """Attache au contexte SELAS uni les objets requis par DOC-045, si attestable.

    No-op (ctx renvoye tel quel) si le dossier n'est pas attestable. Sinon construit
    `societe_spfpl`, `depot_fonds` et `capital_souscription` (un unique souscripteur =
    l'associe president) et les pose sur le contexte. Le titre du president reprend
    son titre d'affichage (« Docteur »), parite modele « par le Président, Docteur X »."""
    if not selas_uni_attestable(payload):
        return ctx

    # R5 (Albane 2026-07-07) : capital groupe par 3 (« 60 000 ») — attestation DOC-045.
    capital = group_montant(str(payload.get("capital_social") or ""))
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    # Valeur nominale d'une action : le formulaire UI ne la porte pas toujours dans le
    # payload (champ calcule, affichage seul). On la reprend du contexte SELARL reutilise
    # (`ctx.capital.valeur_nominale_part`, deja calcule capital / nb actions) ; repli sur
    # le payload. Requise non vide par le generateur d'attestation.
    valeur_action = str(payload.get("valeur_nominale_action") or "")
    if not valeur_action and ctx.capital is not None:
        valeur_action = str(ctx.capital.valeur_nominale_part or "")
    valeur_action = group_montant(valeur_action)  # R5 : groupee des 4 chiffres

    sig = ctx.personne_signataire
    civilite = ""
    prenom = str(payload.get("prenom") or "")
    nom = str(payload.get("nom") or "")
    if sig is not None:
        civilite = str(sig.titre_affichage or "") or civilite
        prenom = prenom or str(sig.prenom or "")
        nom = nom or str(sig.nom or "")
    civilite = civilite or str(payload.get("titre_affichage") or "") or "Docteur"

    ctx.societe_spfpl = SocieteSpfpl(
        denomination=str(payload.get("denomination") or ""),
        forme_sociale=_SELAS_FORME_LIBELLE_LONG,
        capital_social=capital,
        nb_actions_total=nb_actions_total,
        valeur_nominale_action=valeur_action,
        profession=_profession_pluriel_capitalise(ctx),
        siege=_siege_address(ctx, payload),
    )
    ctx.depot_fonds = DepotFonds(
        banque=CessionBanque(nom=str(payload.get("banque_nom") or "")),
    )
    souscripteur = CapitalSouscripteur(
        civilite_affichage=civilite,
        prenom=prenom,
        nom=nom,
        nb_actions=nb_actions_total,
    )
    ctx.capital_souscription = CapitalSouscription(
        nb_actions_total=nb_actions_total,
        valeur_nominale_action=valeur_action,
        apports_numeraire_montant=capital,
        president=CapitalSouscripteur(
            civilite_affichage=civilite,
            prenom=prenom,
            nom=nom,
        ),
        souscripteurs=[souscripteur],
    )
    return ctx


def selas_uni_bundle_codes(
    base_codes: tuple[str, ...],
    payload: dict[str, object],
) -> tuple[str, ...]:
    """Ajoute DOC-045 au bundle SELAS uni si le dossier est attestable.

    Additif : ne retire aucun code. DOC-045 est insere juste apres les statuts
    (1er code), a une position stable, avant le conditionnel regime communautaire
    ajoute par l'appelant."""
    if DOC_ATTESTATION_SELAS in base_codes or not selas_uni_attestable(payload):
        return base_codes
    return (*base_codes, DOC_ATTESTATION_SELAS)
