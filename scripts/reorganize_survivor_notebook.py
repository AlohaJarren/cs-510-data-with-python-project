#!/usr/bin/env python3
"""One-off: reorganize survivoR.ipynb per B+C plan (structure only)."""

from __future__ import annotations

import copy
import json
from pathlib import Path


def _src_lines(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    if not lines:
        return ["\n"]
    if not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    return lines


def md_cell(text: str, cell_id: str | None = None) -> dict:
    cell = {"cell_type": "markdown", "metadata": {}, "source": _src_lines(text)}
    if cell_id is not None:
        cell["id"] = cell_id
    return cell


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "survivoR.ipynb"
    with path.open() as f:
        nb = json.load(f)

    cells = nb["cells"]
    assert len(cells) == 59, f"expected 59 cells, got {len(cells)}"

    # Summary cleaning (49-58) immediately after first summary inspect (5)
    reordered = cells[:6] + cells[49:59] + cells[6:49]

    def take(i: int) -> dict:
        return copy.deepcopy(reordered[i])

    out: list[dict] = []

    out.append(take(0))
    intro2 = "".join(take(1)["source"])
    intro2 = intro2.replace(
        "The following cells provide context for relevance, size, and column descriptions for each CSV file.",
        "The sections below walk through each CSV in the same order: **context**, **raw inspection**, "
        "**cleaning** (when needed), and **after checks**.",
    )
    c1 = take(1)
    c1["source"] = _src_lines(intro2)
    out.append(c1)

    out.append(
        md_cell(
            "## Setup: imports and loading\n\n"
            "Import **pandas** and load all tables from the TidyTuesday CSV mirror.",
            "setup-imports-md",
        )
    )
    out.append(take(2))
    out.append(take(3))

    # --- Table: Summary
    out.append(md_cell("## Table: Summary", "table-summary-h2"))
    s4 = "".join(take(4)["source"])
    s4 = s4.replace("## Summary CSV:\n\n", "", 1)
    csum = take(4)
    csum["source"] = _src_lines("### Context\n\n" + s4.strip() + "\n")
    out.append(csum)
    out.append(md_cell("### Raw inspection", "summary-raw-md"))
    out.append(take(5))

    out.append(
        md_cell(
            "### Cleaning\n\n"
            "The following cells repeat `summary_df` inspection where useful, "
            "then apply parsing and type fixes already developed for this table.",
            "summary-clean-md",
        )
    )
    for j in range(6, 16):
        cell = take(j)
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"])
            if src.strip().startswith("# Cleaning the Summary"):
                cell["source"] = _src_lines(
                    src.replace("# Cleaning the Summary Dataframe", "_Cleaning steps (summary)_", 1)
                )
            if "### Cleaning Results:" in src:
                cell["source"] = _src_lines(
                    src.replace("### Cleaning Results:", "### After checks\n\n**Summary:**", 1)
                )
        out.append(cell)

    # --- Table: Challenges
    out.append(md_cell("## Table: Challenges", "table-challenges-h2"))
    ch6 = "".join(take(16)["source"])
    ch6 = ch6.replace("## Challenges CSV:\n\n", "", 1)
    cch = take(16)
    cch["source"] = _src_lines("### Context\n\n" + ch6.strip() + "\n")
    out.append(cch)
    out.append(md_cell("### Raw inspection", "challenges-raw-md"))
    out.append(take(17))
    out.append(md_cell("### Cleaning", "challenges-clean-md"))
    out.append(take(18))

    # --- Table: Castaways
    out.append(md_cell("## Table: Castaways", "table-castaways-h2"))
    ca9 = "".join(take(19)["source"])
    ca9 = ca9.replace("## Castaways CSV:\n\n", "", 1)
    cca = take(19)
    cca["source"] = _src_lines("### Context\n\n" + ca9.strip() + "\n")
    out.append(cca)
    out.append(md_cell("### Raw inspection", "castaways-raw-md"))
    out.append(take(20))
    bridge = "".join(take(21)["source"])
    cbr = take(21)
    cbr["source"] = _src_lines("### Raw inspection (continued)\n\n" + bridge.strip() + "\n")
    out.append(cbr)
    # Castaways cleaning already opens with "### Data Cleaning: ..." — no extra empty ### Cleaning cell.
    for j in range(22, 53):
        out.append(take(j))
    out.append(md_cell("### After checks", "castaways-after-md"))
    out.append(take(53))
    out.append(take(54))

    # --- Table: Viewers
    out.append(md_cell("## Table: Viewers", "table-viewers-h2"))
    vmd = "".join(take(55)["source"])
    vmd = vmd.replace("## Viewers CSV:\n\n", "", 1)
    cv = take(55)
    cv["source"] = _src_lines("### Context\n\n" + vmd.strip() + "\n")
    out.append(cv)
    out.append(md_cell("### Raw inspection", "viewers-raw-md"))
    out.append(take(56))
    out.append(
        md_cell(
            "### Cleaning\n\n"
            "_No additional cleaning steps in this notebook for `viewers_df` yet._ "
            "Fill this in when you add wrangling for this table.",
            "viewers-clean-stub",
        )
    )
    out.append(
        md_cell(
            "### After checks\n\n"
            "Re-run `viewers_df.info()` after future cleaning; for now the raw inspection above is the check.",
            "viewers-after-md",
        )
    )

    # --- Table: Jury votes
    out.append(md_cell("## Table: Jury votes", "table-jury-h2"))
    jmd = "".join(take(57)["source"])
    jmd = jmd.replace("## Jury Votes CSV:\n\n", "", 1)
    cj = take(57)
    cj["source"] = _src_lines("### Context\n\n" + jmd.strip() + "\n")
    out.append(cj)
    out.append(md_cell("### Raw inspection", "jury-raw-md"))
    out.append(take(58))
    out.append(
        md_cell(
            "### Cleaning\n\n"
            "_No additional cleaning steps in this notebook for `jury_votes_df` yet._ "
            "Fill this in when you add wrangling for this table.",
            "jury-clean-stub",
        )
    )
    out.append(
        md_cell(
            "### After checks\n\n"
            "Re-run `jury_votes_df.info()` after future cleaning; for now the raw inspection above is the check.",
            "jury-after-md",
        )
    )

    out.append(
        md_cell(
            "## Sources Used\n\n"
            "- **Tool:** Cursor (agent)\n"
            "- **How used:** Notebook structure only—reordered cells (Summary cleaning moved next to Summary "
            "inspection), added section headings (B-style spine and C-style subsections), and stub Cleaning "
            "sections for viewers/jury; no changes to data-cleaning logic or substantive analysis text.\n"
            "- **Scope:** Refinement / presentation only—not full draft generation of graded analysis.\n",
            "sources-used",
        )
    )

    nb["cells"] = out
    with path.open("w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")

    print("Wrote", path, "cells:", len(out))


if __name__ == "__main__":
    main()
