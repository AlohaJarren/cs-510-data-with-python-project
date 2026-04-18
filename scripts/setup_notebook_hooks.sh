#!/usr/bin/env bash
# One-time setup per clone: dev dependencies, nbstripout Git filters, pre-commit hooks.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f "$ROOT/requirements-dev.txt" ]]; then
  echo "setup_notebook_hooks: missing requirements-dev.txt at $ROOT" >&2
  exit 1
fi

echo "Installing Python dev dependencies..."
python3 -m pip install -r "$ROOT/requirements-dev.txt"

echo "Installing nbstripout Git filters for this repository..."
# Registers filter.nbstripout.* and diff.ipynb in .git/config; uses committed .gitattributes
python3 -m nbstripout --install --attributes .gitattributes

echo "Installing pre-commit hooks (commit + pre-push)..."
python3 -m pre_commit install
python3 -m pre_commit install --hook-type pre-push

echo "Done. Notebook outputs are stripped on add/commit; validation runs on commit/push."
