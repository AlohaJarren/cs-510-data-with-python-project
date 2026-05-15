# Phase 3 — Living brainstorming (Survivor / `survivoR.ipynb`)

**Purpose:** Shared creative space for the team. Capture ideas at any level of polish—from one-line hooks to full question arcs. **The graded artifact is still the notebook**; this file is not submitted.

**Planning checklist:** [PHASE3_QUESTION_ANSWERING_CONCLUSION.md](PHASE3_QUESTION_ANSWERING_CONCLUSION.md)

**How this doc evolves:** Two **brainstorm rounds** (not Canvas milestones—the repo already uses Phase 1 = acquisition, Phase 2 = EDA). **Round 1** frames the Phase 3 story and concrete questions from your EDA. **Round 2** drills into survivorship bias, feature enrichment, and statistical angles so Phase 3 questions stay honest as we narrow specifics.

**Last updated:** *(edit when you meet)*

---

## Brainstorm round 1 — Questions & Phase 3 arc *(original)*

### Where we are (honest snapshot)

| Area | Status | Notes |
| ---- | ------ | ----- |
| Phase 1 — acquisition & cleaning | Strong | Per-table exploration; issue → rationale → result; `analysis_df` built |
| Phase 2 — EDA | Strong | 3 visuals + mean/median/std/correlations + observations |
| Phase 3 — 3 questions + code answers | **Not started** | No dedicated Phase 3 section yet |
| Conclusion & reflection | **Not started** | Notebook ends after Visual 3 + AI disclaimer |
| `jury_votes_df` | Loaded, **unused** | Big opportunity for “why,” not just “what” |

**Rubric risk today:** Phase 1–2 would score well; Phase 3 would score **0** until questions, answers, and conclusion exist.

---

### The story we are trying to tell (draft spine)

> Survivor winners are not just “better at challenges.” Our EDA suggests a **blend**: fewer votes per day (social game), more challenge and idol success after the idol era, and weak personality typing. Phase 3 should explain **which levers moved together** and **how that mix changed over time**—without claiming true causation from observational data alone.

Use this spine in the **Conclusion** so Phase 3 feels like a culmination, not three unrelated exercises.

---

### Original questions → “why” upgrades

Your opening questions are good **motivation**. Phase 3 needs **testable** versions tied to columns you already built.

| Original (overview) | Why it feels “what” only | Sharper Phase 3 angle (relationship / pattern) |
| ------------------- | ------------------------ | ----------------------------------------------- |
| What does it take to Outwit, Outplay, Outlast? | Slogan, not measurable | **How do winners differ on votes/day vs challenge wins vs idols**—and does that mix **change by era**? |
| What decisions do winners make? | Vague; no decision column | **Do winners combine lower vote exposure with higher outplay metrics** after controlling for how long they stayed? |
| What decisions do losers make? | Same | Compare **finalists who lost** vs **early boots** on votes/day (optional stretch) |
| How have decisions changed as the game evolved? | Broad | **Did the winner–non-winner gap on immunity/reward/idols widen after idols (2005+)?** (you already visualized this—now quantify) |
| Trends that predict performance? | Could be one-column | **Among players who survive past merge, which metrics separate winners from non-winners?** |
| Qualities that predict performance? | MBTI alone is weak | **Is MBTI signal gone after accounting for outplay/social metrics?** (negative result is a valid finding) |
| Changes in trends over time? | Duplicate of era question | Fold into **era × winner** tables, not a fourth question |

**Language habit:** Write “**associated with**,” “**gap between**,” “**after idols were introduced**.” Avoid “proves causes” unless you add jury-vote or experimental logic.

---

### Recommended trio (simple, clear, culminates EDA)

Pick **three** and assign owners. These are designed to pass the **So what?** test with **minimal new code** (mostly `groupby`, filters, and one small derived column).

#### Q1 — Era recipe (culminates Visual 1)

**Context:** Era bar charts showed winners with ~2× immunity/reward wins and ~3× idols post-2005; pre-idol gap was smaller.

**Question (draft):**  
*After grouping seasons into eras, how does the typical winner’s profile (immunity wins, reward wins, idols obtained, votes per day) compare to non-winners—and did that profile change once idols existed?*

**Validation (keep short):**

- Reuse `outplay_analysis_df` + `era` bins (already defined).
- `groupby(["era", "is_winner"]).agg(...)` on key metrics; optionally `winner_minus_loser = winner_mean - loser_mean` per era.
- One small table or bar chart of **gaps** (not another wall of raw output).

**Resolution (one sentence template):**  
*Winning became more strongly associated with challenge dominance and idol use after the idol era, while the early era looked more balanced—suggesting the “price” of winning shifted as the game added idols.*

| So what? check | Pass? |
| -------------- | ----- |
| Multi-column | Yes |
| Pattern / difference | Yes (era × winner) |
| Actionable | Yes (casting/strategy expectations by era) |

**Owner:** __________ **Status:** ☐ draft ☐ coded ☐ written

---

#### Q2 — Outwit vs outplay (culminates Visual 3 + correlation notes)

**Context:** Correlations showed votes barely relate to longevity but modest **negative** link to `is_winner`; violin plot shows winners cluster at **low votes/day**.

**Question (draft):**  
*Among castaways who survive at least halfway through their season, do winners still show lower votes per day than non-winners with similar immunity challenge success?*

**Why this digs deeper:** Separates **social targeting** from **challenge skill** so you are not only saying “winners win more challenges.”

**Validation:**

- Filter: e.g. `order >= season_max_order * 0.5` (or `day` above median within season).
- Compare `votes_per_day` by `is_winner`; optional: bin or filter by `immunity_challenge_wins` (median split) to show the social gap is not only “weak players.”
- Report **medians** + counts in Markdown (violin already showed the shape).

**Resolution template:**  
*Winners are associated with lower vote exposure per day even among players who lasted deep into the game, which supports “outwit” (avoiding tribal heat) as part of the winning pattern—not challenge wins alone.*

| So what? check | Pass? |
| -------------- | ----- |
| Multi-column | Yes (`votes_per_day`, `is_winner`, `order`/`immunity_challenge_wins`) |
| Pattern | Yes |
| Actionable | Yes (social vs physical threat) |

**Owner:** __________ **Status:** ☐ draft ☐ coded ☐ written

---

#### Q3 — Idol era mechanism (culminates Visual 1 + idol footnote)

**Context:** You hypothesized idols let strong players play more aggressively; pre-idol era had smaller winner gaps.

**Question (draft):**  
*In seasons after idols were introduced (season ≥ 11 / year ≥ 2005), is the winner–non-winner gap in immunity wins larger than the gap in votes per day?*

**Validation:**

- Split `analysis_df` (or `outplay_analysis_df`) into pre-idol vs post-idol.
- For each period: mean(or median) by `is_winner` for `immunity_challenge_wins`, `votes_per_day`, `immunity_idols_obtained`; compute gaps.
- Optional: same for **reward** wins if space allows.

**Resolution template:**  
*Post-idol, winning aligns more with outplay advantages (challenges + idols) than with vote totals alone, consistent with idols changing how much challenge strength translates into survival.*

| So what? check | Pass? |
| -------------- | ----- |
| Multi-column | Yes |
| Pattern | Yes (period × metric × winner) |
| Actionable | Yes (meta shift in what “type” wins) |

**Owner:** __________ **Status:** ☐ draft ☐ coded ☐ written

---

### Notebook section template (copy structure, write your own words)

For **each** final question in `survivoR.ipynb`:

```markdown
## Phase 3 — Question N: [short title]

### Context
Our cleaning and EDA showed … [1–3 sentences, cite Visual/stat].

### Question
[Single precise sentence.]

### Validation
[Brief plan; then code cell(s).]

### Resolution
**Answer:** … [2–4 sentences with numbers from the output.]
**So what:** … [one sentence on implication; not causation unless justified.]
```

Keep **one main code cell per question** where possible (plus optional tiny helper). Interpret in Markdown—do not dump an unstyled 20-row frame without explanation.

---

### Idea parking lot (add freely)

#### Simple (good Phase 3 candidates)

- [ ] Winner rate by `personality_type` letter (E/I, T/F) — only if framed as “weak signal, not a predictor”
- [ ] Median `votes_per_day` for winners vs non-winners **by era**
- [ ] Top-quartile immunity winners: what % are actual season winners?
- [ ] `reward_challenge_wins` vs `immunity_challenge_wins` for winners only (which matters more?)

#### Medium (more work, high payoff)

- [ ] **Merge `jury_votes_df`** — do winners receive more favorable jury votes? (closest to your “get jury votes” intro)
- [ ] Finalists only (`order` in top 3–4 per season): compare metrics
- [ ] “Challenge beast” trap: high immunity wins + not winner — rate by era
- [ ] Normalize all outplay stats by `day` everywhere for consistency (you did this for MBTI/votes)

#### Chaotic / future work (conclusion or “future work,” not all three questions)

- [ ] Machine learning: predict `is_winner` from features (Phase 4 vibe)
- [ ] Causal language with propensity scores / matching (probably overkill for 10 pts)
- [ ] Viewer ratings vs gameplay era (`viewers_df` unused)
- [ ] Tribe swap / merged_tribe social networks
- [ ] Text analysis of castaway `result` strings
- [ ] Full MBTI 16-type grid (sparse cells—use letter flags only)

---

### What to avoid (keeps narrative honest)

| Trap | Why | Instead |
| ---- | --- | ------- |
| “Winners have more challenge wins” | Restates Visual 1 | Era change, conditional filters, or gaps |
| “Winners are winners” | Circular | Compare **among deep survivors** or **by era** |
| Raw correlation matrix again | Phase 2 already did | One focused comparison per question |
| Claiming MBTI **causes** wins | Weak r (~0.06) | “Small association; game behavior matters more” |
| Ignoring small winner **n** per era | You noted this in EDA | Repeat in limitations |

---

### Conclusion & reflection — bullet bank

Pull from here when you write the final section (your own synthesis).

**Key findings (draft bullets):**

- Winner–loser gaps in challenges/idols widened in the idol era.
- Vote exposure per day is lower for winners (social/outwit signal).
- MBTI alone is a weak explainer; thinking types show only small associations.
- Longevity and challenge wins correlate; winning is not identical to “most challenges.”

**Limitations (draft):**

- Observational data → association, not causation.
- `analysis_df` excludes some re-entry seasons; cast-level not episode-level strategy.
- Loser pool mixes early boots and runners-up.
- `jury_votes_df` not yet integrated; personality types incomplete (UNKNOWN).
- 40 seasons / small winner counts per era.

**Future work (draft):**

- Jury vote analysis; finalist-only cohorts; episode-level decisions.
- Viewer trend vs gameplay era; richer social network from tribes.

---

## Brainstorm round 2 — Survivorship & enrichment

This round tightens **Round 1** against blind spots: tenure mixing “silent losers” with deep runners-up, weak-feature uplift (MBTI), idol/challenge archetypes, and secondary outcomes. Use it to refine questions—not to spawn twelve analyses.

---

### Clarifying the comparison (winner vs whom?)

Round 1 compares **winners to all non-winners**. That is not winner-vs-winner; the survivorship issue is that **non-winners pool**:

- **Early boots** — little time for idols/challenges; vote metrics behave differently.
- **Deep runners-up / FTC losers** — comparable tenure to winners for fair “conversion” questions.

Raw totals (`immunity_challenge_wins`, votes, idols) mechanically scale with **`day` / `order`** unless normalized or stratified.

---

### 1. Survivorship bias — what goes wrong

| Issue | What happens | Fix (pandas-first) |
| ----- |--------------|-------------------|
| Tenure confound | Longer stay ⇒ more challenges & councils ⇒ higher totals | `*_per_day`, `*_per_order`, or control `day` / `order` |
| Loser heterogeneity | One violin mixes 3-day and 39-day players | **`survival_pct`** buckets or **deep-game** filter |
| Sparse winners | ~1 winner / season | Stratify carefully; report **counts** with percentages |
| Era mechanics | Idols post-2005 change the game | Pre/post idol splits (already in spirit for Visual 1) |

---

### 2. Data transformations & cohort splits

| Transform / split | Idea | Addresses |
|-------------------|------|-----------|
| **`survival_pct`** (`order / season_max_order`) | Compare within similar depth | Silent early exits vs late-game |
| **Deep-game mask** (`order` top quartile per season, or ≥ halfway) | Winners vs FTC-adjacent non-winners | “Beyond surviving” |
| **Per-day normalization** | `votes_per_day`, `immunity_wins_per_day`, `idols_per_day` (`day.clip(lower=1)`) | tenure artifact |
| **Residualized outplay** (stretch) | Regress totals on `day`; use residuals | “Above expected for tenure” |
| **Season awareness** | `groupby('season')` before quartiles | Fair splits within cast size |

---

### 3. Statistical tests & procedures (association, not causation)

| Procedure | When | Implementation sketch |
| --------- | ---- | --------------------- |
| **Stratified aggregates** | Always start here | `groupby(['cohort','is_winner']).agg(...)` |
| **Mann–Whitney / t-test** | Formal gap inside one stratum | `scipy.stats.mannwhitneyu` (optional); watch thin winner counts |
| **Simple logistic regression** | Adjust tenure + era together | `statsmodels` or sklearn — optional if course allows |
| **Chi-square / Fisher** | MBTI × winner | Prefer **letter dummies** or aggregates; 16-type grid is sparse |
| **Partial views** | MBTI vs outcomes **within** tenure bin | Filter → `.corr()` on numeric block |
| **Spearman** | Skewed jury votes / counts | If `jury_votes_df` merged |

Framing: use **“associated with,” “adjusted for,” “within deep-game players.”** Reserve causal language for limitations unless design supports it.

---

### 4. MBTI — transforms & reinterpretation

| Approach | Gain | Caveat |
|----------|------|--------|
| Keep **4 letter flags** (E/I, N/S, T/F, J/P) | Larger cells than 16 types | Already strong direction |
| **MBTI × depth** | Personality vs **votes/day**, idol rate among survivors | Separates persona from “survived long” |
| **UNKNOWN vs known** | Data-quality probe | Narrative + counts |
| **MBTI × era** | Modern meta × type | Needs rows |
| **16-type grid** | Visual completeness | Sparse → unstable; prefer aggregates |

Insight-to-effort: **MBTI × deep-game social/outplay metrics** → solid return; full **16×16 winner correlation** → usually low yield.

---

### 5. Idols & “challenge beast” vs social maneuvering

**Operational sketches:**

- **Beast proxy:** top quartile **`immunity_challenge_wins / day`** within season (or residualized immunity).
- **Social heat:** **`votes_per_day`** or high percentile of votes given tenure.
- **Idol-heavy:** `immunity_idols_obtained >= 1` or idols/day.

**Angles:**

- Cross-tab **beast × idol × winner** (counts + %) — expect sparsity; narrate honestly.
- **Within post-idol era:** median split on immunity/day; compare winner rate descriptively.
- **Scatter / hexbin:** immunity/day vs votes/day, hue `is_winner`.

Insight-to-effort: **median splits + era filter** → high ; fancy clustering → medium effort, uncertain gain.

---

### 6. Tribe / merge “social network” feasibility

**Available:** `original_tribe`, `swapped_tribe`, `swapped_tribe2`, `merged_tribe` per castaway — **not** episode-accurate edges without more joins.

**Lightweight proxies:**

- **Tribe churn:** `nunique` of non-null tribe labels across swap columns per player.
- **Merge reached:** `merged_tribe` usable vs “Not Applicable” / NA patterns after cleaning.

**Heavier:** Same-season graph — edges if two players share same tribal label on same snapshot (coarse). Episode-perfect swaps → likely **out of scope** for five CSVs.

Insight-to-effort: **churn / merge proxies** → medium ; full dynamic SNA → low ratio for Phase 3.

---

### 7. Secondary outcomes when `is_winner` is blunt

| Metric | Role |
|--------|------|
| **`jury_votes_df`** merged on finalist votes | Endgame **received** social capital |
| **`order` ≤ 3–4** | Finalist proxy |
| **`day`** as continuous outcome | Sensitive to bias — pair with strata |
| Vote share / margin | Nuanced win strength |

Tests: merge jury tables; **Spearman** or stratified tables vs prior-season metrics.

---

### 8. Insight-to-effort backlog (Round 2 → notebook priorities)

| Rank | Idea | Effort | Insight |
|:----:|------|--------|---------|
| 1 | **Tenure strata** + same Phase 2 metrics | Low | Very high |
| 2 | **Challenge beast × votes/day × post-idol** | Low–med | Very high |
| 3 | **Consistent per-day normalization** in comparisons | Low | High |
| 4 | **`jury_votes_df` merge** on finalists | Medium | High narrative |
| 5 | **Simple logistic / tenure control** | Medium | High rigor |
| 6 | **MBTI × deep-game** outcomes | Low | Medium |
| 7 | **Tribe churn** proxy | Medium | Medium |
| 8 | Full episode-level SNA | High | Uncertain |

---

### Round 1 ↔ Round 2 linkage

| Round 1 question | Round 2 refinement |
| ---------------- | ------------------- |
| Q1 Era recipe | Keep; optionally report gaps **within survival_pct** to show tenure isn’t driving era story alone |
| Q2 Outwit vs outplay | Already survivorship-aware; add **median split on immunity/day** inside deep-game |
| Q3 Idol mechanism | Add **beast × idol** cross-tab in post-idol subset if space |

---

## Team log

| Date | Who | Added / decided |
| ---- | --- | ---------------- |
| | | |
| | | |

---

## Pre-submit (notebook)

- [ ] Three questions use **Context → Validation → Resolution**
- [ ] Each question has **executed** code + interpreted answer
- [ ] **Conclusion & reflection** (summary, limitations, future work)
- [ ] **Restart kernel and run all**
- [ ] **Sources Used** updated in notebook (AI disclaimer exists—align with [COURSE_POLICY.md](COURSE_POLICY.md))
