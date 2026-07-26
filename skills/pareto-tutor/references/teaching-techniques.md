# Teaching Techniques: Generation, Sabotage, and the Hint Ladder

The exercise-level mechanics. Read this when running Lesson or Project workflows.

## Why generation, in one paragraph

Recognition ("yes, that looks right") and recall ("write it from nothing") are different memory systems, and only the second one is available when the learner sits alone in front of an empty editor. Every technique below forces *production*: writing code, predicting behavior, diagnosing failures, explaining causes. If an activity could be completed by nodding along, replace it.

## Prediction exercises

Show a short snippet (3–10 lines) and ask **"what does this print / do?" before it runs**. Then run it. The gap between prediction and reality is the lesson — when they're wrong, don't correct immediately; ask "walk me through what you expected line by line" so the broken link in the mental model surfaces on its own.

Use predictions: right after introducing a concept (confirm the model formed), as review questions (cheap, fast, gradeable), and especially for the language's known surprises (mutability, closures, async ordering, integer division, truthiness).

## Break-and-fix: the sabotage system

The highest-yield exercise type. Diagnosing a realistic failure forces the learner to form a causal model of the machine, and it directly trains the #1 real-world activity: debugging.

**Consent and safety first.** Announce during kickoff that deliberate breakage is part of the method, so it lands as a game rather than a betrayal. And **only sabotage copies or fresh snippets — never the learner's actual working files without explicitly saying so.** Corrupting their real project unannounced destroys trust and their sense of ground truth.

**Rules:**
- The bug must target the concept just taught **or a concept currently due for review** (this is interleaving — old material returning inside new contexts).
- Bugs must be *realistic* — the kind people actually write — not puzzles or trivia.
- One bug at a time for the first weeks; graduate to two-bug and "is there even a bug?" exercises later (real code doesn't announce how many bugs it has).
- **A patch doesn't count until they explain the root cause in their own words.** "I changed line 4 and it works now" → "OK — *why* did that fix it?"
- Start from the error message or the wrong behavior, exactly as reality presents it.

**Bug taxonomy** — pick to match the concept being exercised:

| Bug type | What diagnosing it teaches | Example (Python-flavored) |
|---|---|---|
| Syntax / structure | Reading parser errors calmly | missing `:`; unbalanced bracket |
| Name & scope | Variable lifetime, typo discipline | using `total` defined inside a loop after it; shadowing |
| Type confusion | The type system's actual rules | `"Total: " + 5`; comparing str to int from `input()` |
| Off-by-one / boundary | Ranges, indexing, loop bounds | `range(1, n)` missing the last item; `<` vs `<=` |
| Mutation & aliasing | Reference vs value semantics | two names for one list; mutable default argument |
| Logic inversion | Careful boolean reading | `and`/`or` mixed up; inverted condition |
| Error-handling gap | Failure paths are real paths | file-not-found uncaught; empty-input crash |
| Idiom misuse | The language's sharp edges | mutating a list while iterating; `==` vs `is` |
| Tool-state (for tools) | State-machine mental models | detached HEAD; container port not mapped; greedy regex |

## The hint ladder

When the learner is stuck, climb one rung at a time, pausing between rungs. Each rung reveals strictly more; jumping rungs steals the encoding.

1. **Reflect a question back.** "What is the error message claiming about `data`?" / "What did you expect on line 6, and what happened instead?"
2. **Point at the location.** "Look at line 12. What's the value of `x` at that moment? Add a print if you're not sure."
3. **Name the concept.** "This is the mutable-default-argument thing — default values are evaluated once, at definition."
4. **Worked parallel example.** Solve a *different* problem using the same principle, narrating the reasoning; they translate the method back to their case.
5. **The answer — plus a transfer task.** If rungs 1–4 didn't land, or they're genuinely out of gas: give the fix, explain it, then *immediately* pose a small variation ("now the same bug is hiding in this other snippet — find it"). The answer alone leaves nothing behind; answer-plus-transfer at least closes the loop.

**Beware the hidden-answer hint.** "Hint: have you tried multiplying both sides by x?" is the answer wearing a costume. Rungs 1–2 should narrow *where* to look, never *what* to type.

**Timing:** let them struggle productively for a few minutes before offering rung 1 — struggle is where encoding happens. Escalate when attempts stop generating new information: the same wrong idea repeated, random mutation of code ("shotgun debugging"), or silence with frustration. Never let a session end inside a pit; if time runs out mid-struggle, climb to rung 4–5 so they leave with closure.

**"Just tell me" pressure:** distinguish *impatient* (engaged, has the pieces, wants speed) from *stuck* (see signals above). For impatience, narrow the question until it's nearly rhetorical and keep them doing the final step — caving teaches that pushback works. For genuinely stuck, a rung-4 or rung-5 move is not caving; it's a foothold.

## Active-recall question bank (for warm-up reviews)

Rotate formats so recall stays flexible, not keyed to one question shape:

- **Produce:** "Write a function that takes a list and returns the top 3 by value. From memory, no docs."
- **Predict:** "What does this print?" (3–8 line snippet on the due concept)
- **Spot the bug:** a taxonomy snippet, "find and explain it."
- **Explain:** "You're explaining `git rebase` vs `merge` to a teammate in two sentences. Go."
- **Translate:** (experienced devs) "Here's the JavaScript. Write the idiomatic Python."
- **Discriminate:** "When would you reach for a tuple over a list? One real example."
- **Command recall:** (tools) "You committed to the wrong branch. What's the sequence?"

Grade each 0–5 per the rubric in `references/spaced-repetition.md`, record with `schedule.py grade`. During review, do **not** reteach — a wrong answer gets the correct answer stated once, a grade, and a queued relearn slot later in the session. Reteaching mid-quiz turns recall practice back into recognition and doubles the review's length.

## Calibration by learner profile

- **True beginner:** longer struggle tolerance is *wrong* here — they lack the vocabulary to struggle productively. Shorter intervals to rung 1–2, heavy use of prediction (builds the machine-model), analogies welcome, celebrate error-message reading as the win it is.
- **Experienced dev, new language:** teach by contrast at every opportunity ("your muscle memory says X; here it's Y because Z"). Their bugs should target *transfer errors* — the mistakes their old language's habits cause in the new one (e.g., a JS dev's `==` habits in Python, a Python dev fighting the borrow checker). Move fast through slots their experience covers; they'll tell you when to slow down.
- **Rusty returner:** their failure mode is shame-driven avoidance ("I should know this"). Normalize decay explicitly — forgetting is the system working as designed, and the schedule will repair it. Reviews first, new material second.

## Anti-patterns — the ways tutoring goes wrong

- **Lecture creep.** Explanations swelling past the ~150-word budget "because it's important context." If it's important, it'll come up in an exercise; teach it then.
- **Doing the typing.** Writing the learner's function "to save time." Time was the price of the encoding.
- **Silent fixes.** Correcting their code without making them read the error first.
- **Over-questioning.** Three Socratic questions before any teaching makes stuck learners disengage. One question per turn, paired with a scaffold that moves them forward regardless of their answer.
- **False praise.** "Great job!" on everything reads as noise within two sessions. Praise the specific behavior: "You checked the type before Googling — that instinct is the skill."
- **Completeness anxiety (yours).** Cramming edge cases into lesson one because leaving them out feels irresponsible. The deferred list exists precisely so you can let go.
- **Grading soft.** Recording 4s for hesitant, hint-assisted answers pushes review intervals out too far and the learner meets the concept again only after it's fully gone. Honest 3s and 2s are kindness with a delay.
