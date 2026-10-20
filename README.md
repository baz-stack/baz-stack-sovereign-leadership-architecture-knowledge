# Sovereign Leadership Architecture™ — Public Knowledge Repository

**Owner:** Baz Porter LLC™ · The Prestige Architect™ · **Founder:** Baz Porter · **ORCID:** [0009-0006-1670-9956](https://orcid.org/0009-0006-1670-9956) · **Site:** [bazporter.com](https://bazporter.com)

> **Version 2026.10.17.** Changes to published content require founder approval. Start at [`KNOWLEDGE_INDEX.md`](./KNOWLEDGE_INDEX.md).

## What this repository is

The public, citable reference for Sovereign Leadership Architecture™: approved definitions, an evidence register that states how well each public claim is supported, research references with their limits, publication and citation metadata, and AI-readable summaries. The frameworks are Baz Porter's proprietary models; they are not independently validated scientific theories, and no outcome is guaranteed.

Protected material (the governing canon, the ideal-client profile, product specifications, unpublished pricing, client records, original evidence files) is held in a separate private repository and is not published here.

## Where to read

| You want | Go to |
|---|---|
| A guided tour | [`docs/wiki/Home.md`](./docs/wiki/Home.md) |
| Agents and retrieval rules | [`agents/RETRIEVAL_POLICY.md`](./agents/RETRIEVAL_POLICY.md) |
| Every public claim and its status | [`registry/public-claims.yaml`](./registry/public-claims.yaml) |
| Definitions | [`frameworks/`](./frameworks/), [`glossary/glossary-and-terms.md`](./glossary/glossary-and-terms.md) |
| Books and identifiers | [`canon/BOOKS.md`](./canon/BOOKS.md) |
| Credentials with evidence status | [`canon/CREDIBILITY.md`](./canon/CREDIBILITY.md) |
| Research and its limits | [`research/README.md`](./research/README.md) |
| How to cite | [`CITATION.cff`](./CITATION.cff), [`citations/chronological-citation.md`](./citations/chronological-citation.md) |
| Machine-readable summaries | [`llms.txt`](./llms.txt), [`llms-full.txt`](./llms-full.txt), [`baz-porter.txt`](./baz-porter.txt) |
| Website AI-context files | [`site/`](./site/) |

## Structure

```
README.md · KNOWLEDGE_INDEX.md · LICENSE.md · CITATION.cff · GOVERNANCE.md · CONTRIBUTING.md
llms.txt · llms-full.txt · baz-porter.txt · robots.txt · sitemap.xml   machine layer (mirrors of site/)
docs/wiki/        public wiki pages (staged Markdown)
canon/            approved public canon (summaries where the original is private)
frameworks/       framework definitions        ip/        framework provenance records
products/         public product records       registry/  claims, decisions, conflicts, classification
research/         research ledger              evidence/  public evidence records (hashes only)
identity/         entity record, JSON-LD       glossary/ faq/ citations/
site/             deployable website AI-context files   metadata/ structured data copy
agents/           retrieval policy and profiles         tools/ validation, tests, generators
reports/          conflict and decision report, validation output
```

## Source hierarchy

1. Current approved public canon in this repository.
2. Verified evidence.
3. Public research references.
4. Approved explanatory documentation.
5. Historical material, labelled historical, which never overrides current canon.

## Status labels

Statements about credentials and achievements carry one of: documented, partly documented, founder-reported, pending verification, requires evidence. Nothing is labelled verified unless an independent source was checked. Open items (for example the date reconciliation for the Amazon ranking record, DEC-048) are kept in the registers rather than resolved silently.

## Marks and rights

™ marks are claimed marks. BAZ PORTER® is registered (Reg. No. 7,125,540, status Registered and live per the USPTO TSDR record checked 2026-10-20). All rights reserved; see [`LICENSE.md`](./LICENSE.md). Publishing machine-readable files does not guarantee inclusion in any AI system's training data, search results or answers.

## Checks

```
python3 -I tools/validate.py && python3 -I tools/retrieval_tests.py && python3 -I tools/tests/test_validate.py && python3 -I tools/check_exposure.py
```

© 2019–2026 Baz Porter LLC™.
