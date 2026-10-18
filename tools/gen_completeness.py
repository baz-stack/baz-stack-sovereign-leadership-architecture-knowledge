#!/usr/bin/env python3
"""Write registry/completeness-register.yaml: one entry per source category of the knowledge environment.
Run: python3 -I tools/gen_completeness.py"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
H = "historical repository (private archive)"
P = "private IP repository"
K = "public knowledge repository"
ITEMS = [
 (1, "Repository root documentation", f"{H}: README.md, GOVERNANCE.md, CONTRIBUTING.md", "2026.07.31.2", "founder decisions, then Rosetta v4.2", "public-confirm", "documented", True, True, "README.md, GOVERNANCE.md, CONTRIBUTING.md", "validate.py", ""),
 (2, "GitHub Wiki repositories", f"{H} wiki remote", "not retrievable", "n/a", "unknown", "unverified", False, False, "docs/wiki/ (replacement built from canon)", "tools/wiki_audit.py", "Wiki remote not readable with the session credential; owner to supply an export or access (reports/09)"),
 (3, "Wiki homepage, sidebar, footer", "docs/wiki/Home.md, _Sidebar.md, _Footer.md", "2026.10.17.1", "public canon", "keep-public", "documented", True, True, "docs/wiki/", "validate.py (wiki integrity)", "Original homepage not retrievable"),
 (4, "Wiki history and attachments", "historical wiki remote", "not retrievable", "n/a", "unknown", "unverified", False, False, "none yet", "tools/wiki_audit.py", "Needs wiki git access; no revision or attachment could be listed"),
 (5, "Canonical documentation", f"{H}: canon/", "2026.07.15.1 to 2026.10.17.1", "Rosetta v4.2 (private)", "public-confirm (44 files, DEC-047) and keep-public", "documented", True, True, "canon/", "validate.py; reports/07", "DEC-047 file approvals"),
 (6, "Research references", f"{H}: research/ledger.yaml", "2026.10.16.1", "founder decisions; research integrity rules", "keep-public", "none of 51 entries verified against originals", True, False, "research/", "validate.py", "Network access to publishers"),
 (7, "Published books", f"{H}: canon/BOOKS.md", "2026.07.31.1", "founder-supplied identifiers", "public-confirm", "founder-confirmed identifiers", True, True, "canon/BOOKS.md, docs/wiki/Publications.md", "validate.py", "ISBN registry check"),
 (8, "ORCID and researcher identifiers", "founder-supplied: 0009-0006-1670-9956", "2026-10-17", "founder instruction", "keep-public", "founder-confirmed live 2026-10-17; not independently read back", True, True, "CITATION.cff, identity/, docs/wiki/, site/", "validate.py (single ORCID check)", "Independent read-back of the public record"),
 (9, "Academic and professional credentials", f"{H}: canon/CREDIBILITY.md", "2026.10.17.1", "claims register", "public-confirm", "per-claim statuses", True, True, "docs/wiki/Credentials-and-Affiliations.md, registry/public-claims.yaml", "validate.py", "Missing documents listed in the register"),
 (10, "Awards, partnerships, affiliations", f"{H}: canon/CREDIBILITY.md", "2026.10.17.1", "claims register", "public-confirm", "founder-reported / partly documented", True, True, "registry/public-claims.yaml", "validate.py", "Platinum Partner membership document; award criteria"),
 (11, "Amazon bestseller evidence", f"{P}: evidence/ (originals); {H}: evidence/CL-026", "2026.10.17.1", "founder instruction DEC-048", "split: record public, originals private", "partly documented; dates unresolved", True, True, "evidence/CL-026-amazon-kindle-rank.md", "validate.py; retrieval_tests.py", "DEC-048 date mapping"),
 (12, "Media appearances and interviews", f"{H}: identity/authority-sources.md", "2026.07.31", "founder link sheet", "public-confirm", "third-party listing; links not re-checked", True, False, "identity/authority-sources.md", "validate.py (links internal only)", "Live link check"),
 (13, "Trademark records", f"{H}: canon/TRADEMARKS.md", "2026.07.15.1", "founder-confirmed identifier", "public-confirm", "pending-verification", True, True, "canon/TRADEMARKS.md", "validate.py", "USPTO record (DEC-016, DEC-026)"),
 (14, "Public Sovereign Leadership frameworks", f"{H}: frameworks/", "2026.07.15.1 to 2026.10.17.1", "Rosetta v4.2 and founder decisions", "keep-public / public-confirm", "proprietary-methodology", True, True, "frameworks/, ip/records/", "validate.py", "DEC-043 stage-to-offer mapping"),
 (15, "Approved founder biography", f"{H}: canon/STORY.md", "public summary 2026.10.17.1", "DEC-046", "split-public-summary", "founder-reported", True, True, "canon/STORY.md, docs/wiki/About-Baz-Porter.md", "validate.py", "Original held privately"),
 (16, "Mission, vision, values, positioning", f"{H}: canon/MANIFESTO.md, canon/CATEGORY.md", "2026.07 to 2026.10", "Rosetta v4.2", "public-confirm", "documented", True, False, "canon/", "validate.py", ""),
 (17, "Public methodology explanations", f"{H}: canon/METHODOLOGY.md", "2026.10.17.1", "Rosetta v4.2", "public-confirm", "proprietary-methodology", True, True, "canon/METHODOLOGY.md, docs/wiki/", "validate.py", ""),
 (18, "Approved client outcome evidence", f"{P}: claims audit", "n/a", "testimonial permission rule", "private", "requires-evidence", False, False, "not published", "validate.py (no testimonials)", "Written permissions"),
 (19, "Claim and evidence registries", f"{P}: data/claims.yaml; {K}: registry/public-claims.yaml", "2026.10.17.1", "founder decisions", "split: public projection only", "see register", True, True, "registry/public-claims.yaml", "validate.py", ""),
 (20, "Citation metadata", f"{H}: CITATION.cff, citations/", "2026.10.17.1", "founder identifiers", "public-confirm", "pending-verification", True, True, "CITATION.cff, citations/", "validate.py", "Repository address live after publication"),
 (21, "Existing AI-readable files", f"{H}: llms.txt, baz-porter.txt", "v4.5 (2026-07-31) to 2026-10-17", "current canon", "public-confirm", "documented", True, True, "llms.txt, llms-full.txt, baz-porter.txt, site/", "validate.py; retrieval_tests.py", "Website deployment"),
 (22, "Structured data", f"{H}: identity/schema-jsonld.md", "2026.10.17.1", "current canon", "public-confirm", "documented", True, True, "site/structured-data.jsonld, metadata/", "validate.py (JSON, ORCID)", "Website deployment"),
 (23, "FAQs", f"{H}: faq/faq.md", "2026.07.31.1", "current canon", "public-confirm", "documented", True, True, "faq/, docs/wiki/Frequently-Asked-Questions.md", "validate.py", ""),
 (24, "Terminology and glossary", f"{H}: glossary/", "2026.07.31.1", "current canon", "public-confirm", "documented", True, True, "glossary/, docs/wiki/Glossary.md", "validate.py", ""),
 (25, "Website URLs and canonical links", "canon pages listing bazporter.com paths", "2026.10.17", "founder", "keep-public", "not read back from the live site", True, True, "site/, docs/wiki/Contact-and-Official-Links.md", "none possible offline", "Live site check"),
 (26, "Published content from authorized project materials", f"{P}: sources/", "n/a", "Rosetta v4.2", "private", "n/a", False, False, "not published", "check_exposure.py", ""),
 (27, "Validation scripts and tests", f"{H}: tools/", "2026.10.17", "n/a", "keep-public", "passing (see report 11)", True, True, "tools/", "self", ""),
 (28, "Public disclosure decisions", f"{H}: registry/decisions.yaml, public-review-ledger.yaml", "2026.10.17.1", "founder", "keep-public", "DEC-047 approvals pending", True, True, "registry/, reports/07", "validate.py", "Founder approval of 44 files"),
 (29, "Historical exposure reports", f"{H}: registry/exposure-register.yaml, reports/05", "2026.10.17.1", "n/a", "keep-public (descriptions only)", "documented", True, True, "registry/exposure-register.yaml", "check_exposure.py", "Search-engine cache removal requests (founder)"),
 (30, "Previously identified missing documentation", f"{H}: registry/conflicts.yaml, decisions.yaml", "2026.10.17.1", "founder", "keep-public", "tracked", True, True, "registry/", "validate.py", "Platinum Partner membership document, Vol. 12 title page, Excel Arena and Princeton evidence, testimonial permissions, counsel review"),
]
KEYS = ["n", "category", "source_location", "current_version", "governing_authority", "classification", "evidence_status", "migrated", "updated", "destination", "validation", "external_dependency"]


def main():
    out = {"register": "source-completeness", "version": "2026.10.17.1", "visibility": "public", "generated": "2026-10-17",
           "note": "One entry per source category. Private items are listed by category only. Nothing is omitted silently: an item that was not migrated says why.",
           "items": [dict(zip(KEYS, i)) for i in ITEMS]}
    (ROOT / "registry" / "completeness-register.yaml").write_text(yaml.safe_dump(out, sort_keys=False, width=200, allow_unicode=True), encoding="utf-8")
    print("completeness register:", len(ITEMS), "items")


if __name__ == "__main__":
    main()
