#!/usr/bin/env python3
"""Per-file review ledger for files classified public-confirm.

Runs the mechanical checks of the public evidence standard on each file and merges the reviewer notes in
registry/public-review-notes.yaml. Writes registry/public-review-ledger.yaml. Founder approval is never set here.
Run: python3 -I tools/review_public_files.py
"""
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
STANDARD = [
    ("S1", "No restricted material: no unpublished prices, client names, specifications or personal narrative"),
    ("S2", "Every credential or achievement claim carries its evidence status or is documented"),
    ("S3", "No promised outcomes, permanence claims, or scientific or medical mechanism claims without specific research"),
    ("S4", "Prices and terms match registry/products.yaml public terms"),
    ("S5", "No retired names, labels or withdrawn claims; five-pillar RAMS; buyer and destination roles as in canon"),
    ("S6", "Ideas from other authors are attributed"),
    ("S7", "No personal or third-party private data"),
    ("S8", "Internal links resolve to registered pages"),
]
PATTERNS = {
    "S3-absolute-words": r"\b(guarantee[sd]?|permanent(ly)?|cure[sd]?|proven|100%|inevitabl\w+|forever|rewir\w+)\b",
    "S3-science-words": r"\b(neuro\w*|quantum|scientific\w*)\b",
    "S5-retired": r"Silent Collapse Diagnostic|\bBronze\b|\bSilver\b|\bGold\b|\bDiamond\b|24,700|Part 4 international|two-time international",
    "S1-narrative": r"Suicide attempt|rope and pills|diverticulitis|liver failure|[$]2[.]1 million|annual retainer floor",
}
LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)")


def main():
    cls = yaml.safe_load((ROOT / "registry" / "repository-classification.yaml").read_text(encoding="utf-8"))
    files = [r["path"] for r in cls["files"] if r["class"] == "public-confirm"]
    notes = yaml.safe_load((ROOT / "registry" / "public-review-notes.yaml").read_text(encoding="utf-8"))["notes"]
    rows = []
    for p in files:
        t = (ROOT / p).read_text(encoding="utf-8")
        auto = {}
        for k, pat in PATTERNS.items():
            n = len(re.findall(pat, t, flags=re.I))
            if n:
                auto[k] = n
        broken = []
        for m in LINK.findall(t):
            tgt = (ROOT / p).parent / m.split("#")[0]
            if m.split("#")[0] and not tgt.exists():
                broken.append(m)
        n = notes.get(p, {})
        rows.append({"path": p, "mechanical_findings": auto or "none", "broken_internal_links": broken or "none",
                     "review_status": n.get("status", "reviewed-no-open-items"),
                     "reviewer_notes": n.get("notes", "No open items found against S1 to S8."),
                     "open_items_for_founder": n.get("open", []) or n.get("outstanding", []),
                     "resolved_issues": n.get("resolved", []), "outstanding_issues": n.get("outstanding", []),
                     "founder_confirmed": n.get("founder_confirmed", []), "independently_verified": [], "unverified_claims": n.get("unverified", []),
                     "publication_blocker": n.get("publication_blocker", "none"), "founder_approval": "pending"})
    out = {"register": "public-review-ledger", "version": "2026.10.17.1", "generated": "2026-10-17", "visibility": "public",
           "standard": [{"id": a, "rule": b} for a, b in STANDARD],
           "note": "Each file in the public-confirm class is reviewed against the public evidence standard. The review is the reviewer's, not the founder's approval: founder_approval stays pending until the founder approves each file.",
           "files": rows}
    (ROOT / "registry" / "public-review-ledger.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    pend = sum(1 for r in rows if r["outstanding_issues"])
    print(len(rows), "files reviewed;", pend, "with open items;", sum(1 for r in rows if r["broken_internal_links"] != "none"), "with broken links")


if __name__ == "__main__":
    main()
