# CS 410/510 — Data With Python (group project)

This repository holds the course **data project** work: notebooks, code, and supporting files for CS 410/510 at Portland State University.

**Course policy (read first):** [docs/COURSE_POLICY.md](docs/COURSE_POLICY.md) — PEP 8, honor code, **AI usage** (refinement and debugging are allowed with **Sources Used** notes; do not submit directly AI-generated graded work), and workflows. The official syllabus link lives in that doc.

**Phase 1 (milestone):** [docs/PHASE1_DATA_ACQUISITION.md](docs/PHASE1_DATA_ACQUISITION.md) — assignment snapshot, rubric alignment, and pre-submit checklist (the Canvas deliverable is still the `.ipynb`).

**Notebook workflow (team proposal):** [docs/JUPYTER_TEAM_WORKFLOW.md](docs/JUPYTER_TEAM_WORKFLOW.md) describes collaborating on Jupyter notebooks in Git (output stripping via Git filters, validation with pre-commit, and team habits). If a notebook is broken after a merge, use [docs/NOTEBOOK_RECOVERY.md](docs/NOTEBOOK_RECOVERY.md). **One-time setup per clone:** install [requirements-dev.txt](requirements-dev.txt), then run `./scripts/setup_notebook_hooks.sh`. After a messy merge, `pre-commit run --all-files` is a good sanity check. To drop this workflow later, revert the change and run `python3 -m nbstripout --uninstall --attributes .gitattributes` in each repository clone (details in the workflow doc).

**Using assistants (any editor or tool):** [AGENTS.md](AGENTS.md) explains how the same rules apply across browser chat, IDE assistants, and Cursor. **Cursor users** may also use [.cursor/rules/cs510-course-policy.mdc](.cursor/rules/cs510-course-policy.mdc) (optional reminders for the agent; not required for everyone).
