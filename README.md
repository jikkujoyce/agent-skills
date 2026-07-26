# agent-skills

Agent skills I use day to day — each one a single `SKILL.md` that encodes a judgment call I'd otherwise have to re-explain in every session.

## Install

Every skill installs the same way. Pick one and set it once:

```bash
SKILL=pr-triage        # or: guided-reading
```

Install it (GitHub CLI v2.90.0+, `gh skill` is in preview):

```bash
gh skill install jikkujoyce/agent-skills "$SKILL" --agent claude-code --scope user
```

`--agent` accepts `claude-code`, `cursor`, `codex`, `github-copilot`, `gemini-cli`, `opencode`, and [many more](https://cli.github.com/manual/gh_skill_install); `--scope user` installs for every project, `--scope project` (the default) only for the current repo.

Pin a version — recommended for anything you rely on in CI:

```bash
gh skill install jikkujoyce/agent-skills "$SKILL@v1.0.0" --agent claude-code --scope user
```

Without a version, `gh` resolves the latest tagged release, falling back to the default branch. A tag or commit SHA also works via `--pin`.

Read a skill before you trust it:

```bash
gh skill preview jikkujoyce/agent-skills "$SKILL"
```

Manual install works too — copy the skill directory wherever your agent looks for skills:

```bash
git clone https://github.com/jikkujoyce/agent-skills
cp -r agent-skills/skills/"$SKILL" ~/.claude/skills/     # or .agents/skills/ in a project
```

For claude.ai, zip the `skills/$SKILL` folder from that clone and upload it under Settings → Capabilities → Skills.

## Skills

| Skill | What it does |
|---|---|
| [`pr-triage`](skills/pr-triage) | Decides whether an inbound pull request deserves a real review, and returns a verdict plus a ready-to-post response. |
| [`guided-reading`](skills/guided-reading) | Reads a document *with* you in interactive chunks instead of summarizing it at you. |

## pr-triage

Written for the position of maintaining a repo that gets more drive-by PRs than you have review hours for. The judgment it encodes is mostly about *ordering and proportion*: read the diff and form your own account of the change before you read the description, because a confident description read first frames every hunk you look at afterward — and that anchoring is how a bad change gets merged. Then spend triage effort in proportion to the effort the PR plausibly cost to produce, cite a file, line, or quote for every finding, and keep the judgment about the work rather than about whether a model was involved. It also refuses to review two things at once: hunks get grouped into concerns, and if the honest one-line summary of the PR needs an "and", the default answer is a split request with a table showing the author how to divide it. Reach for it at the moment you open a PR and feel yourself about to either merge on vibes or sink an afternoon into something that doesn't deserve one. See [`skills/pr-triage/README.md`](skills/pr-triage/README.md) for setup and usage details.

## guided-reading

For documents you keep meaning to finish and never do — long reports, papers, and especially the AI-generated wall of text you just asked for. The judgment it encodes is that comprehension comes from the reader's effort, not the summary's eloquence, so the skill spends its budget on making *you* articulate things rather than on explaining them to you: it asks what you want out of the document first and triages against that purpose, moves in chunks with one question at a time, and makes you summarize at the end rather than doing it for you. The most useful thing it does is notice when your own situation matches an exception or edge case in the document rather than its headline — the part a summary always buries. Reach for it when you're skimming without retaining, when you're staring at something you have to actually understand rather than merely file away, or right after an agent hands you a document too long to absorb. See [`skills/guided-reading/README.md`](skills/guided-reading/README.md) for usage details and limitations.

## Repo layout

```
skills/
  guided-reading/
    SKILL.md
    README.md
  pr-triage/
    SKILL.md
    README.md
    references/
      slop-signals.md
      response-templates.md
CONTRIBUTING.md
LICENSE
```

A skill directory name must match the `name` in its frontmatter — `gh skill publish` fails validation otherwise. `SKILL.md` is the whole skill: it's what `gh skill preview` prints and what the agent loads. A folder `README.md` is for humans only, and only exists where a skill needs setup, extended examples, or caveats.

## Contributing

Small, focused PRs — one concern each; if describing the change needs an "and", it's two PRs. Say what you changed and how you verified it, ideally with a session excerpt showing the behavior before and after. See [CONTRIBUTING.md](CONTRIBUTING.md) for the details and for `gh skill publish --dry-run` validation.

New skills should earn their place. A skill is worth adding when it encodes a repeatable judgment call, not when it restates something the model already does well unprompted.

## License

MIT — see [LICENSE](LICENSE).
