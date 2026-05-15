# Phase 3 — Living brainstorming (Survivor / `survivoR.ipynb`)

**Purpose:** Shared creative space for the team. Capture ideas at any level of polish—from one-line hooks to full question arcs. **The graded artifact is still the notebook**; this file is not submitted.

**Planning checklist:** [PHASE3_QUESTION_ANSWERING_CONCLUSION.md](PHASE3_QUESTION_ANSWERING_CONCLUSION.md)

**Last updated:** *(edit when you meet)*

---

## Where we are (honest snapshot)

| Area | Status | Notes |
| ---- | ------ | ----- |
| Phase 1 — acquisition & cleaning | Strong | Per-table exploration; issue → rationale → result; `analysis_df` built |
| Phase 2 — EDA | Strong | 3 visuals + mean/median/std/correlations + observations |
| Phase 3 — 3 questions + code answers | **Not started** | No dedicated Phase 3 section yet |
| Conclusion & reflection | **Not started** | Notebook ends after Visual 3 + AI disclaimer |
| `jury_votes_df` | Loaded, **unused** | Big opportunity for “why,” not just “what” |

**Rubric risk today:** Phase 1–2 would score well; Phase 3 would score **0** until questions, answers, and conclusion exist.

---

## The story we are trying to tell (draft spine)

> Survivor winners are not just “better at challenges.” Our EDA suggests a **blend**: fewer votes per day (social game), more challenge and idol success after the idol era, and weak personality typing. Phase 3 should explain **which levers moved together** and **how that mix changed over time**—without claiming true causation from observational data alone.

Use this spine in the **Conclusion** so Phase 3 feels like a culmination, not three unrelated exercises.

---

## Original questions → “why” upgrades

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

## Recommended trio (simple, clear, culminates EDA)

Pick **three** and assign owners. These are designed to pass the **So what?** test with **minimal new code** (mostly `groupby`, filters, and one small derived column).

### Q1 — Era recipe (culminates Visual 1)

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

### Q2 — Outwit vs outplay (culminates Visual 3 + correlation notes)

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

### Q3 — Idol era mechanism (culminates Visual 1 + idol footnote)

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

## Notebook section template (copy structure, write your own words)

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

## Idea parking lot (add freely)

### Simple (good Phase 3 candidates)

- [ ] Winner rate by `personality_type` letter (E/I, T/F) — only if framed as “weak signal, not a predictor”
- [ ] Median `votes_per_day` for winners vs non-winners **by era**
- [ ] Top-quartile immunity winners: what % are actual season winners?
- [ ] `reward_challenge_wins` vs `immunity_challenge_wins` for winners only (which matters more?)

### Medium (more work, high payoff)

- [ ] **Merge `jury_votes_df`** — do winners receive more favorable jury votes? (closest to your “get jury votes” intro)
- [ ] Finalists only (`order` in top 3–4 per season): compare metrics
- [ ] “Challenge beast” trap: high immunity wins + not winner — rate by era
- [ ] Normalize all outplay stats by `day` everywhere for consistency (you did this for MBTI/votes)

### Chaotic / future work (conclusion or “future work,” not all three questions)

- [ ] Machine learning: predict `is_winner` from features (Phase 4 vibe)
- [ ] Causal language with propensity scores / matching (probably overkill for 10 pts)
- [ ] Viewer ratings vs gameplay era (`viewers_df` unused)
- [ ] Tribe swap / merged_tribe social networks
- [ ] Text analysis of castaway `result` strings
- [ ] Full MBTI 16-type grid (sparse cells—use letter flags only)

---

## What to avoid (keeps narrative honest)

| Trap | Why | Instead |
| ---- | --- | ------- |
| “Winners have more challenge wins” | Restates Visual 1 | Era change, conditional filters, or gaps |
| “Winners are winners” | Circular | Compare **among deep survivors** or **by era** |
| Raw correlation matrix again | Phase 2 already did | One focused comparison per question |
| Claiming MBTI **causes** wins | Weak r (~0.06) | “Small association; game behavior matters more” |
| Ignoring small winner **n** per era | You noted this in EDA | Repeat in limitations |

---

## Conclusion & reflection — bullet bank

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
