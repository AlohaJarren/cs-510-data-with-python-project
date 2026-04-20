#!/usr/bin/env python3
"""Apply Exploration / Cleaning needs / Methods / Results headings to survivoR.ipynb.

Locates each chapter by ## Table: … line (works with numeric cell ids from git).
"""

from __future__ import annotations

import json
from pathlib import Path


def lines(s: str) -> list[str]:
    if not s.endswith("\n"):
        s += "\n"
    return [ln + "\n" if not ln.endswith("\n") else ln for ln in s.splitlines()]


def md_cell(text: str, cell_id: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": lines(text)}


def join_src(cells: list, i: int) -> str:
    return "".join(cells[i]["source"])


def set_src(cells: list, i: int, text: str) -> None:
    cells[i]["source"] = lines(text)


def find_table_idx(cells: list, label: str) -> int:
    prefix = f"## Table: {label}"
    for idx, c in enumerate(cells):
        if c.get("cell_type") != "markdown":
            continue
        s = "".join(c.get("source", [])).strip()
        if s.startswith(prefix):
            return idx
    raise KeyError(f"table heading {label!r}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "survivoR.ipynb"
    with path.open() as f:
        nb = json.load(f)

    cells = nb["cells"]

    order = ["Summary", "Challenges", "Castaways", "Viewers", "Jury votes"]
    starts = {name: find_table_idx(cells, name) for name in order}
    ends = {}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)

    # --- Summary
    s, e = starts["Summary"], ends["Summary"]
    # Cell after ## Table: Summary is context
    set_src(
        cells,
        s + 1,
        join_src(cells, s + 1)
        .replace("### Context\n\n", "### Initial CSV exploration\n\n#### Context\n\n", 1)
        .replace("### Relevance:", "#### Relevance:", 1)
        .replace("### Size:", "#### Size:", 1)
        .replace("### Column Descriptions (English):", "#### Column descriptions (English):", 1),
    )
    set_src(cells, s + 2, join_src(cells, s + 2).replace("### Raw inspection", "#### Raw inspection", 1))
    for j in range(s, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if src.startswith("### Cleaning\n"):
            set_src(cells, j, src.replace("### Cleaning", "### Cleaning needs", 1))
        if "## Initial Status" in src:
            set_src(cells, j, src.replace("## Initial Status", "#### Initial status", 1))

    # Insert ### Methods before first summary cleaning code (first code after ### Cleaning needs md)
    cleaning_needs_idx = None
    for j in range(s, e):
        if cells[j].get("cell_type") == "markdown" and join_src(cells, j).startswith("### Cleaning needs"):
            cleaning_needs_idx = j
            break
    assert cleaning_needs_idx is not None
    insert_at = None
    for j in range(cleaning_needs_idx + 1, e):
        if cells[j].get("cell_type") == "code":
            insert_at = j
            break
    assert insert_at is not None
    cells.insert(
        insert_at,
        md_cell(
            "### Methods\n\n"
            "The following code cells implement the cleaning steps for `summary_df`.\n",
            "summary-methods-md",
        ),
    )
    # Recompute ends after insert
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)

    s, e = starts["Summary"], ends["Summary"]
    for j in range(s, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if "### After checks" in src and "**Summary:**" in src:
            set_src(cells, j, src.replace("### After checks", "### Results", 1))
            break

    # --- Challenges
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)
    s, e = starts["Challenges"], ends["Challenges"]
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if src.startswith("### Context\n"):
            set_src(
                cells,
                j,
                src.replace("### Context\n\n", "### Initial CSV exploration\n\n#### Context\n\n", 1)
                .replace("### Relevance:", "#### Relevance:", 1)
                .replace("### Size:", "#### Size:", 1)
                .replace("### Column Descriptions (English):", "#### Column descriptions (English):", 1),
            )
        if src.strip() == "### Raw inspection\n" or src.startswith("### Raw inspection\n"):
            set_src(cells, j, src.replace("### Raw inspection", "#### Raw inspection", 1))
        if src.startswith("### Cleaning\n") and not src.startswith("### Cleaning needs"):
            set_src(cells, j, src.replace("### Cleaning", "### Cleaning needs", 1))

    ch_clean_md = None
    ch_code = None
    for j in range(s + 1, e):
        if cells[j].get("cell_type") == "markdown" and join_src(cells, j).startswith("### Cleaning needs"):
            ch_clean_md = j
        if cells[j].get("cell_type") == "code" and ch_clean_md is not None and ch_code is None and j > ch_clean_md:
            ch_code = j
            break
    assert ch_clean_md is not None and ch_code is not None
    cells.insert(
        ch_code,
        md_cell(
            "### Methods\n\n"
            "The following code cell encodes the challenge-row cleaning rules for `challenges_df`.\n",
            "challenges-methods-md",
        ),
    )
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)
    s, e = starts["Challenges"], ends["Challenges"]
    ch_code = None
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "code":
            continue
        if "challenges_cleaned_df = challenges_df.copy()" in join_src(cells, j):
            ch_code = j
            break
    assert ch_code is not None
    cells.insert(
        ch_code + 1,
        md_cell(
            "### Results\n\n"
            "See the printed null counts and `challenges_cleaned_df.info()` / `head()` output above for this run.\n",
            "challenges-results-md",
        ),
    )

    # --- Castaways
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)
    s, e = starts["Castaways"], ends["Castaways"]
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if src.startswith("### Context\n"):
            set_src(
                cells,
                j,
                src.replace("### Context\n\n", "### Initial CSV exploration\n\n#### Context\n\n", 1)
                .replace("### Relevance:", "#### Relevance:", 1)
                .replace("### Size:", "#### Size:", 1)
                .replace("### Column Descriptions (English):", "#### Column descriptions (English):", 1),
            )
        if "### Raw inspection\n" in src and "continued" not in src and src.strip().startswith("### Raw inspection"):
            set_src(cells, j, src.replace("### Raw inspection", "#### Raw inspection", 1))
        if "Raw inspection (continued)" in src:
            set_src(cells, j, src.replace("### Raw inspection (continued)", "#### Raw inspection (continued)", 1))
        if "### Data Cleaning: Fixing Null values" in src:
            set_src(
                cells,
                j,
                src.replace(
                    "### Data Cleaning: Fixing Null values",
                    "### Cleaning needs\n\n#### Data cleaning: Fixing null values",
                    1,
                ),
            )
        if src.startswith("### After checks"):
            set_src(cells, j, src.replace("### After checks", "### Results", 1))

    # Methods before first castaways cleaning code (copy df)
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "code":
            continue
        if "clean_castaways_df = castaways_df.copy()" in join_src(cells, j):
            cells.insert(
                j,
                md_cell(
                    "### Methods\n\n"
                    "The following code cells implement the castaways cleaning steps on `clean_castaways_df`.\n",
                    "castaways-methods-md",
                ),
            )
            break

    # --- Viewers
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)
    s, e = starts["Viewers"], ends["Viewers"]
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if src.startswith("### Context\n"):
            set_src(
                cells,
                j,
                src.replace("### Context\n\n", "### Initial CSV exploration\n\n#### Context\n\n", 1)
                .replace("### Relevance:", "#### Relevance:", 1)
                .replace("### Size:", "#### Size:", 1)
                .replace("### Column Descriptions (English):", "#### Column descriptions (English):", 1),
            )
        if src.strip() == "### Raw inspection\n" or (
            src.startswith("### Raw inspection\n") and "continued" not in src
        ):
            set_src(cells, j, src.replace("### Raw inspection", "#### Raw inspection", 1))
        if "### Cleaning" in src and "viewers_df" in src:
            set_src(cells, j, src.replace("### Cleaning", "### Cleaning needs", 1))
        if src.startswith("### After checks"):
            set_src(cells, j, src.replace("### After checks", "### Results", 1))
    for j in range(s + 1, e):
        if cells[j].get("cell_type") == "markdown" and join_src(cells, j).startswith("### Results"):
            cells.insert(
                j,
                md_cell("### Methods\n\nNone yet for this table in this notebook.\n", "viewers-methods-md"),
            )
            break

    # --- Jury votes
    starts = {name: find_table_idx(cells, name) for name in order}
    for i, name in enumerate(order):
        ends[name] = starts[order[i + 1]] if i + 1 < len(order) else len(cells)
    s, e = starts["Jury votes"], ends["Jury votes"]
    for j in range(s + 1, e):
        if cells[j].get("cell_type") != "markdown":
            continue
        src = join_src(cells, j)
        if src.startswith("### Context\n"):
            set_src(
                cells,
                j,
                src.replace("### Context\n\n", "### Initial CSV exploration\n\n#### Context\n\n", 1)
                .replace("### Relevance:", "#### Relevance:", 1)
                .replace("### Size:", "#### Size:", 1)
                .replace("### Column Descriptions (English):", "#### Column descriptions (English):", 1),
            )
        if src.strip() == "### Raw inspection\n" or (
            src.startswith("### Raw inspection\n") and "continued" not in src
        ):
            set_src(cells, j, src.replace("### Raw inspection", "#### Raw inspection", 1))
        if "### Cleaning" in src and "jury_votes_df" in src:
            set_src(cells, j, src.replace("### Cleaning", "### Cleaning needs", 1))
        if src.startswith("### After checks"):
            set_src(cells, j, src.replace("### After checks", "### Results", 1))
    for j in range(s + 1, e):
        if cells[j].get("cell_type") == "markdown" and join_src(cells, j).startswith("### Results"):
            cells.insert(
                j,
                md_cell("### Methods\n\nNone yet for this table in this notebook.\n", "jury-methods-md"),
            )
            break

    # --- Intro bridge + Sources Used
    for j, c in enumerate(cells):
        if c.get("cell_type") == "markdown" and c.get("id") == "1":
            src = join_src(cells, j)
            set_src(
                cells,
                j,
                src.replace(
                    "**context**, **raw inspection**, **cleaning** (when needed), and **after checks**",
                    "**Initial CSV exploration**, **Cleaning needs**, **Methods**, and **Results**",
                    1,
                ),
            )
            break

    for j in range(len(cells) - 1, -1, -1):
        if cells[j].get("cell_type") == "markdown" and join_src(cells, j).startswith("## Sources Used"):
            src = join_src(cells, j).rstrip() + "\n\n"
            if "Exploration / Cleaning needs / Methods / Results" not in src:
                src += (
                    "- **Second pass (same tool):** Added the **Initial CSV exploration** / **Cleaning needs** / "
                    "**Methods** / **Results** heading scheme under each `## Table:` section; heading and label "
                    "edits only—no Python logic changes.\n"
                )
            set_src(cells, j, src)
            break

    with path.open("w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")

    print("Updated", path, "total cells", len(cells))


if __name__ == "__main__":
    main()
