# Interactive model deployment (planning, graduate section)

**This file is internal planning for the group.** The graded Canvas deliverable is a **single ZIP file** containing your Streamlit app assets, not this document. If anything here disagrees with the [assignment on Canvas](#submission), follow Canvas.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

**Audience:** Graduate students only (see syllabus weight for interactive model deployment).

---

## Assignment snapshot

**Objective:** Operationalize your machine learning model by deploying it into an **interactive Streamlit interface**.

**Deliverable:** Submit a single **ZIP file** containing your project assets: the app script, the trained model, and dependency list. See [Submission](#submission) and [Target folder structure](#target-folder-structure).

**Points:** 15

**Hosting:** Local only (`localhost`). Public deployment is **not** required; graders will run the app on their machines.

---

## Submission

- **Due:** Sunday, **June 7, 2026**, by **11:59 p.m.** (confirm time zone and any “available until” window on the assignment page).
- **Accepted file types:** **`.zip`** only (confirm on the assignment page).
- **Where to submit:** Interactive Model Deployment assignment on Canvas — upload as instructed there.

---

## Work breakdown (four parts)

Complete these in order. Parts 1–3 happen in your repo; Part 4 is packaging only.

### 1. Model serialization

In your **Phase 4 notebook** (`survivoR.ipynb` or equivalent):

- Use **`joblib`** to save your **best-performing trained model** from the ML section.
- Name the file clearly (e.g., `model.joblib` or `model.pkl`).
- Save the **same object** you would call `.predict()` on in the notebook—typically a fitted **`Pipeline`** (preprocessing + estimator), not the raw estimator alone, unless you handle preprocessing separately in the app.
- Confirm the saved artifact loads and reproduces a test prediction before moving on.

| Checkpoint | Done? |
| ---------- | ----- |
| Model saved with `joblib` from executed notebook cells | ☐ |
| Filename is clear and matches what `app.py` will load | ☐ |
| Quick load test: `joblib.load(...)` runs without error | ☐ |

### 2. Streamlit app development

Create a new Python script (e.g., `app.py`) in your project folder.

**Required imports:** `streamlit`, `pandas`, `scikit-learn`, and `joblib` (plus any others your model needs).

The script **must** include:

| Component | Requirements |
| --------- | ------------ |
| **Header section** | A clear **title** and **brief instructions** telling the user how to use the app. |
| **Input interface** | Interactive widgets (**sliders**, **text inputs**, **dropdowns**, etc.) for **every feature** required by your model. Widget types should match data types (numeric vs. categorical). |
| **Integration logic** | Load the `.joblib` file; assemble user inputs into a **`DataFrame`** (or array) with **column names and order** matching training. |
| **Prediction & output** | A trigger (e.g., **“Predict”** button) that runs the model and displays the result **clearly** (class label, value, and **probability** or confidence when applicable). |

**Path discipline:** Use **relative paths** (e.g., `Path(__file__).parent / "model.joblib"`) so the app runs after unzip on the grader’s machine—not hard-coded absolute paths.

**Run locally before packaging:**

```bash
streamlit run app.py
```

### 3. Dependency management

- Work inside your project **virtual environment** (`venv`).
- Install everything the app needs (`streamlit`, `scikit-learn`, etc.).
- Generate **`requirements.txt`** while the venv is active:

```bash
pip freeze > requirements.txt
```

- Spot-check that `requirements.txt` lists `streamlit`, `scikit-learn`, `pandas`, and `joblib` (and any version-specific packages your model requires).

### 4. Packaging

Create a **ZIP file** of your project folder.

**Include:**

- `app.py`
- `model.joblib` (or `.pkl`)
- `requirements.txt`

**Exclude:**

- Virtual environment folder (`venv`, `env`, `.venv`, etc.)
- Notebook checkpoints, `.git`, caches, and other local-only artifacts unless the assignment explicitly asks for them

**ZIP layout:** The archive should contain **one top-level folder** (e.g., `survivoR_deployment/`) with the three files inside—not loose files at the root of the ZIP, and not nested copies of your entire repo.

---

## Target folder structure

On your machine (before zipping):

```text
My_ML_Project/
│
├── venv/                  <-- DO NOT INCLUDE in ZIP
├── app.py                 <-- INCLUDE
├── model.joblib           <-- INCLUDE
└── requirements.txt       <-- INCLUDE
```

After unzip on the grader’s machine:

```text
My_ML_Project/
├── app.py
├── model.joblib
└── requirements.txt
```

Grader workflow (typical):

```bash
cd My_ML_Project
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Rubric alignment (15 points)

Use this when reviewing the ZIP before submission.

### User interface (UI) — 5 pts

| Points | Level | Description |
| ------ | ----- | ----------- |
| **5** | Complete | Includes a **descriptive title** and **clear instructions**. Input widgets are **appropriate for data types**. **Every model feature** has a corresponding input widget. |
| **3** | Partial credit | App is **functional** but instructions are **unclear or missing**, **some widgets are missing**, or widget types are **inappropriate** for the feature (e.g., free text for a bounded numeric field with no validation). |
| **0** | No credit | UI is **missing**, **unusable**, or inputs do **not** cover the features the model expects. |

### Functionality & logic — 5 pts

| Points | Level | Description |
| ------ | ----- | ----------- |
| **5** | Complete | Model **loads successfully** via `joblib`. **“Predict”** (or equivalent) **triggers the model correctly**. Prediction—and **probability** when applicable—is **displayed clearly**. |
| **3** | Partial credit | App **runs** but has **logic errors** (wrong column order/names, dtype mismatches, wrong output shape), or results are **poorly formatted** / hard to interpret. |
| **0** | No credit | App **crashes on predict**, model **fails to load**, or **no prediction path** is implemented. |

### Reproducibility — 5 pts

| Points | Level | Description |
| ------ | ----- | ----------- |
| **5** | Complete | Submission is a **ZIP** that **excludes `venv`**. Includes a **valid `requirements.txt`**. Code uses **relative paths** and runs on a fresh machine **without file-path errors**. |
| **3** | Partial credit | All **required files present**, but the app **fails on the grader’s machine** due to **hard-coded paths**, **missing libraries** in `requirements.txt`, or **wrong ZIP structure**. |
| **0** | No credit | **Wrong deliverable type**, **missing core files** (`app.py`, model artifact, or `requirements.txt`), or **cannot be run** after standard setup. |

**Total:** 15 points

---

## Pre-submit checklist

Use this list against the **ZIP** you will upload.

- [ ] **Phase 4 notebook:** best model saved with **`joblib`**; filename documented and matches the app.
- [ ] **`app.py`** exists with required imports (`streamlit`, `pandas`, `scikit-learn`, `joblib`).
- [ ] **Title and instructions** visible at the top of the Streamlit app.
- [ ] **One widget per model feature**; widget types match numeric vs. categorical data.
- [ ] User inputs assembled into a **DataFrame/array** with **training column names and order**.
- [ ] **Predict button** (or equivalent) runs without error; output is **human-readable**.
- [ ] **Probabilities or confidence** shown when the model supports them (classification).
- [ ] **`requirements.txt`** generated from an **active venv** via `pip freeze > requirements.txt`.
- [ ] **`streamlit run app.py`** works locally from the project folder (not from repo root with broken paths).
- [ ] **Relative paths only**—no `/Users/...` or machine-specific paths.
- [ ] **ZIP** contains **one folder** with `app.py`, model file, and `requirements.txt`.
- [ ] **ZIP excludes** `venv` / `env` / `.venv` and other bloat.
- [ ] Confirm Canvas **due date**, **file type** (`.zip`), and **grad-only** scope on the assignment page.
- [ ] **Sources Used** updated per [COURSE_POLICY.md](COURSE_POLICY.md) if you used AI for refinement or debugging on the app or packaging steps.

---

## Common pitfalls

| Issue | What graders see | Fix |
| ----- | ---------------- | --- |
| Saved estimator without preprocessor | Predict fails or nonsense output | Save the full **`Pipeline`** fit in Phase 4, or replicate preprocessing in `app.py`. |
| Column name mismatch | `ValueError` on predict | Match **exact** training column names; use a one-row `pd.DataFrame`. |
| Absolute paths | `FileNotFoundError` on grader machine | Load model relative to `app.py` location. |
| `venv` inside ZIP | Bloated submission; may confuse setup | Delete or exclude before zipping. |
| Stale `requirements.txt` | Import errors after `pip install -r` | Regenerate with venv active **after** all installs. |
| Missing categorical levels | Wrong encoding / silent mis-prediction | Use **`st.selectbox`** with the same categories seen in training. |

---

## Team maintenance (repo only)

**`deployment/README.md`** is grader-facing and ships inside the Canvas ZIP. Keep repo-only workflow notes here—not in that file.

### Refresh the model

After re-running the bundle cells in `survivoR.ipynb`:

1. Confirm `deployment/model.joblib` was written.
2. Restart Streamlit (or clear cache) so the app loads the new artifact.

### Refresh requirements

Only after changing installed packages, with `deployment/venv` active:

```bash
cd deployment
pip freeze > requirements.txt
```

Keep `scikit-learn` aligned with the version used when the model was saved (currently **1.8.0**).

### Create the Canvas ZIP

From the repo root, zip the `deployment/` folder without the virtual environment:

```bash
zip -r survivoR_deployment.zip deployment \
  -x "deployment/venv/*" -x "deployment/env/*" -x "deployment/__pycache__/*" -x "*.DS_Store"
```

The archive should contain one top-level folder (`deployment/`) with at least `app.py`, `model.joblib`, and `requirements.txt`.

---

## Appendix (optional team notes)

Fill in as your deployment takes shape. Keep user-facing copy in **`app.py`**, not in **`deployment/README.md`**.

| Note | Details |
| ---- | ------- |
| Model file name | *(e.g., `model.joblib`)* |
| Saved object type | *(e.g., `Pipeline(steps=[...])` vs. bare `RandomForestClassifier`)* |
| Feature list for UI | *(column names in **X**—one widget each)* |
| Widget mapping | *(e.g., `age` → slider 18–80; `tribe` → selectbox with training categories)* |
| Target / output labels | *(e.g., “Predicted winner: Yes/No” + probability)* |
| Phase 4 link | *(which notebook cells produced the saved model)* |
| Local test command | *(e.g., `streamlit run app.py` from `My_ML_Project/`)* |
| ZIP folder name | *(exact top-level folder name inside the archive)* |
