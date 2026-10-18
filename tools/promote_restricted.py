#!/usr/bin/env python3
"""Copy the restricted store into a PRIVATE repository checkout after DEC-001 is settled.
Refuses to run if the target is the public working tree or looks public.
Usage: python3 -I tools/promote_restricted.py /path/to/private-repo-checkout"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    dst = Path(sys.argv[1]).resolve()
    if dst == ROOT or ROOT in dst.parents:
        print("Refusing: target is inside the public working tree.")
        return 1
    if not (dst / ".git").exists():
        print("Refusing: target is not a git checkout.")
        return 1
    print("Confirm the target repository is PRIVATE on GitHub before pushing anything from it.")
    shutil.copytree(ROOT / "restricted", dst / "restricted-store", dirs_exist_ok=True)
    print(f"Copied restricted/ to {dst / 'restricted-store'}. Review, commit and push only to a private remote.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
