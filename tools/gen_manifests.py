#!/usr/bin/env python3
"""Generate registry/source-of-truth.yaml, migration-manifest.yaml, restricted-manifest.yaml,
exposure-register.yaml and retired/MANIFEST.yaml. Needs restricted/sources for hashes.
Run: python3 -I tools/gen_manifests.py"""
import hashlib
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE_COMMIT = "358a85777ca7a5ed47fc5115b379791f4b08c35a"
VERSION = "2026.10.16.1"
TODAY = "2026-10-16"
ZIP_SHA = "efcfb4b2b5cae9f470db54336fac93a57e3b3411b5fb3cd641163c9067391ea2"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(o, p):
    p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(o, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")


def ls_base():
    out = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE_COMMIT], cwd=ROOT, text=True)
    return [x for x in out.splitlines() if x]


# (prefix-or-exact, status, retrieval, note)
RULES = [
    ("canon/ICA.md", "retired-tombstone", "deny", "Retired 2026-10-16 (DEC-013); preserved in retired/canon/ICA.md. Replaced by the 2026-10-14 ICA (restricted)."),
    ("canon/PRODUCT-ARCHITECTURE.md", "retired-tombstone", "deny", "Retired 2026-10-16 (DEC-013); preserved in retired/canon/PRODUCT-ARCHITECTURE.md."),
    ("canon/OFFERS.md", "retired-tombstone", "deny", "Retired 2026-10-16 (DEC-013); preserved in retired/canon/OFFERS.md. Policy items present only here: CON-021."),
    ("canon/RETIRED.md", "legacy-canon-under-review", "history-only", "Useful retirement log; contains stale prices."),
    ("canon/FRAMEWORKS.md", "legacy-canon-under-review", "allow-with-caveat", "Definitions usable; offer tables stale; scientific wording CON-015."),
    ("canon/IP-REGISTRY.md", "legacy-canon-under-review", "allow-with-caveat", "Mark registry; trademark status unverified CON-017."),
    ("canon/TRADEMARKS.md", "legacy-canon-under-review", "allow-with-caveat", "CON-017."),
    ("canon/", "legacy-canon-under-review", "allow-with-caveat", "Public brand/credibility text; claims unverified CON-016."),
    ("frameworks/", "legacy-definition-under-review", "allow-with-caveat", "Best available public definition text; offer/pricing sections stale; see ip/records for status."),
    ("institution/", "restricted-content-publicly-exposed", "deny-public-agents", "Labelled private but repo is public. CON-001 / EXP-001."),
    ("_holding/", "archive", "deny", "Superseded machine files."),
    ("llms.txt", "public-machine-layer-stale-offer-language", "allow-with-caveat", "Machine anchor; offer language predates Rosetta v4.2."),
    ("baz-porter.txt", "public-machine-layer-stale-offer-language", "allow-with-caveat", "Credential claims unverified CON-016."),
    ("identity/", "public-identity-layer", "allow-with-caveat", "Credential claims unverified CON-016."),
    ("glossary/", "public-glossary", "allow-with-caveat", "Align to Rosetta after decisions."),
    ("faq/", "public-faq", "allow-with-caveat", ""),
    ("citations/", "public-citations", "allow-with-caveat", ""),
]


def classify(path):
    for pre, st, ret, note in RULES:
        if path == pre or (pre.endswith("/") and path.startswith(pre)):
            return st, ret, note
    return "retained-governance-or-machine-file", "allow", ""


def main():
    base = ls_base()
    # ---- migration manifest ----
    entries = []
    for f in base:
        st, ret, note = classify(f)
        cur = ROOT / f
        orig = subprocess.check_output(["git", "show", f"{BASE_COMMIT}:{f}"], cwd=ROOT)
        if st == "retired-tombstone":
            action = f"retired: moved to retired/{f}; tombstone left at original path (founder decision 2026-10-16)"
            dest = f"retired/{f}"
        elif f == ".gitignore":
            action = "retained in place; infrastructure edit (restricted/ ignored); original in git history"
            dest = f
        elif cur.exists() and cur.read_bytes() != orig:
            action = "retained in place; edited under founder decisions of 2026-10-16 (original preserved in retired/superseded-text/; see reports/04_DECISIONS_APPLIED_LOG.md)"
            dest = f
        else:
            action = "retained in place, byte-identical"
            dest = f
        entries.append({"source": f, "origin": f"git:{BASE_COMMIT[:7]}", "action": action, "destination": dest, "status": st, "retrieval": ret, "note": note})
    z = ROOT / "restricted" / "sources"
    zip_map = {
        "01_CANON/00_Rosetta_Stone_v4.2_UNCHANGED.docx": ("restricted/canon/ROSETTA_STONE_v4.2.md", "CAN-001"),
        "01_CANON/00_Lisa_Miles_Full_ICA_2026-10-14.docx": ("restricted/canon/LISA_MILES_ICA_2026-10-14.md", "CAN-002"),
        "03_IP_AND_FRAMEWORKS/FRAMEWORK_REGISTRY.md": ("registry/frameworks.yaml + ip/records/", "HND-004"),
        "04_RESEARCH_AND_PROVENANCE/RESEARCH_LEDGER.md": ("research/ + restricted/research/", "HND-005"),
        "05_INSTITUTION/INSTITUTION_MAP.md": ("registry/products.yaml PRD-013/014 + restricted/products/", "HND-006"),
        "06_AI_GOVERNANCE/AGENT_ROUTING.md": ("agents/RETRIEVAL_POLICY.md", "HND-002"),
        "06_AI_GOVERNANCE/CLAUDE_MASTER_EXECUTION.md": ("tools/ + PROGRESS.md (process directive)", "HND-001"),
        "07_CAMPAIGNS/COPY_AND_FUNNEL_BRIEF.md": ("restricted/campaigns/", "HND-007"),
        "README.md": ("restricted/sources/README.md (staging notice)", "HND-000"),
        "retired/README.md": ("retired/README.md (superseded by populated archive manifest)", "HND-008"),
    }
    prod_ids = ["PRD-001", "PRD-002", "PRD-003", "PRD-004", "PRD-005", "PRD-006", "PRD-007", "PRD-008", "PRD-009", "PRD-010", "PRD-011"]
    for p in sorted(z.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(z))
        if rel.startswith(("drive/", "website/", "legal/")):
            continue  # founder Drive ingests are not part of the handoff zip
        if rel.startswith("02_PRODUCTS"):
            n = int(p.name[:2])
            dest, i = f"restricted/products/{prod_ids[n-1]}-*.md (+ public projection products/{prod_ids[n-1]}-*.md)", f"SRC-{prod_ids[n-1]}"
        else:
            dest, i = zip_map[rel]
        entries.append({"source": f"zip:{rel}", "origin": f"Sovereign_Knowledge_OS_Claude_Handoff_2026-10-16.zip", "sha256": sha(p), "action": "preserved byte-identical in restricted/sources; converted/derived to destination", "destination": dest, "id": i})
    dump({"manifest": "migration", "version": VERSION, "generated": TODAY, "base_commit": BASE_COMMIT, "handoff_zip_sha256": ZIP_SHA,
          "base_file_count": len(base), "zip_file_count": sum(1 for e in entries if e["source"].startswith("zip:")),
          "rule": "Every base-commit file and every zip file appears exactly once. Nothing deleted.", "entries": entries}, "registry/migration-manifest.yaml")

    # ---- source of truth ----
    def zh(rel):
        return sha(z / rel)
    docs = [
        {"id": "CAN-001", "title": "Rosetta Stone v4.2 (governing business master)", "level": 1, "version": "4.2", "status": "governing-qualified", "visibility": "restricted",
         "location": "restricted/canon/ROSETTA_STONE_v4.2.md (founder-controlled; original DOCX in handoff zip)", "sha256": zh("01_CANON/00_Rosetta_Stone_v4.2_UNCHANGED.docx"),
         "notes": "Version identity preserved; not renamed, not merged with the ICA. Document states whole-document ratification pending."},
        {"id": "CAN-002", "title": "Lisa Miles Full Ideal Client Architecture 2026-10-14", "level": 1, "version": "2026-10-14", "status": "governing-buyer-master-ratification-pending", "visibility": "restricted",
         "location": "restricted/canon/LISA_MILES_ICA_2026-10-14.md", "sha256": zh("01_CANON/00_Lisa_Miles_Full_ICA_2026-10-14.docx"), "notes": "Separate from Rosetta by design."},
    ]
    names = ["Fast Future Freedom Blueprint", "A Million Dreams Circle", "The Reclamation Code", "Manifestation That Finally Works", "The Sovereign Session", "The Becoming", "Coming Home", "Revenue Architecture System", "RAMS Business Profit Accelerator", "Revenue Owner Sprint", "The Gravity Code"]
    for i, pth in enumerate(sorted((z / "02_PRODUCTS_AND_COURSES").glob("*.docx"))):
        docs.append({"id": f"SRC-{prod_ids[i]}", "title": f"Product specification: {names[i]}", "level": 1, "version": "2026-10-16", "status": "current-spec-not-ratified", "visibility": "restricted",
                     "location": f"restricted/sources/02_PRODUCTS_AND_COURSES/{pth.name}", "sha256": sha(pth), "notes": "Below Rosetta in precedence until founder ratifies; spec-internal precedence claims do not override Rosetta."})
    for i, (rel, t, st) in enumerate([("03_IP_AND_FRAMEWORKS/FRAMEWORK_REGISTRY.md", "Handoff framework registry (candidate inventory)", "candidate-inventory"), ("04_RESEARCH_AND_PROVENANCE/RESEARCH_LEDGER.md", "Handoff research worklist", "worklist"),
                                      ("05_INSTITUTION/INSTITUTION_MAP.md", "Handoff institution map", "current-working-architecture"), ("06_AI_GOVERNANCE/AGENT_ROUTING.md", "Handoff retrieval policy", "process-input"),
                                      ("06_AI_GOVERNANCE/CLAUDE_MASTER_EXECUTION.md", "Handoff master execution directive", "process-input"), ("07_CAMPAIGNS/COPY_AND_FUNNEL_BRIEF.md", "Handoff campaign and funnel brief", "not-approved-live-copy")]):
        docs.append({"id": f"HND-{i+1:03d}", "title": t, "level": 2, "version": "2026-10-16", "status": st, "visibility": "restricted-staging", "location": f"restricted/sources/{rel}", "sha256": zh(rel)})
    live = [
        ("LEG-001", "canon/ICA.md", "retired-tombstone"), ("LEG-002", "canon/PRODUCT-ARCHITECTURE.md", "retired-tombstone"), ("LEG-003", "canon/OFFERS.md", "retired-tombstone"),
        ("LEG-004", "canon/FRAMEWORKS.md", "legacy-canon-under-review"), ("LEG-005", "canon/IP-REGISTRY.md", "legacy-canon-under-review"), ("LEG-006", "frameworks/*.md", "legacy-definition-reworded-2026-10-16-founder-read-pending"),
        ("LEG-007", "institution/**", "restricted-content-publicly-exposed"), ("LEG-008", "llms.txt, baz-porter.txt, identity/, glossary/, faq/, citations/", "public-layer-stale-offer-language"),
    ]
    for i, p, s in live:
        docs.append({"id": i, "title": f"Existing repository: {p}", "level": 3, "version": "as of base commit " + BASE_COMMIT[:7], "status": s, "visibility": "public (repo is public)", "location": p, "notes": "Historical evidence; never silently overrides canon."})
    dump({"registry": "source-of-truth", "version": VERSION, "generated": TODAY, "visibility": "public",
          "authority_order": [
              "1. Founder-approved decisions and corrections (explicit, dated)",
              "2. Rosetta Stone v4.2 (CAN-001)",
              "3. Lisa Miles Full ICA 2026-10-14 (CAN-002) - separate document, never merged with Rosetta",
              "4. Current product/course specifications 2026-10-16 (SRC-PRD-*)",
              "5. Latest framework/IP and institution working architecture (HND-*)",
              "6. Existing GitHub material (LEG-*) - historical evidence",
              "7. External research (research/ledger.yaml) - classified, never promoted to fact without verification"],
          "conflict_rule": "Record the conflict in registry/conflicts.yaml, hold for founder approval, never choose silently.",
          "base_commit": BASE_COMMIT, "documents": docs}, "registry/source-of-truth.yaml")

    # ---- restricted manifest ----
    dump({"manifest": "restricted-content", "version": VERSION, "generated": TODAY, "visibility": "public",
          "why": "baz-stack/sovereign-leadership-architecture was a PUBLIC GitHub repository (it has since been made private; verified 2026-10-16 via GitHub API and anonymous HTTP 200). A folder named private does not restrict access. These items are therefore kept OUT of every commit on this branch.",
          "held_out_of_commits": [
              {"id": "CAN-001", "what": "Rosetta Stone v4.2 full text", "reason": "The document itself is marked internal and confidential. Contains unpublished prices, targets, client names, strategy.", "sha256": docs[0]["sha256"]},
              {"id": "CAN-002", "what": "Lisa Miles ICA full text", "reason": "The document itself is marked private; internal governing buyer master.", "sha256": docs[1]["sha256"]},
              {"id": "SRC-PRD-*", "what": "11 product specification texts and buyer-facing draft copy", "reason": "The documents are marked internal. Unapproved value propositions; unpublished terms."},
              {"id": "RES-CLAIMS", "what": "Founder claim audit (restricted/research/claims-audit.yaml)", "reason": "Assesses founder credentials and claims; unverified."},
              {"id": "INS-FULL", "what": "Green Room / Gate Home / succession detail", "reason": "Unlaunched; terms and design undefined."},
              {"id": "CAM-SPEC", "what": "Harvey / GoHighLevel specifications, scoring rubric and campaign briefs", "reason": "Derived from the restricted ICA; unapproved copy."},
          ],
          "local_location": "restricted/ (gitignored). Delivered to the founder as Sovereign_Knowledge_OS_RESTRICTED_BUNDLE.zip.",
          "promotion_path": "After DEC-001 (private repo or private visibility), run tools/promote_restricted.py to move restricted/ into the private location."}, "registry/restricted-manifest.yaml")

    # ---- exposure register ----
    dump({"register": "exposure", "version": VERSION, "generated": TODAY, "visibility": "public",
          "note": "Describes categories and paths only; does not reproduce exposed content.",
          "findings": [
              {"id": "EXP-001", "severity": "P0", "path": "institution/", "category": "proprietary curriculum and internal commercial figures in a public repo", "in_history": True, "action_taken": "none (no deletion without founder approval); not extended by this migration. Founder approved making the repository private on 2026-10-17; the connected GitHub tools cannot change visibility, so the owner must switch it in repository settings", "decision": "DEC-001"},
              {"id": "EXP-002", "severity": "P0", "path": "canon/ICA.md", "category": "internal-only demographic/gender targeting section and unsourced statistics", "in_history": True, "action_taken": "status banner added; content unchanged", "decision": "DEC-001, DEC-013"},
              {"id": "EXP-003", "severity": "P1", "path": "canon/CREDIBILITY.md, canon/STORY.md, frameworks/brand-narrative.md", "category": "unverified credential claims and sensitive personal narrative", "in_history": True, "action_taken": "recorded in restricted claim audit", "decision": "DEC-015"},
              {"id": "EXP-004", "severity": "P1", "path": "robots.txt, GOVERNANCE.md", "category": "controls described as walling off private tier do not restrict GitHub access", "in_history": True, "action_taken": "recorded", "decision": "DEC-001"},
              {"id": "EXP-005", "severity": "P1", "path": "ten other branches and the full commit history", "category": "earlier branches carry the same pre-migration public content; visibility change does not erase clones, caches or search-engine copies", "in_history": True, "action_taken": "recorded; no branch deleted and no history rewritten", "decision": "DEC-001"},
              {"id": "EXP-006", "severity": "P1", "path": "live website mirrors of baz-porter.txt and llms.txt", "category": "website pages repeating withdrawn Delphi figure, undated bestseller wording and unverified credentials", "in_history": False, "action_taken": "replacement copy prepared in the restricted store; no website access", "decision": "DEC-042"},
              {"id": "EXP-007", "severity": "P1", "path": "commits ac44258, 372ba54, 7f10c63, 0d72a44", "category": "early migration commits carrying specification detail, validator price literals, a pilot parameter and pre-edit snapshots with withdrawn claims", "in_history": True, "action_taken": "fixed at head; history untouched pending DEC-045", "decision": "DEC-045"},
              {"id": "EXP-008", "severity": "P2", "path": "pull request 5", "category": "pull request page and diff are public while the repository is public", "in_history": False, "action_taken": "recorded", "decision": "DEC-001"},
              {"id": "EXP-009", "severity": "P0", "path": "canon/STORY.md and canon/CREDIBILITY.md in history and on every branch", "category": "confidential personal narrative with medical details and named third parties", "in_history": True, "action_taken": "removed from the public tree at head; originals preserved privately; history untouched pending DEC-045", "decision": "DEC-045"}]},
         "registry/exposure-register.yaml")

    # ---- retired manifest ----
    moved, snaps = [], []
    for src, rep, why in [("canon/ICA.md", "restricted/canon/LISA_MILES_ICA_2026-10-14.md (CAN-002)", "Cites Rosetta v4.0; superseded by the 2026-10-14 ICA"),
                          ("canon/PRODUCT-ARCHITECTURE.md", "registry/products.yaml", "Three-lane architecture and v4.0 source not in Rosetta v4.2"),
                          ("canon/OFFERS.md", "registry/products.yaml", "Entry door, tiers and prices differ from Rosetta v4.2")]:
        moved.append({"source_path": src, "origin_commit": BASE_COMMIT, "retired_path": "retired/" + src, "tombstone_at_source_path": True, "replacement": rep, "reason": why, "retired_on": TODAY, "authority": "founder decision DEC-013"})
    moved.append({"source_path": "frameworks/silent-collapse-diagnostic.md", "origin_commit": BASE_COMMIT, "retired_path": "retired/frameworks/silent-collapse-diagnostic.md", "tombstone_at_source_path": True,
                  "replacement": "products/PRD-001-fast-future-freedom-blueprint.md", "reason": "Silent Collapse Diagnostic retired; the Fast Future Freedom Blueprint is the entry door", "retired_on": TODAY, "authority": "founder decision DEC-037"})
    snapdir = ROOT / "retired" / "superseded-text"
    if snapdir.exists():
        for q in sorted(x for x in snapdir.rglob("*") if x.is_file()):
            rel = str(q.relative_to(snapdir))
            snaps.append({"source_path": rel, "origin_commit": BASE_COMMIT, "snapshot": str(q.relative_to(ROOT)), "reason": "pre-edit copy kept before founder-approved rewording or retirement edits of 2026-10-16", "see": "reports/04_DECISIONS_APPLIED_LOG.md"})
    prev_path = ROOT / "retired" / "MANIFEST.yaml"
    if prev_path.exists():  # keep entries for files that now live only in the private repository
        import yaml as _y
        prev = _y.safe_load(prev_path.read_text(encoding="utf-8")) or {}
        held_moved = {e["retired_path"]: e for e in prev.get("moved", []) if e.get("location") == "private-repository"}
        held_snaps = {e["snapshot"]: e for e in prev.get("superseded_text_snapshots", []) if e.get("location") == "private-repository"}
        for e in moved:
            if e["retired_path"] in held_moved:
                e["location"], e["sha256"] = "private-repository", held_moved[e["retired_path"]]["sha256"]
        have = {e["snapshot"] for e in snaps}
        for k, e in held_snaps.items():
            if k not in have:
                snaps.append(e)
        snaps.sort(key=lambda e: e["snapshot"])
    dump({"manifest": "retired", "version": VERSION, "generated": TODAY, "moved": moved, "superseded_text_snapshots": snaps,
          "rule": "Retirement preserves prior version, source path, reason and replacement. Git history is also preserved."}, "retired/MANIFEST.yaml")
    print("manifests written;", len(entries), "migration entries")


if __name__ == "__main__":
    main()
