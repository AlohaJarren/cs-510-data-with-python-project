# Jupyter team workflow (proposal)

This document describes a shared workflow for collaborating on `.ipynb` files in Git. Treat it as a **team proposal**: the group can adopt, adjust, or revert the tooling in one PR.

## Why notebooks are awkward in groups (not GitHub-specific)

A Jupyter notebook is a **single JSON document**. Any tool that shares one file among several people—Git, branches, or exporting from Colab—runs into the same issues: **large diffs**, **merge conflicts**, and occasional **invalid JSON** if a merge or save goes wrong. Automation reduces noise and mistakes; it does **not** remove the need to coordinate when two people edit the same notebook at once.

## What we agreed

- **No GitHub Actions** in this course setup: checks run **locally** only.
- **Repository policy:** committed notebooks are **source-only** (no cell outputs). The **Canvas deliverable** is a **clean** notebook (outputs cleared, file valid), aligned with the course notebook requirements.
- **Strong stripping:** outputs are removed by **Git’s clean filter** (`nbstripout`), not only by a pre-commit hook, so even a GUI commit does not store outputs.
- **Validation:** `pre-commit` runs a small **nbformat** check so broken or invalid notebooks are caught before commit/push.

## One-time setup (each clone)

1. Create/activate a virtual environment if you use one (recommended).
2. From the repository root:

   ```bash
   ./scripts/setup_notebook_hooks.sh
   ```

   This installs [requirements-dev.txt](../requirements-dev.txt), runs **`nbstripout --install --attributes .gitattributes`** (registers filters in **this repo’s** `.git/config`), and installs **pre-commit** hooks (**commit** and **pre-push**).

Without step 2, `.gitattributes` is in the repo but **Git does not know the `nbstripout` filter** until `nbstripout --install` has been run in your clone.

## How stripping differs from validation

| Mechanism | What it does |
|-----------|----------------|
| **`.gitattributes` + `nbstripout --install`** | On `git add` / commit, the **clean** filter strips outputs before the blob is stored. Your editor may still show outputs locally until you save/refresh; the **history** stays output-free. |
| **`pre-commit` / `pre-push`** | Runs `scripts/validate_notebooks.py` on staged/changed `.ipynb` files so JSON/schema is valid. It does **not** strip outputs (the filter already did). |

Upstream behavior details: [nbstripout](https://github.com/kynan/nbstripout).

## Daily habits

- **Pull** before long editing sessions.
- Avoid **`git commit --no-verify`** unless you are fixing the hooks themselves; if you must skip hooks, tell the team before merging.
- After a **messy merge**, run `pre-commit run --all-files` or `python scripts/validate_notebooks.py` on the notebook paths you touched.

## Lightweight social rules

- Say in team chat when you’re doing a **large** pass on the shared notebook so others don’t stack conflicting edits.
- For ugly merges, pick **one person** (“merge captain”) to resolve the notebook conflict.
- Don’t base new work on a **`main`** you know is broken; fix or revert first.

## Rollback (if the team drops this workflow)

1. Revert the PR that added the tooling (or remove `.gitattributes`, `.pre-commit-config.yaml`, `requirements-dev.txt`, `scripts/`, and doc links).
2. In **each** local clone, run:

   ```bash
   python3 -m nbstripout --uninstall --attributes .gitattributes
   ```

   so local Git filter configuration does not reference removed tooling.

## Recovery from bad merges or corruption

See [NOTEBOOK_RECOVERY.md](NOTEBOOK_RECOVERY.md).
