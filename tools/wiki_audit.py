#!/usr/bin/env python3
"""Audit a directory of wiki pages (a cloned GitHub wiki, or docs/wiki/).
Per page: size, revision count (if a git clone), internal links that do not resolve, external URLs, and pattern flags
(retired terms, dollar amounts, unqualified outcome words, quantum wording, emails and phone numbers).
Usage: python3 -I tools/wiki_audit.py <wiki-dir> [--json]"""
import json
import re
import subprocess
import sys
from pathlib import Path

FLAGS = {
    "retired": r"Silent Collapse Diagnostic|Rosetta (?:Stone )?v4\.0|Horizon Leaders|\bBronze\b|\bDiamond\b|Baz Porter Institution|Delphi",
    "dollar-amount": r"\$\s?\d[\d,]*",
    "outcome-claim": r"\b(guarantee[sd]?|proven|permanent(?:ly)?|cure[sd]?|100%)\b",
    "quantum": r"\bquantum\b",
    "contact": r"[\w.+-]+@[\w-]+\.[\w.]+|\(\d{3}\)\s?\d{3}-\d{4}",
    "ric-obsolete-rams": r"Reach[/, ]+Acquire|four pillars",
}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def main():
    d = Path(sys.argv[1]).resolve()
    pages = sorted(p for p in d.rglob("*.md") if ".git" not in p.parts)
    names = {p.stem.lower() for p in pages}
    rows = []
    for p in pages:
        t = p.read_text(encoding="utf-8", errors="replace")
        bad, ext = [], []
        for tgt in LINK.findall(t):
            if tgt.startswith("http"):
                ext.append(tgt)
            elif tgt.startswith(("#", "mailto:")):
                continue
            else:
                base = tgt.split("#")[0]
                if base.startswith("../../"):
                    if not (d.parent.parent / base[6:]).exists() and not (d / base).exists():
                        bad.append(tgt)
                elif not ((d / base).exists() or (d / (base + ".md")).exists() or Path(base).stem.lower() in names):
                    bad.append(tgt)
        flags = {k: len(re.findall(v, t, re.I)) for k, v in FLAGS.items() if re.search(v, t, re.I)}
        rev = None
        if (d / ".git").exists():
            rev = int(subprocess.run(["git", "-C", str(d), "rev-list", "--count", "HEAD", "--", p.name], capture_output=True, text=True).stdout.strip() or 0)
        rows.append({"page": p.name, "bytes": len(t.encode()), "revisions": rev, "broken_links": bad, "external_urls": len(ext), "flags": flags})
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
    else:
        print(f"{len(rows)} pages in {d}")
        for r in rows:
            print(f"- {r['page']}: {r['bytes']} bytes, broken links {len(r['broken_links'])}, external URLs {r['external_urls']}, flags {r['flags'] or 'none'}")
    return 1 if any(r["broken_links"] for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
