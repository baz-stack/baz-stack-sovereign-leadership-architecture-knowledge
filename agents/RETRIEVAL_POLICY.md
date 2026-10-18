---
id: GOV-RETRIEVAL
doc_type: ai-governance
status: current
version: 2026.10.16.1
visibility: public
owner: Baz Porter
last_verified: 2026-10-16
---
# AI retrieval and governance policy

Applies to Claude Code, ChatGPT, GoHighLevel assistants, prospecting tools and any other agent that reads this knowledge system. Reads are the default. **Writes need review and explicit founder approval.**

## 1. Start small
Read `KNOWLEDGE_INDEX.md`, then your profile in `agents/profiles/`. Load only the documents the profile lists, then fetch more by ID only when the task needs it. Never load the whole repository. Machine-readable routing: `agents/retrieval-manifest.json`.

## 2. Source selection and precedence
Follow `registry/source-of-truth.yaml`: founder decisions, then Rosetta Stone v4.2, then the 2026-10-14 ICA, then current product specs, then handoff working architecture, then existing GitHub files, then research. A lower source never overrides a higher one. Where a document has `retrieval: deny`, do not use it as current truth. Documents with a status of superseded, conflicts-with-governing-master, archive or restricted-content-publicly-exposed are historical evidence only.

## 3. Conflicts
If sources disagree, do not choose. Output a flagged discrepancy that names both sources and the conflict ID from `registry/conflicts.yaml` (or states that it is new), then continue with whatever is not affected. Never present a proposed offer, price, module or framework as ratified.

## 4. Citation
Every generated artifact states the document IDs and versions it relied on (for example `CAN-001 v4.2`, `PRD-006`, `FW-002`) and the date. Claims are labelled with their evidence class from `research/README.md`. Quote founder-approved wording verbatim; mark paraphrase.

## 5. Privacy and restricted material
- Restricted documents (Rosetta text, ICA text, product specifications, claim audit, campaign specs) live in the founder-controlled restricted store, never in this public repo.
- **External tools (prospecting, enrichment, outreach, third-party LLMs) receive only the export-safe packet** defined in the restricted campaign specs: no pricing, no Rosetta or ICA text, no client names, no unpublished offers, no proprietary curriculum, no personal data about people other than the prospect fields necessary for the approved workflow.
- Never write credentials, tokens or personal data into any repository file.

## 6. Claims
Do not state, as fact: quantum or neuroscience mechanisms for the method; credentials, awards, audience sizes, endorsements or client outcomes; trademark registration beyond what `registry/frameworks.yaml` records; that The Green Room or The Gate Home is launched; that any product is live; that the Delphi AI clone is offered, active or has trained any number of users (it is PAUSED, NOT CURRENTLY OFFERED, DEC-042; the earlier training figure is withdrawn); that a credential is documented unless `canon/CREDIBILITY.md` shows that evidence status for it; that an Amazon ranking is an international bestseller claim or has a date. Do not quote the misattributed Darwin or Einstein lines recorded in `research/ledger.yaml`.

## 6a. Attribution
Ideas that originate with another author are attributed to the original source and never presented as the founder's IP. Example confirmed by the founder on 2026-10-16: the "Three Simple Steps" influence is Trevor G. Blake's 2012 book of that title. Cite originals by name and edition; do not paraphrase them as the founder's own words. Founder credentials are quoted exactly as recorded in `canon/CREDIBILITY.md`, together with the evidence status shown there (founder-reported, requires evidence, documented, third-party page). Testimonial wording and attribution are kept as given, and authorship is not marketing-use consent.

## 7. Founder approval is required before
Changing the meaning of canon; resolving a source conflict; changing a price, promise or launch status; exposing restricted IP; merging to `main`; publishing; sending outreach or changing a live customer system; retiring an active asset.

## 8. Terms every agent must know
Lisa Miles is the entry buyer; Victoria is the destination archetype and never the buyer. RAMS has five pillars. Both are founder-approved (2026-10-16). Outward-facing copy is gender-neutral. Use "investment", "counsel", "architect", "return" or "rebuild" rather than "payment", "coaching", "coach", "transformation" where Rosetta requires. The Gate Home is the future institution; The Green Room is its protected 12-month founding prototype; neither is launched.
