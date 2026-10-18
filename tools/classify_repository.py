#!/usr/bin/env python3
"""Classify every tracked file as keep-public, public-confirm, private-review or private-migrate.

Writes registry/repository-classification.yaml (public: paths, classes and counts only).
Run: python3 -I tools/classify_repository.py
"""
import re
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
TODAY = "2026-10-17"

PRIVATE_MIGRATE = [
    (r"^institution/", "private-tier curriculum drafts, vision and research plan committed before the migration"),
    (r"^retired/canon/", "preserved copies of retired source files (older ICA, offers, product architecture)"),
    (r"^retired/frameworks/", "preserved copy of a retired public framework page that still carries withdrawn claims"),
    (r"^retired/superseded-text/", "pre-edit copies that still carry withdrawn claims, old prices and retired labels"),
    (r"^_holding/", "superseded machine-layer files carrying withdrawn claims"),
    (r"^reports/04_DECISIONS_APPLIED_LOG\.md$", "before and after text of every edit, including withdrawn claims"),
    (r"^tools/decisions_applied_2026-10-16\.json$", "machine copy of the before and after edit log"),
]
SPLIT_SUMMARY = [
    (r"^CHANGELOG\.md$", "public summary only; the detailed history with prices and payment plans is preserved privately"),
    (r"^canon/STORY\.md$", "public founder biography only; the confidential narrative is preserved privately"),
    (r"^canon/AFFILIATE\.md$", "public partnership overview only; commercial mechanics are preserved privately"),
]
PRIVATE_REVIEW = []
PUBLIC_CONFIRM = [
    (r"^canon/", "legacy canon page that is AI-readable by design; founder to confirm"),
    (r"^frameworks/", "framework definition page that is AI-readable by design; founder to confirm"),
    (r"^(glossary|faq|identity|citations)/", "public reference page; founder to confirm"),
    (r"^(README\.md|llms\.txt|baz-porter\.txt|CITATION\.cff|sitemap\.xml|robots\.txt|FOOTER\.md|LICENSE\.md)$", "public-facing file; founder to confirm"),
]


def deny_terms():
    p = ROOT / "restricted" / "denylist.txt"
    if not p.exists():
        return []
    return [l.rstrip("\n") for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def classify(path, text):
    if "doc_type: tombstone" in text[:400]:
        return "keep-public", "tombstone left at a retired path"
    for pat, why in PRIVATE_MIGRATE:
        if re.search(pat, path):
            return "private-migrate", why
    for pat, why in SPLIT_SUMMARY:
        if re.search(pat, path):
            return "split-public-summary", why
    for pat, why in PRIVATE_REVIEW:
        if re.search(pat, path):
            return "private-review", why
    for pat, why in PUBLIC_CONFIRM:
        if re.search(pat, path):
            return "public-confirm", why
    return "keep-public", "registry, evidence, status, research, retrieval or tooling file for the public evidence repository"


def main():
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split("\n")
    terms = deny_terms()
    rows, counts = [], {}
    for p in sorted(f for f in files if f):
        try:
            t = (ROOT / p).read_text(encoding="utf-8")
        except Exception:
            t = ""
        cls, why = classify(p, t)
        flags = []
        if terms and any(x in t for x in terms):
            flags.append("restricted-term-match")
        if re.search(r"PRIVATE|DO NOT PUBLISH", t[:600]):
            flags.append("private-label")
        if len(re.findall(r"\$\d", t)) > 3:
            flags.append("price-figures")
        counts[cls] = counts.get(cls, 0) + 1
        rows.append({"path": p, "class": cls, "reason": why, **({"flags": flags} if flags else {})})
    out = {"register": "repository-classification", "version": "2026.10.17.1", "generated": TODAY, "visibility": "public",
           "note": "Paths, classes and counts only. Classes: keep-public stays in the public evidence repository; public-confirm is public by design pending founder confirmation; split-public-summary has a public summary version while the original is preserved privately; private-review is held for founder review; private-migrate is copied to the private repository and later removed from the public tree. Classification does not remove anything from Git history.",
           "counts": counts, "files": rows}
    (ROOT / "registry" / "repository-classification.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    print(counts)


if __name__ == "__main__":
    main()
