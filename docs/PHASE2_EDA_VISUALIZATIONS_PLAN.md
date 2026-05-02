# Phase 2: EDA & Visualizations — Implementation Plan

**Companion to [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md)** (the rubric / submission summary). This file is the **shared development plan** for the EDA section of the working notebook. It defines the analysis frame, where each column comes from, how it’s built, and how it powers the required visuals.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — graded artifacts, honor code, **Sources Used** when using AI for refinement or debugging, and PEP 8 for Python.

---

## Goal

Produce a **single, narrow, contestant-grain DataFrame** (`analysis_df`) that supports:

- The Phase 2 statistical requirements (mean, median, std, correlations).
- A **correlation heatmap**.
- An **MBTI personality trends over time** chart.
- One additional visual (TBD by team).

Project questions this frame is built to answer:

- What does it take to **Outwit, Outplay, Outlast**?
- What decisions do **winners** make? What about **losers**?
- How have those decisions changed as the game has evolved?
- Are there **trends** or **qualities** that predict performance?
- Have those trends/qualities changed over time?

---

## Final analysis frame

- **Name:** `analysis_df`
- **Grain:** one row per **contestant per season**
- **Approximate size:** ~744 rows × ~13 columns

### Columns (origin and transformation)

| Column | Type | Source table | How it’s produced |
|---|---|---|---|
| `season` | int | `clean_castaways_df` | Passthrough; merge key. |
| `castaway` | str | `clean_castaways_df` | Passthrough (short / show name). |
| `full_name` | str | `clean_castaways_df` | Passthrough; used for labels and tie-breaks. |
| `personality_type` | str | `clean_castaways_df` | Passthrough; `UNKNOWN` already imputed in cleaning. |
| `mbti_ei`, `mbti_sn`, `mbti_tf`, `mbti_jp` *(optional)* | str | derived from `personality_type` | Letters 1–4 of the MBTI code; `NaN` where `personality_type == "UNKNOWN"`. |
| `order` | int | `clean_castaways_df` | Passthrough — longevity rank within season. |
| `day` | int | `clean_castaways_df` | Passthrough — days survived. |
| `total_votes_received` | int | `clean_castaways_df` | Passthrough — social-risk proxy. |
| `immunity_idols_obtained` | int | `clean_castaways_df` | Renamed from `immunity_idols_won`; mechanism-neutral count of idols a contestant came to hold (found, gifted, traded, etc.). |
| `immunity_challenge_wins` | int | aggregated `challenges_cleaned_df` | Per-contestant count of `challenge_type == "immunity"` wins. |
| `reward_challenge_wins` | int | aggregated `challenges_cleaned_df` | Per-contestant count of `challenge_type == "reward"` wins. |
| `is_winner` | bool | derived from `summary_df.winner` | `True` where normalized `castaway == winner` for that season; **exactly one** `True` row per season. |
| `season_year` | int | `summary_df.premiered` | `premiered.dt.year`. |

### Variable groups (mapped to project questions)

- **Identity:** `season`, `castaway`, `full_name`
- **Personality (MBTI):** `personality_type` (+ optional letter flags)
- **Outlast:** `order`, `day`
- **Outwit:** `total_votes_received`, `immunity_idols_obtained`
- **Outplay:** `immunity_challenge_wins`, `reward_challenge_wins`
- **Outcome label:** `is_winner`
- **Evolution axis:** `season_year`

### What is intentionally **not** in this frame

- Viewer / rank / filming / location / tribe-setup columns from `summary_df`. They are either **constant per season** (clutter at contestant grain) or **partially missing**. They stay on `summary_df` and get merged in **only** when a specific season-level chart needs them.
- `winner` from `summary_df` after `is_winner` is computed (drop to avoid an ambiguous helper column).
- Tribe-level challenge wins (`winning_tribe`) — that data is **tribe grain**, not contestant grain, and would require tracking tribe membership over time. Out of scope for the minimal frame.
- Row-level fields from `challenges_cleaned_df` (`episode`, `day`, `winning_tribe`, etc.) — collapsed away by aggregation.

---

## Build plan

### Step 1 — Aggregate challenges to contestant grain

From `challenges_cleaned_df`:

1. Filter out non-individual rows: drop where `winners == "No challenge winner"`.
2. Group by `["season", "winners", "challenge_type"]` and count rows.
3. Pivot `challenge_type` to columns named `immunity_challenge_wins` and `reward_challenge_wins`.
4. Reset the index and rename `winners → castaway`.
5. Result: a small lookup table with `season`, `castaway`, `immunity_challenge_wins`, `reward_challenge_wins`.

### Step 2 — Build a slim season metadata table

From `summary_df`:

1. Select only `["season", "winner", "premiered"]`.
2. Derive `season_year = premiered.dt.year`; drop `premiered`.
3. Result: `season_meta` with `season`, `winner`, `season_year`.

### Step 3 — Start the analysis frame from castaways

From `clean_castaways_df` keep only:

`season`, `castaway`, `full_name`, `personality_type`, `order`, `day`, `total_votes_received`, `immunity_idols_won`.

Then:

- Rename `immunity_idols_won → immunity_idols_obtained`.

### Step 4 — Merge

1. Left-merge `season_meta` on `season`.
2. Left-merge the aggregated challenge table on `["season", "castaway"]`.
3. `fillna(0)` on `immunity_challenge_wins` and `reward_challenge_wins`, cast to `int` (a true zero is the right value for “did not win any”).

### Step 5 — Derive the winner label

1. Normalize both sides: `str.strip().str.casefold()` on `castaway` and `winner`.
2. `is_winner = normalized_castaway == normalized_winner`.
3. **QA check:** assert each `season` has **exactly one** `True` row; print any season with 0 or >1 matches and patch only those.
4. Drop `winner` after the boolean is set.

### Step 6 — (Optional) MBTI letter flags

Only if the dimension-level views are needed:

- `mbti_ei = personality_type.str[0]` (and `[1]`, `[2]`, `[3]` for the other letters).
- Set to `NaN` where `personality_type == "UNKNOWN"`.

### Step 7 — Final QA (one cell, one screen)

- `analysis_df.info()` — verify dtypes and non-nulls.
- `analysis_df["season"].value_counts().sort_index()` — sanity check rows per season.
- `analysis_df.groupby("season")["is_winner"].sum()` — should be `1` for every covered season.
- `analysis_df[["order", "day", "total_votes_received", "immunity_idols_obtained", "immunity_challenge_wins", "reward_challenge_wins"]].describe()` — quick numeric sanity.

---

## Statistical outputs (Phase 2 rubric)

Compute and present clearly with pandas:

- **Per-MBTI-type summaries:** mean / median / std for `order`, `day`, `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins`.
- **Winner vs non-winner summaries:** same metrics grouped by `is_winner`.
- **Era / time summaries:** same metrics grouped by `season_year` bins (or `season`) for evolution observations.
- **Correlation matrix:** focused on the numeric and boolean columns above (not a wall of raw output).

Tie each table to a Markdown observation referencing the relevant figure.

---

## Visualization plan (3 required)

### A) Correlation heatmap

- Use the numeric + boolean columns of `analysis_df`.
- Add clear axis labels and a colorbar; annotate cells if size allows.
- In observations, call out at least one **expected** and one **surprising** relationship.

### B) MBTI trends over time

- X-axis: `season_year` (or `season`).
- Y-axis: share of castaways (or share of finalists / winners) by `personality_type` or by an MBTI letter dimension.
- Use line(s) with a legend; consider rolling average to reduce noise.

### C) Third visual (TBD)

Strong candidates that fit this frame without extra joins:

- Box / violin plot of `order` by `personality_type` (or by E/I, S/N, etc.).
- Stacked bar of personality mix for winners vs non-winners by era.
- Scatter of `age` vs `order`, colored by `is_winner` *(requires keeping `age` from castaways — add to Step 3 if used)*.

Pick whichever best supports the team’s narrative; document the choice in observations.

---

## Caveats to surface in observations

- `personality_type == "UNKNOWN"` was imputed during cleaning; treat those rows carefully in MBTI-only summaries.
- `immunity_idols_obtained` is mechanism-neutral and does **not** equal `immunity_challenge_wins`. The two columns can both be high, both be zero, or move independently.
- Winners are rare (≤ 1 per season), so per-MBTI-type win rates have small sample sizes.
- Any season missing from `summary_df` will end up with `NaN` `season_year` (and won’t contribute to time-trend visuals); document the covered range explicitly.
- Personality labels in this dataset are **metadata**, not clinical MBTI assessments.

---

## How to contribute

1. Read this plan and [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) (rubric).
2. Build / extend `analysis_df` per the steps above; do not add columns outside the table without team agreement.
3. Run the **Final QA** cell after any change to the frame.
4. Add a Markdown observation alongside every new statistic or visual.
5. Update **Sources Used** in the notebook per [COURSE_POLICY.md](COURSE_POLICY.md) when AI assists with refinement or debugging.
