from __future__ import annotations

from sydel_doc_engine.domain.models import Address
from sydel_doc_engine.utils.addresses import (
    compose_city_line,
    compose_full_address,
    compose_street_address,
)


def test_compose_street_address() -> None:
    assert compose_street_address("12", "rue des Lilas") == "12 rue des Lilas"


def test_compose_city_line() -> None:
    assert compose_city_line("75008", "Paris") == "75008 Paris"


def test_compose_full_address_skips_missing_parts() -> None:
    address = Address(num_voie="12", voie="rue des Lilas", cp="75008", ville="Paris")
    assert compose_full_address(address) == "12 rue des Lilas, 75008 Paris"
