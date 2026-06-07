"""Streamlit app for Survivor winner classification."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
import sklearn.ensemble  # required import per assignment
from sklearn.calibration import CalibratedClassifierCV  # supports calibrated saved models
import streamlit as st


APP_DIR = Path(__file__).parent
MODEL_PATH = APP_DIR / "model.joblib"
LOGO_PATH = APP_DIR / "survivor_logo.png"

FEATURE_LABELS = {
    "immunity_wins_per_day": "Immunity wins per day",
    "reward_wins_per_day": "Reward wins per day",
    "idols_per_day": "Idols per day",
    "votes_per_day": "Votes per day",
    "season_year": "Season year",
    "personality_type": "Personality type (MBTI)",
}

FEATURE_HELP = {
    "immunity_wins_per_day": (
        "A normalized challenge metric. Higher values mean more immunity wins "
        "per day survived."
    ),
    "reward_wins_per_day": (
        "A normalized challenge metric. Higher values mean more reward wins "
        "per day survived."
    ),
    "idols_per_day": (
        "A normalized advantage metric. Higher values mean more idols found "
        "per day survived."
    ),
    "votes_per_day": (
        "A normalized social-risk metric. Higher values mean more votes "
        "received per day survived."
    ),
    "season_year": "The year of the Survivor season.",
}


@st.cache_resource
def load_artifact():
    """Load the model bundle once and cache it for the Streamlit session."""
    return joblib.load(MODEL_PATH)


def get_numeric_input(col, bounds, contestant_index):
    """Create a Streamlit numeric widget for a model feature."""
    label = FEATURE_LABELS.get(col, col)
    help_text = FEATURE_HELP.get(col)

    min_value = bounds["min"]
    max_value = bounds["max"]
    default_value = bounds["default"]

    if col == "season_year":
        return st.slider(
            label,
            min_value=int(round(min_value)),
            max_value=int(round(max_value)),
            value=int(round(default_value)),
            step=1,
            help=help_text,
            key=f"{col}_{contestant_index}",
        )

    return st.slider(
        label,
        min_value=float(min_value),
        max_value=float(max_value),
        value=float(default_value),
        step=0.01,
        help=help_text,
        key=f"{col}_{contestant_index}",
    )


def build_contestant_inputs(feature_columns, feature_bounds, encoder, n_players):
    """Collect inputs for each contestant and return names plus model rows."""
    all_rows = []
    contestant_names = []

    for i in range(n_players):
        with st.expander(f"Contestant {i + 1}", expanded=(i == 0)):
            name = st.text_input(
                "Contestant name",
                value=f"Player {i + 1}",
                key=f"name_{i}",
            )

            row = {}

            for col in feature_columns:
                if col == "personality_type":
                    mbti_value = st.selectbox(
                        FEATURE_LABELS[col],
                        options=sorted(encoder.classes_),
                        key=f"personality_type_{i}",
                    )
                    row[col] = encoder.transform([mbti_value])[0]
                else:
                    row[col] = get_numeric_input(
                        col,
                        feature_bounds[col],
                        contestant_index=i,
                    )

            contestant_names.append(name)
            all_rows.append(row)

    input_df = pd.DataFrame(all_rows)[feature_columns]

    return contestant_names, input_df


# Page setup
st.set_page_config(
    page_title="Survivor Winner Predictor",
    page_icon="🔥",
    layout="wide",
)

# Load model artifact
try:
    artifact = load_artifact()
except Exception as exc:
    st.error(f"Error loading model artifact: {exc}")
    st.stop()

try:
    model = artifact["model"]
    encoder = artifact["encoder"]
    feature_columns = artifact["feature_columns"]
    feature_bounds = artifact["feature_bounds"]
    threshold = artifact["threshold"]
except Exception as exc:
    st.error(f"Error unpacking model artifact: {exc}")
    st.stop()

# Header
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=500)

st.title("Survivor Winner Predictor")

st.write(
    "Build a small cast of Survivor contestants, enter their end-of-season "
    "gameplay profile, and click **Predict Winner**. The app ranks the cast "
    "by how winner-like each contestant looks to the Phase 4 Random Forest model."
)

st.caption(
    "This is a local classroom deployment. The model uses post-game statistics, "
    "so it should be read as an exploratory profile tool, not a real preseason "
    "prediction engine."
)

with st.expander("How to read this app"):
    st.write(
        "- **Raw model probability** is the model's direct probability estimate "
        "for each contestant."
    )
    st.write(
        "- **Relative cast chance** normalizes those probabilities across the "
        "contestants you entered, which makes the output easier to compare."
    )
    st.write(
        "- Because Survivor has only one winner per season, the model is better "
        "at ranking winner-like profiles than guaranteeing who would actually win."
    )

# Inputs
st.subheader("Contestant Inputs")

n_players = st.slider(
    "Number of contestants",
    min_value=2,
    max_value=18,
    value=6,
    step=1,
)

names, input_df = build_contestant_inputs(
    feature_columns=feature_columns,
    feature_bounds=feature_bounds,
    encoder=encoder,
    n_players=n_players,
)

# Prediction
if st.button("Predict Winner", type="primary"):
    try:
        probabilities = model.predict_proba(input_df)[:, 1]
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
        st.stop()

    probability_sum = probabilities.sum()

    if probability_sum > 0:
        relative_chances = probabilities / probability_sum
    else:
        relative_chances = np.repeat(1 / len(probabilities), len(probabilities))

    results = pd.DataFrame(
        {
            "Contestant": names,
            "Raw model probability": probabilities,
            "Relative cast chance": relative_chances,
        }
    ).sort_values(
        by="Relative cast chance",
        ascending=False,
    ).reset_index(drop=True)

    winner_name = results.loc[0, "Contestant"]
    winner_chance = results.loc[0, "Relative cast chance"]
    winner_raw_probability = results.loc[0, "Raw model probability"]

    st.divider()
    st.success(f"{winner_name} is the model's most likely winner in this cast.")

    metric_left, metric_right = st.columns(2)

    with metric_left:
        st.metric("Relative cast chance", f"{winner_chance:.1%}")

    with metric_right:
        st.metric("Raw model probability", f"{winner_raw_probability:.1%}")

    st.subheader("Full Cast Rankings")

    st.dataframe(
        results.style.format(
            {
                "Raw model probability": "{:.1%}",
                "Relative cast chance": "{:.1%}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"The Phase 4 tuned winner threshold was {threshold:.0%}. "
        "This app ranks contestants within the entered cast, so the relative "
        "cast chance is usually more useful than reading the raw probability alone."
    )