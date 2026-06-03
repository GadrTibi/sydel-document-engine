"""Scénarios figés (versionnés) pour la génération reproductible de packs.

Un scénario = un `SelarlSliceInput` déterministe représentant un cas client type.
Il alimente `scripts/generate_pack.py` (outil interne de reproductibilité / QA).
Les vraies données client (anonymisées) remplacent simplement un scénario le jour venu.
"""
