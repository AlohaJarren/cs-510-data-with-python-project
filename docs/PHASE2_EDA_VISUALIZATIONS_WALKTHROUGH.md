# Phase 2 EDA — Implementation walkthrough

**Purpose:** Step-by-step guide to implement Phase 2 statistics and visualizations in the working notebook (`survivoR.ipynb`) in a **simple, clean order**: fix the analysis frame → compute required summary statistics → run focused investigations → embed figures that illustrate each investigation.

**Companion docs:**

- [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) — Canvas rubric (what must appear in the notebook).
- [PHASE2_EDA_VISUALIZATIONS_PLAN.md](PHASE2_EDA_VISUALIZATIONS_PLAN.md) — how `analysis_df` is built and the three required visual types.
- [PHASE2_EDA_OUTLINE.md](PHASE2_EDA_OUTLINE.md) — hypotheses, correlation snapshot, era tables, and caveats to verify in the notebook.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — document **Sources Used** when AI assists with refinement or implementation scaffolding.

---

## 1. Principles (keep the notebook readable)

1. **One table or figure → one Markdown paragraph** that states the claim and the limitation (small winner *n*, mechanical correlations, etc.).
2. **Do not paste this walkthrough’s numbers as final truth** — recompute in the notebook; treat the outline as hypotheses until your cells reproduce them.
3. **Separate three ideas** the outline already distinguishes:
   - **Longevity** (`order`, `day`): almost the same signal (*r* ≈ 0.96); both correlate with `is_winner` largely because winners *must* reach the end.
   - **Outwit / Outplay behaviors** (votes, idols, challenge wins): interpret these with care when comparing winners to everyone else, because several metrics **grow with time in the game**.
   - **Composition over time** (casting / MBTI mix): a different question from “what predicts winning.”

---

## 2. Step 0 — Analysis frame fixes (do this first)

Complete these before summary statistics and plots that involve winners or cross-season comparisons.

### 2.1 Season 38 — two winner rows (Chris Underwood / Edge)

**Problem:** Two rows share `is_winner == True` for season 38 (different `order` / `day` for the same person’s arc). Any `groupby("season")["is_winner"].sum()` or winner count breaks the “one winner per season” QA described in the build plan.

**Team decision (pick one and document in Markdown):**

| Option | Behavior | Downstream effect |
|--------|----------|-------------------|
| **A. Collapse** | Keep a single analysis row per contestant-season for the *winning* appearance only (or drop the non-winning appearance for that season). | Restores one `True` per season; simplest for winner-only trends. |
| **B. Flag** | Add `re_entered` (or similar); keep both rows; exclude one from winner aggregations using the flag. | Preserves full history; requires consistent filters in every winner plot. |
| **C. Keep both, no flag** | Document that season 38 has two winner flags. | Fastest but confusing for readers; not recommended unless required for data integrity. |

**Implementation hint:** Whatever you choose, add **one short Markdown cell** titled “Season 38 handling” so graders and teammates see the rule immediately.

### 2.2 Cast size per season

```text
cast_size = analysis_df.groupby("season")["season"].transform("count")
```

(or equivalent). Use this for normalized placement (below).

### 2.3 Normalized placement — `order_norm`

**Why:** `order` runs 1 … *N* where *N* varies by cast size (~16–20). Raw `order` is not comparable across seasons at the same “depth” in the game.

**Definition (recommended):**

```text
order_norm = order / cast_size
```

Values near **1** mean last boots / winner territory; values near **1/cast_size** mean first out. **Caption the formula** in the notebook so readers know whether 1 = best or worst placement (your narrative should fix the direction once).

**Alternative:** percentile within season — heavier to explain; `order / cast_size` is enough for Phase 2.

### 2.4 Normalized time in game — `day_norm`

**Why:** Calendar days in the game differ by era (e.g. longer classic seasons vs shorter modern formats). Raw `day` confounds “played well” with “season was long.”

**Definition (practical, data-driven):**

```text
day_norm = day / day.groupby(season).transform("max")
```

Each season’s last day is scaled to 1.0 for that season.

**Citation:** Add one sentence in the notebook citing where season length / format changes are documented (e.g. official season summaries, or a reputable secondary source such as Wikipedia’s per-season “Days” field — label it as secondary if used).

### 2.5 Optional: tenure-adjusted rates (for stronger claims)

If you compare winners to non-winners on **challenge wins** or **idols**, optionally add:

```text
imm_wins_per_day = immunity_challenge_wins / day.clip(lower=1)
rew_wins_per_day = reward_challenge_wins / day.clip(lower=1)
```

(or use `day_norm` in the denominator after scaling). **Always state** that dividing by `day` partially controls for survival time but does not prove causation.

### 2.6 Dropping vs keeping `order` and `day`

| Keep in `analysis_df`? | Recommendation |
|-------------------------|----------------|
| Raw `order`, `day` | **Yes** for QA, within-season plots, and reproducing the build plan. |
| Both in every correlation heatmap | **No** — redundant story; include at most **one** longevity column in the primary heatmap, or use `order_norm` / `day_norm` only in a **secondary** “structure of the data” figure. |
| For logistic / predictive models | **Exclude** raw `order` and `day` from features if the target is `is_winner` (otherwise **leakage**). |

### 2.7 `personality_type == "UNKNOWN"`

Three rows use an imputed sentinel. **Exclude from MBTI-only plots** or show them explicitly — do not drop silently without a footnote.

### 2.8 Era variable (`era`)

Bin `season_year` (or `season`) into **3–4 eras**. Align at least one boundary with **game structure**:

- **Idols introduced Season 11** — pre-idol vs post-idol eras behave differently for `immunity_idols_obtained` (structural zeros early).

Example bins (adjust labels to match your narrative):

| Era label | Years (approx.) | Notes |
|-----------|-----------------|--------|
| Pre-idol / classic | 2000–2004 | Very low idol counts by rule |
| Early idol | 2005–2009 | Idols + still relatively long seasons |
| Mid / twist growth | 2010–2014 | |
| Modern | 2015–2020 | Shorter seasons, more twists in some years |

**Citation:** Same as season length — one line on why eras are split (format + idol rules).

---

## 3. Part A — Required statistics (rubric)

[PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) requires **mean**, **median**, **standard deviation**, and **correlations**, computed with pandas and **presented clearly** (not an unreadable dump).

### 3.1 Block 1 — Global descriptive statistics

**Columns:** At minimum:

- `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins`
- Plus **one** longevity summary: prefer `order_norm` or `day_norm` after Step 0 (avoid repeating raw `order` and `day` in every table).

**Output:** One `DataFrame.describe()` or a small custom table with **mean**, **median** (50%), **std** for each column.

**Markdown:** One paragraph on skew (votes right-skewed; idols zero-inflated) referencing the outline’s distribution notes.

### 3.2 Block 2 — Winners vs non-winners

**Group by:** `is_winner`.

**Output:** Same metrics as Block 1 — mean / median / std (you can show mean+median side by side in a compact table).

**Markdown:** Explicitly say that **winners have higher raw challenge counts and longer `day`/`order`** partly because they survive longer; highlight **`total_votes_received`** as the metric where winners are **lower** than non-winners (cleaner “Outwit” separation in the aggregate).

### 3.3 Block 3 — Correlation matrix

**Primary matrix (recommended for the heatmap):**

- `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins`, `is_winner` (cast `is_winner` to int for correlation if needed).

**Optional second small matrix or extra rows/columns:**

- Include `order_norm` (or raw `order` **once**) to **show** collinearity between longevity and challenge wins — then **interpret** in Markdown: challenge metrics correlate with *placement* strongly; correlation with `is_winner` is weaker and partly indirect.

**Markdown (rubric “non-obvious” insight):**

- Call out **`total_votes_received` vs `is_winner`** (negative) as a substantive Outwit signal.
- Call out **`total_votes_received` vs `order`** (~0) per outline — votes are not “high because you stayed long” in a simple linear way; interpret carefully.

---

## 4. Part B — Investigations (questions → extra tables)

Map each investigation to **one** extra table (or plot-only, for distributions). Keep era tables small.

### 4.1 Q1 — What does it take to Outwit, Outplay, Outlast?

**Investigation:** Median (and optionally mean) of the six behavioral columns by `is_winner`, **plus** optional rate columns from Step 2.5.

**Deeper check:** If you claim idols or challenges “matter more for winning,” show the same split **within a late-game subset** (e.g. `order <= 6`) if you can justify the cutoff — optional; increases complexity.

### 4.2 Q2 — What distinguishes winners from losers?

**Investigation:**

- Overlapping distributions of `total_votes_received` by `is_winner` (histogram or KDE — can be Visual #3).
- Optional: MBTI at **letter** level (E/I, S/N, T/F, J/P) for winner share vs cast share — **not** full 16 types unless you show *n* per cell.

### 4.3 Q3 — How have traits changed over time?

**Investigation:** For each **era** bin, compute:

- Mean or median of key metrics for **all contestants**, and/or
- Mean or median for **winners only** (small *n* per era — note in caption).

Compare votes, idols, immunity wins across eras. Tie to the “stealth vs armored winner” hypothesis from the outline: early winners may show lower vote totals; modern winners may show higher votes **and** higher idols/challenges — verify in **your** notebook output.

### 4.4 Q4 — Trends or features that predict performance?

**Investigation:** Reuse correlation matrix; optionally rank features by absolute correlation with `order` or `order_norm` (placement target) vs `is_winner` (binary target).

**Markdown:** State clearly that **`order`/`day` as predictors of `is_winner`** are partly **mechanical** (winner = last).

### 4.5 Q5 — Have predictive trends shifted?

**Investigation:** Within each era, correlation between `total_votes_received` and `is_winner` (or simple winner vs non-winner median gap for votes). Sample sizes are small — if you claim an era difference, optional **bootstrap 95% CI** (see Section 7).

---

## 5. Part C — Three required visuals (diversity + alignment)

Rubric: **at least three diverse** plots with titles, axis labels, legends where needed ([PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md)). Team plan: **correlation heatmap**, **MBTI trends over time**, **third visual TBD** ([PHASE2_EDA_VISUALIZATIONS_PLAN.md](PHASE2_EDA_VISUALIZATIONS_PLAN.md)).

Below is a **default trio** that maps cleanly to Parts A–B and stays simple.

### Visual 1 — Correlation heatmap (required)

- **Data:** Columns from Section 3.3 (behavioral + `is_winner`; optionally add `order_norm` once).
- **Tool:** `seaborn.heatmap` or `matplotlib` imshow with annotations if legible.
- **Markdown:** Reference Section 3.3 bullets (votes–winner negative; challenge–longevity strong; mechanical interpretation of longevity).

### Visual 2 — MBTI trends over time (required by team plan)

- **X-axis:** `season_year` or `season`.
- **Y-axis:** Share of cast with a given value — prefer **letter dimensions** (E/I, S/N, T/F, J/P) as separate lines or small multiples to avoid tiny per-type counts per year.
- **Optional:** Rolling mean over 3 seasons to smooth noise.
- **Markdown:** This is primarily a **casting / composition** story unless you explicitly condition on something else. Cite UNKNOWN exclusion. Remind readers MBTI is show metadata, not clinical.

### Visual 3 — Third diverse chart (pick one primary story)

Choose **one** anchor plot; do not try to show every outline idea in one figure.

| Option | Type | Story |
|--------|------|--------|
| **A (recommended)** | Overlaid histograms or KDE | `total_votes_received` by `is_winner` — clearest distributional separator. |
| **B** | Grouped or 100% stacked bars | Era × (winner vs non-winner) for 2–3 metrics (votes, idols, imm wins) — “stealth vs armored” era shift. |
| **C** | Faceted line charts | Winners only: mean/median metric vs `season_year` or era index — “moving winner archetype.” |
| **D** | Scatter | `immunity_challenge_wins` vs `reward_challenge_wins`, color = `is_winner`, size = idols — compact multi-variable view (busier; caption carefully). |

**Stretch (not required for Phase 2):** “Winner lift” bar chart by MBTI type (winner share ÷ cast share), colored by median `day` — see outline Phase 4; use as a **fourth** figure only if time.

---

## 6. Markdown observations section (rubric)

After statistics and plots, add a **dedicated Markdown section** that:

1. Walks **figure by figure** (Visual 1 → 2 → 3).
2. Ties each to **specific** numbers (e.g. median votes winner vs non-winner).
3. States **limitations:** Season 38 rule, UNKNOWN MBTI, small winner *n*, idol pre–Season 11, mechanical longevity.

---

## 7. Optional methods glossary (use only if you use them)

### 7.1 Bootstrap confidence interval (CI)

**What:** Resample rows (with replacement) many times (e.g. 1,000–10,000), recompute the statistic each time, take the 2.5th and 97.5th percentiles of those values → approximate **95% CI**.

**When:** Comparing correlations or means **between eras** with very few winners per bin — to avoid over-claiming from noise.

**What it is not:** Proof of causation; only sampling uncertainty under the resampling scheme.

### 7.2 Logistic regression (stretch)

**Use:** Predict `is_winner` from votes, idols, immunity wins, reward wins — **exclude** raw `order`/`day` from features to reduce leakage.

**Report:** Coefficients with caution on collinearity; optional ROC-AUC. Keep in an appendix if the core Phase 2 work is not yet solid.

---

## 8. Pre-submission checklist

- [ ] Season 38 decision documented; winner counts consistent with that decision.
- [ ] `cast_size`, `order_norm`, and `day_norm` defined; formulas in a Markdown or code comment.
- [ ] `era` bins defined; idol introduction (~Season 11) reflected in narrative or bin edges.
- [ ] Mean, median, std, and correlations displayed in **focused** tables.
- [ ] Three **diverse** visuals embedded with titles, labels, legends as needed.
- [ ] Observations Markdown references each visual and key statistics.
- [ ] Caveats: UNKNOWN MBTI, non-clinical types, structural zeros for idols early seasons, mechanical `order`/`day` vs winning.
- [ ] **Sources Used** updated per [COURSE_POLICY.md](COURSE_POLICY.md) for any AI-assisted scaffolding.

---

## 9. Suggested notebook section order (implementation order)

1. Load / build `analysis_df` (existing pipeline).
2. **Step 0** cells: Season 38, `cast_size`, `order_norm`, `day_norm`, `era`.
3. **Part A** cells: global describe; winner vs non-winner table; correlation matrix.
4. **Part B** cells: era tables (and optional bootstrap in a single cell if pursued).
5. **Part C** cells: Heatmap → MBTI lines → third visual.
6. **Synthesis** Markdown: bullet list of verified insights + limitations.
7. Export cell (if the team uses `exports/`) — optional.

This document is **implementation guidance only**; the graded artifact remains the notebook and your own authored narrative.
