# Survivor Winner Predictor

Streamlit app for the Phase 4 random forest winner-classification model.

## Files

| File | Purpose |
| ---- | ------- |
| `app.py` | Streamlit UI |
| `model.joblib` | Trained model, label encoder, feature bounds, and threshold |
| `requirements.txt` | Python dependencies |

## Run locally

From this folder:

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).
