#!/usr/bin/env python3
"""Fail if restricted material is tracked or staged in git.
Checks: (1) no path under restricted/ in the index; (2) .gitignore protects restricted/;
(3) generic classification markers absent from tracked new files; (4) if restricted/denylist.txt exists,
none of its tokens appear in files changed since the base commit.
Usage: python3 -I tools/check_exposure.py [--staged]"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "358a85777ca7a5ed47fc5115b379791f4b08c35a"
MARKERS = ["INTERNAL GOVERNING PORTFOLIO", "INTERNAL GOVERNING CANON", "CONFIDENTIAL •", "PRIVATE  •", "Source-controlled restoration of the 6 October"]


def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)


def main():
    problems = []
    tracked = git("ls-files").splitlines()
    for t in tracked:
        if t.startswith("restricted/"):
            problems.append(f"tracked restricted path: {t}")
    gi = (ROOT / ".gitignore").read_text()
    if "restricted/" not in gi.splitlines():
        problems.append(".gitignore does not protect restricted/")
    try:
        changed = set(git("diff", "--name-only", BASE).splitlines()) | set(git("ls-files", "--others", "--exclude-standard").splitlines()) | set(git("diff", "--cached", "--name-only").splitlines())
    except subprocess.CalledProcessError:
        changed = set(tracked)  # clean-history tree: no base commit, scan every tracked file
    deny = []
    dl = ROOT / "restricted" / "denylist.txt"
    if dl.exists():
        deny = [x.rstrip("\n") for x in dl.read_text(encoding="utf-8").splitlines() if x.strip()]
    for f in sorted(changed):
        p = ROOT / f
        if not p.is_file() or f.startswith("restricted/") or f.startswith("tools/"):
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        origin = f
        for pre in ("retired/superseded-text/", "retired/"):
            if f.startswith(pre):
                origin = f[len(pre):]
                break
        try:
            base_lines = set(git("show", f"{BASE}:{origin}").splitlines())
        except subprocess.CalledProcessError:
            base_lines = set()
        added = "\n".join(l for l in txt.splitlines() if l not in base_lines)
        for m in MARKERS:
            if m in added:
                problems.append(f"{f}: classification marker {m!r}")
        for d in deny:
            if d in added:
                problems.append(f"{f}: denylist token {d!r} in added text")
                break
    if problems:
        print("EXPOSURE CHECK FAILED")
        print("\n".join(" - " + x for x in problems))
        return 1
    print(f"exposure check passed ({len(changed)} changed files scanned, denylist {'loaded' if deny else 'absent'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
