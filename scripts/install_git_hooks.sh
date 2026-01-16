#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_DIR="$ROOT/.githooks"
GIT_HOOK_DIR="$ROOT/.git/hooks"

for hook in pre-commit post-commit prepare-commit-msg; do
  if [[ -f "$HOOK_DIR/$hook" ]]; then
    cp "$HOOK_DIR/$hook" "$GIT_HOOK_DIR/$hook"
    chmod +x "$GIT_HOOK_DIR/$hook"
  fi
done

echo "✅ Git hooks installed."
