# codebase-mentor — setup and usage notes

Human notes for running this skill. What the skill actually does lives in [`SKILL.md`](SKILL.md).

## Setup

Nothing to configure — no API key, no config file, no scripts to run. Two things are worth doing before a session, though, because they change how much the skill can verify:

```bash
git status                    # start from a clean tree; probes get reverted, not stashed
<the repo's test command>     # confirm the suite runs before the tour needs it
```

The skill checks early whether anything executes, and a working suite or dev server upgrades every verification for the rest of the session — predictions get graded by a stack trace instead of by a second reading of the source. When the toolchain is broken or the code only runs in production, say so up front and it falls back to reading.

## Usage

Ask in natural language; the skill triggers on the intent, not on a keyword:

```
Help me understand this repo.
I just inherited this service and need to own it.
Walk me through how auth works in this codebase.
Where would I start if I had to fix a bug in the checkout flow?
Should we adopt this dependency? Give me an honest read on it.
```

Answer the first question honestly — it asks *why* you're here, and the answer sets the tour radius. "Fixing one bug" gets a single vertical trace; "joining the team" gets the full map-spine-conventions-consolidation route.

A session looks roughly like this:

```
You:    Help me understand this repo — I'm taking over the billing service.

Agent:  Taking ownership, so we'll do the full route. First, the top level,
        trimmed:

          cmd/  internal/  pkg/  migrations/  deploy/

        Before I say anything: what do you think each one holds, and which
        do you suspect is the heart of it?

You:    cmd is entry points, internal is the real logic, pkg is shared
        helpers. Heart is probably internal.

Agent:  Right on all four — and one thing to file away: `pkg/` here isn't
        shared helpers, it's the public client other teams import. Changing
        it breaks them.

        Now the spine. An invoice gets generated. `cmd/worker/main.go:34`
        registers a handler. Before you open it — what do you expect the
        handler itself to do, and what do you expect it to delegate?

You:    Probably pulls the subscription, computes line items, writes the
        invoice.

Agent:  Read lines 34–70. [...continues hop by hop...]
```

Mid-session steering that works well: "I'm new to Go, stop asking me to predict" (drops it into model-first mode, where it traces first and you follow), "smaller scope", "park that and keep going", "just tell me this one" for a single foothold, and "summary mode, I have an incident" to switch out of the tour entirely. At the end, "write that up" turns your own explain-back into a mental-model doc — it isn't produced unless you ask.

## Known limitations

- **It's a conversation, not a job.** The skill needs your replies. Run it in an autonomous or non-interactive context and you get an architecture summary with rhetorical questions in it, which is the exact thing it exists to replace.
- **Without file access you are its hands.** In a plain chat it asks for one artifact at a time — a trimmed tree, one file, one grep result — and the session runs much slower than it does with a cloned repo.
- **Coverage is deliberately partial.** It scopes to the subsystem your goal touches and says what it's skipping. On a large repo, a finished tour means you understand one spine well, not the whole system.
- **The guide can misread code.** When nothing runs, reconciliation is one reading checked against another, and conclusions should be held loosely. The runtime-graded modes exist precisely because this failure is invisible from inside the session.
- **Mutation probes touch the working tree.** Commenting out a line to watch what breaks is a real edit. Keep it on a scratch branch, revert it, and never run probes against a shared or dirty tree.
- **Debugger walks assume a local toolchain.** Stepping through a request needs a debugger you can attach; for async or distributed paths the fallback is temporary log statements, which you have to remember to remove.
- **It ends on purpose.** Once your predictions keep landing, it closes the session rather than continuing to quiz you. Reopening for a different subsystem is a new tour.
