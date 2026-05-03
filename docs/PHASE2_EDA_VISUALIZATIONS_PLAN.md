# Phase 2: EDA & Visualizations — Implementation Plan

**Companion:** [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) (rubric). **Policy:** [COURSE_POLICY.md](COURSE_POLICY.md).

---

## Assumptions & changes (vs prior plan)

| Change | Rationale |
|--------|-----------|
| **`analysis_df` is the only input** to statistical summaries and to every visual pipeline. | Single source of truth; avoids divergent filters or merges. |
| **Two visuals are already implemented** in the working notebook (Emma: era / winner outplay bars; Simeon: MBTI-letter × metrics heatmap). | Treat them as fixed first-class outputs—do not add a second “generic” correlation heatmap or duplicate era/winner challenge logic elsewhere. |
| **Initial statistics precede and justify visuals.** | All tables (mean / median / std / correlations) are computed from `analysis_df` only; visuals reference those numbers in Markdown. |
| **Third visual (new)** | Fills the **social / outwit** gap (vote exposure), completing the story next to **era + outplay/idols** (Emma) and **personality × normalized performance** (Simeon). |
| **“MBTI trends over time” line chart** from the old plan | **Not** implemented and **not** required if the third visual below is adopted—avoids two time-series personality charts and keeps scope tight. |

---

## Goal

Support Phase 2 rubric (summaries + **3 diverse** embedded plots) using one contestant-grain frame and a repeatable pipeline per figure.

**Project questions the frame supports:** Outwit / Outplay / Outlast; winner vs non-winner; evolution over time.

---

## Data: `analysis_df` (SSOT)

- **Grain:** one row per contestant per season (~744 rows).
- **Build:** unchanged from team notebook: castaways + season meta + aggregated challenge wins + `is_winner` + `season_year`. Final QA (`info`, rows per season, exactly one winner per season, `describe` on numeric gameplay columns) stays in one cell after construction.

**Column groups (for stats and transforms):**

- Identity: `season`, `castaway`, `full_name`
- Personality: `personality_type`
- Outlast: `order`, `day`
- Outwit: `total_votes_received`, `immunity_idols_obtained`
- Outplay: `immunity_challenge_wins`, `reward_challenge_wins`
- Outcome / time: `is_winner`, `season_year`

**Caveats** (surface in observations): `UNKNOWN` MBTI; idols ≠ immunity wins; ≤1 winner per season; `season_year` NaN if season missing from summary; personality is metadata not clinical assessment.

---

## Step 0 — Statistical foundation (from `analysis_df` only)

Run **before** any visualization code. Use these outputs to guide plot choices and Markdown (cite specific numbers next to each figure).

1. **Global:** `mean`, `median`, `std` for  
   `order`, `day`, `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins`  
   (`analysis_df[list].agg(["mean", "median", "std"])` or equivalent).
2. **By `is_winner`:** same metrics grouped by winner flag (table).
3. **By era or `season_year`:** same metrics grouped by bins aligned to team era definitions **or** simple decade—pick one and stay consistent with Visual 1’s era labels if you add a stats row for “era.”
4. **Correlations:** focused numeric matrix on the gameplay + longevity columns above (and optionally `is_winner` as 0/1). Present as a **small table** or heatmap **in the statistics section only** if desired—the **submitted** correlation *figure* for the notebook is Visual 2 below (MBTI-focused heatmap), not a duplicate full-variable heatmap.

**Rule:** No visual cell computes its own “global” summary statistics for rubric credit—those live in Step 0. Per-visual transforms may compute aggregates **only** for that plot (e.g., groupby for era means).

---

## Visual pipeline pattern (all figures)

For each visual:

1. Start from `analysis_df.copy()`.
2. Apply **documented** filters and derived columns → name the result `transformed_df` (or a descriptive name: `outplay_analysis_df`, `mbti_heatmap_df`, `votes_by_outcome_df`, etc.).
3. Plot **only** from that transformed frame.
4. In Markdown: state the **question**, tie to **Step 0** statistics, and note **caveats**.

---

## Visual 1 — Implemented (Emma): Era × winner outplay profile

| Item | Definition |
|------|------------|
| **Question** | How do mean immunity wins, reward wins, and idols obtained differ between **winners and non-winners** across **eras** of the show? |
| **Transform** (`outplay_analysis_df`) | From `analysis_df`: exclude agreed re-entry seasons; sort by `season`; `pd.cut` on `season_year` to era labels; `groupby(["era", "is_winner"])` → **mean** of `immunity_challenge_wins`, `reward_challenge_wins`, `immunity_idols_obtained`; set pre-idol era idol mean to 0 for clarity. |
| **Output** | One figure: **three barplots** (shared era × hue=`is_winner`), titles/labels/legend per rubric. |
| **Stats link** | Use Step 0 winner vs non-winner and era-group tables to justify expecting gaps; cite sample-size imbalance (few winners per era). |

**Do not duplicate:** a second “mean challenges by era” chart with different season exclusions—keep one authoritative version here.

---

## Visual 2 — Implemented (Simeon): MBTI letters × performance correlation heatmap

| Item | Definition |
|------|------------|
| **Question** | Do **MBTI letter dimensions** (E/I, N/S, T/F, J/P as binary flags) correlate with **winner status** and **time-adjusted** gameplay signals? |
| **Transform** (`mbti_heatmap_df`) | From `analysis_df`: drop `personality_type == "UNKNOWN"`; add `is_extrovert`, `is_intuitive`, `is_thinking`, `is_judging` (0/1); `winner_flag`; `survival_pct` (order / season max order); `votes_per_day`, `idols_per_day`, `immunity_wins_per_day`, `reward_wins_per_day` (numerators with `day.clip(lower=1)`); correlation block between letter flags and metrics; subset rows/columns for heatmap; optional friendly rename for display. |
| **Output** | **One heatmap** (annotated, labeled colorbar). |
| **Stats link** | Quote Step 0 correlation table for raw numeric relationships; use this figure for **personality-sliced** structure and normalized rates. |

**Do not duplicate:** a separate full-dataset correlation heatmap of the same MBTI×metric cells, or a second notebook section that re-derives the same matrix with different filters.

---

## Visual 3 — Proposed (e.g., Jarren / remaining slot): Vote exposure by outcome

| Item | Definition |
|------|------------|
| **Question** | Do **winners** accumulate **more or less vote exposure** than non-winners after accounting for how long they played? (Outwit / social heat—orthogonal to Emma’s challenge/idol means and Simeon’s personality correlation grid.) |
| **Transform** (`votes_by_outcome_df`) | From `analysis_df`: `votes_per_day = total_votes_received / day.clip(lower=1)` (same definition as Visual 2 for consistency); optional winsorize or cap extreme `votes_per_day` for readability **or** use raw `total_votes_received` with `day` as hue/size—pick one approach and document it. Keep all MBTI types (no `UNKNOWN` drop required here). |
| **Output** | **One** of: **violin or box plot** of `votes_per_day` by `is_winner` (x = outcome, y = rate); or **strip/swarm** with jitter if counts allow. Title/axis/legend per rubric. |
| **Stats link** | Compare medians/means from Step 0’s `total_votes_received` (and optionally `day`) by `is_winner`; state whether distributions overlap or separate. |
| **Why it complements** | Emma emphasizes **physical/idol** outplay over time; Simeon emphasizes **personality × normalized rates**; this visual emphasizes **social targeting** vs **outcome** without repeating era bins or MBTI correlation layout. |

**Alternatives** (only if the team prefers—still one third figure): hexbin `day` × `total_votes_received` colored or faceted by `is_winner`; or KDE of `order` by `is_winner`. Avoid a third bar chart of era means for metrics already in Visual 1.

---

## Implementation order (minimal ambiguity)

1. Build / load `analysis_df` → QA cell.
2. **Step 0** statistics cell(s) — all from `analysis_df`.
3. Visual 1 code → Markdown observations (reference Step 0).
4. Visual 2 code → Markdown observations (reference Step 0).
5. Visual 3: implement `votes_by_outcome_df` pipeline → plot → Markdown.

---

## Contribution checklist

- [ ] No duplicate logic between Visual 1 and any other era/winner bar chart.
- [ ] No second MBTI×metric correlation figure competing with Visual 2.
- [ ] Third plot is a **different chart type** from the other two (bars + heatmap + box/violin/scatter satisfies “diverse”).
- [ ] Restart kernel, run all, update **Sources Used** per policy if AI assisted.

---

## How to contribute

1. Read this plan and the rubric doc.
2. Extend `analysis_df` only via agreed team steps; rerun QA after frame changes.
3. Each new statistic or figure gets Markdown that cites Step 0 where relevant.
