# Curriculum Design: the Pareto Map and the Project Ladder

How to decide *what* to teach and *in what order*. Read this during Kickoff, or whenever the plan needs restructuring.

## The inclusion test

A concept belongs in the core map if it passes the frequency test: **"Will the learner hit this in their first two weeks of real usage?"** Not "is it fundamental to the theory of the language" — frequency, not elegance. When in doubt, ask: if you grepped a thousand ordinary repos/scripts in this language, how often would this construct appear?

A concept belongs on the **deliberately deferred** list if it is powerful but low-frequency for a newcomer (metaclasses, macro systems, custom allocators, advanced type-level programming, performance tuning, exotic syntax). Always write the deferred list down and show it to the learner. Two reasons: it proves the 20% is a strategy rather than ignorance, and it gives completionists a place to park their anxiety ("it's on the list, we'll get there if you need it").

## Recipe: concept map for a programming language

Nearly every mainstream language's vital 20% fills these ten slots. Instantiate each with the language's specifics:

1. **Values, variables, core types** — numbers, strings, booleans, null-ish values; declaring and assigning.
2. **Control flow** — conditionals, loops, boolean logic.
3. **Functions** — defining, calling, parameters, return values, basic scope.
4. **The two workhorse collections** — the list/array/vector and the map/dict/object, plus the iteration idioms for each. (These two structures carry the overwhelming majority of everyday code.)
5. **Error handling, the language's way** — exceptions, `Result`/`Option`, error returns, whatever the idiom is. Taught early, not as an "advanced topic": real code fails constantly.
6. **Modules and dependencies** — importing, project layout, and the package manager (`pip`/`uv`, `npm`, `cargo`, `go mod`…). Unusable-in-practice is the same as unknown.
7. **Strings and I/O** — reading/writing files, formatting output, parsing simple input. Most first real programs are "read a thing, transform it, write a thing".
8. **The toolchain** — how to run code, the REPL if there is one, the formatter, how to run tests, and print-debugging. Environment setup lives here and is a legitimate lesson one.
9. **Reading error messages and stack traces** — treated as an explicit skill with its own exercises, not something absorbed by osmosis.
10. **The language's one big idea** — the concept that makes this language *this language*. Skipping it produces someone who writes Python-flavored Rust. Examples:

| Language | The one big idea to teach explicitly |
|---|---|
| Python | Duck typing + the comprehension/iterator idiom set |
| JavaScript/TS | The event loop and async (callbacks → promises → async/await) |
| Rust | Ownership, borrowing, lifetimes (spread across multiple lessons) |
| Go | Goroutines/channels + "small interfaces, explicit errors" culture |
| Java/C# | The type system + interfaces/inheritance as design tools |
| C | Pointers and manual memory |
| SQL | Set-based thinking (stop writing loops in your head) |
| Haskell/FP | Purity, higher-order functions, algebraic data types |

Order the map **breadth-first**: the learner should be able to write a small end-to-end program using shallow versions of slots 1–8 within the first couple of sessions, then loop back to deepen. Depth-first ("we'll master the type system before writing a program") postpones the productive phase for weeks and kills motivation.

## Recipe: concept map for a tool (git, Docker, k8s, regex, a shell…)

Same test, but the unit is a **task**, not a construct: list the 8–12 tasks the learner will do weekly, map each to the minimal command/config surface, and defer the rest.

Worked example — **git core map**: (1) init/clone and the mental model of the three states (working dir / staging / history); (2) status, diff, log — reading the current state; (3) add + commit with good messages; (4) branch, switch, merge; (5) push/pull/remotes; (6) the undo toolkit — restore, revert, reset, and *which one is safe when*; (7) .gitignore; (8) resolving a merge conflict without panic. **Deferred:** interactive rebase, bisect, submodules, hooks, reflog surgery, filter-repo.

For tools, replace the project ladder with a **scenario ladder**: realistic situations to get into and out of. Break-and-fix is especially natural here — "here's a repo in a detached-HEAD state / a container that won't start / a regex that over-matches; diagnose and fix it."

## Recipe: concept map for a framework (React, Django, Rails…)

Frameworks assume the host language, so first check the learner's standing in the language itself (a quick 5-question probe). Then the map is: the framework's mental model (e.g., React: UI as a function of state; Django: request → URL → view → template), the 6–8 primitives used in every app (components/props/state/effects; models/views/templates/ORM basics), the dev-loop toolchain, and the framework's *one big idea* (React: unidirectional data flow + "don't fight the render"; Django: convention and the ORM). Defer: SSR nuances, custom middleware, performance optimization, the plugin ecosystem.

## Designing the project ladder

Rules:

1. **4–6 rungs**, sized from one session (rung 1) to roughly a week of sessions (final rung).
2. **Every rung ships.** Each project must *work* and do something the learner could show someone. Functional beats polished; a working ugly thing teaches more than a perfect fragment.
3. **Each rung reuses all prior rungs' concepts** and adds 2–4 new ones. This makes the ladder itself a spaced-repetition device — old material gets retrieved inside new contexts (interleaving), which is far stronger review than flashcards alone.
4. **Retheme to the learner's goal.** A photographer learning Python should build an EXIF organizer, not a todo app. Ask what they'd actually use, then map the same concept coverage onto their domain. Personal relevance is rocket fuel for consistency.
5. **Write acceptance checks per rung** ("done when…"), so both of you know when it's finished. Open-ended projects stall.

Worked ladder — **Python, general-purpose learner**:

| Rung | Project | New concepts exercised | Size |
|---|---|---|---|
| 1 | CLI number-guessing or word game | variables, control flow, input/print, running a script | 1 session |
| 2 | Text-file stats tool (word counts, top-N) | files, strings, dicts, functions | 1–2 sessions |
| 3 | Expense tracker with JSON persistence | modules, error handling, data modeling, CLI args | 2–3 sessions |
| 4 | API-consuming CLI (weather, prices…) | pip/venv, HTTP, JSON APIs, third-party docs | 2–3 sessions |
| 5 | Small web app or scraper, with tests | a framework's basics, pytest, project structure | 4–6 sessions |

Worked ladder — **git (scenario form)**: (1) solo project: init, commit rhythm, useful messages; (2) "I broke it": practice each undo tool against staged/unstaged/committed mistakes; (3) branching: feature branch → merge, then a manufactured conflict to resolve; (4) remote collaboration: push/pull against a real remote, simulate a rejected push; (5) capstone: contribute a change through a fork-and-PR flow end to end.

## Calibrating the map to the learner profile

- **True beginner** (first language ever): use the full ten slots, split slot 10 across the whole plan, allocate extra time to slots 8–9 (toolchain and error-reading — the places beginners silently drown). Analogies to everyday processes help; precision can come later.
- **Experienced developer, new language**: compress slots 1–4 into a rapid "diff tour" against a language they know ("here's the table: your `dict` is a `HashMap`, your `try/except` is `Result`…"). They can absorb a dense mapping table plus exercises in one session. Spend the reclaimed time on slot 10 and the toolchain, which is where experienced devs actually differ from natives. Their project ladder can start at rung 2–3.
- **Rusty returner**: run a short diagnostic quiz across the map *first*, then rebuild the plan from the misses only. Re-teaching what they still know insults them; skipping the diagnostic overestimates them.

## Maintaining the plan

The map is a living document. When the learner's goal shifts, or a "deferred" topic becomes suddenly relevant to their project (it happens — that's fine, frequency has changed *for them*), promote it into the map, note the change in the session log, and re-balance the remaining rungs. The plan serves the learner, never the reverse.
