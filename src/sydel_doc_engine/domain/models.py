from __future__ import annotations

from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

from sydel_doc_engine.domain.enums import Gender


class Address(BaseModel):
    num_voie: str | None = None
    voie: str | None = None
    cp: str | None = None
    ville: str | None = None
    adresse_affichee: str | None = None


class Person(BaseModel):
    genre: Gender
    civilite: str
    prenom: str
    nom: str
    titre_affichage: str | None = None
    adresse_personnelle_affichee: str | None = None
    adresse_perso: Address | None = None
    date_naissance: date | None = None
    nationalite: str | None = None
    nom_pere: str | None = None
    nom_mere: str | None = None
    fonction_dirigeant: str | None = None


class Company(BaseModel):
    forme_sociale: str | None = None
    forme_sociale_affichage: str | None = None
    forme_sociale_libelle_long: str | None = None
    forme_sociale_complete: str | None = None
    forme_sociale_abregee: str | None = None
    denomination: str | None = None
    capital: str | None = None
    capital_social: str | None = None
    capital_variable: bool | None = None
    capital_variable_mention: str | None = None
    capital_variable_formule_intro: str | None = None
    siege: Address | None = None
    ville_rcs: str | None = None


class Signature(BaseModel):
    lieu: str
    date: date
    image_optionnelle: Path | None = None
    nombre_exemplaires: str | None = None


class Domiciliation(BaseModel):
    adresse_domiciliation_affichee: str | None = None


class DossierOptions(BaseModel):
    derogation: bool = False
    regime_communautaire: bool = False
    cession: bool = False
    apport: bool = False
    associe_unique: bool = False


class BailParty(BaseModel):
    civilite_affichage: str | None = None
    civilite_courte: str | None = None
    prenom: str | None = None
    nom: str | None = None
    profession: str | None = None
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    nationalite: str | None = None
    adresse_affichee: str | None = None


class BailContext(BaseModel):
    bailleur: BailParty | None = None
    locataire: BailParty | None = None
    date_signature_origine: date | str | None = None
    date_avenant: date | str | None = None
    societe_en_cours_immatriculation: bool = False
    bailleur_accepte_changement_locataire: bool = False


class CessionBanque(BaseModel):
    nom: str | None = None


class CessionDestinataire(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionFinancement(BaseModel):
    banque: CessionBanque | None = None
    destinataire: CessionDestinataire | None = None
    montant_deblocage: str | None = None


class CessionCabinet(BaseModel):
    denomination_ou_adresse_affichee: str | None = None


class CessionVendeur(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None


class CessionAcquereur(BaseModel):
    denomination_societe: str | None = None


class CessionContext(BaseModel):
    type_cabinet: str | None = None
    financement: CessionFinancement | None = None
    cabinet: CessionCabinet | None = None
    vendeur: CessionVendeur | None = None
    acquereur: CessionAcquereur | None = None


class OperationSpfpl(BaseModel):
    type: str | None = None


class SpfplDirigeant(BaseModel):
    fonction: str | None = None


class SocieteSpfpl(BaseModel):
    denomination: str | None = None
    forme_sociale: str | None = None
    forme_sociale_abregee: str | None = None
    capital_social: str | None = None
    activite: str | None = None
    profession: str | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None
    siege: Address | None = None
    dirigeant: SpfplDirigeant | None = None


class SpfplPerson(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    genre: Gender | None = None


class SocieteCible(BaseModel):
    denomination: str | None = None
    forme_sociale: str | None = None
    forme_sociale_complete: str | None = None
    profession_reglementee: str | None = None
    profession_reglementee_pluriel: str | None = None
    capital_social: str | None = None
    capital_social_lettres: str | None = None
    nb_parts_total: int | None = None
    valeur_nominale_part: str | None = None
    siege: Address | None = None
    ville_rcs: str | None = None
    numero_rcs: str | None = None


class AssocieCible(BaseModel):
    type: str = "personne_physique"
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    denomination: str | None = None
    nb_parts_avant: int | None = None
    nb_parts_apres: int | None = None
    plage_parts: str | None = None
    numero_part_unique: str | None = None
    qualite: str | None = None
    est_present_ou_represente: bool = True


class CessionParts(BaseModel):
    nb_parts: int | None = None
    nb_parts_lettres: str | None = None
    plage_parts: str | None = None


class OperationTitres(BaseModel):
    nb_titres: int | None = None


class DocumentSignataire(BaseModel):
    prenom: str | None = None
    nom: str | None = None


class DocumentContext(BaseModel):
    nombre_exemplaires_lettres: str | None = None
    signataire: DocumentSignataire | None = None


class Apport(BaseModel):
    montant: str | None = None
    montant_lettres: str | None = None


class RegimeCommunautaireAvertissement(BaseModel):
    date_signature: date | str | None = None


class RegimeCommunautaireRenonciation(BaseModel):
    lieu_signature: str | None = None
    date_signature: date | str | None = None
    nombre_exemplaires_lettres: str | None = None


class RegimeCommunautaire(BaseModel):
    avertissement: RegimeCommunautaireAvertissement | None = None
    renonciation: RegimeCommunautaireRenonciation | None = None
    date_courrier_avertissement: date | str | None = None
    regime_matrimonial: str | None = None
    qualite_renoncee: str | None = None


class OrdreAddress(BaseModel):
    ligne_1: str | None = None
    cp: str | None = None
    ville: str | None = None


class OrdreProfessionnel(BaseModel):
    conseil_departemental_libelle: str | None = None
    destinataire_appel: str | None = None
    profession_signataire_affichee: str | None = None
    profession_ligne_destinataire: str | None = None
    profession_reglementee_pluriel: str | None = None
    adresse_affichee: str | None = None
    adresse_bloc_affiche: str | None = None
    adresse: OrdreAddress | None = None
    derogation_mention_manuelle: str | None = None


class Mandataire(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    fonction: str | None = None
    cabinet: str | None = None
    libelle_affiche: str | None = None


class Associe(BaseModel):
    genre: Gender
    civilite_affichage: str
    prenom: str
    nom: str
    nb_parts: int
    est_present_ou_represente: bool = True


class DirigeantNomine(BaseModel):
    genre: Gender
    civilite_affichage: str
    prenom: str
    nom: str
    date_naissance: date | str | None = None
    ville_naissance: str | None = None
    departement_naissance: str | None = None
    nationalite: str | None = None
    adresse_personnelle: Address | None = None
    fonction_affichage: str = "gérant"
    ref_associe_index: int | None = None


class DecisionContext(BaseModel):
    date: date | str | None = None


class ReunionPresident(BaseModel):
    civilite_affichage: str | None = None
    prenom: str | None = None
    nom: str | None = None
    qualite: str | None = None


class ReunionContext(BaseModel):
    annee_lettres: str | None = None
    date_lettres: str | None = None
    heure: str | None = None
    president: ReunionPresident | None = None


class CapitalContext(BaseModel):
    nb_parts_total: int | None = None
    valeur_nominale_part: str | None = None
    nb_parts_representees: int | None = None


class Emprunt(BaseModel):
    actif: bool = False
    montant_max: str | None = None


class BienImmobilier(BaseModel):
    adresse: Address | None = None


class DocumentGenerationContext(BaseModel):
    structure: str | None = None
    dossier_options: DossierOptions | None = None
    personne_signataire: Person
    conjoint: Person | None = None
    signature: Signature
    societe: Company | None = None
    domiciliation: Domiciliation | None = None
    ordre: OrdreProfessionnel | None = None
    mandataire: Mandataire | None = None
    associes: list[Associe] = Field(default_factory=list)
    dirigeant_nomine: DirigeantNomine | None = None
    decision: DecisionContext | None = None
    reunion: ReunionContext | None = None
    capital: CapitalContext | None = None
    emprunt: Emprunt | None = None
    bien_immobilier: BienImmobilier | None = None
    apport: Apport | None = None
    regime_communautaire: RegimeCommunautaire | None = None
    bail: BailContext | None = None
    cession: CessionContext | None = None
    operation_spfpl: OperationSpfpl | None = None
    societe_spfpl: SocieteSpfpl | None = None
    cedant: SpfplPerson | None = None
    apporteur: SpfplPerson | None = None
    societe_cible: SocieteCible | None = None
    associes_cible: list[AssocieCible] = Field(default_factory=list)
    cession_parts: CessionParts | None = None
    operation_titres: OperationTitres | None = None
    document: DocumentContext | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
