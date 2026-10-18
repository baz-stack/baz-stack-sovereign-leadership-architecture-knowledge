#!/usr/bin/env python3
"""Mutation tests: inject one known defect into a throwaway copy of the repo and assert the matching check FAILS.
Usage: python3 -I tools/tests/test_validate.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(mut):
    tmp = Path(tempfile.mkdtemp(prefix="kos-test-"))
    dst = tmp / "repo"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("restricted", "__pycache__"), symlinks=True)
    mut(dst)
    out = subprocess.run([sys.executable, "-I", "tools/validate.py"], cwd=dst, capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return out.stdout


def append(path, text):
    return lambda d: (d / path).write_text((d / path).read_text(encoding="utf-8") + "\n" + text + "\n", encoding="utf-8")


def sub(path, a, b):
    def f(d):
        t = (d / path).read_text(encoding="utf-8")
        assert a in t, f"{a!r} not in {path}"
        (d / path).write_text(t.replace(a, b, 1), encoding="utf-8")
    return f


def newfile(path, text):
    def f(d):
        (d / path).parent.mkdir(parents=True, exist_ok=True)
        (d / path).write_text(text, encoding="utf-8")
    return f


def track_restricted(d):
    (d / "restricted").mkdir(exist_ok=True)
    (d / "restricted" / "leak.md").write_text("x", encoding="utf-8")
    subprocess.run(["git", "add", "-f", "restricted/leak.md"], cwd=d, check=True)


def delete_base(d):
    (d / "canon" / "BOOKS.md").unlink()
    subprocess.run(["git", "rm", "-q", "--cached", "canon/BOOKS.md"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "del"], cwd=d, check=True)


CASES = [
    ("price drift in a product record", append("products/PRD-006-the-becoming.md", "Investment: $1,999 per month."), "Prices consistent"),
    ("Victoria positioned as buyer", append("KNOWLEDGE_INDEX.md", "Victoria is the entry buyer of every campaign."), "Lisa/Victoria"),
    ("RAMS wrong composition", append("KNOWLEDGE_INDEX.md", "RAMS has four pillars."), "Lisa/Victoria"),
    ("Green Room wrong price in public file", append("operations/INSTITUTION_AND_OPERATIONS_STATUS.md", "The Green Room costs $1,234 per month."), "Green Room price"),
    ("retired term in active content", append("agents/RETRIEVAL_POLICY.md", "The source is Rosetta Stone v4.0."), "Retired terminology"),
    ("guarantee as fact", append("products/PRD-003-the-reclamation-code.md", "This course heals you and results are guaranteed."), "unapproved claims"),
    ("quantum causal claim", append("products/PRD-004-manifestation-that-finally-works.md", "Quantum entanglement proves the manifestation works."), "unapproved claims"),
    ("broken link", append("KNOWLEDGE_INDEX.md", "See [missing](products/NOPE.md)."), "links"),
    ("orphan file", newfile("products/ORPHAN.md", "---\nid: X\nstatus: current\nversion: 1\nvisibility: public\nlast_verified: 2026-10-16\n---\nlost\n"), "orphaned"),
    ("missing metadata", newfile("operations/NOMETA.md", "no front matter\n"), "metadata"),
    ("profile reads exposed institution folder", sub("agents/profiles/research.yaml", "research/README.md", "institution/VISION.md"), "retrieval paths"),
    ("restricted file tracked", track_restricted, "restricted material"),
    ("base file deleted", delete_base, "Migration manifest"),
    ("product marked live", sub("registry/products.yaml", "unverified (no live readback performed)", "live", ), "unapproved claims"),
    ("quantum claim reappears in legacy layer", append("frameworks/silent-collapse.md", "Silent Collapse is a quantum identity crisis."), "Founder decisions"),
    ("Victoria as starting state reappears", append("canon/FRAMEWORKS.md", "The Victoria-to-Oliver Bridge is the arc."), "Founder decisions"),
    ("retired Coming Home tier reappears", append("frameworks/the-becoming.md", "| REPAIR | Coming Home\u2122 - Repair | $27,000 |"), "Founder decisions"),
    ("Robbins credential regresses", append("canon/PROFILE.md", "Tony Robbins Platinum Partnership"), "Founder decisions"),
    ("tombstone replaced by live file", sub("canon/OFFERS.md", "doc_type: tombstone", "doc_type: canon"), "Founder decisions"),
    ("Robbins example reappears in Five Imposters", append("frameworks/five-imposters.md", "Where it shows up: Tony Robbins events."), "Founder decisions"),
    ("unsupported credential count reappears", append("canon/CREDIBILITY.md", "Business Mastery (twice)"), "Founder decisions"),
    ("removed program reappears", append("canon/CREDIBILITY.md", "Wealth Mastery"), "Founder decisions"),
    ("Gravity Code economics reappear", append("frameworks/the-gravity-code.md", "Investment: $100,000 paid in full."), "Founder decisions"),
    ("uniqueness claim reappears", append("canon/PROFILE.md", "It is the only methodology of its kind."), "Founder decisions"),
    ("future-outcome timeline reappears", append("frameworks/the-gravity-code.md", "| Year 3 | Thirty days fully off. |"), "Founder decisions"),
    ("ORCID drift", append("docs/wiki/Home.md", "ORCID https://orcid.org/0000-0000-0000-0001"), "ORCID"),
    ("obsolete repository name", append("llms.txt", "https://github.com/baz-stack/sovereign-leadership-knowledge"), "AI-readable"),
    ("withheld ranking date appears", append("canon/CREDIBILITY.md", "Ranked on March 27, 2025."), "Founder decisions"),
    ("private-engagement price reappears", append("frameworks/the-becoming.md", "Investment: $1,620/mo."), "Founder decisions"),
    ("Gravity Code seat count reappears", append("frameworks/the-gravity-code.md", "There are eight seats a year."), "Founder decisions"),
    ("duplicate id", append("registry/products.yaml", ""), None),
]


def main():
    bad = 0
    has_base = subprocess.run(["git", "cat-file", "-e", "358a85777ca7a5ed47fc5115b379791f4b08c35a"], cwd=ROOT, capture_output=True).returncode == 0
    for name, mut, check in CASES:
        if check is None or (name == "base file deleted" and not has_base):
            continue  # a clean-history tree has no base commit to delete files from
        out = run(mut)
        failed = [l for l in out.splitlines() if l.startswith("FAIL")]
        hit = any(check.lower() in l.lower() for l in failed)
        print(("ok   " if hit else "MISS ") + name + ("" if hit else f"  (failed checks: {failed})"))
        bad += 0 if hit else 1
    # control: pristine copy must pass
    out = run(lambda d: None)
    ok = "0 failing checks" in out
    print(("ok   " if ok else "MISS ") + "control: unmodified tree passes")
    bad += 0 if ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
