import datetime
ITEMS = [
    ("done", "Socle : sous-formulaire cession reutilisable (byte-identique SELARL)"),
    ("wip",  "SELAS — genere ses docs de cession (cablage)"),
    ("done", "SELAS uni — regime communautaire (DOC-005/006)"),
    ("done", "SAS — complet vs canon (verifie)"),
    ("todo", "SPFPL apport — contrat d'apport + 2 attestations"),
    ("todo", "SPFPL cession — note d'info + PV agrement + actes"),
    ("todo", "SCM — satellites (pacte / depenses / frais communs / reglement)"),
    ("todo", "SCI / SCI IRIS — lettre option IS (conditionnel)"),
    ("todo", "Parite bloc A — 13 logiques SELARL portees aux autres types"),
]
SKIP = [("Derog cumul SELARL salarie", "non faisable : modele inexistant (liste au canon SELAS, aucun .doc nulle part)")]
MARK = {"done": "✅", "wip": "🔨", "todo": "⬜"}
done = sum(1 for s, _ in ITEMS if s == "done")
tot = len(ITEMS)
w = 24
fill = round(done / tot * w)
bar = "█" * fill + "░" * (w - fill)
pct = round(done / tot * 100)
L = []
L.append("  ┌─ SYDEL · Completude V2 (tous types vs canon) ──────────")
L.append("  │")
L.append(f"  │   GLOBAL   [{bar}]  {done}/{tot}  ·  {pct}%")
L.append("  │")
for s, lib in ITEMS:
    L.append(f"  │   {MARK[s]}  {lib}")
L.append("  │")
for nom, raison in SKIP:
    L.append(f"  │   ⊘  {nom} — {raison}")
L.append("  └────────────────────────────────────────────────────────")
board = "\n".join(L)
print(board)
stamp = datetime.date.today().isoformat()
open("docs/review/AVANCEMENT_COMPLETUDE.md", "w", encoding="utf-8").write(
    f"# Avancement — Complétude V2 (tous types vs canon)\n> MAJ {stamp}. Régénéré par `_scoreboard_completude.py`.\n\n```\n{board}\n```\n"
)
print("\n[AVANCEMENT_COMPLETUDE.md écrit]")
