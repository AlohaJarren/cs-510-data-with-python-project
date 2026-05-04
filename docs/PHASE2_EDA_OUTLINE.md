# Phase 2: EDA Outline (`analysis_df`)

**Internal planning doc.** The graded artifact is the working notebook (`survivoR.ipynb`); this file just collects observations, hypotheses, and visualization ideas to inform what the team writes there. See [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) for the rubric and [PHASE2_EDA_VISUALIZATIONS_PLAN.md](PHASE2_EDA_VISUALIZATIONS_PLAN.md) for how `analysis_df` is built.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md). Treat the observations below as **starting points** to verify in the notebook; do not paste them in as final narrative. Document any AI assistance in **Sources Used**.

**Source file:** `exports/analysis_df.csv` — one row per contestant per season.

---

## Phase 1 — Data understanding

### Shape and schema

- **Rows:** 742
- **Columns:** 11
- **Missing values:** 0 across all columns (cleaning was completed in Phase 1; `personality_type == "UNKNOWN"` is an imputed sentinel, not a `NaN`).

| Column | Dtype | Role | Notes |
|---|---|---|---|
| `season` | int64 | identity / merge key | Seasons 1–40 (40 unique). |
| `full_name` | str | identity | Display label; not a guaranteed unique key (see anomaly below). |
| `personality_type` | str | categorical (MBTI) | 17 distinct values: 16 MBTI codes + `"UNKNOWN"` (only 3 rows). |
| `order` | int64 | Outlast | Longevity rank within season (1 = first out). Range 1–23. |
| `day` | int64 | Outlast | Days survived. Range 1–41. |
| `total_votes_received` | int64 | Outwit (social risk) | Range 0–22; mean ~6.4. |
| `immunity_idols_obtained` | int64 | Outwit | Mechanism-neutral idol count. Range 0–5; ~50% of contestants have 0. |
| `immunity_challenge_wins` | int64 | Outplay | Range 0–12; mean ~3.4. |
| `reward_challenge_wins` | int64 | Outplay | Range 0–11; mean ~3.4. |
| `is_winner` | bool | outcome label | 41 `True` rows across 40 seasons (see Phase 2 anomaly). |
| `season_year` | int64 | evolution axis | 2000–2020. |

### Categorical inventory (MBTI distribution)

Top types by count: ENFP (73), ESFP (67), ISFP (65), ESTP (63), ESTJ (53), INFP / ISTJ (52 each). Rarest typed: INTJ (26), INFJ (26), ENTJ (30). `UNKNOWN` = 3 rows. **Caveat to surface in observations:** these are show-supplied/imputed labels, not clinical MBTI assessments — interpret type-level effects accordingly.

### Key variables, grouped by project frame

- **Outlast (longevity):** `order`, `day`
- **Outwit (social game):** `total_votes_received`, `immunity_idols_obtained`
- **Outplay (challenges):** `immunity_challenge_wins`, `reward_challenge_wins`
- **Identity / strategy:** `personality_type` (and optional letter splits per the build plan)
- **Outcome:** `is_winner`
- **Evolution axis:** `season_year`

---

## Phase 2 — Initial exploration

### Descriptive statistics (numeric, all contestants)

|  | order | day | votes_recv | idols | imm_wins | rew_wins |
|---|---|---|---|---|---|---|
| mean | 9.91 | 23.92 | 6.36 | 0.49 | 3.39 | 3.40 |
| std  | 5.50 | 12.12 | 3.75 | 0.96 | 2.35 | 2.46 |
| min  | 1    | 1    | 0    | 0    | 0    | 0    |
| 25%  | 5    | 14   | 4    | 0    | 2    | 1.25 |
| 50%  | 10   | 24   | 6    | 0    | 3    | 3    |
| 75%  | 14   | 36   | 8    | 1    | 5    | 5    |
| max  | 23   | 41   | 22   | 5    | 12   | 11   |

### Correlation snapshot

|  | order | day | votes | idols | imm | rew | is_winner |
|---|---|---|---|---|---|---|---|
| order | 1.00 | 0.96 | -0.01 | 0.49 | 0.69 | 0.63 | **0.37** |
| day | 0.96 | 1.00 | 0.01 | 0.47 | 0.68 | 0.63 | 0.29 |
| votes_recv | -0.01 | 0.01 | 1.00 | -0.07 | -0.06 | -0.07 | **-0.18** |
| idols | 0.49 | 0.47 | -0.07 | 1.00 | 0.58 | 0.30 | 0.30 |
| imm_wins | 0.69 | 0.68 | -0.06 | 0.58 | 1.00 | 0.71 | 0.23 |
| rew_wins | 0.63 | 0.63 | -0.07 | 0.30 | 0.71 | 1.00 | 0.19 |
| is_winner | 0.37 | 0.29 | -0.18 | 0.30 | 0.23 | 0.19 | 1.00 |

### Patterns worth verifying in the notebook

1. **`order` and `day` are nearly redundant (r = 0.96).** They measure the same construct (longevity). For modeling / heatmap presentation, prefer one (or scale `day` by season length, since modern seasons are ~26 days vs older ones at 39+).
2. **Challenge wins track longevity strongly** (`imm_wins`–`order` = 0.69, `rew_wins`–`order` = 0.63) but **modestly with winning** (0.23, 0.19). Challenge dominance keeps you alive but is not the dominant winning signal.
3. **Votes received is essentially uncorrelated with longevity** (r ≈ 0) yet **negatively correlated with winning** (-0.18). Hypothesis: winners actively avoid drawing votes; the relationship is not "few votes → long stay" but "few votes → likely winner conditional on reaching the end."
4. **Idol acquisition is a distinct lane.** It correlates moderately with longevity (0.49) and `is_winner` (0.30) but only weakly with votes received (-0.07). Idols seem to extend tenure rather than reduce social risk.

### Distributions and shape

- `order` is approximately uniform / right-shifted (mechanically, every season has one of each rank up to its size).
- `day` is bimodal — clusters near early-out (~3–10 days) and finalist range (35+).
- `total_votes_received` is right-skewed (median 6, max 22); a small number of "vote magnets" pull the tail.
- `immunity_idols_obtained` is heavily zero-inflated (median 0, ~50% are zero).

### Data quality flags (escalate to the team)

- **Season 38 has two `is_winner == True` rows**, both Chris Underwood (`order=3, day=8` and `order=20, day=39`). This reflects the Edge of Extinction return mechanic — he was voted out then re-entered and won. The build script's QA check (`is_winner.sum() == 1` per season) will flag this. **Decision needed:** keep both rows (each season-appearance is its own grain), collapse to the winning appearance only, or add a `re_entered` flag. Document whichever is chosen.
- **`personality_type == "UNKNOWN"`** for 3 rows — exclude from MBTI-only summaries, or call them out as "unknown" instead of dropping silently.
- **Season length changed.** Seasons 1–27 ran 39 days; later seasons shortened to 26–39. `day` is therefore not strictly comparable across eras — consider `day / max(day per season)` for cross-era plots.
- **Idol mechanic was introduced in Season 11 (2005)**; `immunity_idols_obtained == 0` for early seasons is structural, not behavioral. Era splits should reflect this.
- **`order` ceiling varies by cast size** (16–20). For cross-season ranking visuals, prefer normalized rank (`order / cast_size_per_season`) or a percentile.

---

## Phase 3 — Thematic analysis

For each guiding question: relevant variables, what the data **suggests** (to be confirmed in the notebook), and limitations the team should call out.

### Q1. What does it take to "Outwit, Outplay, Outlast"?

- **Variables:** all six numeric metrics, grouped by the three pillars; `is_winner` as the outcome anchor.
- **Pattern (raw means, winners vs non-winners):**

  |  | order | day | votes_recv | idols | imm_wins | rew_wins |
  |---|---|---|---|---|---|---|
  | non-winners | 9.4 | 23.1 | 6.5 | 0.42 | 3.3 | 3.3 |
  | winners | **18.2** | **38.2** | **3.5** | **1.68** | **5.7** | **5.3** |

  Winners go ~2× further (`order`), receive ~half the votes, and roughly double everything else.
- **Hypothesis to test:** all three pillars contribute, but their *signals* differ. Outlast (`order`/`day`) is essentially a tautology for winners (you must reach the end); Outplay (challenges) is a *necessary*-looking but not sufficient feature; Outwit (low votes + idols held) shows the cleanest *separating* signal.
- **Limitations:** "winning" requires surviving — so any metric that grows with tenure (`day`, challenge wins) inflates winner means mechanically. Control for tenure (e.g., per-day rate, or condition on reaching the merge / final) before claiming any of them are "what it takes."

### Q2. What decisions or traits distinguish winners from losers?

- **Variables:** `total_votes_received`, `immunity_idols_obtained`, `personality_type`, plus tenure-normalized challenge rates.
- **Pattern:** the strongest clean separator is `total_votes_received` (negative, r = -0.18 with `is_winner`) — winners absorb fewer votes despite being present longer. Idol behavior is the second cleanest signal.
- **MBTI angle:** sample sizes are tiny (≤ ~6 winners per type for the most common types, often 0–1 for rarer ones). Treat any per-type win rate as a directional anecdote, not a rate. A grouped E/I, S/N, T/F, J/P breakdown gives larger cells.
- **Hypothesis to test:** "winners are players who buy survival cheaply" — they convert tenure into challenge wins and idols without paying for it in votes.
- **Limitations:** small winner sample (n = 41); MBTI labels are show metadata; vote totals are a proxy for social risk, not strategy.

### Q3. How have these decisions or traits changed over time?

- **Variables:** all numeric metrics by `season_year` (or a small number of era bins).
- **Pattern (winner-only means by era):**

  | era | imm_wins | rew_wins | idols | votes_recv |
  |---|---|---|---|---|
  | 2000–2004 | 4.78 | 3.89 | 1.56 | 2.22 |
  | 2005–2009 | 6.00 | 6.50 | 1.30 | 3.50 |
  | 2010–2014 | 6.60 | 5.20 | 2.30 | 3.50 |
  | 2015–2020 | 5.25 | 5.58 | 1.58 | 4.58 |

  Total idols held by **all** contestants in the dataset: 74 (00–04) → 76 → 97 → 116. Modern winners eat more votes than early winners (2.2 → 4.6) — consistent with a more aggressive, idol-fueled era where survival doesn't require staying invisible.
- **Hypothesis to test:** the game has shifted from "stealth winner" (low-vote, low-challenge) to "armored winner" (more votes drawn, but neutralized by idols and challenge play).
- **Limitations:** idol mechanic introduced S11 (2005), so 00–04 idols are essentially zero by rule, not by choice. The 15–20 winner sample is also affected by twist-heavy seasons (Edge of Extinction etc.).

### Q4. Are there trends or features that predict performance?

- **Variables:** numeric metrics as features, `order` (continuous performance) or `is_winner` (binary) as targets.
- **Pattern:** `immunity_challenge_wins` is the strongest single linear predictor of `order` (r = 0.69), followed by `reward_challenge_wins` (0.63) and `immunity_idols_obtained` (0.49). For `is_winner`, the order is `order`/`day` (mechanical), then `idols` (0.30), `imm_wins` (0.23), `rew_wins` (0.19), `votes_recv` (-0.18).
- **Hypothesis to test:** for *finishing position*, challenges dominate; for *winning*, the marginal signal is social (votes received, idols held). A simple logistic model on the four behavioral features (excluding `order`/`day` to avoid leakage) should outperform any single feature.
- **Limitations:** all features are heavily collinear; `order` and `day` leak the outcome; sample is 742 / 41 winners.

### Q5. Have these predictive trends shifted across different eras or conditions?

- **Variables:** the same features split by era (and optionally by twist-presence flags if the team adds them later from `summary_df`).
- **Pattern:** the *correlations themselves* shift: in early eras, votes received vs `is_winner` is closer to zero (winners and losers both received few votes); in modern eras, votes received vs `is_winner` becomes more clearly negative as the variance in vote totals grows.
- **Hypothesis to test:** "what predicts winning" is era-dependent. In post-idol eras, `idols` and `imm_wins` carry more weight than they did in 00–04.
- **Limitations:** within-era winner samples are 8–11 per era; correlation differences need bootstrap CIs (or at least caveats) before claiming era effects.

---

## Phase 4 — Visual storytelling brainstorm (10 ideas)

Mix of required (Phase 2 rubric) and stretch ideas. Pick 3 for the rubric; keep the others as a creative bench.

| # | Chart type | x / y / color / size | Story it tells | Why it works here |
|---|---|---|---|---|
| 1 | **Correlation heatmap** | numeric + `is_winner`, annotated | Which metrics travel together; surface the tenure–challenge collinearity and the unique vote/idol axes. | Required by the rubric; works in one figure across all six numeric features. |
| 2 | **Boxplot of `order` by `personality_type`** | x = type (sorted by median), y = order, hue/highlight = `is_winner` | Whether some types systematically last longer; mark winners as overlay points. | Single-shot summary that combines distribution + outcome; tolerates small per-type N. |
| 3 | **Line chart: MBTI dimension shares over time** | x = `season_year`, y = share of cast, color = E/I (or S/N, T/F, J/P) | Casting evolution and whether type mix has shifted. | Aggregating to letter dimensions fixes the small-cell problem of full 4-letter types. |
| 4 | **Stacked / 100% bar: idol-era vs pre-idol-era winner profile** | x = era bin, y = mean per metric (faceted), color = winner/non-winner | Era-level shift in what winning looks like. | Directly answers Q3/Q5 with one panel per metric. |
| 5 | **Scatter: `imm_wins` vs `rew_wins`, color = `is_winner`, size = `idols`** | x, y, color, size as listed | Whether challenge-dominant players are the winning archetype, and where idol-heavy players sit. | Encodes four variables in one chart; immediately readable. |
| 6 | **Histogram + KDE: `total_votes_received`, split by `is_winner`** | x = votes_recv, two overlaid distributions | Visualizes the cleanest separator (vote count) for winners vs non-winners. | Distribution comparison is more honest than a means table for skewed counts. |
| 7 | **Lollipop / dot plot: per-MBTI-letter win *rate*** | y = letter dimension (E/I/S/N/T/F/J/P), x = win rate, with CIs | Whether any letter dimension over- or under-indexes on winning. | Letter-level cells are large enough to plot CIs; surfaces a non-obvious finding if it exists. |
| 8 | **Faceted line: per-metric trend over `season_year` (winner only)** | x = season, y = metric value, one line per metric, faceted | The "winner archetype" as a moving target. | Compactly shows era effects across all six metrics in one figure. |
| 9 | **Heatmap: season × `order` cell colored by `total_votes_received`** | x = season, y = order rank, fill = votes | "Vote weather map" — where in the bracket and which seasons did social risk concentrate? | Reveals season-level patterns the aggregate stats hide. |
| 10 | **Bump chart / parallel coordinates of the final 5 each season** | one line per finalist, axes = `imm_wins`, `idols`, `votes_recv`, color = winner | The endgame fingerprint of winners vs runner-ups. | Frames the problem at the decision-relevant grain (final 5), where small differences matter most. |

**Plotting conventions reminder:** matplotlib / seaborn (per rubric), titles, axis labels, legends, palettes consistent across the notebook.

---

## Phase 5 — Synthesis

### Insights worth carrying into the notebook narrative (to verify and write up)

1. **Longevity is a tautology — strip it before claiming anything.** `order` and `day` correlate 0.96 and both correlate strongly with winning, but they encode "you reached the end." The interesting features are the rate-style ones (`votes_received`, `idols`, challenge wins).
2. **The cleanest single winner signal is *fewer votes received*, not *more wins*.** Across 742 contestants, vote count separates winners from non-winners more cleanly than challenge counts do, and is essentially uncorrelated with raw tenure — it's a true "Outwit" signal.
3. **The game has gotten louder.** Modern winners draw more votes but offset them with idols and challenge wins; early winners survived by staying invisible. The "what wins" recipe shifts visibly across eras.

### Hypotheses to test further

- **H1 (separation):** A logistic regression on `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins` (excluding `order`/`day` to avoid leakage) classifies winners materially better than chance, with `total_votes_received` as the largest standardized coefficient.
- **H2 (era shift):** The negative coefficient on `total_votes_received` in H1 weakens (closer to 0) when the model is fit on 2000–2004 only, and strengthens in 2010–2020.
- **H3 (MBTI letter, not type):** Aggregating to MBTI dimensions (E/I, S/N, T/F, J/P) reveals a letter that over-indexes on winning at small but stable rates; the four-letter type breakdown does not, due to sample size.

### Recommended next steps

1. **Resolve the Season 38 anomaly explicitly** in the notebook (one short markdown + a `re_entered` flag or row collapse) so downstream stats are unambiguous.
2. **Add a normalized longevity column** (`order_norm = order / cast_size_per_season`, or `day_norm = day / max(day per season)`) and use it for cross-era charts. Keep the raw columns for within-season views.
3. **Bin seasons into 3–4 eras** (e.g., pre-idol 00–04, idol-introduced 05–09, twist-era 10–14, modern 15–20) and re-run the per-metric summaries by era. Most Q3/Q5 storytelling lives in this pivot.
4. **Build a single "winner archetype" figure** (idea #5 or #8 above) as the anchor visual the team's narrative orbits around.
5. **If pursuing modeling beyond Phase 2:** start with logistic regression on the four leakage-free features, then layer in MBTI dimension dummies; track ROC-AUC and report the model on a per-era split to address H2.

---

## Open questions for the team

- Do we keep both Season 38 rows for Chris Underwood, or collapse to the winning row? (Affects winner counts and any per-season aggregation.)
- Do we report `day` raw, or normalize it to handle the season-length change?
- For the third required visual, which of the 10 ideas above best supports the narrative voice the team wants?
