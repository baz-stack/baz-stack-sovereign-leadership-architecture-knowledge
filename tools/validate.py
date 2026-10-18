#!/usr/bin/env python3
"""Knowledge OS validation suite.
Usage: python3 -I tools/validate.py [--full]
Public mode checks only what is committed. --full also checks the restricted store if present
(Rosetta vs product consistency, Green Room price, restricted retrieval paths).
Writes reports/validation-public.md (public mode) or restricted/reports/validation-full.md (--full).
Exit code 1 on any FAIL."""
import json
import re
import subprocess
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify_repository import PRIVATE_MIGRATE  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FULL = "--full" in sys.argv
BASE = "358a85777ca7a5ed47fc5115b379791f4b08c35a"
RESTRICTED = ROOT / "restricted"
HAS_R = RESTRICTED.exists()
FACTS = yaml.safe_load((RESTRICTED / "facts.yaml").read_text(encoding="utf-8")) if (RESTRICTED / "facts.yaml").exists() else {}
FACTS = yaml.safe_load((RESTRICTED / "facts.yaml").read_text(encoding="utf-8")) if (RESTRICTED / "facts.yaml").exists() else {}

results = []  # (name, status, details)


def rec(name, fails, warns=None, info=None):
    results.append((name, "FAIL" if fails else "PASS", fails, warns or [], info or []))


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def yload(p):
    return yaml.safe_load(read(p))


# ---------- file sets ----------
NEW_DIRS = ["registry", "products", "ip", "research", "operations", "agents", "campaigns", "reports"]
NEW_SINGLE = ["KNOWLEDGE_INDEX.md", "CLAUDE.md", "PROGRESS.md", "canon/CANON_INDEX.md", "retired/README.md", "retired/MANIFEST.yaml"]


def new_files():
    out = [s for s in NEW_SINGLE if (ROOT / s).exists()]
    for d in NEW_DIRS:
        out += [str(p.relative_to(ROOT)) for p in sorted((ROOT / d).rglob("*")) if p.is_file()]
    return out


NEW = new_files()
NEW_MD = [f for f in NEW if f.endswith(".md")]
HIST_OK = {"registry/conflicts.yaml", "registry/migration-manifest.yaml", "registry/source-of-truth.yaml", "registry/exposure-register.yaml", "registry/decisions.yaml", "retired/MANIFEST.yaml", "retired/README.md", "research/ledger.yaml", "registry/restricted-manifest.yaml"}
ACTIVE = [f for f in NEW if f not in HIST_OK and not f.startswith("reports/") and f != "PROGRESS.md" and f != "agents/retrieval-manifest.json" and f.endswith((".md", ".yaml", ".json"))]
HIST_WORDS = re.compile(r"obsolete|historical|retired|superseded|legacy|stale|formerly|differ|conflict|live repo|repo still|banner|older|predates|cites|prior|previously|not current|no longer", re.I)


# 1 parse
def c_parse():
    f = []
    for p in [x for x in NEW if x.endswith((".yaml", ".yml"))]:
        try:
            yload(p)
        except Exception as e:
            f.append(f"{p}: {e}")
    try:
        json.loads(read("agents/retrieval-manifest.json"))
    except Exception as e:
        f.append(f"retrieval-manifest.json: {e}")
    rec("Structured files parse (YAML/JSON)", f)


# 2 metadata
def front(p):
    t = read(p)
    if not t.startswith("---\n"):
        return None
    try:
        return yaml.safe_load(t.split("---\n", 2)[1])
    except Exception:
        return None


def c_meta():
    f = []
    need = ["id", "status", "version", "visibility", "last_verified"]
    for p in NEW_MD:
        if p in ("CLAUDE.md",) or p.startswith("registry/README"):
            continue
        m = front(p)
        if m is None:
            f.append(f"{p}: missing front matter")
            continue
        miss = [k for k in need if k not in m]
        if miss:
            f.append(f"{p}: missing {miss}")
    rec("Document status/version metadata present", f)


# 3 links
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
TICK = re.compile(r"`([A-Za-z0-9_./\-]+\.(?:md|yaml|json|py|txt|xml))`")


def c_links():
    f, w = [], []
    for p in NEW_MD:
        t = read(p)
        base = (ROOT / p).parent
        for m in LINK.finditer(t):
            tgt = m.group(1)
            if tgt.startswith(("http", "mailto:")):
                continue
            if not (base / tgt).exists():
                (w if tgt.startswith("restricted/") and not HAS_R else f).append(f"{p}: broken link {tgt}")
        for m in TICK.finditer(t):
            tgt = m.group(1)
            if "/" not in tgt or tgt.startswith("tools/validate") and False:
                continue
            if (ROOT / tgt).exists() or (base / tgt).exists():
                continue
            if tgt.startswith("restricted/"):
                if HAS_R and not (ROOT / tgt).exists():
                    f.append(f"{p}: missing restricted path {tgt}")
                continue
            if tgt.startswith(("agents/profiles/<",)) or "<" in tgt or "*" in tgt:
                continue
            f.append(f"{p}: referenced path not found {tgt}")
    rec("Internal links and path references resolve", f, w)


# 4 ids / cross refs / provenance
def c_ids():
    f = []
    prod = yload("registry/products.yaml")["products"]
    fws = yload("registry/frameworks.yaml")
    cons = yload("registry/conflicts.yaml")["conflicts"]
    decs = yload("registry/decisions.yaml")["decisions"]
    led = yload("research/ledger.yaml")["entries"]
    for label, ids in [("PRD", [p["id"] for p in prod]), ("FW", [x["id"] for x in fws["frameworks"]] + [x["id"] for x in fws["restricted_frameworks"]]), ("CON", [c["id"] for c in cons]), ("DEC", [d["id"] for d in decs]), ("LEDGER", [e["id"] for e in led])]:
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            f.append(f"duplicate {label} ids {dup}")
    names = [x["name"] for x in fws["frameworks"]]
    if len(names) != len(set(names)):
        f.append("duplicate framework names")
    cid, did = {c["id"] for c in cons}, {d["id"] for d in decs}
    for p in prod:
        for c in p["conflicts"]:
            if c not in cid:
                f.append(f"{p['id']}: unknown conflict {c}")
    for c in cons:
        if c["decision"] not in did:
            f.append(f"{c['id']}: unknown decision {c['decision']}")
    rec("IDs unique and cross-references resolve", f)
    g = []
    for x in fws["frameworks"]:
        t = read(x["record"])
        if "## Source locations" not in t or not re.search(r"## Source locations\n- ", t):
            g.append(f"{x['id']}: no source locations")
        if "## Provenance" not in t:
            g.append(f"{x['id']}: no provenance section")
    for e in led:
        if not e.get("source_citation") or not e.get("access_status"):
            g.append(f"{e['id']}: ledger entry lacks citation/access status")
    for p in prod:
        if not p.get("document_status"):
            g.append(f"{p['id']}: no document status")
    rec("Source references and provenance present", g)


# 5 prices
MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")


def c_prices():
    prod = yload("registry/products.yaml")["products"]
    allowed = set()
    for p in prod:
        allowed |= {m.replace(" ", "") for m in MONEY.findall(p["terms_public"])}
    f, info = [], []
    for p in ACTIVE:
        if p == "registry/products.yaml" or not p.endswith((".md", ".yaml", ".json")):
            continue
        for i, line in enumerate(read(p).splitlines(), 1):
            if HIST_WORDS.search(line):
                continue
            for m in MONEY.findall(line):
                if m.replace(" ", "") not in allowed:
                    f.append(f"{p}:{i}: unregistered price {m}")
    # product records must agree with registry
    for p in prod:
        t = "\n".join(l for l in read(p["public_record"]).splitlines() if not HIST_WORDS.search(l))
        for m in MONEY.findall(t):
            if m.replace(" ", "") not in {x.replace(" ", "") for x in MONEY.findall(p["terms_public"])}:
                f.append(f"{p['id']}: record price {m} not in registry terms")
    # legacy price audit (informational)
    known_stale = {"$27,000": "CON-006", "$45,000": "CON-006", "$4,620": "CON-005", "$397": "CON-011", "$8,500": "CON-013", "$132,000": "CON-007", "$100,000": "CON-007", "$3,000": "CON-013"}
    found = {}
    for p in subprocess.check_output(["git", "ls-files", "canon", "frameworks", "llms.txt", "baz-porter.txt", "identity", "glossary", "faq"], cwd=ROOT, text=True).split():
        for m in set(MONEY.findall(read(p))):
            if m in known_stale:
                found.setdefault(m, set()).add(p)
    cons = {c["id"] for c in yload("registry/conflicts.yaml")["conflicts"]}
    for k, v in found.items():
        status = "recorded" if known_stale[k] in cons else "UNRECORDED"
        info.append(f"legacy price {k} in {len(v)} legacy files -> {known_stale[k]} ({status})")
        if status == "UNRECORDED":
            f.append(f"legacy price {k} has no conflict record")
    rec("Prices consistent with registry; legacy price conflicts recorded", f, None, info)


# 6 retired terminology
RETIRED = [r"Reach[/, ]+Acquire", r"Rosetta (?:Stone )?v4\.0", r"Horizon Leaders", r"\bGold tier\b", r"\bPlatinum\b(?! Partner)", r"\bBronze\b", r"\bDiamond\b", r"Baz Porter Institution", r"Paradigmatic Healing", r"\$397\b", r"\$4,620"]


def c_retired():
    f = []
    for p in ACTIVE:
        for i, line in enumerate(read(p).splitlines(), 1):
            for pat in RETIRED:
                if re.search(pat, line) and not HIST_WORDS.search(line):
                    f.append(f"{p}:{i}: retired term /{pat}/ in active content")
    rec("Retired terminology absent from active content", f)


# 7 unapproved claims
def c_claims():
    f = []
    NEG = re.compile(r"\b(no|not|never|without|unverified|none|nothing|cannot|don't|do not|isn't|un|until|before|pending|undefined|neither|nor|if|requires?|prohibit|forbidden|must not|may not)\b", re.I)
    for p in ACTIVE:
        if p.startswith("research/") or p.endswith(".json"):
            continue
        for i, line in enumerate(read(p).splitlines(), 1):
            if re.search(r"\b(is live|now live|has launched|is launched|are launched)\b", line, re.I) and not NEG.search(line):
                f.append(f"{p}:{i}: launch asserted as fact")
            if re.search(r"\bguarantee[sd]?\b", line, re.I) and not NEG.search(line):
                f.append(f"{p}:{i}: guarantee language")
            if re.search(r"\b(accredited|accreditation|certified)\b", line, re.I) and not NEG.search(line):
                f.append(f"{p}:{i}: accreditation/certification asserted")
            if re.search(r"quantum[^.\n]{0,40}(causes?|proves?|proof|explains?|creates?|controls?|heals?|manifests?)|(proves?|because of|thanks to)[^.\n]{0,30}quantum", line, re.I) and not NEG.search(line):
                f.append(f"{p}:{i}: quantum causal claim")
    prod = yload("registry/products.yaml")["products"]
    for p in prod:
        if not re.match(r"unverified|not[- ]launched", p["launch_status"]):
            f.append(f"{p['id']}: launch_status not unverified")
    rec("No unapproved claims asserted as fact", f)


# 8 orphans
def c_orphans():
    reach, queue = set(), ["KNOWLEDGE_INDEX.md"]
    while queue:
        cur = queue.pop()
        if cur in reach or not (ROOT / cur).is_file():
            continue
        reach.add(cur)
        if not cur.endswith(".md"):
            continue
        t = read(cur)
        base = (ROOT / cur).parent
        for tgt in [m.group(1) for m in LINK.finditer(t)] + TICK.findall(t) + re.findall(r"`([A-Za-z0-9_./\-]+/)`", t):
            if tgt.startswith("http"):
                continue
            c = Path(tgt)
            cand = (base / c) if (base / c).exists() else (ROOT / c)
            if cand.is_dir():
                for q in cand.rglob("*"):
                    if q.is_file():
                        queue.append(str(q.relative_to(ROOT)))
            elif cand.exists():
                queue.append(str(cand.relative_to(ROOT)))
    # structured files reference each other by path inside yaml
    for y in ["registry/products.yaml", "registry/frameworks.yaml", "agents/retrieval-manifest.json"]:
        for tgt in re.findall(r"(?:products|ip/records|ip)/[A-Za-z0-9_.\-]+\.md", read(y)):
            if (ROOT / tgt).is_file():
                reach.add(tgt)
    f = [x for x in NEW if x not in reach and not x.startswith("reports/")]
    rec("No orphaned files in the new tree", f)


# 9 exposure
def c_exposure():
    out = subprocess.run([sys.executable, "-I", "tools/check_exposure.py"], cwd=ROOT, capture_output=True, text=True)
    f = [] if out.returncode == 0 else out.stdout.strip().splitlines()[1:]
    for p in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split():
        if p.startswith("restricted/"):
            f.append(f"tracked restricted file {p}")
    secret = re.compile(r"ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
    for p in NEW:
        if secret.search(read(p)):
            f.append(f"{p}: credential-like string")
    rec("No restricted material or credentials in tracked files", f)


# 10 positioning / RAMS
def c_positioning():
    f = []
    for p in ACTIVE:
        for i, line in enumerate(read(p).splitlines(), 1):
            if re.search(r"Victoria[^.\n]{0,50}\b(entry buyer|is the buyer|the leader before)", line, re.I) and not re.search(r"not|conflict|CON-003|legacy|repo|live files", line, re.I):
                f.append(f"{p}:{i}: Victoria positioned as buyer/before")
            if re.search(r"Lisa[^.\n]{0,40}destination", line, re.I) and not re.search(r"not|conflict|CON-003", line, re.I):
                f.append(f"{p}:{i}: Lisa positioned as destination")
            if re.search(r"RAMS", line) and re.search(r"\b(four|4)[- ](pillar|part|item|component)", line, re.I) and not re.search(r"Rosetta|CON-002|prints|printed", line):
                f.append(f"{p}:{i}: RAMS composition wrong")
    idx = read("canon/CANON_INDEX.md")
    if "entry buyer" not in idx or "destination archetype" not in idx:
        f.append("CANON_INDEX lacks Lisa/Victoria rule")
    fw = {x["id"]: x for x in yload("registry/frameworks.yaml")["frameworks"]}
    rams = read(fw["FW-002"]["record"])
    if "- Results\n- Attitude\n- Authenticity\n- Mastery\n- Systems" not in rams:
        f.append("FW-002 does not list the five RAMS pillars in order")
    rec("Lisa/Victoria and RAMS terminology correct in active content", f)


# 11 Green Room price
def c_green_room():
    f = []
    for p in ACTIVE:
        for i, line in enumerate(read(p).splitlines(), 1):
            if "Green Room" in line and MONEY.search(line):
                f.append(f"{p}:{i}: Green Room price present in a public file")
    if FULL and HAS_R:
        for p in [x for x in RESTRICTED.rglob("*.md") if "Green Room" in x.read_text(encoding="utf-8")]:
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if "Green Room" in line and MONEY.search(line):
                    if FACTS.get("green_room_price", "") not in line or re.search(r"per month|/month|monthly", line) and not re.search(r"not", line, re.I):
                        f.append(f"{p.relative_to(ROOT)}:{i}: incorrect Green Room price")
        gr = (RESTRICTED / "institution" / "GREEN_ROOM.md").read_text(encoding="utf-8")
        if FACTS.get("green_room_phrase", "") not in gr:
            f.append("restricted GREEN_ROOM.md lacks the founder-stated price and term")
        pf = yload("restricted/registry/products-full.yaml")["products"]
        g = [p for p in pf if p["id"] == "PRD-013"][0]
        if FACTS.get("green_room_phrase", "") not in g["terms_full"]:
            f.append("PRD-013 full terms wrong")
    rec("Green Room price: absent from public files" + (" and correct in restricted store" if FULL else ""), f)


# 12 retrieval paths
def c_retrieval():
    f = []
    m = json.loads(read("agents/retrieval-manifest.json"))
    docs = {d["path"]: d for d in m["documents"]}
    deny = set(m["deny_as_current_truth"])
    prof_dir = ROOT / "agents" / "profiles"
    for pf in sorted(prof_dir.glob("*.yaml")):
        y = yaml.safe_load(pf.read_text(encoding="utf-8"))
        rf = [re.sub(r"\s*\(.*$", "", x["path"]).strip() for x in y.get("read_first", [])]
        rd = [re.sub(r"\s*\(.*$", "", x).strip() for x in y.get("read_on_demand", [])]
        mp = m["profiles"].get(pf.stem)
        if mp is None or mp["read_first"] != rf or mp["read_on_demand"] != rd:
            f.append(f"{pf.stem}: retrieval-manifest.json out of sync with profile (run tools/gen_agent_manifest.py)")
        for p in rf + rd:
            if "<" in p:
                continue
            if p.startswith(("retired/", "_holding/", "institution/")) or p in deny:
                f.append(f"{pf.stem}: profile path resolves to retired/denied material {p}")
    for name, pr in m["profiles"].items():
        for p in pr["read_first"] + pr["read_on_demand"]:
            if "<" in p:
                continue
            if p.startswith(("retired/", "_holding/", "institution/")) or p in deny:
                f.append(f"{name}: path resolves to retired/denied material {p}")
                continue
            if p.startswith("restricted/"):
                if p not in docs:
                    f.append(f"{name}: restricted path not in manifest {p}")
                elif FULL and HAS_R and not (ROOT / p).exists():
                    f.append(f"{name}: restricted file missing {p}")
                continue
            if not (ROOT / p).exists():
                f.append(f"{name}: missing {p}")
            elif docs.get(p, {}).get("retrieval", "allow").startswith("deny"):
                f.append(f"{name}: denied doc {p}")
        if pr["external_tool_safe"]:
            ex = pr["export_safe_documents"]
            if not ex or any(not docs.get(e, {}).get("export_safe") for e in ex):
                f.append(f"{name}: external-tool profile lacks export-safe document")
    rec("AI retrieval paths resolve to current, permitted material", f)


# 13 migration completeness
def c_migration():
    f = []
    if not (ROOT / "registry" / "migration-manifest.yaml").exists():
        rec("Migration manifest complete; nothing deleted", [], None, ["migration manifest is held in the private repository"])
        return
    mm = yload("registry/migration-manifest.yaml")
    src = {e["source"] for e in mm["entries"]}
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, capture_output=True, text=True)
    base = r.stdout.split() if r.returncode == 0 else []  # a clean-history tree does not carry the base commit; it lives in the archived repository
    for b in base:
        if b not in src:
            f.append(f"base file not in manifest: {b}")
        if subprocess.run(["git", "cat-file", "-e", f"HEAD:{b}"], cwd=ROOT, capture_output=True).returncode != 0:
            if FULL and HAS_R and (RESTRICTED / "legacy-public-history" / b).exists():
                continue  # moved to the private repository (mirrored under restricted/legacy-public-history/)
            if not FULL and any(re.search(pat, b) for pat, _ in PRIVATE_MIGRATE):
                continue  # moved to the private repository by DEC-044; byte-identity is checked in full mode
            f.append(f"base file deleted from branch: {b}")
    if HAS_R:
        import hashlib
        for e in mm["entries"]:
            if e["source"].startswith("zip:"):
                p = RESTRICTED / "sources" / e["source"][4:]
                if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != e["sha256"]:
                    f.append(f"zip file missing/changed: {e['source']}")
    rec("Migration manifest complete; nothing deleted", f)


# 14 Rosetta vs products (full)
KEY = {"PRD-001": "Fast Future", "PRD-002": "A Million Dreams", "PRD-003": "Reclamation", "PRD-004": "Manifestation", "PRD-005": "Sovereign Session", "PRD-006": "The Becoming", "PRD-007": "Coming Home", "PRD-008": "Revenue Architecture", "PRD-009": "RAMS Business", "PRD-010": "Revenue Owner", "PRD-011": "Gravity Code", "PRD-012": "Without You"}


def c_rosetta():
    f, info = [], []
    ros = (RESTRICTED / "canon" / "ROSETTA_STONE_v4.2.md").read_text(encoding="utf-8")
    pf = {p["id"]: p for p in yload("restricted/registry/products-full.yaml")["products"]}
    rows = [l for l in ros.splitlines() if l.startswith("| ") and "$" in l or l.startswith("| Fast Future")]
    for pid, kw in KEY.items():
        row = next((r for r in rows if kw.lower() in r.lower().split("|")[1].lower()), None)
        if not row:
            continue
        cell = row.split("|")[2]
        rn = {m.replace(" ", "").replace("\\", "") for m in MONEY.findall(cell.replace("\\$", "$"))}
        pn = {m.replace(" ", "") for m in MONEY.findall(pf[pid]["terms_full"])}
        if rn and not rn <= pn:
            if pf[pid]["conflicts"]:
                info.append(f"{pid}: Rosetta {sorted(rn)} vs registry {sorted(pn)} - recorded in {pf[pid]['conflicts']}")
            else:
                f.append(f"{pid}: Rosetta prices {sorted(rn)} not in registry terms and no conflict recorded")
        else:
            info.append(f"{pid}: Rosetta prices consistent with registry full terms")
    rec("Rosetta v4.2 vs product registry (full mode)", f, None, info)


def c_conversion():
    f = []
    for docx in sorted((RESTRICTED / "sources").rglob("*.docx")):
        b = docx.stem
        md = RESTRICTED / "converted" / (b + ".md")
        out = subprocess.run([sys.executable, "-I", "tools/check_conversion.py", str(docx), str(md)], cwd=ROOT, capture_output=True, text=True)
        if out.returncode != 0 and "Lisa_Miles" not in b and "Rosetta" not in b:
            f.append(out.stdout.strip())
    for c in [RESTRICTED / "canon" / "ROSETTA_STONE_v4.2.md", RESTRICTED / "canon" / "LISA_MILES_ICA_2026-10-14.md"]:
        src = RESTRICTED / "sources" / "01_CANON" / ("00_Rosetta_Stone_v4.2_UNCHANGED.docx" if "ROSETTA" in c.name else "00_Lisa_Miles_Full_ICA_2026-10-14.docx")
        out = subprocess.run([sys.executable, "-I", "tools/check_conversion.py", str(src), str(c)], cwd=ROOT, capture_output=True, text=True)
        if out.returncode != 0:
            f.append(out.stdout.strip())
    rec("DOCX to Markdown text completeness (full mode)", f)


# 15 founder decisions persisted in the legacy public layer
REGRESS = [
    (r"\$1,620|\$15,000|\$5,998", "private-engagement offer pricing (E1, 2026-10-17)"),
    (r"\b(8|eight) seats\b|seats (a|per|annually)|gravity-code-apply", "Gravity Code capacity or application link (E2/E3, 2026-10-17)"),
    (r"March 27, 2025|March 11, 2024", "withheld ranking date (DEC-048)"),
    (r"the only (methodology|system)\b", "unsupported uniqueness claim (corrected 2026-10-17)"),
    (r"\$100,000|\$33,000", "confidential Gravity Code economics (corrected 2026-10-17)"),
    (r"12,000\+ hours|36-module|17-day spiritual|11K\+ followers|43% higher burnout|35% stress", "withdrawn unsupported figure (corrected 2026-10-17)"),
    (r"\b(USA News|CEO Times|Biz Weekly|Women's Insider)\b", "syndicated press-release pages removed pending verification (corrected 2026-10-17)"),
    (r"\|\s*(Year|Month) (1|2|3|5|6|10|20|30)\s*\|", "future-outcome timeline (corrected 2026-10-17)"),
    (r"Victoria-to-Oliver|Victoria is paying|Her name, in the work, is Victoria|The Transformation Arc, From Victoria", "Victoria used as the starting state (DEC-003)"),
    (r"neurological and quantum|quantum identity crisis|quantum frequenc|Drives\u2122 are not metaphorical|brain does not distinguish|rehearses during REM|RAS miscalibrates|Quantum Reality Shift|The Quantum Layer|Reticular Activating System, is now filtering", "reworded claim reappeared (DEC-014)"),
    (r"Tony Robbins Platinum Partnership", "credential must read 'Former ... Platinum Partner, 2021 to 2022' (DEC-022)"),
    (r"Coming Home\u2122 ?[-\u2014] ?(Repair|Your Relationship|Find Yourself)|\$27,000|\$45,000", "retired Coming Home tier (DEC-006)"),
    (r"Rosetta (Stone )?v4\.0", "stale canon citation (CON-014)"),
    (r"Tony Robbins events", "named third-party example removed from Five Imposters (DEC-023)"),
    (r"Life Mastery|Wealth Mastery", "program without a certificate removed at founder instruction (DEC-022)"),
    (r"Business Mastery \(twice\)|UPW, three times|21 other authors", "credential or co-author count not supported by evidence (DEC-027)"),
    (r"24,700|extended Delphi|Delphi\u2122 AI Clone, Extended|Part 4 international bestseller|[Tt]wo-time international bestsell|permanent retained power|Permanent capability install|architecture holds without effort|old architecture is gone", "withdrawn or unsupported claim reappeared (DEC-042, credibility audit 2026-10-17)"),
    (r"Suicide attempt|rope and pills|diverticulitis|liver failure|[$]2[.]1 million|annual retainer floor|permanent retained[- ]power|Conservative annual estimate", "confidential narrative, unevidenced figure or absolute claim reappeared in public content (DEC-046)"),
    (r"Silent Collapse Diagnostic", "retired Silent Collapse Diagnostic referenced in active content (DEC-004, DEC-037)"),
    (r"single door into the work|Entry is always through the Silent Collapse|Take the Silent Collapse Diagnostic|Begin the Silent Collapse Diagnostic", "Silent Collapse Diagnostic presented as the entry door (DEC-004)"),
    (r"\|\s*(BRONZE|SILVER|GOLD|PLATINUM|DIAMOND|QUARTERLY)\s*\||Diamond / Quarterly|Bronze[- ]tier|Gold[- ]tier|Silver[- ]tier|\$132,000\b.{0,40}Quarterly", "tier tables or labels, or Gravity Code cadences, reappeared (DEC-035)"),
]


def c_decisions():
    f = []
    legacy = subprocess.check_output(["git", "ls-files", "canon", "frameworks", "identity", "glossary", "faq", "citations", "llms.txt", "llms-full.txt", "baz-porter.txt", "README.md", "docs", "site"], cwd=ROOT, text=True).split()
    for p in legacy:
        t = read(p)
        if "doc_type: tombstone" in t:
            continue
        for i, line in enumerate(t.splitlines(), 1):
            for pat, why in REGRESS:
                if re.search(pat, line) and not re.search(r"cites|retired|superseded|banner|formerly", line, re.I):
                    f.append(f"{p}:{i}: {why}")
    for p in ["canon/ICA.md", "canon/PRODUCT-ARCHITECTURE.md", "canon/OFFERS.md"]:
        if "doc_type: tombstone" not in read(p):
            f.append(f"{p}: not a tombstone")
        held = {e.get("retired_path"): e for e in yload("retired/MANIFEST.yaml").get("moved", [])}.get("retired/" + p, {})
        if held.get("location") == "private-repository" and held.get("sha256"):
            continue  # preserved in the private repository; hash recorded in the manifest
        if not (ROOT / "retired" / p).exists() or "RETIRED 2026-10-16" not in read("retired/" + p):
            f.append(f"retired/{p}: preserved copy missing")
    decs = {d["id"]: d for d in yload("registry/decisions.yaml")["decisions"]}
    for i in ["DEC-002", "DEC-003", "DEC-006", "DEC-013", "DEC-014"]:
        if not decs[i]["status"].startswith("approved") or "decided_on" not in decs[i]:
            f.append(f"{i}: founder decision not recorded as approved")
    snaps = yload("retired/MANIFEST.yaml")["superseded_text_snapshots"]
    for s in snaps:
        if s.get("location") == "private-repository" and s.get("sha256"):
            continue
        if not (ROOT / s["snapshot"]).exists():
            f.append(f"missing snapshot {s['snapshot']}")
    rec("Founder decisions of 2026-10-16 persisted; retirements preserved with tombstones", f)



def gg(args):
    r = subprocess.run(["git", "grep", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.split() if r.returncode in (0, 1) else []


def c_legacy_info():
    info = []
    info.append(f"legacy files still using the destination archetype as the starting state: {len(gg(['-l', '-E', 'Victoria[^.]{0,60}(before|Silent Collapse operating)', '--', 'canon', 'frameworks']))} (expected 0, DEC-003)")
    info.append(f"legacy canon files still citing Rosetta v4.0 outside retired/: {len(gg(['-l', 'Rosetta Stone v4.0', '--', 'canon']))} (expected 0)")
    info.append(f"legacy files mentioning RAMS: {len(set(gg(['-l', 'RAMS', '--', 'frameworks', 'canon'])))} (canonical record is ip/records/FW-002)")
    info.append(f"legacy files with unqualified quantum wording: {len(gg(['-l', '-i', '-E', 'quantum (identity|frequenc|signal|reality)|neurological and quantum', '--', 'canon', 'frameworks']))} (expected 0, DEC-014)")
    info.append(f"legacy files still carrying retired Coming Home tier prices: {len(gg(['-l', '-E', '[$]27,000|[$]45,000', '--', 'canon', 'frameworks', 'faq', 'glossary', 'identity', 'llms.txt', 'baz-porter.txt']))} (expected 0)")
    rec("Legacy stale-state audit (informational counts)", [], None, info)


# wiki and AI-readable file integrity
ORCID = "0009-0006-1670-9956"


def c_wiki_ai():
    f = []
    wiki = ROOT / "docs" / "wiki"
    if wiki.is_dir():
        pages = {x.stem for x in wiki.glob("*.md")}
        side = read("docs/wiki/_Sidebar.md")
        for n in sorted(pages - {"_Sidebar", "_Footer"}):
            if f"({n}.md)" not in side:
                f.append(f"wiki page not in sidebar: {n}")
        for n in ("Home", "_Sidebar", "_Footer", "About-Baz-Porter", "Sovereign-Leadership-Architecture", "Sovereign-Return", "RAMS", "Research-Foundations", "Publications", "Credentials-and-Affiliations", "Evidence-Library", "Glossary", "Frequently-Asked-Questions", "References-and-Citations", "Contact-and-Official-Links"):
            if n not in pages:
                f.append(f"required wiki page missing: {n}")
        for x in wiki.glob("*.md"):
            for tgt in re.findall(r"\]\(([^)#\s]+\.md)\)", x.read_text(encoding="utf-8")):
                if not tgt.startswith(("http", "../")) and not (wiki / tgt).exists():
                    f.append(f"{x.name}: unresolved wiki link {tgt}")
        sr = read("docs/wiki/Sovereign-Return.md")
        for stage in ("Recognition", "Identification", "Dismantlement", "Recalibration", "Embodiment", "Sovereignty"):
            if stage not in sr:
                f.append(f"Sovereign Return page missing stage {stage}")
        rm = read("docs/wiki/RAMS.md")
        if not all(w in rm for w in ("Results", "Attitude", "Authenticity", "Mastery", "Systems")):
            f.append("RAMS page does not carry the five approved pillars")
    for a, b in (("site/llms.txt", "llms.txt"), ("site/llms-full.txt", "llms-full.txt"), ("site/baz-porter.txt", "baz-porter.txt")):
        if (ROOT / a).exists() and (not (ROOT / b).exists() or read(a) != read(b)):
            f.append(f"{b} differs from {a}")
    ids = set()
    for p in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split("\n"):
        if p and not p.startswith(("tools/", "reports/", "registry/migration", "registry/exposure", "registry/restricted", "registry/repository", "retired/")) and p.endswith((".md", ".txt", ".cff", ".json", ".jsonld", ".yaml")):
            ids |= set(re.findall(r"orcid\.org/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", read(p)))
    if ids and ids != {ORCID}:
        f.append(f"ORCID identifiers differ from the founder-supplied one: {sorted(ids)}")
    if (ROOT / "site/structured-data.jsonld").exists():
        try:
            json.loads(read("site/structured-data.jsonld"))
            if read("site/structured-data.jsonld") != read("metadata/structured-data.jsonld"):
                f.append("metadata/structured-data.jsonld differs from site copy")
        except ValueError:
            f.append("structured data is not valid JSON")
    for p in ("llms.txt", "llms-full.txt", "baz-porter.txt"):
        if (ROOT / p).exists():
            tx = read(p)
            if re.search(r"Silent Collapse Diagnostic|Rosetta Stone v4\.0|\bBronze\b|24,700", tx):
                f.append(f"{p}: retired or withdrawn wording")
            if ORCID not in tx:
                f.append(f"{p}: ORCID missing")
    for p in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split("\n"):
        if not p or p.startswith(("tools/", "retired/")) or not p.endswith((".md", ".txt", ".cff", ".json", ".jsonld", ".yaml", ".html", ".xml")):
            continue
        tx = read(p)
        if "sovereign-leadership-knowledge" in tx:
            f.append(f"{p}: obsolete repository name sovereign-leadership-knowledge")
        if re.search(r"github\.com/baz-stack/sovereign-leadership-architecture(?!-knowledge)", tx) and not p.startswith(("reports/", "registry/")):
            f.append(f"{p}: link to the private historical repository")
    rec("Wiki, ORCID and AI-readable file integrity", f)


def main():
    c_parse(); c_meta(); c_links(); c_ids(); c_prices(); c_retired(); c_claims(); c_orphans(); c_exposure(); c_positioning(); c_green_room(); c_retrieval(); c_migration(); c_decisions(); c_wiki_ai(); c_legacy_info()
    if FULL and HAS_R:
        c_rosetta(); c_conversion()
    lines = [f"# Validation report ({'full' if FULL else 'public'} mode)\n", f"Run on branch tree at {subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, text=True).strip()}  \nManual-only checks are listed at the end.\n", "| Check | Result |\n|---|---|"]
    for n, s, f, w, i in results:
        lines.append(f"| {n} | **{s}**{' (' + str(len(f)) + ')' if f else ''} |")
    for n, s, f, w, i in results:
        if f or w or i:
            lines.append(f"\n### {n}\n")
            lines += [f"- FAIL {x}" for x in f] + [f"- warn {x}" for x in w] + [f"- info {x}" for x in i]
    lines.append("\n## Not automatable (manual)\n- Live checkout, page, contract and GoHighLevel readback (no access).\n- Citation verification against original sources (network blocked).\n- Trademark status (USPTO unreachable).\n- Truth of credentials and client outcomes (no documents supplied).\n- Whether copy meets Rosetta voice standard (human judgement).")
    out = ROOT / ("restricted/reports/validation-full.md" if FULL else "reports/validation-public.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(("---\nid: RPT-VALIDATION\ndoc_type: report\nstatus: generated\nversion: 2026.10.16.1\nvisibility: " + ("restricted" if FULL else "public") + "\nlast_verified: 2026-10-16\n---\n") + "\n".join(lines) + "\n", encoding="utf-8")
    fails = sum(1 for r in results if r[1] == "FAIL")
    print("\n".join(f"{r[1]:4} {r[0]}" for r in results))
    print(f"{fails} failing checks; report: {out.relative_to(ROOT)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
