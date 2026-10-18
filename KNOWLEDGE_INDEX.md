---
id: IDX-ROOT
doc_type: root-index
status: current
version: 2026.10.16.1
visibility: public
owner: Baz Porter
last_verified: 2026-10-16
---
# Knowledge index and navigation map

Sovereign Leadership Architecture™ knowledge operating system. **Version 2026.10.17. Changes to published content require founder approval.**

> **Read this first.** This repository is **public**. The governing Rosetta Stone v4.2, the Lisa Miles ICA, the product specifications, the claim audit and the campaign specifications are held in a founder-controlled restricted store and are referenced here by ID, version and SHA-256 only. See `registry/restricted-manifest.yaml` and decision DEC-001.

## Start here by task
| If you need | Go to |
|---|---|
| Which document governs a question | `canon/CANON_INDEX.md`, `registry/source-of-truth.yaml` |
| Rules for AI agents | `agents/RETRIEVAL_POLICY.md`, then your profile in `agents/profiles/` |
| A product, price status or prerequisite | `products/README.md`, `registry/products.yaml` |
| A framework definition, provenance or gap | `ip/README.md`, `registry/frameworks.yaml`, definition text in `frameworks/` |
| Whether a scientific claim is safe | `research/README.md`, `research/ledger.yaml` |
| What is in conflict | `registry/conflicts.yaml` |
| What the founder must decide | `registry/decisions.yaml` |
| Institution, pilot, succession status | `operations/INSTITUTION_AND_OPERATIONS_STATUS.md` |
| Terms, refunds, cancellation, privacy status | `operations/POLICIES_STATUS.md` |
| Evidence records for public claims | `evidence/CL-026-amazon-kindle-rank.md` |
| Public claim register (status of every public claim) | `registry/public-claims.yaml` |
| Publication records and listing status | `registry/publications.yaml` |
| Research reference table | `research/REFERENCES_INDEX.md` |
| Branded website reference page source | `site/baz-porter-txt.html` |
| Public wiki pages (start at Home) | `docs/wiki/Home.md` |
| Full-text AI reference | `llms-full.txt` |
| Campaign and CRM enablement | `campaigns/README.md` |
| What was retired or edited, and why | `retired/README.md`, `retired/MANIFEST.yaml`, 04_DECISIONS_APPLIED_LOG.md (held in the private repository) |
| Validation results | `reports/`, `tools/validate.py` |

## Map
```
KNOWLEDGE_INDEX.md      this file
`CLAUDE.md`             instructions for Claude Code agents
canon/                  existing canon files (historical evidence) + CANON_INDEX.md
frameworks/             existing public framework definitions (unchanged)
ip/                     framework records with provenance and status
products/               product and course records
research/               evidence ledger and taxonomy
operations/             institution and operations status
agents/                 retrieval policy, role profiles, retrieval manifest
campaigns/              campaign and CRM enablement index
registry/               machine-readable registries and manifests (`registry/README.md`)
reports/                conflict and decision report; validation output
retired/                retirement archive and pre-edit snapshots
tools/                  build, validation and exposure scripts
```

## Status words used everywhere
Verified = checked against the real result. Specified = described in a source, not checked live. Proposed = suggested, not approved. SOURCE REQUIRED = no primary text exists in the supplied sources. Nothing is marked live or launched without live readback; none has been performed.
