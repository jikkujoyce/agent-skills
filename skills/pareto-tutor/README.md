# pareto-tutor — setup and usage notes

Human notes for running this skill. What the skill actually does lives in [`SKILL.md`](SKILL.md).

## Setup

No API key and no config file, but two things need to be true before the scheduling half of the skill works.

**Python 3.8+ for the scheduler.** `scripts/schedule.py` is standard-library only, so if `python3` runs, it runs:

```bash
python3 --version
python3 skills/pareto-tutor/scripts/schedule.py --help
```

**A home for your state files.** Spaced repetition needs memory across sessions and the agent's context does not survive between them, so everything lives in two files that belong to you:

| File | What it holds |
|---|---|
| `LEARNING_PLAN.md` | Goal, learner profile, concept map, project ladder, session log |
| `progress.json` | Review scheduling data — ease factors, intervals, due dates, grade history |

On a persistent filesystem, keep both in `learning/<topic>/` and let the tutor run the script directly:

```bash
mkdir -p learning/rust && cd learning/rust
```

In an ephemeral chat, the tutor writes both files each session and you must **download them and re-attach them next time**. This is the one failure the system can't recover from — lose `progress.json` and every interval resets. Where no code runs at all, the tutor skips `progress.json` and keeps a fixed-interval review table inside `LEARNING_PLAN.md` instead, per the fallback in `references/spaced-repetition.md`.

The scheduler is also usable directly, which is handy for checking where you stand outside a session:

```bash
python3 schedule.py stats --file progress.json
python3 schedule.py due   --file progress.json
```

## Usage

Start a topic, or resume one:

```
Teach me Rust — I write TypeScript and want to build a CLI.
Continue my Python lessons. (attach LEARNING_PLAN.md and progress.json)
Quiz me on what's due.
How am I doing? What's left?
My rung-3 project is crashing and I can't see why.
```

Answer the four kickoff questions honestly, especially the goal one — "learn Python" gets you a generic ladder, while "organize my photo library by EXIF date" rethemes every project in it. The first session always ends with real code you wrote, not just a plan.

A session looks roughly like this:

```
You:    Continue my Rust lessons. [attaches both files]

Agent:  Two concepts due. Warm-up, 3 minutes.

        First: write me a function that takes a &str and returns its
        length in characters, not bytes.

You:    fn len(s: &str) -> usize { s.chars().count() }

Agent:  Correct, and you reached for .chars() unprompted — that's the
        distinction most people take a week to internalize. Grade 5.

        Second: what does this print?

          let v = vec![1, 2, 3];
          let w = v;
          println!("{:?}", v);

You:    3? No wait — v moved into w, so it won't compile.

Agent:  Right, and the recovery matters more than the first answer.
        Grade 4.

        Today: error handling with Result, then you'll add it to the
        file parser from rung 2. [...lesson begins...]
```

Mid-session steering that works well: "slow down, I don't have this yet", "skip the break-and-fix today", "I've got 15 minutes, review only", and "I've been away a month" — the last one gets a longer review and honest re-grading rather than a restart. Asking it to just write the code will get you a hint or a parallel example instead; that's deliberate, and "I'm genuinely stuck, give me the first step" is the phrasing that gets a real foothold.

## Known limitations

- **It's a conversation across weeks, not a job.** The skill needs your replies and your typing. Run it non-interactively and you get a lesson plan nobody executed.
- **The state files are load-bearing.** No `progress.json` means no scheduling, and the review system is most of what separates this from ordinary tutoring. In ephemeral chats, download both files at the end of every session.
- **Nothing enforces the schedule.** There are no reminders and no notifications — the tutor knows what's due only when you start a session and hand it the files.
- **Grades are the agent's judgment.** The 0–5 scores that drive every interval come from how it read your answer in the moment, so intervals are approximate. If a concept feels shakier than the schedule thinks, say so and ask it to re-grade.
- **The scheduler is SM-2-lite, not Anki.** No sub-day intervals, no fuzz, no leech handling; a lapse resets the interval to one day and re-climbs.
- **The tutor can't see your machine unless it can.** In a plain chat you paste code and errors yourself, and the agent takes your word for what ran. Environment problems are much faster to work through with file and shell access.
- **It won't do your project for you.** Rung work is yours to write. If you need working code today rather than skill in a month, this is the wrong tool.
