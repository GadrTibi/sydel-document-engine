"""DNC par ASSOCIE — helpers PARTAGES (retour Rafael 2026-07-09).

Regle client : « il faut une declaration de non-condamnation pour CHAQUE associe —
2 associes = 2 documents, 100 = 100 », dans TOUS les cas (SCI, SCI IRIS, SCS cites
explicitement ; regle generale partout). L'orchestrateur du tronc commun produit
UNE DNC (celle du signataire, renommee O24-02) ; ces helpers generent la DNC de
chaque AUTRE associe PERSONNE PHYSIQUE, nommee distinctement
(``declaration_non_condamnation_<Nom>.docx``), a partir des donnees deja portees
par ``StatutsCivilsAssocie`` (identite / adresse / date saisies une seule fois)
et de la filiation PAR associe (``nom_pere`` / ``nom_mere``, champs additifs).

Partage par : socle civil (SCI / SCI IRIS / SCM / SCS / micro holding), SELARL
multi (membres additionnels) et SELAS pluripersonnelle (qui etend sa logique
« une DNC par dirigeant » R7 a « une DNC par associe »). Un seul bloc, jamais
reimplemente par type (feedback-reuse-validated-blocks-across-types). Les
personnes MORALES n'ont pas de DNC (le document declare une personne physique).
"""

from __future__ import annotations

import re
from pathlib import Path
from unicodedata import combining, normalize

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    DocumentGenerationContext,
    Person,
    StatutsCivilsAssocie,
)
from sydel_doc_engine.front_app.address_oneline import parse_address_full
from sydel_doc_engine.front_app.field_derivations import (
    derive_gender_from_civilite,
    parse_associe_birthdate,
)
from sydel_doc_engine.generators.lot_01.declaration_non_condamnation import (
    DeclarationNonCondamnationGenerator,
)


def associe_filename_slug(associe: StatutsCivilsAssocie) -> str:
    """Slug de nom de fichier base sur le nom de l'associe (R7).

    Inclut le nom de l'associe pour distinguer les documents emis PAR associe
    (DNC, couples DOC-005/006). Repli sur le prenom si le nom est vide. Sans
    accents ni caracteres exotiques (compatibilite OS)."""
    base = (associe.nom or associe.prenom or associe.prenoms or "associe").strip()
    normalized = "".join(c for c in normalize("NFKD", base) if not combining(c))
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", normalized).strip("_")
    return cleaned or "associe"


def rename_with_slug(path: Path, slug: str) -> Path:
    """Renomme un fichier genere en y inserant le slug de l'associe.

    « declaration_non_condamnation.docx » -> « declaration_non_condamnation_Dupont.docx ».
    En cas de collision (deux associes au meme nom), suffixe un index — jamais
    d'ecrasement silencieux (le nombre de DNC doit rester = nombre d'associes).
    """
    # Idempotence (re-Akainu tour 6, MINEUR O24-05) : si la source a deja ete consommee
    # (renommee par un run anterieur / etat FS perime / race Windows), ne JAMAIS lever de
    # FileNotFoundError -> retenir la cible deja produite, sinon le chemin tel quel. (Meme
    # robustesse que ui_runtime.rename_dnc_with_signataire ; cause de la flakiness ~20 %.)
    base_target = path.with_name(f"{path.stem}_{slug}{path.suffix}")
    if not path.exists():
        return base_target if base_target.exists() else path
    target = base_target
    if target.exists() and target != path:
        index = 2
        while True:
            candidate = path.with_name(f"{path.stem}_{slug}_{index}{path.suffix}")
            if not candidate.exists():
                target = candidate
                break
            index += 1
    path.replace(target)
    return target


def _adresse_perso(associe: StatutsCivilsAssocie) -> Address:
    """Adresse STRUCTUREE de l'associe pour la DNC (voie / cp / ville requis).

    Reprend l'adresse structuree si le formulaire l'a posee ; a defaut, parse
    l'adresse affichee sur UNE ligne (O24-03, « 1 rue Exemple, 75000 Paris ») —
    meme parseur que la saisie reelle, aucune re-saisie demandee."""
    if associe.adresse_personnelle is not None:
        return associe.adresse_personnelle
    affichee = str(associe.adresse_personnelle_affichee or "").strip()
    parsed = parse_address_full(affichee) if affichee else None
    return parsed or Address()


def dnc_context_for_associe(
    base_ctx: DocumentGenerationContext,
    associe: StatutsCivilsAssocie,
) -> DocumentGenerationContext:
    """Contexte DNC d'UN associe : signataire = cet associe.

    Identite / adresse / date reprises de l'associe (saisie unique, #8) ;
    filiation depuis ses champs ``nom_pere`` / ``nom_mere`` (DNC par associe,
    Rafael 2026-07-09). Le generateur DOC-001 valide lui-meme les champs requis
    (jamais de document incomplet silencieux)."""
    genre = associe.genre or derive_gender_from_civilite(
        associe.civilite_affichage or "Monsieur"
    )
    adresse = _adresse_perso(associe)
    person = Person(
        genre=genre or Gender.MASCULIN,
        civilite=associe.civilite_affichage or "Monsieur",
        prenom=associe.prenom or associe.prenoms or "",
        nom=associe.nom or "",
        date_naissance=parse_associe_birthdate(associe.date_naissance),
        ville_naissance=associe.ville_naissance or "",
        departement_naissance=associe.departement_naissance or None,
        nationalite=associe.nationalite or "",
        nom_pere=str(associe.nom_pere or ""),
        nom_mere=str(associe.nom_mere or ""),
        adresse_perso=adresse,
        adresse_personnelle_affichee=adresse.adresse_affichee,
        qualification_principale=associe.qualification_principale or "",
    )
    return base_ctx.model_copy(update={"personne_signataire": person})


def generate_dnc_autres_associes(
    base_ctx: DocumentGenerationContext,
    associes: list[StatutsCivilsAssocie],
    output_dir: Path,
) -> list[Path]:
    """Genere la DNC de chaque associe PERSONNE PHYSIQUE de la liste.

    A appeler avec les associes AUTRES que le signataire du tronc commun (dont la
    DNC vient de l'orchestrateur, renommee par ``rename_dnc_with_signataire``).
    Chaque DNC est generee sous le nom generique PUIS renommee avec le nom de
    l'associe — l'appel doit donc venir APRES le renommage de la DNC du
    signataire (sinon elle serait ecrasee). Les personnes morales sont ignorees.
    """
    generator = DeclarationNonCondamnationGenerator()
    produced: list[Path] = []
    for associe in associes:
        if associe.type_personne != "personne_physique":
            continue
        ctx = dnc_context_for_associe(base_ctx, associe)
        path = generator.generate(ctx, output_dir)
        produced.append(rename_with_slug(path, associe_filename_slug(associe)))
    return produced
