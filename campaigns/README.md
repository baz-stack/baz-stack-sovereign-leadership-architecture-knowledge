---
id: IDX-CAMPAIGNS
doc_type: index
status: current
version: 2026.10.16.1
visibility: public
owner: Baz Porter
last_verified: 2026-10-16
---
# Campaigns and sales enablement

**Nothing here is live. No outreach has been sent, no page published, no CRM changed.**

Campaign assets reference canon by document ID. They are never a competing source of truth. Sequence from the handoff brief (not approved live copy): manifesto, leadership report, Fast Future Freedom Blueprint, then The Becoming as the single primary offer of the first campaign, and only then prospecting and CRM attribution.

## Traceability map
| Asset | Governing source | Product record | Status |
|---|---|---|---|
| Manifesto | CAN-001 (WHY, voice), CAN-002 (entry-state language), `canon/MANIFESTO.md` (legacy, review) | n/a | Not approved; rewrite needed |
| Leadership report | CAN-001 s04 (free discovery assets) | n/a | No spec supplied |
| Fast Future Freedom Blueprint | CAN-001 s04 s10, CAN-002 | PRD-001 | Page copy supplied by the founder (restricted); live page not read back; entry door decided (DEC-037) |
| The Becoming | CAN-001 s04 s05 | PRD-006 | Primary offer for the first campaign; terms conflict CON-005 |
| Prospecting (Harvey) | CAN-002 qualification | PRD-001, PRD-006 | Specification in restricted store; tool access not available |
| CRM (GoHighLevel) | CAN-001 s19 | n/a | Deployment-ready configuration in restricted store; not applied |

## Live pages supplied by the founder (2026-10-16)
| Page | URL | Role | Status |
|---|---|---|---|
| Fast Future Freedom Blueprint | https://bazporter.com/fast-future-freedom-blueprint | The updated Blueprint page; the entry gate under Rosetta v4.2 | Founder states it is updated. **Not read back**: the host was unreachable from the migration environment |
| Manifesto | https://bazporter.com/manifesto | The hub where the assets converge: readers can read it and find the next step | Founder-supplied. **Not read back** |

Until both pages are read back, nothing here describes their content, and the canon files that still point at the earlier entry-door URL are unchanged (DEC-004).

## Why the specifications are not here
The qualification rubric, scoring tiers, outreach copy and routing are derived from the restricted ICA and unapproved copy. They are delivered in the restricted bundle (`campaigns/` inside it) and must pass the founder's approval gate before any activation. Consent, suppression and outreach safeguards are specified there and enforced by `tools/validate.py` in full mode.

## Approval gates before launch
Pages complete and founder-approved; Blueprint language updated; DEC-004 and DEC-005 decided; consent capture, suppression and tracking verified live; human-review step in place; explicit founder authorization to send.
