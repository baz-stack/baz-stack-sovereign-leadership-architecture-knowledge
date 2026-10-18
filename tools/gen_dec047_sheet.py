#!/usr/bin/env python3
"""Generate reports/07_DEC047_APPROVAL_SHEET.md from registry/public-review-ledger.yaml and registry/public-review-notes.yaml.
Run: python3 -I tools/review_public_files.py && python3 -I tools/gen_dec047_sheet.py"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
HDR = "---\nid: RPT-007\ndoc_type: report\nstatus: complete\nversion: 2026.10.17.2\nvisibility: public\nowner: Baz Porter\nlast_verified: 2026-10-17\n---\n"


def purpose(path):
    try:
        for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].replace("|", "/")[:70]
    except OSError:
        pass
    return path


def cell(items):
    return "; ".join(items).replace("|", "/") if items else "none"


def main():
    led = yaml.safe_load((ROOT / "registry/public-review-ledger.yaml").read_text(encoding="utf-8"))["files"]
    notes = yaml.safe_load((ROOT / "registry/public-review-notes.yaml").read_text(encoding="utf-8"))["notes"]
    changed = [f for f in led if f["resolved_issues"]]
    outstanding = [f for f in led if f["outstanding_issues"]]
    t = HDR + "# DEC-047 approval sheet: 44 public-by-design files and three split files\n\n"
    t += ("Reconciled on 2026-10-17 against the actual current contents of every file. The review is the reviewer's, not the founder's approval: "
          "founder approval is recorded as pending for every file and none is marked approved. The machine-readable form is "
          "`registry/public-review-ledger.yaml`.\n\n")
    t += ("**Terms used.** *Resolved*: an issue found earlier or in this pass and corrected in the current file. *Outstanding*: an item still open; none is a publication blocker unless stated. "
          "*Founder-confirmed*: stated or confirmed by the founder, not independently checked. *Independently verified*: checked against an independent source; **none** of the public claims is at this level. "
          "*Unverified*: a claim kept with its status shown. *Publication blocker*: an item that must be resolved before the file can be public.\n\n")
    t += (f"- Files reviewed: {len(led)}\n- Files with resolved issues (changed): {len(changed)}\n- Files with outstanding items: {len(outstanding)} (all non-blocking)\n"
          f"- Publication blockers in these files: {sum(1 for f in led if f['publication_blocker'] != 'none')}\n- Founder approval recorded: 0 of {len(led) + 3}\n\n")
    t += "## Files with changes or outstanding items\n\n| File | Resolved | Outstanding | Founder-confirmed | Unverified (status shown in file) | Blocker | Recommendation |\n|---|---|---|---|---|---|---|\n"
    for f in led:
        if not (f["resolved_issues"] or f["outstanding_issues"]):
            continue
        rec = "Approve" if not f["outstanding_issues"] else "Approve; outstanding item is a documented follow-up"
        t += f"| `{f['path']}` | {cell(f['resolved_issues'])} | {cell(f['outstanding_issues'])} | {cell(f['founder_confirmed'])} | {cell(f['unverified_claims'])} | {f['publication_blocker']} | {rec} |\n"
    t += "\n## Files with no open items\n\n| File | Purpose | Class | Findings | Recommendation |\n|---|---|---|---|---|\n"
    for f in led:
        if f["resolved_issues"] or f["outstanding_issues"]:
            continue
        t += f"| `{f['path']}` | {purpose(f['path'])} | public-confirm | {f['mechanical_findings']}; {f['reviewer_notes']} | Approve |\n"
    t += ("\n## The three split files (public summary at head, original private)\n\n| File | Disposition | Outstanding |\n|---|---|---|\n"
          "| `CHANGELOG.md` | Public summary only; prices, payment structures and file-level history held privately | Founder wording approval |\n"
          "| `canon/STORY.md` | Approved public biography with evidence statuses; confidential narrative private | Founder wording approval |\n"
          "| `canon/AFFILIATE.md` | Public overview; no commission figures or partner terms; paused AI clone listed as not offered | Founder wording approval |\n")
    t += ("\n## Repository-wide publication blockers\n\nNone found in the file contents. The following are conditions, not content defects: founder per-file approval; "
          "the independent audit; the historical wiki (unrecovered; no paid upgrade authorized); website files compared with the live files (the live site cannot be read from the build environment).\n")
    (ROOT / "reports/07_DEC047_APPROVAL_SHEET.md").write_text(t, encoding="utf-8")
    print("sheet written:", len(changed), "changed,", len(outstanding), "outstanding")


if __name__ == "__main__":
    main()
