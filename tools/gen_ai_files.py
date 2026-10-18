#!/usr/bin/env python3
"""Generate llms-full.txt from the wiki pages and keep the root copies of the site files identical.
Writes: site/llms-full.txt, llms-full.txt, and copies site/llms.txt and site/baz-porter.txt to the repository root.
Run: python3 -I tools/gen_ai_files.py"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/baz-stack/sovereign-leadership-architecture-knowledge"
ORDER = ["Home", "About-Baz-Porter", "Sovereign-Leadership-Architecture", "Sovereign-Leadership", "Philosophical-Principles", "Sovereign-Return", "RAMS", "Research-Foundations",
         "Publications", "Researcher-Identification-and-ORCID", "Credentials-and-Affiliations", "Evidence-Library", "Glossary", "Frequently-Asked-Questions",
         "References-and-Citations", "Current-Offerings-and-Entry-Pathway", "Contact-and-Official-Links", "Source-Hierarchy-and-Governance"]


def plain(t):
    t = t.split("---\n", 2)[2] if t.startswith("---\n") else t
    def sub(m):
        label, tgt = m.group(1), m.group(2)
        if tgt.startswith("http") or tgt.startswith("#"):
            return f"{label} ({tgt})" if label != tgt else tgt
        if tgt.startswith("../../"):
            return f"{label} ({REPO}/blob/main/{tgt[6:]})"
        return label
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", sub, t).strip()


def main():
    head = ("# Baz Porter® — Sovereign Leadership Architecture™: full reference\n"
            "# Canonical: https://bazporter.com/llms-full.txt · concise version: https://bazporter.com/llms.txt\n"
            "# Generated from the public knowledge repository wiki pages. Last updated: 2026-10-17 · release candidate\n\n")
    body = ""
    for n in ORDER:
        body += "\n\n=====\n" + plain((ROOT / "docs" / "wiki" / f"{n}.md").read_text(encoding="utf-8")) + "\n"
    (ROOT / "site" / "llms-full.txt").write_text(head + body.lstrip(), encoding="utf-8")
    for src, dst in [("site/llms-full.txt", "llms-full.txt"), ("site/llms.txt", "llms.txt"), ("site/baz-porter.txt", "baz-porter.txt")]:
        shutil.copyfile(ROOT / src, ROOT / dst)
    print("ai files written")


if __name__ == "__main__":
    main()
