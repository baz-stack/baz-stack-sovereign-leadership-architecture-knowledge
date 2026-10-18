#!/usr/bin/env python3
"""Build the sanitized public tree with a clean single-commit history (nothing is pushed).

Usage: python3 -I tools/build_clean_public_tree.py <empty-target-directory>

Copies every tracked file except those classified private-migrate in registry/repository-classification.yaml,
marks the retired-file manifest entries for the excluded files as held in the private repository, then makes
one commit. The historical repository is preserved privately; no history is rewritten here.
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent


def main():
    target = Path(sys.argv[1]).resolve()
    if target.exists() and any(target.iterdir()):
        sys.exit("target must be empty or absent")
    cls = yaml.safe_load((ROOT / "registry" / "repository-classification.yaml").read_text(encoding="utf-8"))
    mig = {r["path"] for r in cls["files"] if r["class"] == "private-migrate"}
    files = [f for f in subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).split("\n") if f]
    sha = {}
    for f in files:
        if f in mig:
            sha[f] = hashlib.sha256((ROOT / f).read_bytes()).hexdigest()
            continue
        (target / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, target / f)
    # References to files that now live only in the private repository become plain statements, not paths.
    for f in files:
        if f in mig or not (target / f).exists() or not f.endswith((".md", ".txt", ".cff")):
            continue
        if f.startswith("tools/") or f in ("retired/MANIFEST.yaml", "registry/repository-classification.yaml", "registry/migration-manifest.yaml"):
            continue  # manifests and tooling keep real paths
        t = (target / f).read_text(encoding="utf-8")
        o = t
        for pth in sorted(mig, key=len, reverse=True):
            base = pth.rsplit("/", 1)[-1]
            esc = re.escape(pth)
            t = re.sub(r"\[([^\]]*)\]\((?:\.\./|\./)*" + esc + r"\)", r"\1 (held in the private repository)", t)
            t = re.sub(r"`" + esc + r"`", f"{base} (held in the private repository)", t)
            t = re.sub(r"(?<![\w/.])" + esc + r"(?![\w])", f"{base} (held in the private repository)", t)
        if t != o:
            (target / f).write_text(t, encoding="utf-8")
    man = yaml.safe_load((target / "retired" / "MANIFEST.yaml").read_text(encoding="utf-8"))
    for key in ("moved", "superseded_text_snapshots"):
        for e in man.get(key, []):
            for field in ("retired_path", "snapshot"):
                p = e.get(field)
                if p in mig:
                    e["location"] = "private-repository"
                    e["sha256"] = sha[p]
    man["note"] = "Entries with location private-repository are held in the private repository at legacy-public-history/<path>; their SHA-256 is recorded here."
    (target / "retired" / "MANIFEST.yaml").write_text(yaml.safe_dump(man, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    subprocess.check_call(["git", "init", "-q", "-b", "main"], cwd=target)
    subprocess.check_call(["git", "add", "-A"], cwd=target)
    subprocess.check_call(["git", "-c", "user.name=Baz Porter LLC", "-c", "user.email=ask@bazporter.com", "commit", "-q", "-m", "Initial public release: sanitized tree with clean history"], cwd=target)
    print(f"built clean tree: {len(files) - len(mig)} files, {len(mig)} excluded, at {target}")


if __name__ == "__main__":
    main()
