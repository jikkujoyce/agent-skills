# Spaced Repetition: Scheduling Against the Forgetting Curve

How review timing works. Read this when running reviews, grading, or explaining the system to the learner.

## The two-sentence theory

Ebbinghaus measured that memory for new material decays steeply — most of it gone within days — unless refreshed, and that each successful retrieval flattens the curve so the *next* refresh can wait longer. So the optimal schedule reviews each item at expanding intervals, ideally just before it would fade; anything more frequent wastes time, anything less loses the item.

## The algorithm (SM-2 lite, implemented in `scripts/schedule.py`)

Each concept carries: an **ease factor** `ef` (starts 2.5), an **interval** in days, a **repetition count**, and a **due date**. After each review the learner's answer is graded 0–5, and:

- **Grade ≥ 3 (success):** repetitions += 1. Interval becomes **1 day** after the first success, **4 days** after the second, then **previous interval × ef** (rounded) thereafter. `ef` drifts up slightly for 5s and down slightly for hesitant 3s: `ef ← ef + (0.1 − (5−q) × (0.08 + (5−q) × 0.02))`, floored at 1.3.
- **Grade < 3 (lapse):** repetitions reset to 0 and the interval resets to **1 day** — the item re-climbs the ladder. `ef` still takes the adjustment, so chronically hard items earn permanently shorter intervals.
- **Due date** = today + interval.

Worked example: "list comprehensions" reviewed on days 1 (grade 4), 2 (4), 6 (5), and 16 (3) lands its next review on day 41 — five touches across six weeks instead of daily drilling, and each touch took under a minute.

Typical successful trajectory: `1 → 4 → 10 → 25 → 60+` days. That's the forgetting curve being beaten with about five minutes of total effort per concept.

## Grading rubric (0–5)

Calibrate honestly — soft grading delays the next encounter until after the memory is gone.

| Grade | Meaning, for code recall |
|---|---|
| 5 | Instant, fluent, idiomatic. Produced it like a native. |
| 4 | Correct with brief hesitation or one minor slip self-corrected. |
| 3 | Correct, but slow, or needed one small nudge (a rung-1 hint). |
| 2 | Wrong or blocked, but recognized the right answer immediately once shown. |
| 1 | Wrong; only vague familiarity ("I know we covered this…"). |
| 0 | Blank. No recognition. |

In-project usage counts: when the learner meaningfully uses a due concept inside their project unaided, grade that as a review (usually a 4–5). Authentic use is the strongest review there is — this is why the project ladder deliberately reuses old concepts.

## Running the review (mechanics)

```bash
python3 scripts/schedule.py init --file progress.json --topic "Python"   # once, at kickoff
python3 scripts/schedule.py add  --file progress.json dicts "Dicts and iteration idioms"
python3 scripts/schedule.py due  --file progress.json                    # start of each session
python3 scripts/schedule.py grade --file progress.json dicts 4           # after each quiz item
python3 scripts/schedule.py stats --file progress.json                   # progress overview
```

Keep reviews to 2–5 minutes: one active-recall question per due concept (formats in `references/teaching-techniques.md`), grade, move on. If more than ~8 items are due (usually after a gap), review the 6–8 most overdue and push the rest to next session — a marathon quiz at session start kills the session.

## Cadence advice for the learner

- **Frequency beats duration.** Five 25-minute sessions beat one 3-hour Saturday; the schedule *needs* gaps to do its work, and consistency is the mechanism by which syntax becomes reflex.
- Daily is ideal early on (intervals are short); after two weeks, most items live at 10+ day intervals and 3×/week sustains everything.
- **After a long gap:** run `due` (everything will be overdue — that's fine), review honestly, and let lapses reset intervals. No shame, no restart-from-zero. The system is *designed* to absorb decay and repair it.

## Manual fallback (no code execution available)

Maintain a table in `LEARNING_PLAN.md` with columns: concept · last reviewed · next due · streak. Use fixed intervals **1 → 3 → 7 → 14 → 30 → 60 days**, advancing one step per successful review (grade ≥ 3) and resetting to 1 on a lapse. It's coarser than SM-2 but captures most of the benefit; the expanding shape matters far more than the exact numbers.
