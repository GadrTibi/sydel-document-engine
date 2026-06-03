"""generate_pack — outil interne de génération reproductible d'un pack documentaire.

Usage :
    python scripts/generate_pack.py selarl_medecin_simple
    python scripts/generate_pack.py selarl_dentiste_simple --out artifacts/packs
    python scripts/generate_pack.py --all

Le pack produit (DOCX + ZIP) est un **artefact jetable** : c'est la sortie
reproductible de (commit + scénario). Voir ~/.claude/playbooks/doc-factory-operating-model.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from sydel_doc_engine.front_app.selarl_slice import (  # noqa: E402
    build_selarl_plan,
    generate_selarl_dossier,
)
from sydel_doc_engine.scenarios.selarl import (  # noqa: E402
    SELARL_SCENARIOS,
    build_selarl_scenario,
)


def generate_one(scenario_key: str, out_root: Path) -> int:
    data = build_selarl_scenario(scenario_key)
    plan = build_selarl_plan(data)
    out_dir = out_root / scenario_key
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Scénario : {scenario_key} ===")
    print(f"Documents attendus : {', '.join(plan.document_codes)}")
    if not plan.can_generate:
        print(f"  BLOQUÉ : {plan.reason}")
        for blocker in plan.blockers:
            print(f"    - {blocker}")
        return 1

    result = generate_selarl_dossier(data, out_dir)
    print(f"DOCX générés ({len(result.docx_paths)}) :")
    for path in result.docx_paths:
        print(f"    - {path.name}  ({path.stat().st_size} octets)")
    print(f"ZIP : {result.zip_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Génère un pack SELARL reproductible.")
    parser.add_argument(
        "scenario",
        nargs="?",
        choices=sorted(SELARL_SCENARIOS),
        help="Clé du scénario à générer.",
    )
    parser.add_argument("--all", action="store_true", help="Génère tous les scénarios.")
    parser.add_argument(
        "--out",
        default="artifacts/packs",
        help="Dossier racine de sortie (défaut : artifacts/packs).",
    )
    args = parser.parse_args(argv)

    out_root = Path(args.out)
    if args.all:
        return max(generate_one(key, out_root) for key in sorted(SELARL_SCENARIOS))
    if not args.scenario:
        parser.error("Préciser un scénario, ou --all.")
    return generate_one(args.scenario, out_root)


if __name__ == "__main__":
    raise SystemExit(main())
