# Survivor winner predictor (Streamlit)

Interactive deployment for the Phase 4 random forest model. Grad assignment spec: [docs/INTERACTIVE_MODEL_DEPLOYMENT.md](../docs/INTERACTIVE_MODEL_DEPLOYMENT.md).

## Contents

| File | Purpose |
| ---- | ------- |
| `app.py` | Streamlit UI |
| `model.joblib` | Fitted model, label encoder, feature bounds, and 0.20 threshold |
| `requirements.txt` | Pinned deps for local run and Canvas ZIP |

Do **not** commit or zip `venv/` — create it locally only.

## Run locally

From this folder (`deployment/`):

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501). Adjust sliders, choose an MBTI type, and click **Predict**.

## Refresh the model

After re-running the bundle cells in `survivoR.ipynb`:

1. Confirm `model.joblib` was written to this folder.
2. Restart Streamlit (or clear cache) so the app loads the new artifact.

## Refresh requirements

Only after changing installed packages, with `venv` active:

```bash
pip freeze > requirements.txt
```

Keep `scikit-learn` aligned with the version used when the model was saved (currently **1.8.0**).

## Canvas ZIP

From the repo root, zip the folder without the virtual environment:

```bash
zip -r survivoR_deployment.zip deployment \
  -x "deployment/venv/*" -x "deployment/__pycache__/*" -x "*.DS_Store"
```

The archive should contain `deployment/app.py`, `deployment/model.joblib`, and `deployment/requirements.txt`.
