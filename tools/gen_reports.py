#!/usr/bin/env python3
"""Generate reports/02_CONFLICT_AND_DECISION_REPORT.md and reports/04_DECISIONS_APPLIED_LOG.md.
Run: python3 -I tools/gen_reports.py"""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
HDR = "---\nid: {i}\ndoc_type: report\nstatus: complete\nversion: 2026.10.16.1\nvisibility: public\nowner: Baz Porter\nlast_verified: 2026-10-16\n---\n"


def main():
    cons = yaml.safe_load((ROOT / "registry/conflicts.yaml").read_text(encoding="utf-8"))["conflicts"]
    decs = yaml.safe_load((ROOT / "registry/decisions.yaml").read_text(encoding="utf-8"))["decisions"]
    t = HDR.format(i="RPT-002") + "# Conflict and founder-decision report\n\nConflicts are recorded, never silently resolved. Founder decisions given on 2026-10-16 are marked. Evidence, options and values are in the restricted register.\n\n"
    for sev in ["P0", "P1", "P2"]:
        t += f"## {sev}\n\n| ID | Title | Category | Decision | Status |\n|---|---|---|---|---|\n"
        for c in cons:
            if c["severity"] == sev:
                t += f"| {c['id']} | {c['title']} | {c['category']} | {c['decision']} | {c['status']} |\n"
        t += "\n"
    t += "## Summaries\n\n" + "".join(f"**{c['id']} - {c['title']}.** {c['summary']}\n\n" for c in cons)
    t += "## Founder decision queue\n\n| ID | Decision | Gate | Status | Decided |\n|---|---|---|---|---|\n"
    for d in decs:
        t += f"| {d['id']} | {d['title']} | {d['gate']} | {d['status']} | {d.get('decided_on', '')} |\n"
    (ROOT / "reports/02_CONFLICT_AND_DECISION_REPORT.md").write_text(t, encoding="utf-8")

    # The before/after log carries withdrawn text, so it lives in the private repository (mirrored under restricted/).
    src = ROOT / "restricted" / "legacy-public-history" / "tools" / "decisions_applied_2026-10-16.json"
    if not src.exists():
        src = ROOT / "tools/decisions_applied_2026-10-16.json"
    if not src.exists():
        print("reports written; decisions log not available (private repository not mounted), report 04 skipped")
        return
    log = json.loads(src.read_text(encoding="utf-8"))
    u = HDR.format(i="RPT-004") + "# Founder decisions applied, 2026-10-16: before and after\n\nEvery edit made to existing public files after the founder's instruction. Originals are preserved in `retired/superseded-text/` (edited files) and `retired/` (retired files) and in git history. Rewording is conservative: mechanism claims were removed or labelled as the founder's model; no new claims were authored. **The founder has not yet read the reworded text.**\n\n"
    cur = None
    for path, why, old, new in log:
        if path != cur:
            u += f"\n## `{path}`\n\n"
            cur = path
        o = str(old).replace("\n", " ")[:500]
        n = str(new).replace("\n", " ")[:500]
        u += f"- **{why}.**\n  - Before: {o}\n  - After: {n}\n"
    dest = ROOT / "reports/04_DECISIONS_APPLIED_LOG.md" if (ROOT / "tools/decisions_applied_2026-10-16.json").exists() else ROOT / "restricted" / "reports" / "04_DECISIONS_APPLIED_LOG.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(u, encoding="utf-8")
    print("reports written;", len(log), "edits logged")


if __name__ == "__main__":
    main()
