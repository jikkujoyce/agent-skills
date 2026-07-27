# pr-triage — setup and usage notes

Human notes for running this skill. What the skill actually does lives in [`SKILL.md`](SKILL.md).

## Setup

The skill works best with an authenticated GitHub CLI, since that's the only path that gives it PR metadata, CI status, and author history in one place:

```bash
gh auth login                 # needs the repo scope for private repositories
gh auth status                # confirm the account and scopes
```

Nothing else to configure — no API keys, no config file, no scripts to run.

Two access details worth knowing before you rely on the report:

- **Author-history signals** (`gh search prs --author ...`) use the GitHub search API, which is rate-limited separately and unavailable to unauthenticated requests. Without auth, the skill can't check whether the same PR shape is open across ten other repos.
- **GitLab and Bitbucket** have no `gh` equivalent here. Fetch the merge request locally first and point the skill at the branch:

```bash
git fetch origin merge-requests/<N>/head:mr-<N>     # GitLab
git fetch origin pull-requests/<N>/from:pr-<N>      # Bitbucket Server/Data Center only — Cloud doesn't expose PR refs; fetch the source branch instead
```

## Usage

Ask for triage by PR number, URL, or after pasting a diff:

```
Triage PR #482 in owner/repo
Is this PR worth reviewing? https://github.com/owner/repo/pull/482
What does this PR actually change? I don't trust the description.
Triage the PR on branch pr-482 against main — no gh access here.
```

The report comes back in a fixed shape, so it's skimmable and comparable across PRs:

```
# PR Triage: acme/parser#482 — Request split

**What it actually does:** Fixes a null dereference when the attribute list
is empty, renames the logger factory across six call sites, and reformats
three untouched files.
**Description says:** "Fix parser crash" — partially matches.

## Change inventory
| Concern | Files | Classification | Notes |
|---|---|---|---|
| Null deref fix | parser.c:120-134, test_parser.py | bugfix | Real; test fails without it |
| Logger rename | log.py + 6 call sites | refactor | Unrelated to the fix |
| Reformatting | three untouched files | formatting | Drive-by |

## Claims audit
| Claim | Status | Evidence |
|---|---|---|
| "All tests pass" | Verified | CI green, 412 tests, matches suite |
| "Minimal change" | Contradicted | 9 files, 2 unrelated concerns |

## Signals
S7 drive-by churn — three reformatted files untouched by the fix — Verified

## Verdict: Request split — ...
## Suggested response
...
```

Useful follow-ups once you have a report: "run the split table by me again", "post the suggested response", "the fix concern looks good — do a real review of just those hunks", or "add this pattern to the slop catalog" (the signal catalog in `references/slop-signals.md` is meant to grow as new patterns show up).

## Known limitations

- **Triage, not review.** A `deep-review` verdict means the PR earned a careful read, not that it's correct. Don't merge on a triage report alone.
- **Degraded modes are real but weaker.** With a pasted diff and no `gh`, author history and CI status are simply unavailable; the report says so and lowers its confidence, but you're getting a subset of the signal.
- **Running the suite executes contributor code.** The skill only reaches that step late and when the environment permits, but that's still untrusted code from a stranger's branch — use a container or CI, not your laptop, when the PR is one you already suspect.
- **Generated files are counted, not read.** Lockfiles, snapshots, and vendored dependencies are recorded in the inventory and skipped. A change hidden inside a regenerated bundle will not be caught.
- **Very large PRs strain it.** Above a few thousand changed lines the diff won't fit comfortably in context; scope the triage to a subset of files and say so, or expect the concern grouping to be coarse.
- **Verdicts are inputs to your decision.** `Close` in particular is a recommendation with cited evidence attached, and the evidence is the part to read — especially with a first-time contributor writing in a second language, where the skill deliberately prefers asking for evidence over closing.
