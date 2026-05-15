# Phase 3: Question answering and conclusion (planning)

**This file is internal planning for the group.** The graded Canvas deliverable is your **working Jupyter Notebook (`.ipynb`)**, not this document. If anything here disagrees with the [assignment on Canvas](#submission), follow Canvas.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

---

## Assignment snapshot

**Objective:** Formulate analytical questions based on your EDA, use Python to answer them, then summarize your entire process.

**Deliverable:** Submit your **updated working `.ipynb`** via Canvas (file upload). The notebook must include **completed work from Phases 1 and 2** plus the Phase 3 sections. See [Submission](#submission).

**Points:** 10

---

## Submission

- **Due:** Sunday by **11:59 p.m.** (confirm the exact calendar date and time zone on the assignment page).
- **Available until:** **May 22, 2026**, by **11:59 p.m.** (late submission window—confirm on Canvas).
- **Accepted file types:** **`.ipynb`** and **`.pdf`** (confirm whether Canvas expects one or both on the assignment page).
- **Where to submit:** Phase 3 assignment on Canvas — upload as instructed there. *(If your course uses the same module pattern as Phases 1–2, the link may be `https://canvas.pdx.edu/courses/115534/assignments/1210372` — always use the link on the live assignment page.)*

---

## Notebook requirements (must appear in the notebook)

### Question formulation and answering

- Formulate at least **3 specific, insightful questions** grounded in **patterns and characteristics** from your Phase 2 EDA (not generic questions unrelated to what you observed).
- For **each** question:
  - State the question clearly in **Markdown** (before or with the analysis).
  - Include and **execute** code cells that **manipulate the data** and **fully answer** the question.
  - Present the **answer/findings** in Markdown (or clearly labeled output) so a reader can interpret results without guessing.

### Conclusion and reflection

Write a **complete Conclusion and Reflection** section (Markdown) that includes:

1. **Summary** — key findings and core insights from the project (Phases 1–3, with emphasis on what your questions revealed).
2. **Limitations** — what your current analysis cannot claim (data scope, missing variables, causal vs. correlational claims, sample bias, etc.).
3. **Reflection** — how the overall data analysis process went and **concrete suggestions for future work** (next questions, data to collect, methods to try).

### “So what?” test (before you lock in your 3 questions)

Run each candidate question through this filter. If the answer is **no** to the checks below, the question is likely **too shallow** for Phase 3.

| Check | If **no**… |
| ----- | ----------- |
| Does the question require **more than one column** of data to answer? | It may be only a **descriptive statistic** or single-column lookup. |
| Does the question look for a **relationship**, **difference**, or **pattern**? | It may be a **lookup task**, not analysis. |
| Could the answer support an **action or prediction** (even hypothetically) for a community or business? | Prefer questions whose answers **inform decisions** (e.g. “sales double when X” for planning) over trivia (e.g. “what is the max?” alone). |

**Example (from the assignment):** Knowing that **sales double when X occurs** is more useful for inventory planning than knowing only the **maximum** sales value.

---

## Rubric alignment (Phase 3)

Use this when reviewing the notebook before submission.

### Question quality (3 pts)

- **Full credit (3 pts):** At least **3** questions are formulated. They are **specific**, **relevant to EDA findings**, and pass the **“So what?”** test (relationships, differences, or patterns—not simple lookups). They show **analytical thinking**.
- **Partial (2 pts):** Three questions are present, but they **fail** the “So what?” test **or** only **2** strong questions are provided.
- **No credit (0 pts):** **1 or fewer** questions; questions are **irrelevant** to EDA; or questions are **missing**.

### Analysis execution (3 pts)

- **Full credit (3 pts):** Code for all **3** questions is **efficient**, **correct**, and uses **pandas** (and related tools) effectively to reach the answer.
- **Partial (2 pts):** Answers are **correct** but code is **inefficient** or has **minor errors** that do not change the final results.
- **No credit (0 pts):** Code **fails to run**, has **major logic errors**, or does **not** answer the proposed questions.

### Findings clarity (2 pts)

- **Full credit (2 pts):** Answers are clearly presented in **Markdown**; results are **easy to interpret**; key numbers or patterns are **highlighted** and **tied back** to each question.
- **Partial (1 pt):** Findings exist but are **disorganized**; raw DataFrames printed **without** interpretation or reader-friendly formatting.
- **No credit (0 pts):** Findings **missing**, illegible, or output does **not** address the question asked.

### Conclusion and reflection (2 pts)

- **Full credit (2 pts):** Section is **complete**: summary of key findings, **limitations**, and **future work**; reflection is **thoughtful** and specific to your project.
- **Partial (1 pt):** Section is present but **superficial**; may omit **summary**, **limitations**, or **future work**; lacks detail.
- **No credit (0 pts):** **No** Conclusion and Reflection; notebook **ends without** a process summary.

**Total:** 10 points

---

## Pre-submit checklist

Use this list against the **notebook** you will upload.

- [ ] Notebook still contains **complete Phase 1** (justification, cleaning with issue/rationale/result) and **Phase 2** (visualizations, summary statistics, observations).
- [ ] At least **3** EDA-grounded questions; each passes the **[“So what?”](#so-what-test-before-you-lock-in-your-3-questions)** test where possible.
- [ ] For **each** question: Markdown statement → **executed** code → clear **findings** tied to the question.
- [ ] **Conclusion and Reflection** includes: **key findings**, **limitations**, **process reflection**, and **future work**.
- [ ] Answers use **pandas** effectively (groupby, filters, merges, aggregations—as appropriate—not only `describe()` on one column).
- [ ] **Restart kernel and run all** — no errors top to bottom.
- [ ] Confirm Canvas **file type** (`.ipynb` vs `.pdf`) and **due / available until** dates on the assignment page.
- [ ] **Sources Used** (and citations) updated per [COURSE_POLICY.md](COURSE_POLICY.md) if you used AI for refinement or debugging, or note that you did not.

---

## Appendix (optional team notes)

Fill in as your project takes shape. Keep long narratives in the **notebook**, not here.

| Note | Details |
| ---- | ------- |
| EDA hooks for Q1–Q3 | *(which Phase 2 plots/stats each question extends—e.g. correlation, group differences)* |
| Question drafts | *(working titles; pass/fail on “So what?” before final wording)* |
| Conclusion themes | *(1–3 bullet core insights to echo in the final section)* |
| Known limitations | *(sample, missing columns, survivorship, season, etc.)* |
| Future work ideas | *(extra data, modeling, causal follow-ups)* |
