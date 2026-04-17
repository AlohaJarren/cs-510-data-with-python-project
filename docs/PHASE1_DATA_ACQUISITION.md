# Phase 1: Data acquisition and cleaning (planning)

**This file is internal planning for the group.** The graded Canvas deliverable is your **working Jupyter Notebook (`.ipynb`)**, not this document. If anything here disagrees with the [assignment on Canvas](#submission), follow Canvas.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

---

## Assignment snapshot

**Objective:** Identify a suitable dataset, import it into a Jupyter Notebook with **pandas**, and systematically clean and prepare the data for analysis.

**Deliverable:** Submit the working **`.ipynb`** via Canvas (file upload). See [Submission](#submission) for the assignment link and due date.

**Points:** 10

---

## Submission

- **Due:** Sunday, **April 19, 2026**, by **11:59 p.m.** (confirm time zone and any “available until” window on the assignment page).
- **Where to submit:** [Phase 1 assignment on Canvas](https://canvas.pdx.edu/courses/115534/assignments/1210370?module_item_id=5280339) — upload your **`.ipynb`** as instructed there.

---

## Project foundation (must appear in the notebook)

- **Dataset justification** in a dedicated **Markdown** section in the notebook:
  - **Source** (where it comes from, how to access, citation or link as appropriate).
  - **Column descriptions** (what each important variable means).
  - **Size** (rows/columns or comparable summary).
  - **Relevance** — why this dataset fits your project question(s).
- **Import** the data in the notebook using **pandas** (e.g., `read_csv` or appropriate reader).

---

## Data cleaning (must appear in the notebook)

- **Systematic examination** of raw data, including at least:
  - Data types (`dtypes` / inference).
  - Missing values (counts, patterns).
  - Outliers or implausible values (as relevant to your columns).
- **Implement and execute** all cleaning steps in code cells (not described only in prose).
- **For every cleaning step**, include a **Markdown cell** that states:
  1. **Issue** — what was wrong or risky.
  2. **Rationale** — why you chose this fix (e.g., impute vs. drop, which statistic, caps vs. removal).
  3. **Result** — evidence such as **before/after** null counts, row counts, or summary stats.

---

## Rubric alignment (Phase 1)

Use this when reviewing the notebook before submission.

### Dataset selection and import (2 pts)

- **Full credit:** Dataset is **highly suitable** (guideline: **about 1,000+ rows**), imported correctly with pandas, and the Markdown section thoroughly covers **source, columns, size, and relevance**.
- **Partial:** Imported and generally suitable, but justification is vague or missing one or two key pieces.
- **No credit:** Far below size expectations, failed import, or missing justification.

### Cleaning coverage (4 pts)

- **Full credit:** Clear systematic examination; **major** issues addressed — missing values, incorrect types, outliers (where applicable) — and fixed in code.
- **Partial:** Partial cleaning; a major problem overlooked.
- **No credit:** Little or no cleaning; raw data left in bad shape.

### Documentation and rationale (3 pts)

- **Full credit:** **Every** cleaning step has Markdown: issue, **why** this method, and **before/after** (or equivalent) evidence.
- **Partial:** Documentation present but shallow (what without why, or missing before/after).
- **No credit:** No Markdown documentation for cleaning; code only.

### Execution and readiness (1 pt)

- **Full credit:** All cells run **sequentially without errors**; final dataset is **clean and ready** for analysis.
- **Partial:** Runs but with problematic warnings or minor quirks that slow analysis.
- **No credit:** Runtime errors, or final data unusable.

**Total:** 10 points

---

## Pre-submit checklist

Use this list against the **notebook** you will upload.

- [ ] Planning doc vs. submission: I am uploading the **`.ipynb`** on Canvas, not this file.
- [ ] Markdown section: **source**, **column descriptions**, **size**, **relevance**.
- [ ] Data loaded with **pandas**.
- [ ] Raw data examined: **types**, **missing values**, **outliers** (as applicable).
- [ ] Each cleaning step has: **issue** → **rationale** → **before/after** (or equivalent evidence).
- [ ] All cleaning code is **executed**; final table is analysis-ready.
- [ ] **Restart kernel and run all** — no errors top to bottom.
- [ ] **Sources Used** (and citations) updated per [COURSE_POLICY.md](COURSE_POLICY.md) if you used AI for refinement or debugging, or note that you did not.

---

## Appendix (optional team notes)

Fill in as your project takes shape. Keep long narratives in the **notebook**, not here.

| Note | Details |
|------|---------|
| Raw data location in repo | *(path or “external only”) * |
| Reproducibility | *(Python version, `requirements`/`environment`, path assumptions)* |
| License / attribution | *(dataset license, citation, terms of use)* |
