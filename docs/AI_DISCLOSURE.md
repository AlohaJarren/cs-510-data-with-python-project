# AI assistance — repository files (disclosure)

This note documents **AI-assisted work on files in this repository other than the graded Jupyter notebook**, so collaborators and graders can see what was automated or drafted versus reviewed by humans. It does **not** replace the course requirement to document AI use on **submissions**; see [COURSE_POLICY.md](COURSE_POLICY.md) and the **Sources Used** section in your notebook when that applies.

## Scope

### Out of scope for this disclosure (document elsewhere)

- **Course Jupyter notebooks** (`*.ipynb` at repository root or elsewhere): treated as the **graded, student-authored artifact**. Document AI use for **refinement** or **debugging** only in each deliverable’s **Sources Used** section, per [COURSE_POLICY.md](COURSE_POLICY.md). Do not rely on this file alone for notebook attribution.

### In scope for this disclosure (AI-assisted, human-reviewed)

The following categories list repository content that has been **drafted or modified using AI assistance**, with **subsequent human review and edits**. This list is **maintained incrementally**: add a row (or extend a bullet) whenever AI-assisted material is added or when a file’s status changes.

| Area | Paths / patterns | Notes |
|------|------------------|--------|
| Top-level documentation | `README.md` | Overview, links, onboarding. |
| Team workflow and disclosure | `docs/JUPYTER_TEAM_WORKFLOW.md`, `docs/NOTEBOOK_RECOVERY.md`, `docs/AI_DISCLOSURE.md` | Jupyter/Git collaboration and attribution. |
| Other documentation under `docs/` | *(add paths here, e.g. `docs/EXAMPLE.md`)* | Include only files that are AI-assisted; omit course- or instructor-provided text unless the team also used AI on that file. |
| Automation scripts | `scripts/setup_notebook_hooks.sh`, `scripts/validate_notebooks.py` | Extend with additional `scripts/*` as added. |
| Dependency manifests | `requirements-dev.txt` | Dev-only packages for hooks and filters. |
| Git and hook configuration | `.gitattributes`, `.pre-commit-config.yaml`, `.gitignore` | Filters, validation hooks, ignore rules. |
| Optional editor configuration | `.cursor/rules/cs510-course-policy.mdc` (and siblings under `.cursor/rules/` if present) | Tool reminders only; not a substitute for [COURSE_POLICY.md](COURSE_POLICY.md). |

**Process (for additions):** When new AI-assisted files appear in the tree, update this table (or the placeholder under **Other documentation**), revise **Tools** if the product or workflow changed, and confirm **Human oversight** still applies.

## Tools

- **Primary tool:** Cursor (IDE-embedded assistant), including chat and agent-style edits to the repository tree.
- **How it was used:** drafting and iterating on documentation, shell scripts, and config; suggestions were **accepted, revised, or rejected** by project members before merging.

Update this section if other tools (e.g. browser-based chat) contributed materially to the same kinds of files.

## Human oversight

Project members remain responsible for:

- Correctness of commands, paths, and policy alignment with [COURSE_POLICY.md](COURSE_POLICY.md).
- Agreeing as a team to adopt or change workflow tooling.

## When to update this document

- When major new AI-assisted repo content is added (new docs, scripts, or configs).
- When the team’s use of tools or level of human review changes materially.

_Last updated: Spring 2026 (CS 410/510 group project)._
