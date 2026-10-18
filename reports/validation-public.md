---
id: RPT-VALIDATION
doc_type: report
status: generated
version: 2026.10.16.1
visibility: public
last_verified: 2026-10-16
---
# Validation report (public mode)

Run on branch tree at df738f3  
Manual-only checks are listed at the end.

| Check | Result |
|---|---|
| Structured files parse (YAML/JSON) | **PASS** |
| Document status/version metadata present | **PASS** |
| Internal links and path references resolve | **PASS** |
| IDs unique and cross-references resolve | **PASS** |
| Source references and provenance present | **PASS** |
| Prices consistent with registry; legacy price conflicts recorded | **PASS** |
| Retired terminology absent from active content | **PASS** |
| No unapproved claims asserted as fact | **PASS** |
| No orphaned files in the new tree | **PASS** |
| No restricted material or credentials in tracked files | **PASS** |
| Lisa/Victoria and RAMS terminology correct in active content | **PASS** |
| Green Room price: absent from public files | **PASS** |
| AI retrieval paths resolve to current, permitted material | **PASS** |
| Migration manifest complete; nothing deleted | **PASS** |
| Founder decisions of 2026-10-16 persisted; retirements preserved with tombstones | **PASS** |
| Wiki, ORCID and AI-readable file integrity | **PASS** |
| Legacy stale-state audit (informational counts) | **PASS** |

### Migration manifest complete; nothing deleted

- info migration manifest is held in the private repository

### Legacy stale-state audit (informational counts)

- info legacy files still using the destination archetype as the starting state: 0 (expected 0, DEC-003)
- info legacy canon files still citing Rosetta v4.0 outside retired/: 0 (expected 0)
- info legacy files mentioning RAMS: 26 (canonical record is ip/records/FW-002)
- info legacy files with unqualified quantum wording: 0 (expected 0, DEC-014)
- info legacy files still carrying retired Coming Home tier prices: 0 (expected 0)

## Not automatable (manual)
- Live checkout, page, contract and GoHighLevel readback (no access).
- Citation verification against original sources (network blocked).
- Trademark status (USPTO unreachable).
- Truth of credentials and client outcomes (no documents supplied).
- Whether copy meets Rosetta voice standard (human judgement).
