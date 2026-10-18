---
id: IDX-CANON
doc_type: canon-index
status: current
version: 2026.10.16.1
visibility: public
owner: Baz Porter
last_verified: 2026-10-16
---
# Canon index

This index says which document governs which question. The governing documents are **not stored in this public repository**; see `registry/restricted-manifest.yaml` for why. Their identity is pinned here by version and SHA-256 so any copy can be verified.

| ID | Document | Version | Status | SHA-256 (original DOCX) | Location |
|---|---|---|---|---|---|
| CAN-001 | Rosetta Stone (governing business master) | **v4.2**, identity and version unchanged | Governing, qualified. Foundation approved 2026-10-14; whole-document ratification pending | `a664a72c...bea6de` (full hash in `registry/source-of-truth.yaml`) | Founder-controlled restricted store |
| CAN-002 | Lisa Miles Full Ideal Client Architecture | 2026-10-14 | Internal governing buyer master; founder ratification pending | `77b7373a...bde16` (full hash in `registry/source-of-truth.yaml`) | Founder-controlled restricted store |

## Rules that bind every agent
1. Rosetta and the ICA are **separate** documents. Never merge them or cite one for the other's subject.
2. **Lisa** is the entry buyer: the person at the turning point. **Victoria** is the destination archetype, not the buyer. Outward-facing copy is gender-neutral.
3. **RAMS** = Results, Attitude, Authenticity, Mastery, Systems (founder-approved 2026-10-16, DEC-002). The Reach/Acquire/Monetize/Scale reading is obsolete and historical.
4. **The Gate Home** is the future institution. **The Green Room** is its protected twelve-month founding prototype. Neither is launched. Do not invent a launch date, curriculum, guarantee or a different price (founder-stated price is in the restricted record).
5. Prices and launch status come from `registry/products.yaml` and the restricted product records, never from older files.

## Founder decisions of 2026-10-16 that bind this index
1. **Rosetta Stone v4.2 takes precedence** over older files and over product specifications wherever it speaks.
2. **RAMS has five pillars** (DEC-002).
3. **Victoria is the destination archetype, never the buyer**; Lisa Miles is the entry buyer (DEC-003). Prior usages of Victoria as the starting state were removed.
4. **Coming Home is a single offer** (DEC-006).
5. Superseded material is **retired**, preserved with provenance (DEC-013). Quantum and neuroscience statements were **reworded** (DEC-014); the founder has not yet read the new text.
6. Ideas that originate with other authors are attributed to them; they are not presented as the founder's IP.

## Existing files in `canon/`
These are historical evidence (Level 3) unless noted.

| File | Status |
|---|---|
| `canon/ICA.md` | **Retired.** Tombstone at this path; preserved copy in ICA.md (held in the private repository) |
| `canon/PRODUCT-ARCHITECTURE.md` | **Retired.** Tombstone; preserved in `retired/canon/` |
| `canon/OFFERS.md` | **Retired.** Tombstone; preserved in `retired/canon/`. Policy items found only there are pending confirmation (DEC-019) |
| `canon/RETIRED.md`, `FRAMEWORKS.md`, `IP-REGISTRY.md`, `METHODOLOGY.md`, `PROFILE.md`, `STORY.md`, `CREDIBILITY.md`, `VOICE.md`, `MANIFESTO.md` | Edited 2026-10-16 under the decisions above; originals in `retired/superseded-text/` |
| other `canon/` files | Unchanged legacy text, under review |

Details of every edit: 04_DECISIONS_APPLIED_LOG.md (held in the private repository). Open items: `registry/decisions.yaml`.
