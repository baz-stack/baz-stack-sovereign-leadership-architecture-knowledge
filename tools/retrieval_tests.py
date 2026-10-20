#!/usr/bin/env python3
"""End-to-end retrieval scenarios from the master directive. Simulates an agent resolving a task through
agents/retrieval-manifest.json and checks the answer is reachable, current and correct.
Public mode runs the public-resolvable subset; --full also reads the restricted store.
Usage: python3 -I tools/retrieval_tests.py [--full]"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FULL = "--full" in sys.argv and (ROOT / "restricted").exists()
FACTS = __import__("yaml").safe_load((ROOT / "restricted" / "facts.yaml").read_text(encoding="utf-8")) if FULL and (ROOT / "restricted" / "facts.yaml").exists() else {}
M = json.loads((ROOT / "agents" / "retrieval-manifest.json").read_text(encoding="utf-8"))
DOCS = {d["path"]: d for d in M["documents"]}
fails = []


def profile_paths(role):
    p = M["profiles"][role]
    return p["read_first"] + p["read_on_demand"]


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


def txt(p):
    return (ROOT / p).read_text(encoding="utf-8")


# 1 draft a manifesto paragraph: messaging agent must reach WHY (Rosetta) and Lisa language (ICA), never legacy ICA
paths = profile_paths("ica-messaging")
check("manifesto: ica-messaging profile reaches ICA and Rosetta", any("LISA_MILES_ICA" in p for p in paths) and any("ROSETTA_STONE" in p for p in paths))
check("manifesto: legacy canon/ICA.md is denied", "canon/ICA.md" in M["deny_as_current_truth"] and not any(p == "canon/ICA.md" for p in paths))
if FULL:
    ica = txt("restricted/canon/LISA_MILES_ICA_2026-10-14.md")
    check("manifesto: Lisa entry-state line retrievable", "When the role that defined you changes, you still get to decide who you become." in ica)
    check("buyer language: ICA s09 'Who am I now?' retrievable", "Who am I now?" in ica)
# 2 correct Becoming spec
y = txt("registry/products.yaml")
check("becoming: PRD-006 resolves in public registry with open conflict CON-005", "PRD-006" in y and "CON-005" in y)
check("becoming: public registry does not mark it live", "launch_status: unverified" in y)
if FULL:
    pf = txt("restricted/registry/products-full.yaml")
    check("becoming: full record carries both payment options", FACTS.get("becoming_upfront", "?") in pf and FACTS.get("becoming_monthly", "?") in pf)
# 3 trace RAMS origin
fw = txt("ip/records/FW-002-rams.md")
check("rams origin: provenance names doctrine claim and says source required", "British Army" in fw and "SOURCE REQUIRED" in fw)
check("rams: five pillars in order", "- Results\n- Attitude\n- Authenticity\n- Mastery\n- Systems" in fw)
check("rams: old Reach/Acquire reading marked historical", "obsolete" in fw.lower() and "historical" in fw.lower())
# 4 exclude retired / superseded material
check("retired: legacy OFFERS/PRODUCT-ARCHITECTURE are denied for prices and entry", DOCS["canon/PRODUCT-ARCHITECTURE.md"]["retrieval"].startswith("deny") and DOCS["canon/OFFERS.md"]["retrieval"].startswith("deny"))
check("retired: tombstones and retired copies are denied", all(DOCS[x]["retrieval"].startswith("deny") for x in ["canon/ICA.md", "retired/canon/ICA.md", "retired/canon/OFFERS.md"]))
check("retired: no profile reads retired/_holding/institution", not any(p.startswith(("retired/", "_holding/", "institution/")) for r in M["profiles"] for p in profile_paths(r)))
check("retired: Coming Home extra tiers flagged, not current", "CON-006" in y)
# 5 Green Room price
public_hits = [p for p in DOCS if not p.startswith("restricted/") and (ROOT / p).is_file() and "Green Room" in txt(p) and "$" in txt(p) and p.startswith(("products/", "ip/", "registry/", "operations/", "agents/", "campaigns/", "research/"))]
check("green room: price not retrievable from any public new-tree file", all("Green Room" not in line or "$" not in line for p in public_hits for line in txt(p).splitlines()))
check("green room: operations profile reaches restricted record", any(p.endswith("GREEN_ROOM.md") for p in profile_paths("operations")))
if FULL:
    check("green room: founder-stated price and term, not per month", FACTS.get("green_room_phrase", "?") in txt("restricted/institution/GREEN_ROOM.md"))
# 6 external tools get only the export-safe packet
check("prospecting: exactly one export-safe document", M["profiles"]["prospecting"]["export_safe_documents"] == ["restricted/campaigns/PROSPECTING_EXPORT_PACKET.md"])
if FULL:
    pk = txt("restricted/campaigns/PROSPECTING_EXPORT_PACKET.md")
    deny = [l.strip() for l in txt("restricted/denylist.txt").splitlines() if l.strip()]
    check("prospecting: export packet contains no denylisted token", not any(d in pk for d in deny if d not in ("Lisa Miles",)), [d for d in deny if d in pk])
    check("prospecting: export packet has no prices", "$" not in pk)
# 7 public AI-readable surface and wiki
ORC = "0009-0006-1670-9956"
check("ai files: llms.txt, llms-full.txt and baz-porter.txt carry the founder-supplied ORCID", all(ORC in txt(f) for f in ("llms.txt", "llms-full.txt", "baz-porter.txt")))
check("ai files: entry door is the Fast Future Freedom Blueprint, retired diagnostic absent", "Fast Future Freedom Blueprint" in txt("llms.txt") and "Silent Collapse Diagnostic" not in txt("llms.txt") + txt("llms-full.txt") + txt("baz-porter.txt"))
check("ai files: ranking claim has exact approved wording and no date or international designation", "reached #1 in two Amazon Kindle bestseller categories" in txt("llms.txt") and "March 27, 2025" not in txt("llms-full.txt") and "March 11, 2024" not in txt("llms-full.txt") and "No international bestseller designation" in txt("llms.txt"))
check("ai files: founder-reported credentials are labelled", "founder-reported" in txt("llms.txt").lower())
claims = __import__("yaml").safe_load(txt("registry/public-claims.yaml"))["claims"]
cl = {c["id"]: c for c in claims}
check("claims: CL-026 is partly documented with the discrepancy open", cl["CL-026"]["status"] == "partly-documented" and "DEC-048" in cl["CL-026"]["open_issue"])
check("claims: no public claim is marked verified", all(c["status"] != "verified" for c in claims))
check("claims: Platinum Partner stays founder-reported or partly documented, Princeton stays founder-reported", cl["CL-011"]["status"] in ("founder-reported", "partly-documented") and cl["CL-013-A"]["status"] == "founder-reported")
check("wiki: Home reaches every page through the sidebar", all(f"({n}.md)" in txt("docs/wiki/_Sidebar.md") for n in ("Sovereign-Return", "RAMS", "Publications", "Evidence-Library", "Glossary")))
check("wiki: six Sovereign Return stages in order", all(txt("docs/wiki/Sovereign-Return.md").index(a) < txt("docs/wiki/Sovereign-Return.md").index(b) for a, b in zip(("Recognition", "Identification", "Dismantlement", "Recalibration", "Embodiment"), ("Identification", "Dismantlement", "Recalibration", "Embodiment", "Sovereignty"))))
check("wiki: RAMS expansion is Results, Attitude, Authenticity, Mastery, Systems", "Results, Attitude, Authenticity, Mastery, Systems" in txt("docs/wiki/Glossary.md"))
print(f"{len(fails)} failing scenarios")
sys.exit(1 if fails else 0)
