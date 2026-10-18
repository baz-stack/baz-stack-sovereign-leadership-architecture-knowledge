#!/usr/bin/env python3
"""Generate agents/retrieval-manifest.json from registry/migration-manifest.yaml, agents/profiles and the public tree.
Run: python3 -I tools/gen_agent_manifest.py"""
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
VERSION = "2026.10.16.1"


def clean(p):
    return re.sub(r"\s*\(.*$", "", p).strip()


def main():
    mm = yaml.safe_load((ROOT / "registry" / "migration-manifest.yaml").read_text(encoding="utf-8"))
    docs = []
    for e in mm["entries"]:
        if e["source"].startswith("zip:"):
            continue
        docs.append({"path": e["source"], "status": e["status"], "retrieval": e["retrieval"], "tier": "historical", "note": e.get("note", "")})
        if e["destination"] != e["source"]:
            docs.append({"path": e["destination"], "status": "retired", "retrieval": "deny", "tier": "historical", "note": "retired copy"})
    new_dirs = ["registry", "products", "ip", "research", "operations", "agents", "campaigns", "reports"]
    singles = ["KNOWLEDGE_INDEX.md", "CLAUDE.md", "PROGRESS.md", "canon/CANON_INDEX.md", "retired/README.md", "retired/MANIFEST.yaml"]
    new = [s for s in singles if (ROOT / s).exists()]
    for d in new_dirs:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and p.name != "retrieval-manifest.json":
                new.append(str(p.relative_to(ROOT)))
    for path in new:
        tier = 0 if path in ("KNOWLEDGE_INDEX.md", "CLAUDE.md", "canon/CANON_INDEX.md") else (1 if path.startswith(("agents/", "registry/")) else 2)
        docs.append({"path": path, "status": "current", "retrieval": "allow", "tier": tier, "approx_bytes": (ROOT / path).stat().st_size})
    for p in ["restricted/canon/ROSETTA_STONE_v4.2.md", "restricted/canon/LISA_MILES_ICA_2026-10-14.md", "restricted/registry/products-full.yaml", "restricted/registry/conflicts-detail.yaml",
              "restricted/registry/decisions-detail.yaml", "restricted/research/claims-audit.yaml", "restricted/institution/GREEN_ROOM.md", "restricted/institution/GATE_HOME.md",
              "restricted/institution/WITHOUT_YOU.md", "restricted/institution/OPERATIONS.md", "restricted/campaigns/HARVEY_SPEC.md", "restricted/campaigns/GHL_CONFIG.md",
              "restricted/campaigns/SAFEGUARDS.md", "restricted/campaigns/PROSPECTING_EXPORT_PACKET.md", "restricted/campaigns/COPY_TRACEABILITY.md", "restricted/campaigns/ghl-config.json"]:
        docs.append({"path": p, "status": "current", "retrieval": "allow-restricted-store-only", "tier": "restricted", "export_safe": p.endswith("PROSPECTING_EXPORT_PACKET.md")})
    profiles = {}
    for pf in sorted((ROOT / "agents" / "profiles").glob("*.yaml")):
        y = yaml.safe_load(pf.read_text(encoding="utf-8"))
        profiles[pf.stem] = {"read_first": [clean(x["path"]) for x in y.get("read_first", [])] if "read_first" in y else [], "read_on_demand": [clean(x) for x in y.get("read_on_demand", [])],
                             "uses_profile": y.get("uses_profile"), "external_tool_safe": y.get("external_tool_safe", False), "export_safe_documents": y.get("export_safe_documents", []), "profile_file": f"agents/profiles/{pf.name}"}
    deny = sorted({d["path"] for d in docs if d["retrieval"] in ("deny", "deny-public-agents")} | {"retired/"})
    out = {"manifest": "agent-retrieval", "version": VERSION, "generated": "2026-10-16",
           "start": ["KNOWLEDGE_INDEX.md", "agents/RETRIEVAL_POLICY.md"],
           "rules": {"load_whole_repo": False, "writes": "founder approval required", "on_conflict": "flag, do not choose", "external_tools": "export-safe packet only"},
           "deny_as_current_truth": deny, "profiles": profiles, "documents": docs}
    (ROOT / "agents" / "retrieval-manifest.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("manifest:", len(docs), "documents,", len(profiles), "profiles")


if __name__ == "__main__":
    main()
