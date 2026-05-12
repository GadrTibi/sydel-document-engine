from __future__ import annotations

from sydel_doc_engine.domain.models import Address


def _clean(parts: list[str | None]) -> list[str]:
    return [part.strip() for part in parts if part and part.strip()]


def compose_street_address(num_voie: str | None, voie: str | None) -> str:
    return " ".join(_clean([num_voie, voie]))


def compose_city_line(cp: str | None, ville: str | None) -> str:
    return " ".join(_clean([cp, ville]))


def compose_full_address(address: Address) -> str:
    parts = [
        compose_street_address(address.num_voie, address.voie),
        compose_city_line(address.cp, address.ville),
    ]
    return ", ".join(part for part in parts if part)
