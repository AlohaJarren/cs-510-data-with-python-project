# Phase 2: Exploratory Data Analysis (EDA) (planning)

**This file is internal planning for the group.** The graded Canvas deliverable is your **working Jupyter Notebook (`.ipynb`)**, not this document. If anything here disagrees with the [assignment on Canvas](#submission), follow Canvas.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

---

## Assignment snapshot

**Objective:** Thoroughly analyze the characteristics of your **cleaned** dataset using **statistical summaries** and **visualizations**.

**Deliverable:** Submit your **updated working `.ipynb`** via Canvas (file upload). The notebook must include **completed Phase 1 work** plus the Phase 2 sections. See [Submission](#submission).

**Points:** 10

---

## Submission

- **Due:** Sunday by **11:59 p.m.** (confirm the exact calendar date and time zone on the assignment page).
- **Available until:** **May 8, 2026**, by **11:59 p.m.** (late submission window—confirm on Canvas).
- **Where to submit:** [Phase 2 assignment on Canvas](https://canvas.pdx.edu/courses/115534/assignments/1210371?module_item_id=5280340) — upload your **`.ipynb`** as instructed there.

---

## Notebook requirements (must appear in the notebook)

### Visualization

- At least **3 diverse** visualizations (e.g. histograms, scatter plots, box plots).
- Use **`matplotlib`** and/or **`seaborn`** (or consistent plotting stack agreed by the team).
- Plots should be **embedded** in the notebook (not only described).
- Each plot should have **clear titles**, **axis labels**, and **legends** where appropriate.
- Choose plot types **suited to the variables** you are exploring.

### Summary statistics

Calculate and display, using **pandas** (or clear tabular output derived from your DataFrame):

- **Mean**
- **Median**
- **Standard deviation**
- **Correlations** (e.g. correlation matrix for numeric columns—present clearly, not only as an unreadable dump)

### Observations

- A **dedicated Markdown section** that interprets both the **visualizations** and the **summary statistics**.
- Call out **patterns**, **relationships**, and **distributions** that matter for your project question(s).
- Tie observations to **specific** figures and statistics where possible.

### Status check (implicit rubric expectation)

- Data should remain **clean** and consistent with Phase 1.
- The notebook should show that you **understand** the dataset’s characteristics (not only code with no narrative).

---

## Rubric alignment (Phase 2)

Use this when reviewing the notebook before submission.

### Visualization quality (4 pts)

- **Full credit (4 pts):** At least **3 diverse**, high-quality visualizations embedded; plot types fit the data; **titles**, **axis labels**, and **legends** (where appropriate) are present and clear.
- **Partial (2 pts):** Only **2** visualizations, **or** 3 that lack diversity; and/or missing key labels/titles; and/or a plot type slightly ill-suited to the data.
- **No credit (0 pts):** **1 or fewer** visualizations; plots missing labels, illegible, or code fails to produce graphs.

### Statistical coverage (2 pts)

- **Full credit (2 pts):** **Mean**, **median**, **standard deviation**, and **correlations** are accurately computed and **clearly displayed** with pandas (focused presentation, not a wall of raw output).
- **Partial (1 pt):** Most statistics present but **one or two** missing or unclear (e.g. massive dump without focus).
- **No credit (0 pts):** Little or no summary statistics, or errors prevent display.

### Insight and documentation (4 pts)

- **Full credit (4 pts):** Dedicated Markdown describes observations for **all** visuals and statistics; insights are **thoughtful** and show **deep understanding** (including non-obvious points where the data supports them).
- **Partial (2 pts):** Observations are **superficial**; and/or some graphs or statistics lack explanation.
- **No credit (0 pts):** **No** Markdown observations—only code and plots without interpretation.

**Total:** 10 points

---

## Pre-submit checklist

Use this list against the **notebook** you will upload.

- [ ] Notebook still contains **complete Phase 1** sections (dataset justification, cleaning with issue/rationale/result).
- [ ] At least **3 diverse** plots (`matplotlib` / `seaborn`), embedded, with **titles**, **labels**, and **legends** where needed.
- [ ] **Mean**, **median**, **standard deviation**, and **correlations** computed and **clearly** shown (pandas).
- [ ] **Dedicated Markdown** section: observations for **every** plot and the **statistics**; connects to project questions where relevant.
- [ ] Data remains **clean**; narrative shows you **understand** the dataset.
- [ ] **Restart kernel and run all** — no errors top to bottom.
- [ ] **Sources Used** (and citations) updated per [COURSE_POLICY.md](COURSE_POLICY.md) if you used AI for refinement or debugging, or note that you did not.

---

## Appendix (optional team notes)

Fill in as your project takes shape. Keep long narratives in the **notebook**, not here.

| Note | Details |
|------|---------|
| Plot conventions | *(color palette, figure size defaults, which columns are primary EDA targets)* |
| Correlation scope | *(all numeric columns vs. a focused subset—and why)* |
| Reproducibility | *(Python version, `requirements`/`environment`, path assumptions)* |
