#!/usr/bin/env python3
"""Build public-safe projections (committed) and full restricted outputs (gitignored)
from the full-fidelity datasets in restricted/data/.

Public rule: nothing marked restricted (unpublished prices/offers, buyer language, strategy,
named clients, proprietary curriculum) is written outside restricted/.
Run: python3 -I tools/build_projections.py   (from repo root, with restricted/data present)
"""
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "restricted" / "data"
VERSION = "2026.10.16.1"
TODAY = "2026-10-16"

# Titles/summaries safe for the public repo where the full title would disclose unpublished offers.
PUBLIC_TITLES = {
    "CON-012": ("Succession program naming, status and scope",
                "A rename and defined structure for a succession offer appear in the governing master; no product spec or legal scope was supplied and the live repo shows a different name and curriculum size. Not launched."),
    "CON-018": ("Institution naming lineage and pilot",
                "Institution and pilot naming in the governing master is not reflected in the live repo, which still refers to an earlier institution label. Neither is launched."),
    "CON-008": ("Single-session offer price record",
                "The governing master and the product spec disagree on whether a price is confirmed."),
    "CON-009": ("Implementation cohort format",
                "Duration and format differ between the governing master and the product spec. Delivery assets are not yet built; not launched."),
    "DEC-011": ("Succession program specification and legal scope", None),
    "DEC-017": ("Pilot and institution design parameters", None),
    "DEC-008": ("Single-session offer price", None),
    "DEC-009": ("Implementation cohort and accelerator format", None),
    "DEC-005": ("The Becoming payment structure and continuation", None),
}


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def dump(obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(obj, fh, sort_keys=False, allow_unicode=True, width=110)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fm(d):
    return "---\n" + yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110) + "---\n"


def bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "- none recorded"


def main():
    products = load("products.yaml")
    unspecified = load("unspecified_assets.yaml")
    fws = load("frameworks.yaml")
    cons = load("conflicts.yaml")
    decs = load("decisions.yaml")
    claims = load("claims.yaml")
    ledger = load("research_ledger.yaml")

    # ---------------- PRODUCTS ----------------
    for old in list((ROOT / "products").glob("PRD-*.md")) + list((ROOT / "ip" / "records").glob("FW-*.md")) + list((ROOT / "restricted" / "products").glob("PRD-*.md")) + list((ROOT / "restricted" / "ip").glob("FW-*.md")):
        old.unlink()
    pub_registry, res_registry = [], []
    for p in products:
        fname = f"{p['id']}-{slug(p['name'])[:48]}.md"
        pub = p["public"]
        ok = pub["price_public_ok"]
        rec = {
            "id": p["id"], "name": p["name"], "type": p["type"],
            "terms_public": pub["terms"],
            "launch_status": "unverified (no live readback performed)",
            "approval_status": p.get("approval_note", "specified-not-ratified"),
            "document_status": "current product specification 2026-10-16" if p["source_spec"] else "no product specification supplied",
            "conflicts": p["conflicts"],
            "last_verified": TODAY,
            "restricted_record": f"restricted/products/{fname}",
            "public_record": f"products/{fname}",
        }
        pub_registry.append(rec)
        res_registry.append({**rec, "terms_full": p["terms"], "stated_status": p["stated_status"],
                             "source_spec": p["source_spec"], "rosetta_refs": p["rosetta_refs"]})

        meta = {"id": p["id"], "doc_type": "product-record", "status": "draft-for-founder-review",
                "version": VERSION, "visibility": "public", "owner": "Baz Porter", "last_verified": TODAY,
                "launch_status": "unverified", "approval_status": p.get("approval_note", "specified-not-ratified")}
        body = f"# {p['name']}\n\n"
        body += f"**Type:** {p['type']}  \n**Public terms:** {pub['terms']}  \n"
        body += "**Launch status:** unverified. No live checkout, page, contract or workflow readback has been performed.  \n"
        body += f"**Open conflicts:** {', '.join(p['conflicts']) if p['conflicts'] else 'none recorded'}  \n\n"
        body += ("## Held in the restricted record\nDelivery components, prerequisites, claims limits and buyer-facing language come from internal "
                 "specifications that are not approved for publication. They are in the restricted record until the founder approves publication.\n\n")
        body += ("## Sources\nGoverning master: Rosetta Stone v4.2 (restricted, see registry/source-of-truth.yaml). "
                 "Spec: current product specification dated 2026-10-16 (restricted source).\n")
        (ROOT / "products").mkdir(exist_ok=True)
        (ROOT / "products" / fname).write_text(fm(meta) + body, encoding="utf-8")

        rmeta = dict(meta, visibility="restricted")
        rb = f"# {p['name']}\n\n"
        rb += f"**Type:** {p['type']}  \n**Terms (full):** {p['terms']}  \n**Source-stated status:** {p['stated_status']}  \n"
        rb += f"**Source spec:** {p['source_spec']}  \n**Rosetta sections:** {', '.join(p['rosetta_refs'])}  \n"
        rb += f"**Open conflicts:** {', '.join(p['conflicts']) or 'none'}  \n\n"
        rb += f"## Intended buyer and qualification\n{p['buyer_and_qualification']}\n\n## Transformation / outcome (draft, not founder-approved language)\n{p['outcome']}\n\n"
        rb += "## Delivery\n" + bullets(p["delivery"]) + f"\n\n## Prerequisites\n{p['prerequisites']}\n\n## Next offer\n{p['next_offer']}\n\n"
        rb += f"## Claims limits\n{p['claims_limits']}\n\n## Operational dependencies\n{p['dependencies']}\n\n"
        rb += "## Evidence\nNo outcome evidence supplied for this offer. Proof index required (Rosetta s12).\n\n"
        rb += f"## Reconciliation (founder precedence rule, 2026-10-16)\n{p.get('approval_note', 'none')}\n\nSpec variance not adopted: {p.get('spec_variance', 'none')}\n\n"
        rb += f"## Approval status\n{p.get('approval_note', 'specified-not-ratified')}. Last document verification {TODAY}; live systems not verified.\n"
        (ROOT / "restricted" / "products").mkdir(parents=True, exist_ok=True)
        (ROOT / "restricted" / "products" / fname).write_text(fm(rmeta) + rb, encoding="utf-8")

    dump({"registry": "products", "version": VERSION, "visibility": "public", "generated": TODAY,
          "note": "Public projection. Launch status is never 'live' without live readback; none performed.",
          "products": pub_registry,
          "unspecified_catalog_items": [u["name"] for u in unspecified if not u["name"].startswith("Rise")] + ["Further catalog items held in the restricted registry"]},
         ROOT / "registry" / "products.yaml")
    dump({"registry": "products", "visibility": "restricted", "products": res_registry, "unspecified": unspecified},
         ROOT / "restricted" / "registry" / "products-full.yaml")

    # ---------------- FRAMEWORKS ----------------
    (ROOT / "ip" / "records").mkdir(parents=True, exist_ok=True)
    pub_fw, res_fw = [], []
    for f in fws:
        fname = f"{f['id']}-{slug(f['name'])[:48]}.md"
        public = bool(f["public_ok"])
        entry = {"id": f["id"], "name": f["name"], "kind": f["kind"], "status": f["status"], "approval": f["approval"],
                 "visibility": "public" if public else "restricted", "unresolved_count": len(f["unresolved"]),
                 "record": (f"ip/records/{fname}" if public else f"restricted/ip/{fname}")}
        (pub_fw if public else res_fw).append(entry)
        meta = {"id": f["id"], "doc_type": "framework-record", "status": f["status"], "approval": f["approval"],
                "version": VERSION, "visibility": entry["visibility"], "owner": "Baz Porter", "last_verified": TODAY}
        body = f"# {f['name']}\n\n**Kind:** {f['kind']}  \n**Documentation status:** {f['status']}  \n**Approval:** {f['approval']}\n\n"
        ov = f.get("public_override") if public else None
        body += f"## Definition (as found in sources)\n{(ov or f)['definition']}\n\n## Components\n{bullets((ov or f)['components'])}\n\n"
        body += f"## Source locations\n{bullets(f['sources'])}\n\n## Provenance\n{f['provenance']}\n\n"
        body += f"## Limits and claims cautions\n{f['limits']}\n\n## Unresolved questions\n{bullets(f['unresolved'])}\n\n"
        body += "_Anything marked SOURCE REQUIRED has no primary text in any supplied source and has not been invented._\n"
        if public:
            (ROOT / "ip" / "records" / fname).write_text(fm(meta) + body, encoding="utf-8")
        else:
            (ROOT / "restricted" / "ip").mkdir(parents=True, exist_ok=True)
            (ROOT / "restricted" / "ip" / fname).write_text(fm(meta) + body, encoding="utf-8")
    # restricted-only frameworks still appear by id/name only in the public registry
    pub_ids = [{"id": e["id"], "name": e["name"], "visibility": "restricted", "record": e["record"]} for e in res_fw]
    dump({"registry": "frameworks", "version": VERSION, "visibility": "public", "generated": TODAY,
          "note": "Trademark symbols denote claimed branding, not verified registration.",
          "frameworks": pub_fw, "restricted_frameworks": pub_ids}, ROOT / "registry" / "frameworks.yaml")

    # ---------------- CONFLICTS & DECISIONS ----------------
    pc = []
    for c in cons:
        t, s = PUBLIC_TITLES.get(c["id"], (c["title"], c["public_summary"]))
        pc.append({"id": c["id"], "title": t, "severity": c["severity"], "category": c["category"],
                   "summary": s or c["public_summary"], "decision": c["decision"], "status": c["status"].split(":")[0]})
    dump({"registry": "conflicts", "version": VERSION, "visibility": "public", "generated": TODAY,
          "rule": "Conflicts are recorded, never silently resolved. Detail and values are in the restricted register.",
          "conflicts": pc}, ROOT / "registry" / "conflicts.yaml")
    dump({"registry": "conflicts", "visibility": "restricted", "conflicts": cons}, ROOT / "restricted" / "registry" / "conflicts-detail.yaml")
    pd = [{"id": d["id"], "title": PUBLIC_TITLES.get(d["id"], (d["title"], None))[0], "gate": d["gate"], "status": d["status"], **({"decided_on": d["decided_on"]} if "decided_on" in d else {})} for d in decs]
    dump({"registry": "founder-decisions", "version": VERSION, "visibility": "public", "generated": TODAY,
          "note": "Decisions marked approved were given by the founder on 2026-10-16; nothing else is approved. Options, evidence and recommendations are in the restricted register.",
          "decisions": pd}, ROOT / "registry" / "decisions.yaml")
    dump({"registry": "founder-decisions", "visibility": "restricted", "decisions": decs}, ROOT / "restricted" / "registry" / "decisions-detail.yaml")

    # ---------------- RESEARCH ----------------
    (ROOT / "research").mkdir(exist_ok=True)
    dump({"ledger": "research-evidence", "version": VERSION, "visibility": "public", "generated": TODAY,
          "access_note": ("No source was fetched in full. WebFetch and direct HTTP to publishers were blocked in the migration "
                          "environment; every entry rests on search-result summaries or background knowledge and must be re-verified "
                          "against the original before external use."),
          "entries": ledger}, ROOT / "research" / "ledger.yaml")
    dump({"audit": "founder-claims", "visibility": "restricted", "claims": claims}, ROOT / "restricted" / "research" / "claims-audit.yaml")
    # ---------------- INDEX PAGES ----------------
    hdr = lambda i, t: fm({"id": i, "doc_type": "index", "status": "current", "version": VERSION, "visibility": "public", "owner": "Baz Porter", "last_verified": TODAY}) + f"# {t}\n\n"
    rows = "\n".join(f"| [{r['id']}]({r['public_record'].split('/',1)[1]}) | {r['name']} | {r['type']} | {r['terms_public']} | {', '.join(r['conflicts']) or '-'} |" for r in pub_registry)
    (ROOT / "products" / "README.md").write_text(hdr("IDX-PRODUCTS", "Product and course registry") + "Machine-readable: `registry/products.yaml`. Launch status is **unverified** for every record (no live readback). Terms for unpublished offers are withheld in this public repo; full records are in the restricted store.\n\n| ID | Name | Type | Public terms | Open conflicts |\n|---|---|---|---|---|\n" + rows + "\n\nCatalog items with no supplied specification: " + ", ".join(u["name"] for u in unspecified if not u["name"].startswith("Rise")) + ", and one further paid feature held in the restricted registry.\n", encoding="utf-8")
    frows = "\n".join(f"| [{e['id']}]({e['record'].replace('ip/', '', 1)}) | {e['name']} | {e['status']} | {e['approval']} | {e['unresolved_count']} |" for e in pub_fw)
    (ROOT / "ip" / "README.md").write_text(hdr("IDX-IP", "IP and framework registry") + "Machine-readable: `registry/frameworks.yaml`. Trademark symbols show claimed branding, not verified registration (CON-017). **SOURCE REQUIRED** means no primary text exists in any supplied source; nothing has been invented. Existing public definition files remain in `frameworks/`.\n\n| ID | Name | Documentation status | Approval | Open questions |\n|---|---|---|---|---|\n" + frows + "\n\nRestricted-only records: " + ", ".join(e["id"] for e in res_fw) + " (names only here).\n", encoding="utf-8")
    print("built:", len(products), "products,", len(fws), "frameworks,", len(cons), "conflicts,", len(decs), "decisions,", len(ledger), "ledger,", len(claims), "claims")


if __name__ == "__main__":
    sys.exit(main())
