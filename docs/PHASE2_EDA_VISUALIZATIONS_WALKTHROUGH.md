# Phase 2 EDA — Guided walkthrough (KISS)

**Purpose:** A straight line through Phase 2 in `survivoR.ipynb`: one table (`analysis_df`) → required statistics → three figures → observations. No detours unless you want them.

**Read with:**

- [PHASE2_EDA_VISUALIZATIONS_PLAN.md](PHASE2_EDA_VISUALIZATIONS_PLAN.md) — authoritative visual specs and “do not duplicate” rules.
- [PHASE2_EDA_VISUALIZATIONS.md](PHASE2_EDA_VISUALIZATIONS.md) — Canvas rubric (what graders look for).
- [PHASE2_EDA_OUTLINE.md](PHASE2_EDA_OUTLINE.md) — extra hypotheses and caveats if you need talking points.

**Course policy:** [COURSE_POLICY.md](COURSE_POLICY.md) — **Sources Used** when AI helps with refinement or scaffolding.

---

## The whole story in one breath

1. **`analysis_df`** = single source of truth. Everything else is a **copy + transform** for one job.
2. **Statistics first** — mean, median, std, group tables, correlation table — all computed **only** from `analysis_df`. Rubric credit lives here; plots **interpret** these numbers, they don’t replace them.
3. **Three plots** — two are already in the notebook; add the third. Pattern every time:  
   `analysis_df.copy()` → filter / new columns → **named** `something_df` → `sns` / `plt` → Markdown that cites Step 2.

You’ve got the hard framing work; this walkthrough is just the order of operations and what not to double-build.

---

## Step 1 — `analysis_df` exists and passes QA

Do this once after your merge / winner logic.

- `analysis_df.info()` — dtypes look sane.
- One winner per season: `analysis_df.groupby("season")["is_winner"].sum()` should be `1` everywhere you care about. If not (e.g. Edge return seasons), fix or document **once** in Markdown so everyone uses the same rule.
- Quick `describe()` on the numeric gameplay columns — no surprises (all NaN, etc.).

**Stop here** if the frame is wrong; don’t plot on broken keys.

---

## Step 2 — Statistics block (from `analysis_df` only)

Run this **before** any visualization cells. Use pandas; keep tables **small and labeled** (not a 50-column dump).

| # | What to compute | Tip |
|---|------------------|-----|
| 1 | **Global** mean, median, std for: `order`, `day`, `total_votes_received`, `immunity_idols_obtained`, `immunity_challenge_wins`, `reward_challenge_wins` | One table or `agg` |
| 2 | **By `is_winner`** — same metrics | Two-row or pivoted table; easy to cite in Markdown |
| 3 | **By era** (optional but nice) — same metrics, bins **matching** Visual 1’s era labels if you use eras in prose | Keeps stats and Emma’s chart aligned |
| 4 | **Correlations** — focused subset: gameplay + longevity columns, optionally `is_winner` as `int` | **Table** (and optional tiny heatmap **in this section only**). The **graded correlation figure** is Visual 2 (MBTI heatmap), not a second full duplicate heatmap |

**Rule:** Don’t hide the rubric stats inside a plot cell. Readers (and you) should see numbers first, pictures second.

---

## Step 3 — Visual 1 (already built — Emma)

**Question:** How do **winners vs non-winners** compare on **mean** immunity wins, reward wins, and idols **by era**?

**Pipeline:** `analysis_df` → `outplay_analysis_df` (drop agreed seasons, `pd.cut` on `season_year`, groupby era + `is_winner`, means; handle pre-idol era for idols as your cell already does) → three `barplot`s.

**Your job when polishing:** Titles, axis labels, legend. In Markdown, **quote Step 2** (winner vs non-winner or era table) and note small winner *n* per era.

**Do not:** Build a second “era × winner means” chart with different season drops unless you’re replacing this one.

---

## Step 4 — Visual 2 (already built — Simeon)

**Question:** How do **MBTI letter flags** line up with **winner flag** and **time-normalized** metrics?

**Pipeline:** `analysis_df` → `mbti_heatmap_df` (drop `UNKNOWN`, 0/1 letter columns, per-day rates, `survival_pct`, correlation slice) → one annotated `heatmap`.

**Your job when polishing:** Same labeling discipline. Markdown: tie weak/strong cells to Step 2’s correlation story; remind readers MBTI is show metadata.

**Do not:** Add another full notebook heatmap of the same MBTI × metric block.

---

## Step 5 — Visual 3 (to implement — vote exposure)

**Question:** After rough **time control**, do **winners** see **more or less vote exposure** than non-winners? (Fills the **Outwit** slot next to Emma’s **Outplay/era** bars and Simeon’s **personality** grid.)

**Pipeline (copy-paste mental model):**

```text
votes_by_outcome_df = analysis_df.copy()
votes_by_outcome_df["votes_per_day"] = (
    votes_by_outcome_df["total_votes_received"]
    / votes_by_outcome_df["day"].clip(lower=1)
)
# then: sns.boxplot or violinplot: x=is_winner, y=votes_per_day
```

**Keep it simple:** one plot type, clear title, label both axes. If outliers squash the box, cap or winsorize **and say so** in one sentence.

**Markdown:** Compare to Step 2 medians/means for `total_votes_received` by `is_winner`. One limitation sentence (e.g. early boots vs deep runners in the “non-winner” bucket).

**Diversity check:** bars + heatmap + box/violin = three distinct types. Good.

---

## Step 6 — Observations section (rubric)

One short section that:

1. Walks **stats** first (what surprised you, with numbers).
2. Walks **Visual 1 → 2 → 3** in order, each with: claim + Step 2 citation + caveat.
3. Repeats the standing caveats once: `UNKNOWN` MBTI, idols ≠ challenge wins, rare winners, personality not clinical.

---

## Pre-submit checklist (copy-friendly)

- [ ] `analysis_df` QA done; winner-per-season rule documented if special cases exist.
- [ ] Step 2 tables: mean, median, std, correlations — all from `analysis_df`, shown clearly.
- [ ] Visual 1 and 2 untouched in spirit (no duplicate era bar trio, no duplicate MBTI correlation figure).
- [ ] Visual 3 implemented from `votes_by_outcome_df` (or team-agreed alternative from the plan doc).
- [ ] Every figure: title, axis labels, legend where it helps.
- [ ] Restart kernel → run all → no errors.
- [ ] **Sources Used** updated if AI assisted ([COURSE_POLICY.md](COURSE_POLICY.md)).

---

## Optional extras (only if time and energy)

- Deeper era tables, bootstrap CIs, or `order_norm` / `day_norm` — see [PHASE2_EDA_OUTLINE.md](PHASE2_EDA_OUTLINE.md). **Not** required to satisfy the streamlined plan.
- Fourth figure — only if it adds a genuinely new question; rubric asks for three.

---

*Graded work stays in the notebook; this file is a map, not a submission. You’re in good shape once Step 2 is honest and the three plots each answer one clear question.*
