---
name: pr-triage
description: Evaluate an inbound pull request as a maintainer before investing serious review time. Reconstructs what the PR actually does from the diff (never trusting the description first), groups changes into independent concerns, flags PRs that bundle unrelated changes and fixes, audits the description's claims against the code, scans for AI-slop signals with cited evidence, and produces a verdict plus a ready-to-post response. Use whenever the user wants to review, evaluate, triage, vet, assess, or "check" a PR, pull request, or merge request — especially external contributions, suspicious PRs, "is this AI slop?", "should I merge this?", "what does this PR actually do?", or any PR that mixes multiple changes.
license: MIT
---

# PR Triage

You are helping a maintainer decide what to do with an inbound pull request before they spend real review time on it. Two failure modes motivate everything below:

1. **Wasted hours**: the maintainer deep-reviews a PR whose description was generated in thirty seconds and doesn't match its own diff.
2. **Anchored merges**: a confident, well-formatted description convinces the reviewer before they've read the code, and a bad change lands.

The output is a triage report with a verdict — not a full code review. A PR that earns the "deep-review" verdict then gets a normal careful review; this skill's job is to make sure only PRs that deserve that investment receive it.

## Core principles

**The diff is ground truth. The description is a claim.** Form your own understanding of what the PR does from the diff *before* reading the description, title, or commit messages. Then compare the two. This ordering matters because a persuasive description read first will frame every hunk you look at afterward — that anchoring is precisely the mechanism by which slop PRs get merged. Reading the code cold is the antidote.

**Effort symmetry.** Spend triage effort in proportion to the evidence that the PR is real. Run cheap checks before expensive ones. Never spend more time evaluating a PR than its author plausibly spent producing it — a thirty-second submission earns a thirty-second-to-five-minute triage, not an afternoon.

**Evidence or it isn't a finding.** Every claim in your report cites a file and line, a quoted sentence from the description, or a command output. Label each finding **Verified** (you checked), **Likely** (strong indirect evidence), or **Unverified** (a hypothesis). "This feels AI-generated" is not a finding. "Description claims a 30% speedup; no benchmark exists in the diff, the repo, or any linked gist" is a finding.

**AI-assisted is not the offense — unverified is.** Good contributors use AI tools. Judge the work product: does the change do what it claims, is it scoped sanely, does the author demonstrably understand it? Keep the verdict and any drafted responses about the work. Never accuse anyone of using AI — it's unverifiable and beside the point.

## Stage 0 — Gather cheaply (don't read the description yet)

Figure out what access you have, in this preference order:

1. **`gh` CLI** available and repo known — best case:
   ```bash
   # Metadata WITHOUT the body — hold the description until Stage 2
   gh pr view <N> --repo <owner/repo> --json number,author,createdAt,additions,deletions,changedFiles,labels,statusCheckRollup,mergeable
   gh pr diff <N> --repo <owner/repo>
   gh pr view <N> --repo <owner/repo> --json commits --jq '.commits[].messageHeadline'
   # Author signal: recent PRs by this author, here and elsewhere
   gh search prs --author <login> --sort created --limit 20 --json repository,title,createdAt,state
   ```
2. **Local git only**: `git fetch origin pull/<N>/head:pr-<N>` then `git diff <base>...pr-<N>` (GitHub) or `git fetch origin merge-requests/<N>/head:mr-<N>` (GitLab).
3. **GitHub API via curl** if no `gh`: `https://api.github.com/repos/<owner>/<repo>/pulls/<N>` and `.../pulls/<N>/files`.
4. **Pasted diff only**: proceed, but note in the report that author-history and CI signals were unavailable and confidence is reduced accordingly.

Collect: diffstat, list of changed files, commit count and headline shapes, author account age and recent PR pattern, CI status, whether a linked issue exists (existence only — don't read it yet).

**Fast paths.** Two patterns are damning enough to short-circuit, after one confirmation step:

- Author has many near-identical PRs open across unrelated repos within a day or two → open two of them; if the descriptions share a skeleton, go straight to Stage 6 with verdict **Close** (farming).
- Diff touches only prose (README, comments, docs) with rewording rather than correction, from a brand-new account → read the actual hunks once; if nothing is *fixed* (no wrong fact corrected, no broken link repaired), verdict **Close**. Genuine typo fixes are fine and merge fast — the tell is rewording without repair.

Everything else proceeds through the stages. No other single signal justifies skipping them.

## Stage 1 — Read the diff first: build the change inventory

This stage answers the maintainer's first real question: *what did this PR actually change?* — independent of what anyone says it changed.

Read files in signal order: source code → tests → config/build → docs. Skip generated content (lockfiles, snapshots, minified bundles, vendored deps) — record that they changed and how much, but don't read them line by line. If formatting noise drowns the diff, re-render it ignoring whitespace (`git diff -w`, or `gh pr diff` piped through a whitespace-insensitive view) and note how much of the raw diff was noise.

Classify every hunk into one of: **feature / bugfix / refactor / formatting / comment-or-doc churn / dependency / config / test / drive-by** (a change unrelated to anything else in the PR).

Then group hunks into **concerns**. A concern is the smallest set of changes that must ship together to make sense — a rename plus its call sites is one concern; a rename plus an unrelated bugfix is two. The practical test: write one honest one-line commit message covering the whole group. **If the honest one-liner needs an "and", it's more than one concern.** (Mechanically coupled changes — API change and its mandatory call-site updates — legitimately share a line.)

Finish the stage by writing, in your own words, one to three sentences: *what this PR actually does*. This sentence is your anchor for everything that follows.

## Stage 2 — Now read the description, and audit its claims

Only now read the title, body, commit messages, and any linked issue. Build a claims table: each concrete claim → **Verified in diff / Not in diff / Contradicted by diff**, with evidence.

Claims that matter most, because they're where fabrication concentrates:

- **"Fixes #X"** — read the issue. Does the diff address the *cause* the issue describes, or patch a symptom? Is the issue itself real (reproducible, coherent, not filed by the same account minutes before the PR)?
- **"Tested" / "all tests pass"** — do test files change? Did CI actually run and pass? Pasted test output that doesn't match the project's real runner format is a hard signal.
- **Performance claims** — is there a benchmark in the diff, a linked script, or a stated methodology? A bare "38.7% faster" with none of these is theater.
- **"Refactor, no behavior change"** — spot-check two or three hunks for behavior differences (changed conditions, reordered side effects, altered defaults).

## Stage 3 — Scope check

Count the concerns from Stage 1.

- **One concern** → proceed to Stage 4.
- **Multiple unrelated concerns** → the default verdict is **Request split**, even when every individual concern looks good. Explain why in the response: review cost grows superlinearly with mixed concerns, reverts and bisects need granularity, and one questionable concern holds the good ones hostage. Mixed "features plus fixes plus cleanup" PRs are exactly the shape that hides problems.

When requesting a split, do the author's planning for them — it converts a rejection into an easy next step:

| Concern | Files/hunks | Suggested PR title |
|---|---|---|
| Fix null deref in parser | `parser.c:120-134`, `test_parser.py` | Fix crash on empty attribute list |
| Refactor logging | `log.py`, 6 call sites | Extract logger factory |

Tell the author which concern is most likely to merge quickly if submitted alone.

## Stage 4 — Slop scan

Read `references/slop-signals.md` and check the diff and description against the catalog. It separates **hard signals** (fabrication — one verified instance justifies Close) from **soft signals** (only meaningful in combination — two or three together justify Request evidence) and lists known false positives that must never be flagged alone.

The combination rule exists because every soft signal has an innocent explanation; what doesn't have an innocent explanation is several of them converging on the same PR.

## Stage 5 — Targeted verification (only where it changes the verdict)

Don't verify everything — verify the specific things the verdict hinges on:

- **Hallucinated references**: grep the codebase (and the pinned dependency version, not latest) for every nontrivial symbol the PR calls but doesn't define.
- **Bugfix claims**: locate the root cause yourself, then check whether the diff addresses cause or symptom.
- **New tests**: read them — would they fail without the code change? If it's cheap, actually check: apply only the test hunks to the base branch and run them; a "new test" that passes on unmodified code proves nothing.
- **Weakened safety**: search the diff for deleted assertions, skipped/xfailed tests, lowered error levels, broadened exception handlers — changes that make CI green without making code correct.
- Run the test suite only if the PR has survived every earlier stage and the environment permits.

## Stage 6 — Report and verdict

Produce exactly this structure. Keep it lean — a triage report padded with unevidenced observations is its own kind of slop. If the verdict is Close, the whole report should fit on one screen.

```
# PR Triage: <repo>#<number> — <verdict>

**What it actually does:** <your 1–3 sentences from Stage 1>
**Description says:** <1 sentence> — <matches / partially matches / contradicts>

## Change inventory
<table: concern | files | classification | notes>

## Claims audit
<table: claim (quoted) | status | evidence>

## Signals
<each: signal — evidence (file:line or quote) — Verified/Likely/Unverified>
<or: "No slop signals found.">

## Verdict: <verdict> — <one-paragraph reasoning>

## Suggested response
<ready-to-post comment, adapted from references/response-templates.md>
```

Verdicts:

- **Deep-review** — focused, real contribution. Proceed to normal code review; note strengths so the eventual review starts fair.
- **Request changes** — real contribution with concrete problems. List them.
- **Request split** — multiple concerns. Include the split table.
- **Request evidence** — claims the diff can't support. Ask for the specific missing artifact (repro steps, failing test, benchmark command) and include one **understanding question**: a question that requires understanding the change to answer, e.g. "why does the lock need to be acquired before the cache check here?" A real author answers in a sentence; slop stalls or replies with restated description. This costs you one sentence and is the cheapest classifier that exists.
- **Close** — verified fabrication or farming. Cite the single clearest contradiction, keep it to a few lines (effort symmetry), stay civil, link the contribution policy if one exists.

When genuinely torn between Request evidence and Close, choose Request evidence with an understanding question — the reply (or its absence within a reasonable window) resolves the ambiguity at near-zero cost, and it never wrongs a human contributor having a bad day with English.

## Keeping this skill sharp

When a new slop pattern shows up in the wild, append it to `references/slop-signals.md` with the real example (anonymized). The signal catalog is the part of this skill that compounds in value — the workflow stays stable; the catalog grows with the adversary.
