# Phase 4: Machine learning (planning)

**This file is internal planning for the group.** The graded Canvas deliverable is your **working Jupyter Notebook (`.ipynb`)**, not this document. If anything here disagrees with the [assignment on Canvas](#submission), follow Canvas.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

---

## Assignment snapshot

**Objective:** Incorporate the **machine learning** component into your project.

**Deliverable:** Submit your **updated working `.ipynb`** via Canvas (file upload). The notebook must include **completed work from Phases 1–3** plus a new **Machine Learning** section. See [Submission](#submission).

**Points:** 10

---

## Submission

- **Due:** Sunday by **11:59 p.m.** (confirm the exact calendar date and time zone on the assignment page).
- **Available until:** **June 5, 2026**, by **11:59 p.m.** (late submission window—confirm on Canvas).
- **Accepted file types:** **`.ipynb`** only (confirm on the assignment page).
- **Where to submit:** Phase 4 assignment on Canvas — upload as instructed there. *(If your course uses the same module pattern as Phases 1–3, the link may be `https://canvas.pdx.edu/courses/115534/assignments/1210373` — always use the link on the live assignment page.)*

---

## Notebook requirements (must appear in the notebook)

Add a **new, clearly labeled section** (Markdown heading) for machine learning. It should read as one coherent mini-study—not scattered cells—with the four parts below.

### 1. Predictive objective

State in **Markdown** (before modeling code):

- **What you are trying to predict** (target variable) and **why** it matters for your project.
- **Input features** you will use (and any you intentionally exclude, with brief rationale).
- **Problem type** (e.g. binary/multiclass classification, regression) so the reader knows which metrics and interpretation tools apply.

The objective should connect to your **Phase 2 EDA** and **Phase 3 questions** where possible (e.g. extending a pattern you already explored into a predictive claim).

### 2. Model implementation

Include **executed** code that shows a technically sound pipeline:

| Step | What to show |
| ---- | ------------ |
| **Data split** | Train/test (or train/validation/test) split; state split ratio and whether you used stratification or random seed for reproducibility. |
| **Preprocessing** | Steps required for your model—e.g. scaling numeric features, encoding categoricals, handling missing values, defining feature matrix **X** and target **y**. Fit preprocessors on **training data only** (or inside a pipeline) to avoid leakage. |
| **Model fitting** | Fit at least one appropriate model (e.g. `sklearn` classifier or regressor) on the prepared training set. |

Use a model and preprocessing choices that match your **data types** (numeric vs. categorical, class imbalance, sample size).

### 3. Evaluation

Evaluate performance on held-out data (typically the **test** set) using **metrics relevant to your objective**, for example:

| Problem type | Examples of relevant metrics |
| ------------ | ---------------------------- |
| **Classification** | Accuracy, precision, recall, F1, ROC-AUC (when appropriate); confusion matrix. |
| **Regression** | MAE, MSE/RMSE, R². |

Present metrics clearly (tables or labeled printouts)—not only raw code output with no context.

### 4. Interpretation

In **Markdown** (supported by code output where helpful):

- **What the metrics mean** for your predictive objective (not only the numbers).
- **Model fit:** discuss **overfitting** vs. **underfitting** (e.g. compare train vs. test performance, or cross-validation if you use it).
- **Feature importance or coefficients:** interpret which inputs drove predictions (e.g. `feature_importances_`, coefficients, or permutation importance)—tied back to your domain and earlier EDA where possible.

---

## Rubric alignment (Phase 4)

Use this when reviewing the notebook before submission.

### ML implementation (5 pts)

| Points | Level | Description |
| ------ | ----- | ----------- |
| **5** | Complete | Predictive objective is **clearly stated**. Data splitting (train/test), preprocessing (scaling/encoding), and model fitting are **technically sound** and **appropriate** for the data type. |
| **3** | Partial credit | ML objective is **vague**. Implementation has **minor technical flaws** or **skips a key preprocessing step** required for the chosen model. |
| **0** | No credit | Model **fails to run**, uses **inappropriate techniques** for the data, or the implementation section is **missing entirely**. |

### ML evaluation and interpretation (5 pts)

| Points | Level | Description |
| ------ | ----- | ----------- |
| **5** | Complete | Performance is measured with **relevant metrics**. Includes a **thoughtful discussion** on over/underfitting and interprets **feature importance or coefficients**. |
| **3** | Partial credit | Metrics are calculated but are **irrelevant to the task** or **lack context**. Evaluation is **purely numerical** with little or no interpretation of what results mean for the objective. |
| **0** | No credit | **No evaluation metrics** are provided, or there is **no attempt** to interpret the model’s output or feature importance. |

**Total:** 10 points

---

## Pre-submit checklist

Use this list against the **notebook** you will upload.

- [ ] Notebook still contains **complete Phase 1** (justification, cleaning with issue/rationale/result), **Phase 2** (visualizations, summary statistics, observations), and **Phase 3** (≥3 questions with code answers and Conclusion and Reflection).
- [ ] New **Machine Learning** section with a clear **predictive objective** (target, features, problem type, project relevance).
- [ ] **Train/test split** documented; **preprocessing** appropriate for the model (scaling/encoding/etc.); **model fit** on training data without obvious leakage.
- [ ] **Evaluation** on held-out data with **task-appropriate metrics** and readable presentation.
- [ ] **Interpretation** covers metric meaning, **over/underfitting**, and **feature importance or coefficients** in domain terms.
- [ ] **Restart kernel and run all** — no errors top to bottom.
- [ ] Confirm Canvas **due / available until** dates and **file type** (`.ipynb`) on the assignment page.
- [ ] **Sources Used** (and citations) updated per [COURSE_POLICY.md](COURSE_POLICY.md) if you used AI for refinement or debugging, or note that you did not.

---

## Appendix (optional team notes)

Fill in as your project takes shape. Keep long narratives in the **notebook**, not here.

| Note | Details |
| ---- | ------- |
| Target variable | *(e.g. `is_winner`, placement, votes—confirm dtype and class balance)* |
| Feature set | *(columns in **X**; dropped columns and why)* |
| Model choice | *(algorithm + why it fits the data and objective)* |
| Split & seed | *(e.g. 80/20, `random_state=`, stratify yes/no)* |
| Metrics to report | *(list before running—classification vs. regression)* |
| Leakage risks | *(e.g. target-derived features, future information, duplicate rows)* |
| EDA / Phase 3 links | *(which earlier findings this model extends)* |
