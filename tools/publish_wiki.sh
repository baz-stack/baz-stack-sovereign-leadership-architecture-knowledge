#!/usr/bin/env bash
# Publish docs/wiki/ to the GitHub Wiki of the public knowledge repository.
# Prerequisites (owner actions): the wiki feature is enabled on the repository and its first page has been created once in the
# GitHub interface (GitHub creates the wiki git remote only then); the caller has push credentials for the repository.
# Usage: tools/publish_wiki.sh <owner/repo> [--dry-run]
# Nothing is pushed with --dry-run. The script only adds a commit to the wiki remote; it never force-pushes.
set -euo pipefail
REPO="${1:?usage: publish_wiki.sh owner/repo [--dry-run]}"
DRY="${2:-}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/docs/wiki"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
if [ "$DRY" != "--dry-run" ]; then
  git clone "https://github.com/${REPO}.wiki.git" "$WORK/wiki"
else
  mkdir -p "$WORK/wiki"
fi
for f in "$SRC"/*.md; do
  b="$(basename "$f")"
  # strip front matter; sibling links lose .md; ../../path links become repository blob URLs
  awk 'BEGIN{fm=0} NR==1&&/^---$/{fm=1;next} fm==1&&/^---$/{fm=0;next} fm==0{print}' "$f" \
    | sed -E "s#\]\(\.\./\.\./([^)]+)\)#](https://github.com/${REPO}/blob/main/\1)#g; s#\]\(([A-Za-z0-9_-]+)\.md\)#](\1)#g" > "$WORK/wiki/$b"
done
if [ "$DRY" = "--dry-run" ]; then
  echo "dry run: $(ls "$WORK/wiki" | wc -l) pages converted"; exit 0
fi
cd "$WORK/wiki"
git add -A
git -c user.name="Baz Porter LLC" -c user.email="ask@bazporter.com" commit -m "Publish knowledge base wiki from docs/wiki" || { echo "nothing to commit"; exit 0; }
git push origin HEAD
