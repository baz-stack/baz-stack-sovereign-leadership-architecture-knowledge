#!/bin/sh
# Install a pre-commit hook that blocks restricted material from public commits.
set -e
ROOT=$(git rev-parse --show-toplevel)
cat > "$ROOT/.git/hooks/pre-commit" <<'HOOK'
#!/bin/sh
python3 -I tools/check_exposure.py --staged || { echo "Commit blocked: restricted material detected."; exit 1; }
HOOK
chmod +x "$ROOT/.git/hooks/pre-commit"
echo "pre-commit exposure hook installed"
