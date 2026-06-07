"""Streamlit app for Survivor winner classification."""

from pathlib import Path

import joblib
import pandas as pd
import sklearn.ensemble  # required import per assignment
from sklearn.calibration import CalibratedClassifierCV
import streamlit as st


MODEL_PATH = Path(__file__).parent / "model.joblib"

FEATURE_LABELS = {
    "immunity_wins_per_day": "Immunity wins per day",
    "reward_wins_per_day": "Reward wins per day",
    "idols_per_day": "Idols per day",
    "votes_per_day": "Votes per day",
    "season_year": "Season year",
}

# Cache the artifact to avoid reloading it on every predict button click
@st.cache_resource
def load_artifact():
    return joblib.load(MODEL_PATH)

# Try to load the artifact, if it fails, show an error and stop the app
try:
    artifact = load_artifact()
except Exception as exc:
    st.error(f"Error loading model: {exc}")
    st.stop()

# Unpack the artifact, if it fails, show an error and stop the app
try:
    model = artifact["model"]
    encoder = artifact["encoder"]
    feature_columns = artifact["feature_columns"]
    feature_bounds = artifact["feature_bounds"]
    threshold = artifact["threshold"]
except Exception as exc:
    st.error(f"Error unpacking artifact: {exc}")
    st.stop()

# Header and instructions
st.title("Survivor Winner Predictor")
st.write(
    "Enter stats for each contestant, then click Predict to see who the model thinks will win."
)
st.caption(
    "This model uses gameplay and social stats collected after a season unfolds; "
    "it describes winner-like profiles, not preseason forecasts."
)

st.image("survivor_logo.png", use_container_width=True)

n_players = st.slider("Number of contestants", min_value=2, max_value=18, value=6)

all_inputs = []
for i in range(n_players):
    with st.expander(f"Contestant {i+1}", expanded=(i==0)):
        player = {}
        player["name"] = st.text_input("Name", value=f"Player {i+1}", key=f"name_{i}")
        for col in feature_columns:
            if col == "personality_type":
                continue
            bounds = feature_bounds[col]
            label = FEATURE_LABELS.get(col, col)
            step = 1 if col == "season_year" else 0.01
            player[col] = st.slider(label, min_value=bounds["min"], max_value=bounds["max"],
                                    value=bounds["default"], step=step, key=f"{col}_{i}")
        player["personality_type"] = encoder.transform([
            st.selectbox("Personality type (MBTI)", options=sorted(encoder.classes_), key=f"mbti_{i}")
        ])[0]
        all_inputs.append(player)

if st.button("Predict"):
    names = [p.pop("name") for p in all_inputs]
    df = pd.DataFrame(all_inputs)[feature_columns]

    # Get winner probabilities for all players
    probs = model.predict_proba(df)[:, 1]
    st.write(df)        # check the input dataframe looks correct
    st.write(probs)     # check raw probabilities before normalization

    results = pd.DataFrame({
        "Contestant": names,
        "Win Probability": probs
    }).sort_values("Win Probability", ascending=False).reset_index(drop=True)

    results["Win Probability (Normalized)"] = results["Win Probability"] / results["Win Probability"].sum()

    st.success(f"{results.iloc[0]['Contestant']} is most likely to win!")

    st.subheader("Full Cast Rankings")
    st.dataframe(
        results[["Contestant", "Win Probability (Normalized)"]].style.format(
            {"Win Probability (Normalized)": "{:.1%}"}
        )
    )
