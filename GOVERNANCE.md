# GOVERNANCE

**Version:** v2026.07.31.1
**Owner:** Baz Porter LLC® · The Prestige Architect™

---

## What This Repository Is

This repository is the single source of truth for Baz Porter LLC®. Every skill, page builder, workflow, email, sales page, podcast description, and content asset resolves against this canon. If an output conflicts with this canon, the canon wins.

---

## Authority

- **Owner and final authority:** Baz Porter (founder, Baz Porter LLC®).
- **Decision rule:** The canon in this repository is authoritative. Downstream tools update to match canon, never the reverse.
- **Marks:** Every public mention of a Class A mark carries ®; every public mention of a Class B mark carries ™. Trademark spelling is enforced on every output. See [`canon/IP-REGISTRY.md`](./canon/IP-REGISTRY.md).

---

## Repository Structure

| Path | Contents | Visibility |
|:----|:----|:----|
| root | README, machine layer (`llms.txt`, `baz-porter.txt`, `robots.txt`, `sitemap.xml`), governance files | Public |
| `canon/` | Source-of-truth canon files (OFFERS, VOICE, ICA, IP-REGISTRY, MANIFESTO, STORY, PROFILE, CREDIBILITY, BOOKS, METHODOLOGY, CATEGORY, and related) | Public |
| `frameworks/` | Proprietary framework definitions | Public |
| `identity/` | Entity/founder record, JSON-LD, authority sources | Public |
| `glossary/` | Canonical defined terms | Public |
| `citations/` | Citation reference and chronological index | Public |
| `faq/` | Plain-language Q&A | Public |

---

## Private material

Protected material is held in a separate private repository and is referenced in this repository by identifier, version and hash only. No protected content moves to a public surface without the founder's approval.

---

## Change Process

1. **Reconcile, don't clobber.** Read the whole repo first. Build only the gaps. Improve existing schema, licensing, and footers in place — never overwrite good work with a blank.
2. **Never delete without flagging.** Move, don't remove. Anything moved is logged in [`CHANGELOG.md`](./CHANGELOG.md). Deletion requires Baz's approval.
3. **Never fake a source.** Real, verifiable citation — or mark it `[RESEARCH PENDING]`. No invented papers, authors, or links.
4. **Voice.** Client-facing copy is warm and plain, with the reader. IP/authority copy is clinical, precise, anti-motivational. Banned language is enforced per [`canon/VOICE.md`](./canon/VOICE.md).
5. **Versioning.** The canon version string is `vYYYY.MM.DD.n`. Material changes bump the version and add a `CHANGELOG.md` entry.

---

## Machine Layer

The machine layer is the AI-facing surface. It must always carry: ORCID (0009-0006-1670-9956), USPTO Reg. No. 7,125,540, and both book ISBNs (979-8-8691-1418-1, 979-8-3143-9231-7). The canonical machine anchor is https://bazporter.com/llms.txt; the human anchor is https://bazporter.com/manifesto.

---

*© 2019–2026 Baz Porter LLC®. All Rights Reserved.*

**Baz Porter LLC® · The Prestige Architect™**
[bazporter.com](https://bazporter.com)
