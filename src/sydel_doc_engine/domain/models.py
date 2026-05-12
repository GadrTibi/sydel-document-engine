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
    denomination: str | None = None
    capital: str | None = None
    siege: Address | None = None


class Signature(BaseModel):
    lieu: str
    date: date
    image_optionnelle: Path | None = None


class Domiciliation(BaseModel):
    adresse_locaux_affichee: str | None = None


class DocumentGenerationContext(BaseModel):
    structure: str | None = None
    personne_signataire: Person
    signature: Signature
    societe: Company | None = None
    domiciliation: Domiciliation | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
