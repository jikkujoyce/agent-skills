# Response templates

Adapt these — never post them verbatim without filling the specifics. Tone rules that apply to all of them: be brief, be concrete, address the work and not the author's tools, and never speculate about whether AI was involved (unverifiable, and irrelevant — the standard is verified, scoped, working changes). If the repo has a CONTRIBUTING.md or PR policy, link it instead of restating it.

## Request split

> Thanks for the PR. This currently combines [N] independent changes: [one-line list]. We review and revert at the granularity of one concern per PR, so I'd like to ask you to split it:
>
> 1. **[Concern A — suggested title]** — [files]. This one looks straightforward and would likely merge quickly on its own.
> 2. **[Concern B — suggested title]** — [files].
>
> Happy to review [A] as soon as it's up separately.

Why this shape works: it converts "no" into a concrete, small next step, and naming the fastest-to-merge concern gives a genuine contributor an immediate win while costing a farming account effort it won't spend.

## Request evidence

> Thanks for the PR. Before I can review this I need [the missing artifact — pick what applies]:
>
> - Steps to reproduce the bug this fixes on [base branch], or a failing test that this change turns green.
> - The benchmark command and environment behind the [quoted number] figure.
>
> Also, one question so I understand the approach: [understanding question — must require comprehension of the change, e.g. "why does the lock need to be acquired before the cache check in `store.py:88`, rather than after?"]

The understanding question is the load-bearing part. Make it specific to a real decision in the diff, answerable in one or two sentences by anyone who wrote or understood the change. If the reply stalls, restates the description, or answers a different question, close with the Close template.

## Request changes (real contribution, concrete issues)

> Thanks — the [concern] change is welcome. A few things before it can merge:
>
> 1. **[Blocking]** [issue, file:line, why it blocks].
> 2. **[Blocking]** [issue].
> 3. *(Non-blocking)* [nit — mark it clearly as such].
>
> [One line on what's good about the PR, if true — it keeps real contributors coming back.]

## Close (verified fabrication or farming)

> Closing this. [Single clearest contradiction, stated plainly: e.g. "The description says all tests pass, but no tests exist for this path and CI was never run" / "The `retry_with_backoff` helper this calls doesn't exist in this codebase or in requests 2.31."]
>
> [If a policy exists:] Please see [CONTRIBUTING.md] before submitting again.

Keep it to those few lines. A long rebuttal of a generated PR is time donated to a process that consumed none — and detailed rejections get pasted back into the next generation as a prompt. One verified fact, cited, is unanswerable.

## Deep-review handoff (internal note, not a comment)

When the verdict is Deep-review, end the triage report with a short handoff so the real review starts fair: the concern being reviewed, the two or three files where the substance lives, anything already verified (so it isn't re-checked), and any strengths worth acknowledging in the eventual review.
