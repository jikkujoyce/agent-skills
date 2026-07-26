# Contributing

Thanks for your interest in improving these skills. Contributions are welcome — the bar is simply that a change must make the skill *better in practice*, not just longer.

## Ground rules

- **Instructions first.** These skills are prose instructions plus reference files. A skill may bundle a small helper script where one genuinely earns its place — `pareto-tutor` ships a spaced-repetition scheduler — but it must be standard-library only, make no network calls beyond what the user's own request requires, and never be the thing the skill's judgment depends on: the skill has to degrade to instructions when the script can't run. No binaries, no dependencies to install. That's what keeps these portable and safe to install.
- **Preserve each skill's core principle.** Every skill here exists to encode one judgment call, stated near the top of its `SKILL.md` — the reader does the thinking in `guided-reading`, the diff outranks the description in `pr-triage`. Changes that quietly reverse that principle will be declined even when they add capability.
- **One concern per PR.** If describing your change needs an "and", it's two PRs.

## Proposing a change

1. Open an issue describing the failure mode you saw in a real session — what the agent did, what it should have done instead. Session excerpts, with anything sensitive removed, are the most useful evidence there is.
2. For fixes, edit `skills/<name>/SKILL.md` and open a pull request. Leave the frontmatter `name` and `description` intact unless the change is specifically about when the skill triggers.
3. Test before submitting: run the modified skill on a real case in the agent of your choice and include a short note on how it went.

Behavior belongs in `SKILL.md` — it's the file `gh skill preview` prints and the only file the agent loads. A skill's `README.md` is for humans, and carries only setup, extended examples, and caveats. Please don't document behavior in both places; they drift.

## Validation

Before submitting, check the skills still pass spec validation:

```sh
gh skill publish --dry-run
```

This validates against the [Agent Skills specification](https://agentskills.io) — name format, required fields, and the requirement that each directory name matches its frontmatter `name`.

## Style

- Write instructions in direct, imperative prose. Explain *why* a rule exists when it isn't obvious; agents follow reasoned instructions more faithfully than bare ones.
- Prefer removing words to adding them. A `SKILL.md` loads into the agent's context, so every line costs tokens in every session that uses it.

## License

By contributing, you agree your contributions are licensed under the repository's [MIT License](LICENSE).
