"""Streamlit app for Survivor winner classification."""

from pathlib import Path

import joblib
import pandas as pd
import sklearn.ensemble  # required import per assignment
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
    "Adjust the inputs below to describe a contestant's end-of-season profile, "
    "then click **Predict** to estimate their probability of winning."
)
st.caption(
    "This model uses gameplay and social stats collected after a season unfolds; "
    "it describes winner-like profiles, not preseason forecasts."
)

# Build the user inputs dataframe
user_inputs = {}
for col in feature_columns:
    if col == "personality_type":
        continue

    bounds = feature_bounds[col]
    label = FEATURE_LABELS.get(col, col)

    if col == "season_year":
        user_inputs[col] = st.slider(
            label,
            min_value=bounds["min"],
            max_value=bounds["max"],
            value=bounds["default"],
            step=1,
        )
    else:
        user_inputs[col] = st.slider(
            label,
            min_value=bounds["min"],
            max_value=bounds["max"],
            value=bounds["default"],
            step=0.01,
        )

# Provide a selectbox for the personality type
personality_type = st.selectbox(
    "Personality type (MBTI)",
    options=sorted(encoder.classes_),
)

# On predict button click:
if st.button("Predict"):
    # Encode the personality type
    user_inputs["personality_type"] = encoder.transform([personality_type])[0]
    # Build the dataframe
    row = pd.DataFrame([user_inputs])[feature_columns]

    # Predict the probability
    probability = model.predict_proba(row)[0, 1]
    # Determine if the contestant is a winner
    is_winner = probability >= threshold

    # Display the prediction and probability
    st.divider()
    st.success(f"Prediction: {'Winner' if is_winner else 'Not Winner'}")
    st.metric("Probability of winner", f"{probability:.1%}")
    st.caption(f"Decision threshold: {threshold:.0%} (from Phase 4 tuning)")
