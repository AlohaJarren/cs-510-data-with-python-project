#!/usr/bin/env python3
"""Validate Jupyter notebooks using nbformat (schema + structure)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat
from nbformat.reader import NotJSONError
from nbformat.validator import NotebookValidationError


def _iter_notebooks_from_args(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        path = Path(p)
        if not path.is_file():
            print(f"validate_notebooks: not a file: {path}", file=sys.stderr)
            sys.exit(1)
        if path.suffix.lower() == ".ipynb":
            out.append(path)
    return out


def _discover_notebooks(root: Path) -> list[Path]:
    skip_parts = {".git", ".ipynb_checkpoints", "node_modules", ".venv", "venv"}
    found: list[Path] = []
    for path in root.rglob("*.ipynb"):
        if any(part in skip_parts for part in path.parts):
            continue
        found.append(path)
    return sorted(found)


def validate_path(path: Path) -> None:
    with path.open(encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    nbformat.validate(nb)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Notebook paths (default: discover *.ipynb under current directory)",
    )
    args = parser.parse_args()

    if args.paths:
        notebooks = _iter_notebooks_from_args(args.paths)
    else:
        notebooks = _discover_notebooks(Path.cwd())

    if not notebooks:
        return 0

    failed = False
    for path in notebooks:
        try:
            validate_path(path)
        except (NotebookValidationError, NotJSONError, OSError, ValueError) as e:
            print(f"validate_notebooks: {path}: {e}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
