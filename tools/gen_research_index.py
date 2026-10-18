#!/usr/bin/env python3
"""Generate research/REFERENCES_INDEX.md from research/ledger.yaml.
Run: python3 -I tools/gen_research_index.py"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
HDR = "---\nid: IDX-RESEARCH-REFS\ndoc_type: index\nstatus: current\nversion: 2026.10.17.2\nvisibility: public\nowner: Baz Porter\nlast_verified: 2026-10-17\n---\n"


def cell(s):
    return " ".join(str(s).split()).replace("|", "/")


def main():
    d = yaml.safe_load((ROOT / "research" / "ledger.yaml").read_text(encoding="utf-8"))
    e = d["entries"]
    t = HDR + "# Research reference index\n\n"
    t += ("A readable index of the 51 entries in [`ledger.yaml`](./ledger.yaml), which is the source. Each row gives the citation as recorded, "
          "the evidence classification, what the source supports and what it does not establish. **None of the 51 sources was read in full or verified against the original**: "
          "DOI, volume and page details marked unverified in the ledger must be checked before external use. Cited research is background; it does not validate the founder's proprietary models, "
          "and ideas from physics, neuroscience, philosophy and spiritual traditions are not presented as established mechanisms of personal or business change.\n\n")
    t += "| ID | Subject | Citation as recorded | Classification | Access | Supports | Does not establish | Cautions |\n|---|---|---|---|---|---|---|---|\n"
    for x in e:
        t += (f"| {x['id']} | {cell(x['subject'])} | {cell(x['source_citation'])} | {x['category']} | {x['access_status']} | "
              f"{cell(x['supports'])} | {cell(x['does_not_establish'])} | {cell(x['cautions'])} |\n")
    t += "\n## Classification key\n\n"
    t += "established_empirical: replicated or well-documented finding. debated_hypothesis: live disagreement. theory: formal theory, not settled fact. philosophy, spiritual: preserved, not judged as science. practitioner_method: applied method with limited or mixed evidence. metaphor: figurative framing. founder_synthesis: original synthesis by the founder. unsupported: no adequate support found.\n"
    (ROOT / "research" / "REFERENCES_INDEX.md").write_text(t, encoding="utf-8")
    print("research index:", len(e), "entries")


if __name__ == "__main__":
    main()
