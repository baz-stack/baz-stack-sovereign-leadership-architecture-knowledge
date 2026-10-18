# Instructions for Claude Code and other agents

1. Read `KNOWLEDGE_INDEX.md` and `agents/RETRIEVAL_POLICY.md`. Then load your profile from `agents/profiles/`. Do not load the whole repository.
2. This repository is **public**. Never commit anything from `restricted/` (it is gitignored) or any text of the Rosetta Stone, the ICA, product specifications, prices of unpublished offers, client names, or campaign specs. Run `python3 -I tools/check_exposure.py` before every commit.
3. Never resolve a conflict silently. Record it in `registry/conflicts.yaml` (via the restricted dataset and `tools/build_projections.py`).
4. Do not edit Rosetta Stone v4.2 or the ICA. Do not change prices, promises or launch status. Do not merge to `main`, publish, send outreach or change a live CRM without explicit founder approval.
5. After editing data, rebuild and validate: `python3 -I tools/build_projections.py && python3 -I tools/validate.py`.
