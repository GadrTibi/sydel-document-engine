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


class Person(BaseModel):
    genre: Gender
    civilite: str
    prenom: str
    nom: str
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


class ReunionContext(BaseModel):
    date_lettres: str | None = None
    heure: str | None = None


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
    personne_signataire: Person
    signature: Signature
    societe: Company | None = None
    domiciliation: Domiciliation | None = None
    associes: list[Associe] = Field(default_factory=list)
    dirigeant_nomine: DirigeantNomine | None = None
    decision: DecisionContext | None = None
    reunion: ReunionContext | None = None
    capital: CapitalContext | None = None
    emprunt: Emprunt | None = None
    bien_immobilier: BienImmobilier | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
