import sys, os; sys.path.insert(0, os.path.abspath("src"))

import re
import tempfile
from datetime import date
from pathlib import Path

from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    RegimeCommunautaireAssocie,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
)
from sydel_doc_engine.front_app import selas_multi_slice as slc


# ---------------------------------------------------------------------------
# Payload de bundle COMPLET SELAS multi (canon) — donnees PARTAGEES homogenes.
# 2 associes physiques exercants ; le 1er = president (dirigeant). Le 2e est
# marie sous regime communautaire -> declenche DOC-005 + DOC-006 (conditionnel
# active). Vocabulaire ACTIONS. Toutes les valeurs partagees (denomination,
# capital, siege, RCS, identites, dates) sont posees UNE fois pour qu'un ecart
# entre documents soit un VRAI bug, pas un bug de fixture.
# ---------------------------------------------------------------------------

DENOMINATION = "SELAS DU CENTRE MEDICAL DES TILLEULS"
CAPITAL = "330 000"
NB_ACTIONS = 3300
VILLE_RCS = "Bordeaux"
SIEGE_NUM = "12"
SIEGE_VOIE = "rue des Tilleuls"
SIEGE_CP = "33000"
SIEGE_VILLE = "Bordeaux"
SIEGE_AFFICHE = "12 rue des Tilleuls, 33000 Bordeaux"
SIGNATURE_LIEU = "Bordeaux"
SIGNATURE_DATE = date(2026, 9, 15)
DECISION_DATE = date(2026, 9, 15)
CLOTURE = "31 décembre 2027"

PRES_PRENOM = "Claire"
PRES_NOM = "Durand"
PRES_ADR_NUM = "8"
PRES_ADR_VOIE = "avenue de la Republique"
PRES_ADR_CP = "33000"
PRES_ADR_VILLE = "Bordeaux"
PRES_ADR_AFFICHE = "8 avenue de la Republique, 33000 Bordeaux"


def _physique(prenom, nom, nb_actions, montant, *, adresse_affichee,
              regime=None, profession="médecin"):
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.FEMININ,
        civilite_affichage="Madame",
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        date_naissance="1 janvier 1980",
        ville_naissance="Lyon",
        departement_naissance="69",
        nationalite="française",
        profession=profession,
        situation_maritale="mariée",
        adresse_personnelle_affichee=adresse_affichee,
        qualification_principale="qualifiée en médecine générale",
        ordre_departemental="Gironde",
        numero_ordre="33-12345",
        numero_rpps="10100000001",
        qualite_capital="associée exerçante",
        nb_actions=nb_actions,
        nb_actions_lettres=str(nb_actions),
        apport=StatutsCivilsApport(montant=montant, montant_lettres=montant),
        regime_communautaire_associe=regime,
    )


associe1 = _physique(PRES_PRENOM, PRES_NOM, 1650, "165 000",
                     adresse_affichee=PRES_ADR_AFFICHE)
associe2 = _physique(
    "Marie", "Lefevre", 1650, "165 000",
    adresse_affichee="4 cours Victor Hugo, 33000 Bordeaux",
    regime=RegimeCommunautaireAssocie(
        actif=True,
        regime_matrimonial="communauté légale",
        conjoint_civilite="Monsieur",
        conjoint_genre=Gender.MASCULIN,
        conjoint_prenom="Paul",
        conjoint_nom="Lefevre",
    ),
)

payload = {
    "denomination": DENOMINATION,
    "siege": SIEGE_AFFICHE,
    "siege_num": SIEGE_NUM,
    "siege_voie": SIEGE_VOIE,
    "siege_cp": SIEGE_CP,
    "siege_ville": SIEGE_VILLE,
    "profession_reglementee": "médecin",
    "profession_reglementee_pluriel": "médecins",
    "capital_social": CAPITAL,
    "nb_actions_total": NB_ACTIONS,
    "valeur_nominale_action": "100",
    "ville_rcs": VILLE_RCS,
    "adresse_lieu_exercice": SIEGE_AFFICHE,
    "banque_nom": "CIC CHAPEAU ROUGE BORDEAUX",
    "banque_adresse": "1 rue Banque, 33000 Bordeaux",
    "date_cloture": CLOTURE,
    "signature_lieu": SIGNATURE_LIEU,
    "signature_date": SIGNATURE_DATE,
    "associes": [associe1, associe2],
    "president_index": 0,
    # bloc dirigeants nommes (president seul) reconstruit pour le PV
    "dirigeants_nomines": [
        {
            "ref_associe_index": 0,
            "fonction_affichage": "Président",
            "civilite_affichage": "Madame",
            "prenom": PRES_PRENOM,
            "nom": PRES_NOM,
            "genre": Gender.FEMININ,
            "date_naissance_iso": SIGNATURE_DATE,
            "date_naissance_affichee": "1 janvier 1980",
            "ville_naissance": "Lyon",
            "departement_naissance": "69",
            "nationalite": "française",
            "adresse_num": PRES_ADR_NUM,
            "adresse_voie": PRES_ADR_VOIE,
            "adresse_cp": PRES_ADR_CP,
            "adresse_ville": PRES_ADR_VILLE,
            "adresse_personnelle_affichee": PRES_ADR_AFFICHE,
        }
    ],
    "cession_context": None,
    "bail_context": None,
    "scm_cession_context": None,
    # --- documents communs (signataire = president) ---
    "decision_date": DECISION_DATE,
    "ordre_departement": "Gironde",
    "ordre_connecteur": "de",
    "ordre_adresse_ligne_1": "Place de la Bourse",
    "ordre_cp": "33000",
    "ordre_ville": "Bordeaux",
    "ordre_numero": "33-99999",
    "ordre_president_feminin": False,
    "mandataire_prenom": "Jordan",
    "mandataire_nom": "ELBAZ",
    # signataire (DNC / procuration) = president
    "signataire_nom_pere": "Durand",
    "signataire_nom_mere": "Petit",
    "signataire_adresse_num": PRES_ADR_NUM,
    "signataire_adresse_voie": PRES_ADR_VOIE,
    "signataire_adresse_cp": PRES_ADR_CP,
    "signataire_adresse_ville": PRES_ADR_VILLE,
    "signataire_nationalite": "française",
    "signataire_titre": "Docteur",
    "signataire_date_naissance": date(1980, 1, 1),
    # regime communautaire global INACTIF -> chemin per-associe (associe2)
    "regime_communautaire": False,
}


def docx_text(path):
    document = Document(str(path))
    parts = [p.text for p in document.paragraphs if p.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.extend(p.text for p in cell.paragraphs if p.text)
    return "\n".join(parts)


def main():
    out = Path(tempfile.mkdtemp(prefix="selas_audit_", dir="."))
    plan = slc.build_selas_plan(payload)
    print("PLAN can_generate=", plan.can_generate, "status=", plan.status)
    if not plan.can_generate:
        print("BLOCKERS:", plan.blockers)
        return
    print("PLANNED CODES:", plan.document_codes)
    dossier = slc.generate_dossier(payload, out)
    print("GENERATED", len(dossier.docx_paths), "docx:")
    texts = {}
    for p in dossier.docx_paths:
        name = Path(p).name
        texts[name] = docx_text(p)
        print("  -", name, f"({len(texts[name])} chars)")

    # ---- relever les valeurs des champs PARTAGES dans chaque doc ----
    print("\n==== PRESENCE DES VALEURS PARTAGEES PAR DOCUMENT ====")
    probes = {
        "denomination": DENOMINATION,
        "capital_330000": "330 000",
        "siege_affiche": SIEGE_AFFICHE,
        "siege_rue": "rue des Tilleuls",
        "ville_rcs": "Bordeaux",
        "president_nom": PRES_NOM,
        "president_prenom": PRES_PRENOM,
        "nb_actions_3300": "3 300",
        "nb_actions_3300_nospace": "3300",
        "cloture_2027": "2027",
        "associe2_nom": "Lefevre",
        "conjoint_nom": "Paul",
    }
    rows = {}
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        rows[name] = {}
        for key, val in probes.items():
            v = " ".join(val.split())
            rows[name][key] = (v in norm)
    # tableau
    hdr = "DOC".ljust(46) + "".join(k[:14].ljust(15) for k in probes)
    print(hdr)
    for name in texts:
        line = name[:44].ljust(46)
        for key in probes:
            line += ("Y" if rows[name][key] else ".").ljust(15)
        print(line)

    # ---- comparaisons explicites de divergences possibles ----
    print("\n==== EXTRACTION CIBLEE (regex) ====")
    # capital: chercher montants type "330 000" vs autres montants pres du mot capital
    for name, txt in texts.items():
        norm = " ".join(txt.split())
        caps = re.findall(r"capital[^.]{0,60}?(\d[\d  ]{2,}\d)", norm, re.IGNORECASE)
        denoms = DENOMINATION in norm
        print(f"[{name}] denom={denoms} capital_montants={caps[:4]}")

    print("\nDONE. tmp dir =", out)


if __name__ == "__main__":
    main()
